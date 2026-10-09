from __future__ import annotations

import asyncio
import copy
import json
import math

import httpx

from .model import (AuthenticationError, Capabilities, ProviderRequestError, Response,
                    TransientModelError, audit_dispatch, audit_update, output_token_ceiling)
from .schemas import Incomplete, canonical
from .settings import MODEL_ID, Settings

WIRE_CAP = 131072
RESPONSE_CAP = 262144


def transport_schema(original):
    """Provider subset only. Original DTO validation remains authoritative."""
    def convert(node):
        if not isinstance(node, dict):
            return node
        result = {k: copy.deepcopy(v) for k, v in node.items()
                  if k in ('$ref', '$defs', 'type', 'properties', 'items', 'anyOf', 'enum', 'description')}
        # Preserve DTO bounds as model-visible instructions even on providers
        # whose strict schema subset cannot enforce those keywords. The local
        # DTO remains the authority; descriptions are not enforcement.
        bounds = {key: node[key] for key in ('minItems', 'maxItems', 'minLength', 'maxLength',
                                           'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum')
                  if key in node}
        if bounds:
            result['description'] = (result.get('description', '') +
                                     ' Required bounds: ' + canonical(bounds) + '.').strip()
        if 'prefixItems' in node:
            items = node['prefixItems']
            if not items or any(item != items[0] for item in items):
                raise ProviderRequestError('unsupported_tuple_schema')
            result['items'] = convert(items[0])
        elif 'items' in result:
            result['items'] = convert(result['items'])
        if '$defs' in result:
            result['$defs'] = {key: convert(value) for key, value in result['$defs'].items()}
        if 'anyOf' in result:
            result['anyOf'] = [convert(value) for value in result['anyOf']]
        if node.get('type') == 'object':
            required = set(node.get('required', []))
            properties = {}
            for name, value in node.get('properties', {}).items():
                converted = convert(value)
                if name not in required:
                    converted = {'anyOf': [converted, {'type': 'null'}]}
                properties[name] = converted
            result.update(properties=properties, required=list(properties), additionalProperties=False)
        return result
    return convert(original)


def restore_defaults(value, schema, root):
    """Remove null placeholders only for originally optional, non-null fields."""
    if '$ref' in schema:
        ref = schema['$ref']
        if not ref.startswith('#/$defs/'):
            raise ProviderRequestError('unsupported_schema_reference')
        return restore_defaults(value, root['$defs'][ref.removeprefix('#/$defs/')], root)
    if isinstance(value, dict) and schema.get('type') == 'object':
        result = dict(value)
        required = set(schema.get('required', []))
        for name, spec in schema.get('properties', {}).items():
            if name not in result:
                continue
            nullable = spec.get('type') == 'null' or any(x.get('type') == 'null' for x in spec.get('anyOf', []))
            if result[name] is None and name not in required and not nullable:
                del result[name]
            else:
                result[name] = restore_defaults(result[name], spec, root)
        return result
    if isinstance(value, list):
        if 'prefixItems' in schema:
            return [restore_defaults(item, schema['prefixItems'][i], root)
                    if i < len(schema['prefixItems']) else item for i, item in enumerate(value)]
        if 'items' in schema:
            return [restore_defaults(item, schema['items'], root) for item in value]
    return value


