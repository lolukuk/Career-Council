import asyncio
import json
import threading
import time

import pytest

from council.model import AuthenticationError, Capabilities, Response, TransientModelError
from council.runtime import Council
from council.schemas import Config
from council.scripted import ScriptedAdapter


def execute(retriever, personas, adapter, **kwargs):
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, adapter, **kwargs)
    return asyncio.run(c.run())


class Flaky(ScriptedAdapter):
    def __init__(self, error, recover=False):
        super().__init__()
        self.error, self.recover, self.counts = error, recover, {}

    async def generate(self, request):
        p = request.payload()
        task_id = p.get('repair', {}).get('base_request_id', request.request_id)
        count = self.counts.get(task_id, 0)
        self.counts[task_id] = count + 1
        if not self.recover or count == 0:
            if self.error == 'json':
                self.requests.append(request)
                return Response('{')
            raise self.error('test')
        return await super().generate(request)


def test_same_frozen_request_repair(retriever, personas):
    adapter = Flaky('json', recover=True)
    c = execute(retriever, personas, adapter)
    assert c.status == 'consensus' and c.attempts == 44
    for id_ in adapter.counts:
        calls = [r for r in adapter.requests if r.payload().get('repair', {}).get('base_request_id', r.request_id) == id_]
        assert len(calls) == 2 and calls[0].request_id != calls[1].request_id
        before, after = map(lambda r: r.payload(), calls)
        repair = after.pop('repair')
        assert before == after and repair['base_request_id'] == calls[0].request_id
        assert repair['validation_code'] == 'schema_invalid'
        assert calls[0].attempt_id != calls[1].attempt_id


@pytest.mark.parametrize('error', ['json', TransientModelError, AuthenticationError])
def test_exhausted_or_auth_no_consensus(retriever, personas, error):
    adapter = Flaky(error)
    c = execute(retriever, personas, adapter)
    assert c.status == 'failed' and not c.decisions
    assert max(adapter.counts.values()) == (1 if error == AuthenticationError else 2)


def test_unconfigured_live_denied_before_disclosure(retriever, personas):
    class Live(ScriptedAdapter):
        mode = 'model'
        capabilities = Capabilities()
    with pytest.raises(ValueError):
        Council('Career?', personas, tuple(retriever.sources.values()), retriever, Live())


def test_live_token_cap_prevents_dispatch(retriever, personas):
    class Live(ScriptedAdapter):
        mode = 'model'
        capabilities = Capabilities(True, True, 1000, True, 'test-model')
        def count_tokens(self, request):
            return 2000
    adapter = Live()
    c = execute(retriever, personas, adapter)
    assert c.status == 'incomplete' and not adapter.requests


def test_timeout_and_cancel_late_result(retriever, personas):
    class Slow(ScriptedAdapter):
        async def generate(self, request):
            await asyncio.sleep(.2)
            return await super().generate(request)
    c = execute(retriever, personas, Slow(), config=Config(model_timeout=.01))
    assert c.status == 'failed' and not c.positions
    event = threading.Event()
    class Cancel(ScriptedAdapter):
        async def generate(self, request):
            value = await super().generate(request)
            if request.stage == 'review':
                event.set()
            return value
    c = execute(retriever, personas, Cancel(), cancel=event)
    assert c.status == 'cancelled' and not c.votes


def test_suppressed_cancellation_cannot_revive_expired_attempt(retriever, personas):
    class Late(ScriptedAdapter):
        async def generate(self, request):
            try:
                await asyncio.sleep(.05)
            except asyncio.CancelledError:
                await asyncio.sleep(.02)
            return await super().generate(request)
    started = time.monotonic()
    c = execute(retriever, personas, Late(), config=Config(model_timeout=.001))
    assert c.status == 'failed' and not c.positions and not c.decisions
    assert not c.active_attempts
    assert not any(e.get('accepted') is True for e in c.events)
    assert time.monotonic() - started < .5


def test_expired_attempt_errors_are_consumed(retriever, personas):
    class Late(ScriptedAdapter):
        async def generate(self, request):
            try:
                await asyncio.sleep(.05)
            except asyncio.CancelledError:
                await asyncio.sleep(.02)
            return await super().generate(request)
    errors = []
    async def scenario():
        asyncio.get_running_loop().set_exception_handler(lambda loop, context: errors.append(context))
        c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, Late(),
                    Config(model_timeout=.001))
        await c.run()
        await asyncio.sleep(.1)
        return c
    c = asyncio.run(scenario())
    assert c.status == 'failed' and not errors


def test_slow_retrieval_does_not_hold_run_or_publish_late_packet(retriever, personas):
    original = retriever.search
    def slow(queries, **kwargs):
        time.sleep(.2)
        return original(queries, **kwargs)
    retriever.search = slow
    started = time.monotonic()
    c = execute(retriever, personas, ScriptedAdapter(), config=Config(deadline=.02))
    assert c.status == 'incomplete' and c.attempts == 0
    assert time.monotonic() - started < .1
    time.sleep(.25)  # Let the deliberately slow fixture finish; it cannot mutate run/coverage.
    assert not c.positions and not c.ranked and not retriever.coverage
