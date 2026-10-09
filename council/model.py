from __future__ import annotations

import asyncio
import contextvars
import json
import time
from dataclasses import dataclass, replace
from typing import Protocol

from .schemas import Incomplete, canonical
from .packing import unpack_context

AITUNNEL_TEST_OUTPUT_CEILING = 8000


class TransientModelError(RuntimeError):
    safe_code = 'provider_transient'


class AuthenticationError(RuntimeError):
    safe_code = 'provider_authentication'


class ProviderRequestError(RuntimeError):
    """Terminal provider refusal/configuration error; message is a safe category."""

    def __init__(self, code):
        allowed = {'unsupported_tuple_schema', 'unsupported_schema_reference',
                   'model_not_in_chat_catalog', 'invalid_catalog_limits', 'catalog_not_prepared',
                   'invalid_input_token_count', 'provider_response_byte_budget', 'provider_body_error',
                   'provider_model_mismatch', 'provider_output_token_budget',
                   'provider_incomplete_or_refused', 'provider_unexpected_output',
                   'provider_unexpected_choices', 'provider_secret_echo'}
        http_code = (isinstance(code, str) and code.startswith('provider_http_') and
                     len(code) == len('provider_http_') + 3 and code[-3:].isdigit())
        self.safe_code = code if code in allowed or http_code else 'provider_request_rejected'
        super().__init__(self.safe_code)


# Each invoke owns its audit. Closing it prevents detached/late work from publishing.
ATTEMPT_AUDIT = contextvars.ContextVar('council_provider_attempt', default=None)


def audit_update(**values):
    audit = ATTEMPT_AUDIT.get()
    if audit is not None and not audit.get('closed'):
        audit.update(values)


def audit_dispatch():
    audit = ATTEMPT_AUDIT.get()
    if audit is not None and not audit.get('closed'):
        audit['http_dispatches'] += 1


@dataclass(frozen=True)
class Capabilities:
    configured: bool = False
    reliable_token_accounting: bool = False
    context_window: int = 0
    cooperative_cancel: bool = False
    identity: str = 'unconfigured'
    accounting_policy: str = 'certified'
    provider: str = 'custom'
    output_limit_policy: str = 'strict'


@dataclass(frozen=True)
class Request:
    stage: str
    persona_id: str
    run_id: str
    snapshot_id: str
    version: int
    request_id: str
    attempt_id: str
    system_policy: str
    payload_json: str
    response_schema_json: str
    output_tokens: int

    def serialized(self):
        return canonical(self.__dict__)

    def payload(self):
        """Decode input tables for fixtures/audit, never model output."""
        return unpack_context(json.loads(self.payload_json))


@dataclass(frozen=True)
class Response:
    payload_json: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    metadata: dict | None = None


class ModelAdapter(Protocol):
    mode: str
    capabilities: Capabilities

    def count_tokens(self, request: Request) -> int: ...
    async def generate(self, request: Request) -> Response: ...


def check_adapter(adapter):
    if adapter.mode == 'scripted':
        return
    cap = adapter.capabilities
    policy_ok = ((cap.accounting_policy in ('certified', 'server_exact') and cap.reliable_token_accounting) or
                 (cap.accounting_policy == 'server_enforced' and cap.provider == 'aitunnel' and not cap.reliable_token_accounting))
    output_ok = (cap.output_limit_policy == 'strict' or
                 (cap.output_limit_policy == 'aitunnel_test' and cap.provider == 'aitunnel' and
                  cap.accounting_policy == 'server_enforced' and not cap.reliable_token_accounting))
    if adapter.mode != 'model' or not cap.configured or not policy_ok or not output_ok or not cap.cooperative_cancel or cap.context_window <= 0 or cap.identity in ('', 'unconfigured'):
        raise ValueError('live adapter needs configured identity, reliable accounting and bounded cancellation before disclosure')


def output_token_ceiling(capabilities, requested):
    return AITUNNEL_TEST_OUTPUT_CEILING if capabilities.output_limit_policy == 'aitunnel_test' else requested


async def invoke(adapter, request, timeout):
    check_adapter(adapter)
    audit = {'http_dispatches': 0, 'preflight_count': None,
             'input_tokens': None, 'output_tokens': None, 'returned_model': None,
             'cost_rub': None, 'closed': False}

    async def perform():
        token = ATTEMPT_AUDIT.set(audit)
        try:
            if adapter.mode == 'model':
                preflight = getattr(adapter, 'preflight', None)
                tokens = await preflight(request) if preflight else adapter.count_tokens(request)
                if adapter.capabilities.accounting_policy == 'server_enforced':
                    if tokens is not None:
                        raise ValueError('server-enforced accounting must not certify an estimate')
                else:
                    if type(tokens) is not int or tokens < 0:
                        raise ValueError('invalid certified token count')
                    audit_update(preflight_count=tokens)
                    if tokens + request.output_tokens > adapter.capabilities.context_window:
                        raise Incomplete('provider context token budget')
            # A cancelled/expired count must never initiate a later generation,
            # even if a transport or third-party coroutine suppresses cancellation.
            if audit['closed'] or time.monotonic() >= expires or asyncio.current_task().cancelling():
                raise asyncio.CancelledError
            return await adapter.generate(request)
        finally:
            ATTEMPT_AUDIT.reset(token)

    expires = time.monotonic() + timeout
    task = asyncio.create_task(perform())
    try:
        done, _ = await asyncio.wait({task}, timeout=timeout)
        if not done or time.monotonic() >= expires:
            # Expiry is authoritative even when generate suppresses CancelledError.
            raise asyncio.TimeoutError('attempt expired')
        result = task.result()
        return replace(result, metadata={k: v for k, v in audit.items() if k != 'closed'})
    except Exception as exc:
        exc.safe_metadata = {k: v for k, v in audit.items() if k != 'closed'}
        raise
    finally:
        audit['closed'] = True
        if not task.done():
            task.cancel()
            # Do not await unbounded provider cleanup or accept its late response.
            task.add_done_callback(discard_task)
        else:
            discard_task(task)  # Also retrieve an already-done, expired child error.


def discard_task(task):
    if not task.cancelled():
        task.exception()  # Retrieve a detached error; never publish late payload.