class ProviderAdapter:
    mode = 'model'

    def __init__(self, settings: Settings, *, transport=None):
        self.settings = settings
        # No SDK retries, redirects, proxy-environment routing or user-controlled URL.
        self.client = httpx.AsyncClient(transport=transport, timeout=45, follow_redirects=False,
                                       trust_env=False, limits=httpx.Limits(max_connections=5))
        self.capabilities = Capabilities(settings.provider == 'openai', settings.provider == 'openai',
                                        32768 if settings.provider == 'openai' else 0,
                                        True, settings.model,
                                        'server_exact' if settings.provider == 'openai' else 'server_enforced',
                                        settings.provider,
                                        'aitunnel_test' if settings.aitunnel_test_mode else 'strict')
        self.catalog_metadata = None

    def __repr__(self):
        return f'ProviderAdapter(provider={self.settings.provider!r}, model={self.settings.model!r})'

    async def aclose(self):
        # Bounded cleanup; cancellation is not proof of remote stop/billing stop.
        await asyncio.wait_for(self.client.aclose(), timeout=2)

    async def prepare(self, output_tokens=2000):
        if self.settings.provider == 'openai':
            return
        data = await self._http('GET', 'https://api.aitunnel.ru/public/aitunnel/models', None,
                                authenticated=False, cap=2097152)
        chat = data.get('chat')
        entry = chat.get(self.settings.model) if isinstance(chat, dict) else None
        if not isinstance(entry, dict):
            raise ProviderRequestError('model_not_in_chat_catalog')
        context, maximum = entry.get('context_size'), entry.get('max_output')
        if type(context) is not int or context <= 0 or type(maximum) is not int or maximum < output_tokens:
            raise ProviderRequestError('invalid_catalog_limits')
        upstream = entry.get('provider')
        upstream = upstream if isinstance(upstream, str) and len(upstream) <= 64 and upstream.replace('_', '').replace('-', '').isalnum() else 'unknown'
        self.catalog_metadata = {'context_size': context, 'max_output': maximum, 'upstream_provider': upstream}
        self.capabilities = Capabilities(True, False, context, True, self.settings.model,
                                        'server_enforced', 'aitunnel',
                                        'aitunnel_test' if self.settings.aitunnel_test_mode else 'strict')

    def _wire(self, request):
        original = json.loads(request.response_schema_json)
        schema = transport_schema(original)
        if self.settings.provider == 'openai':
            body = {'model': self.settings.model, 'instructions': request.system_policy,
                    'input': [{'role': 'user', 'content': request.payload_json}],
                    'text': {'format': {'type': 'json_schema', 'name': request.stage,
                                        'schema': schema, 'strict': True}}}
        else:
            body = {'model': self.settings.model,
                    'messages': [{'role': 'system', 'content': request.system_policy},
                                 {'role': 'user', 'content': request.payload_json}],
                    'response_format': {'type': 'json_schema', 'json_schema': {
                        'name': request.stage, 'schema': schema, 'strict': True}},
                    'max_tokens': request.output_tokens, 'stream': False,
                    'plugins': [{'id': 'context-compression', 'enabled': False}]}
            # AI Tunnel documents the modern OpenAI cap explicitly. Do not rely
            # on gateway translation of legacy max_tokens for reasoning routes.
            if self.catalog_metadata and self.catalog_metadata['upstream_provider'] == 'openai':
                body['max_completion_tokens'] = body.pop('max_tokens')
        if self.settings.reasoning_effort is not None:
            body['reasoning'] = {'effort': self.settings.reasoning_effort}
        return body

    async def preflight(self, request):
        if len(request.serialized().encode('utf-8')) > 32768:
            raise Incomplete('complete serialized request byte budget')
        body = self._wire(request)
        if self.settings.provider == 'aitunnel':
            if self.catalog_metadata is None:
                raise ProviderRequestError('catalog_not_prepared')
            if request.output_tokens > self.catalog_metadata['max_output']:
                raise Incomplete('provider output token budget')
            self._encoded(body)
            return None
        # Same frozen input/instructions/schema as generation. No output tokens generated.
        self._encoded({**body, 'max_output_tokens': request.output_tokens, 'truncation': 'disabled', 'store': False})
        data = await self._http('POST', 'https://api.openai.com/v1/responses/input_tokens', body)
        count = data.get('input_tokens')
        if data.get('object') != 'response.input_tokens' or type(count) is not int or count < 0:
            raise ProviderRequestError('invalid_input_token_count')
        return count

    def _encoded(self, body):
        encoded = canonical(body).encode('utf-8')
        if len(encoded) > WIRE_CAP:
            raise Incomplete('provider wire byte budget')
        return encoded

    async def _http(self, method, url, body, *, authenticated=True, cap=RESPONSE_CAP):
        headers = {'Content-Type': 'application/json'}
        if authenticated:
            headers['Authorization'] = 'Bearer ' + self.settings.api_key
        encoded = self._encoded(body) if body is not None else None
        audit_dispatch()
        try:
            async with self.client.stream(method, url, headers=headers, content=encoded) as response:
                if response.status_code in (401, 403):
                    raise AuthenticationError('provider_authentication')
                if response.status_code == 429 or response.status_code >= 500:
                    raise TransientModelError('provider_transient')
                if response.status_code != 200:
                    raise ProviderRequestError(f'provider_http_{response.status_code}')
                chunks, size = [], 0
                async for chunk in response.aiter_bytes():
                    size += len(chunk)
                    if size > cap:
                        raise ProviderRequestError('provider_response_byte_budget')
                    chunks.append(chunk)
                raw = b''.join(chunks)
        except (httpx.TimeoutException, httpx.TransportError):
            raise TransientModelError('provider_network') from None
        try:
            data = json.loads(raw)
        except (ValueError, UnicodeError):
            raise ValueError('provider_invalid_json') from None
        if not isinstance(data, dict):
            raise ValueError('provider_invalid_envelope')
        if url.endswith(('/chat/completions', '/responses')):
            self._capture_usage(data)
        if data.get('error'):
            error = data['error']
            code = error.get('code') if isinstance(error, dict) else None
            if isinstance(code, str) and len(code) == 3 and code.isascii() and code.isdigit():
                code = int(code)
            if type(code) is int:
                if code in (401, 403):
                    raise AuthenticationError('provider_authentication')
                if code == 429 or 500 <= code <= 599:
                    raise TransientModelError('provider_transient')
            raise ProviderRequestError('provider_body_error')
        return data

    def _capture_usage(self, data):
        usage = data.get('usage')
        fields = ('input_tokens', 'output_tokens') if self.settings.provider == 'openai' else ('prompt_tokens', 'completion_tokens')
        usage = usage if isinstance(usage, dict) else {}
        counts = [usage.get(key) for key in fields]
        safe = [x if type(x) is int and x >= 0 else None for x in counts]
        actual = data.get('model')
        safe_model = actual if isinstance(actual, str) and MODEL_ID.fullmatch(actual) and self.settings.api_key not in actual else None
        cost = usage.get('cost_rub') if self.settings.provider == 'aitunnel' else None
        cost = cost if type(cost) in (int, float) and math.isfinite(cost) and cost >= 0 else None
        audit_update(input_tokens=safe[0], output_tokens=safe[1], returned_model=safe_model, cost_rub=cost)
        return safe

    def _usage(self, data):
        safe = self._capture_usage(data)
        if None in safe:
            raise ValueError('provider_missing_usage')
        total = data['usage'].get('total_tokens')
        if total is not None and (type(total) is not int or total != sum(safe)):
            raise ValueError('provider_invalid_usage_total')
        if data.get('model') != self.settings.model:
            raise ProviderRequestError('provider_model_mismatch')
        return safe

    async def generate(self, request):
        body = self._wire(request)
        if self.settings.provider == 'openai':
            body.update(max_output_tokens=request.output_tokens, truncation='disabled', store=False)
            data = await self._http('POST', 'https://api.openai.com/v1/responses', body)
        else:
            data = await self._http('POST', 'https://api.aitunnel.ru/v1/chat/completions', body)
        counts = self._usage(data)
        if counts[1] > output_token_ceiling(self.capabilities, request.output_tokens):
            raise ProviderRequestError('provider_output_token_budget')
        if self.settings.provider == 'openai':
            output = data.get('output')
            if data.get('status') != 'completed' or not isinstance(output, list):
                raise ProviderRequestError('provider_incomplete_or_refused')
            messages = [item for item in output if isinstance(item, dict) and item.get('type') == 'message']
            if len(messages) != 1 or any(not isinstance(x, dict) or x.get('type') not in ('message', 'reasoning') for x in output):
                raise ProviderRequestError('provider_unexpected_output')
            content = messages[0].get('content')
            if (messages[0].get('role') != 'assistant' or messages[0].get('status') != 'completed' or
                    not isinstance(content, list) or len(content) != 1 or not isinstance(content[0], dict) or
                    content[0].get('type') != 'output_text'):
                raise ProviderRequestError('provider_incomplete_or_refused')
            text = content[0].get('text')
        else:
            choices = data.get('choices')
            if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
                raise ProviderRequestError('provider_unexpected_choices')
            message = choices[0].get('message')
            if choices[0].get('finish_reason') != 'stop' or not isinstance(message, dict) or message.get('tool_calls') or message.get('refusal'):
                raise ProviderRequestError('provider_incomplete_or_refused')
            text = message.get('content')
        if not isinstance(text, str) or not text.strip() or len(text.encode('utf-8')) > 65536:
            raise ValueError('provider_invalid_text')
        if self.settings.api_key in text:
            raise ProviderRequestError('provider_secret_echo')
        parsed = json.loads(text)
        original = json.loads(request.response_schema_json)
        return Response(canonical(restore_defaults(parsed, original, original)), *counts)


def make_adapter(settings, *, transport=None):
    return ProviderAdapter(settings, transport=transport)
