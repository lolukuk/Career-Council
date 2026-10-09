import asyncio
import contextvars
import gc
import importlib
import json
import time
from dataclasses import replace
from types import SimpleNamespace

import httpx
import pytest

from council.main import main
from council.model import (AuthenticationError, Capabilities, ProviderRequestError,
                           Request, check_adapter, invoke)
from council.providers import ProviderAdapter, restore_defaults, transport_schema
from council.report import render
from council.runtime import Council
from council.schemas import Config, ConflictInput, Incomplete, Position, canonical
from council.scripted import ScriptedAdapter
from council.settings import Settings, SettingsError, load_settings

SECRET = 'sk-fixture-secret'
MODEL = 'fixture-model-2026'


def request(**updates):
    value = Request('initial', 'peter_thiel', 'run', 'snapshot', 0, 'request', 'attempt',
                    'Immutable policy', '{"untrusted":"досье"}',
                    canonical({'type': 'object', 'properties': {'ok': {'type': 'boolean'}},
                               'required': ['ok'], 'additionalProperties': False}), 2000)
    return replace(value, **updates)


def response(provider, text='{"ok":true}', **updates):
    if provider == 'openai':
        data = {'model': MODEL, 'status': 'completed',
                'output': [{'type': 'message', 'role': 'assistant', 'status': 'completed',
                            'content': [{'type': 'output_text', 'text': text}]}],
                'usage': {'input_tokens': 100, 'output_tokens': 50, 'total_tokens': 150}}
    else:
        data = {'model': MODEL, 'choices': [{'finish_reason': 'stop', 'message': {'content': text}}],
                'usage': {'prompt_tokens': 100, 'completion_tokens': 50, 'total_tokens': 150,
                          'cost_rub': 0.125, 'balance': 999}}
    data.update(updates)
    return data


def fixture_adapter(provider, handler):
    async def dispatch(req):
        if req.url.path == '/public/aitunnel/models':
            assert 'authorization' not in req.headers
            return httpx.Response(200, json={'chat': {MODEL: {'context_size': 8192, 'max_output': 4096}}})
        return await handler(req)
    return ProviderAdapter(Settings(provider, MODEL, SECRET), transport=httpx.MockTransport(dispatch))


async def use(adapter, action):
    try:
        await adapter.prepare()
        return await action(adapter)
    finally:
        await adapter.aclose()


def test_settings_provider_keys_and_precedence(tmp_path):
    path = tmp_path / '.env'
    path.write_text('LLM_PROVIDER=aitunnel\nLLM_MODEL="custom/model"\nAITUNNEL_API_KEY=ait-key\n'
                    'OPENAI_API_KEY=open-key\nLLM_API_KEY=legacy-secret\n', encoding='utf-8')
    ait = load_settings(path, environ={})
    direct = load_settings(path, provider='openai', environ={'LLM_MODEL': MODEL})
    assert ait.api_key == 'ait-key' and ait.model == 'custom/model'
    assert direct.api_key == 'open-key' and direct.model == MODEL
    assert 'open-key' not in repr(direct)
    with pytest.raises(SettingsError, match='OPENAI_API_KEY'):
        load_settings(tmp_path / 'missing', provider='openai', model=MODEL,
                      environ={'AITUNNEL_API_KEY': SECRET, 'LLM_API_KEY': SECRET})
    with pytest.raises(SettingsError):
        load_settings(path, model='auto', environ={})
    with pytest.raises(SettingsError):
        load_settings(path, model='thing~latest', environ={})


def test_missing_model_cli_before_dossier(tmp_path, monkeypatch, capsys):
    for key in ('LLM_PROVIDER', 'LLM_MODEL', 'OPENAI_API_KEY', 'AITUNNEL_API_KEY'):
        monkeypatch.delenv(key, raising=False)
    assert main(['--mode', 'model', '--provider', 'openai', '--env-file', str(tmp_path / '.env'),
                 '--dossier', str(tmp_path / 'dossier'), '--output', str(tmp_path / 'out')]) == 2
    assert not (tmp_path / 'out').exists()
    assert SECRET not in capsys.readouterr().err


def test_schema_defaults_and_tuple_guards():
    original = Position.model_json_schema()
    converted = transport_schema(original)
    assert set(converted['required']) == set(original['properties'])
    assert converted['additionalProperties'] is False
    conflict = converted['$defs']['ConflictInput']['properties']['citations']
    assert 'prefixItems' not in conflict and conflict['items'] == {'$ref': '#/$defs/Citation'}
    assert '"maxItems":4' in converted['properties']['criteria']['description']
    assert '"minItems":1' in converted['properties']['criteria']['description']
    assert '"maxItems":2' in conflict['description'] and '"minItems":2' in conflict['description']
    assert '"maxLength":400' in converted['$defs']['Citation']['properties']['quote']['description']
    restored = restore_defaults({'missing_data': None, 'recommendation': None,
                                'arguments': [{'text': 'x', 'basis': 'assumption', 'citations': None,
                                               'impact': None}]}, original, original)
    assert 'missing_data' not in restored and restored['recommendation'] is None
    assert restored['arguments'][0] == {'text': 'x', 'basis': 'assumption'}
    with pytest.raises(ValueError):
        ConflictInput.model_validate_json(canonical({'text': 'conflict', 'citations': [{'chunk_id': 'e1', 'quote': 'x'}]}))


def test_optional_effort_precedence_and_validation(tmp_path):
    path = tmp_path / '.env'
    path.write_text(f'LLM_PROVIDER=openai\nLLM_MODEL={MODEL}\nOPENAI_API_KEY={SECRET}\n'
                    'LLM_REASONING_EFFORT=low\n', encoding='utf-8')
    assert load_settings(path, environ={}).reasoning_effort == 'low'
    assert load_settings(path, environ={'LLM_REASONING_EFFORT': 'medium'}).reasoning_effort == 'medium'
    assert load_settings(path, reasoning_effort='none', environ={'LLM_REASONING_EFFORT': 'medium'}).reasoning_effort == 'none'
    with pytest.raises(SettingsError):
        load_settings(path, reasoning_effort='secret-invalid', environ={})


@pytest.mark.parametrize('provider', ['openai', 'aitunnel'])
def test_optional_effort_frozen_in_wire(provider):
    adapter = ProviderAdapter(Settings(provider, MODEL, SECRET, 'none'), transport=httpx.MockTransport(lambda req: None))
    default = ProviderAdapter(Settings(provider, MODEL, SECRET), transport=httpx.MockTransport(lambda req: None))
    assert adapter._wire(request())['reasoning'] == {'effort': 'none'}
    assert 'reasoning' not in default._wire(request())
    async def close():
        await adapter.aclose()
        await default.aclose()
    asyncio.run(close())


@pytest.mark.parametrize('provider', ['openai', 'aitunnel'])
def test_exact_wire_and_usage(provider):
    wire = []
    async def handler(req):
        assert req.headers['authorization'] == 'Bearer ' + SECRET
        assert req.url.host == ('api.openai.com' if provider == 'openai' else 'api.aitunnel.ru')
        body = json.loads(req.content)
        wire.append((req.url.path, body))
        assert SECRET not in req.content.decode()
        if req.url.path.endswith('/input_tokens'):
            return httpx.Response(200, json={'object': 'response.input_tokens', 'input_tokens': 100})
        return httpx.Response(200, json=response(provider))
    async def action(adapter):
        check_adapter(adapter)
        result = await invoke(adapter, request(), 1)
        assert result.input_tokens == 100 and result.output_tokens == 50
        assert result.metadata['returned_model'] == MODEL
        assert result.metadata['http_dispatches'] == (2 if provider == 'openai' else 1)
        assert result.metadata['preflight_count'] == (100 if provider == 'openai' else None)
        assert 'balance' not in result.metadata
        assert SECRET not in canonical(result.metadata) and SECRET not in repr(adapter)
    asyncio.run(use(fixture_adapter(provider, handler), action))
    if provider == 'openai':
        count, generation = wire[0][1], wire[1][1]
        assert {k: generation[k] for k in count} == count
        assert generation['truncation'] == 'disabled' and generation['store'] is False
    else:
        body = wire[0][1]
        assert body['plugins'] == [{'id': 'context-compression', 'enabled': False}]
        assert body['max_tokens'] == 2000 and body['stream'] is False
        assert body['messages'][1]['content'] == request().payload_json


def test_openai_overbudget_no_generation():
    paths = []
    async def handler(req):
        paths.append(req.url.path)
        return httpx.Response(200, json={'object': 'response.input_tokens', 'input_tokens': 32700})
    async def action(adapter):
        with pytest.raises(Incomplete):
            await invoke(adapter, request(), 1)
    asyncio.run(use(fixture_adapter('openai', handler), action))
    assert paths == ['/v1/responses/input_tokens']


@pytest.mark.parametrize('provider', ['openai', 'aitunnel'])
@pytest.mark.parametrize('failure', ['auth', '400', 'body', 'mismatch', 'refusal', 'length', 'usage', 'text', 'tool', 'overbudget'])
def test_rejected_provider_response_audited(provider, failure):
    async def handler(req):
        if req.url.path.endswith('/input_tokens'):
            return httpx.Response(200, json={'object': 'response.input_tokens', 'input_tokens': 100})
        if failure == 'auth':
            return httpx.Response(401, json={'error': {'message': SECRET}})
        if failure == '400':
            return httpx.Response(400, json={'error': {'message': 'context overflow ' + SECRET}})
        data = response(provider)
        if failure == 'body':
            data['error'] = {'message': SECRET}
        elif failure == 'mismatch':
            data['model'] = 'other-model'
        elif failure == 'usage':
            data['usage'] = {'input_tokens': True, 'prompt_tokens': True}
        elif failure == 'overbudget':
            data['usage'] = {'input_tokens': 100, 'output_tokens': 3753,
                             'prompt_tokens': 100, 'completion_tokens': 3753, 'total_tokens': 3853}
        elif provider == 'openai':
            if failure == 'length':
                data['status'] = 'incomplete'
            elif failure == 'refusal':
                data['output'][0]['content'] = [{'type': 'refusal', 'refusal': SECRET}]
            elif failure == 'tool':
                data['output'].append({'type': 'function_call'})
            else:
                data['output'][0]['content'][0]['text'] = '{'
        else:
            if failure == 'length':
                data['choices'][0]['finish_reason'] = 'length'
            elif failure == 'refusal':
                data['choices'][0]['message']['refusal'] = SECRET
            elif failure == 'tool':
                data['choices'][0]['message']['tool_calls'] = [{'name': 'bad'}]
            else:
                data['choices'][0]['message']['content'] = '{'
        return httpx.Response(200, json=data)
    async def action(adapter):
        with pytest.raises((AuthenticationError, ProviderRequestError, ValueError)) as caught:
            await invoke(adapter, request(), 1)
        exc = caught.value
        assert SECRET not in str(exc) and SECRET not in canonical(exc.safe_metadata)
        if failure in ('body', 'mismatch', 'refusal', 'length', 'tool', 'text'):
            assert exc.safe_metadata['output_tokens'] == 50
        if failure == 'overbudget':
            assert isinstance(exc, ProviderRequestError) and exc.safe_metadata['output_tokens'] == 3753
    asyncio.run(use(fixture_adapter(provider, handler), action))


def test_preflight_and_generation_share_deadline():
    paths = []
    async def handler(req):
        paths.append(req.url.path)
        await asyncio.sleep(.04)
        return httpx.Response(200, json={'object': 'response.input_tokens', 'input_tokens': 100})
    async def action(adapter):
        with pytest.raises(asyncio.TimeoutError) as caught:
            await invoke(adapter, request(), .005)
        assert caught.value.safe_metadata['http_dispatches'] == 1
    asyncio.run(use(fixture_adapter('openai', handler), action))
    assert paths == ['/v1/responses/input_tokens']


def test_total_deadline_includes_completed_count_and_generation():
    paths = []
    async def handler(req):
        paths.append(req.url.path)
        if req.url.path.endswith('/input_tokens'):
            await asyncio.sleep(.03)
            return httpx.Response(200, json={'object': 'response.input_tokens', 'input_tokens': 100})
        await asyncio.sleep(.12)
        return httpx.Response(200, json=response('openai'))
    async def action(adapter):
        with pytest.raises(asyncio.TimeoutError):
            await invoke(adapter, request(), .1)
    asyncio.run(use(fixture_adapter('openai', handler), action))
    assert paths == ['/v1/responses/input_tokens', '/v1/responses']


def test_cancel_suppressed_preflight_cannot_dispatch_generation():
    paths = []
    async def handler(req):
        paths.append(req.url.path)
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            await asyncio.sleep(.01)
        return httpx.Response(200, json={'object': 'response.input_tokens', 'input_tokens': 100})
    async def action(adapter):
        with pytest.raises(asyncio.TimeoutError) as caught:
            await invoke(adapter, request(), .005)
        saved = dict(caught.value.safe_metadata)
        await asyncio.sleep(.04)
        assert caught.value.safe_metadata == saved
    asyncio.run(use(fixture_adapter('openai', handler), action))
    assert paths == ['/v1/responses/input_tokens']


@pytest.mark.parametrize('entry', [None, {'context_size': True, 'max_output': 4000},
                                {'context_size': 8000, 'max_output': 1000}])
def test_unusable_catalog_refuses_before_generation(entry):
    paths = []
    async def handler(req):
        paths.append(req.url.path)
        return httpx.Response(200, json={'chat': {} if entry is None else {MODEL: entry}})
    adapter = ProviderAdapter(Settings('aitunnel', MODEL, SECRET), transport=httpx.MockTransport(handler))
    async def action():
        try:
            with pytest.raises(ProviderRequestError):
                await adapter.prepare()
            with pytest.raises(ValueError):
                check_adapter(adapter)
        finally:
            await adapter.aclose()
    asyncio.run(action())
    assert paths == ['/public/aitunnel/models']


def scripted_http_adapter(provider, scenario, test_mode=False):
    original_request = contextvars.ContextVar('fixture_original_request')
    scripted = ScriptedAdapter(scenario)
    class Adapter(ProviderAdapter):
        async def generate(self, value):
            token = original_request.set(value)
            try:
                return await super().generate(value)
            finally:
                original_request.reset(token)
    async def handler(req):
        if req.url.path == '/public/aitunnel/models':
            return httpx.Response(200, json={'chat': {MODEL: {'context_size': 8192, 'max_output': 4096}}})
        if req.url.path.endswith('/input_tokens'):
            return httpx.Response(200, json={'object': 'response.input_tokens', 'input_tokens': 100})
        text = (await scripted.generate(original_request.get())).payload_json
        data = response(provider, text)
        if test_mode:
            data['usage'].update(completion_tokens=3753, total_tokens=3853)
        return httpx.Response(200, json=data)
    return Adapter(Settings(provider, MODEL, SECRET, aitunnel_test_mode=test_mode), transport=httpx.MockTransport(handler))


@pytest.mark.parametrize('provider,test_mode', [('openai', False), ('aitunnel', False), ('aitunnel', True)])
@pytest.mark.parametrize('scenario', ['agree', 'revise', 'disagree'])
def test_live_adapter_protocol_with_http_fixtures(provider, test_mode, scenario, retriever, personas):
    adapter = scripted_http_adapter(provider, scenario, test_mode)
    async def action(value):
        council = Council('Career?', personas, tuple(retriever.sources.values()), retriever, value)
        await council.run()
        trace = council.trace()
        assert council.status == ('no_consensus' if scenario == 'disagree' else 'consensus')
        assert len(council.decisions) == {'agree': 1, 'revise': 2, 'disagree': 3}[scenario]
        assert all(u['accepted'] and u['returned_model'] == MODEL for u in trace['usage'])
        assert all(u['preflight_count'] == (100 if provider == 'openai' else None) for u in trace['usage'])
        assert trace['output_limit_policy'] == ('aitunnel_test' if test_mode else 'strict')
        assert trace['accepted_output_token_ceiling'] == (8000 if test_mode else 2000)
        assert all(u['requested_output_tokens'] == 2000 and u['output_limit_exceeded'] is test_mode for u in trace['usage'])
        assert ('Условный тестовый режим AI Tunnel' in render(trace)) is test_mode
        assert SECRET not in canonical(trace) and SECRET not in render(trace)
        assert 'server_enforced' in render(trace) if provider == 'aitunnel' else 'server_exact' in render(trace)
    asyncio.run(use(adapter, action))


@pytest.mark.parametrize('tokens', [3753, 8000, 8001])
def test_aitunnel_test_ceiling_is_bounded(tokens):
    async def handler(req):
        if req.url.path.endswith('/models'):
            return httpx.Response(200, json={'chat': {MODEL: {'context_size': 8192, 'max_output': 8192}}})
        assert json.loads(req.content)['max_tokens'] == 2000
        data = response('aitunnel')
        data['usage'].update(completion_tokens=tokens, total_tokens=100+tokens)
        return httpx.Response(200, json=data)
    adapter = ProviderAdapter(Settings('aitunnel', MODEL, SECRET, aitunnel_test_mode=True), transport=httpx.MockTransport(handler))
    async def action(value):
        if tokens <= 8000:
            reply = await invoke(value, request(), 1)
            assert reply.output_tokens == tokens
        else:
            with pytest.raises(ProviderRequestError, match='provider_output_token_budget') as caught:
                await invoke(value, request(), 1)
            assert caught.value.safe_metadata['output_tokens'] == tokens
    asyncio.run(use(adapter, action))


def test_test_profile_rejects_openai_before_disclosure(tmp_path, monkeypatch, capsys):
    with pytest.raises(SettingsError):
        Settings('openai', MODEL, SECRET, aitunnel_test_mode=True)
    with pytest.raises(SettingsError):
        load_settings(tmp_path/'missing', provider='openai', model=MODEL, aitunnel_test_mode=True, environ={})
    assert main(['--mode', 'model', '--provider', 'openai', '--model', MODEL, '--aitunnel-test-mode',
                 '--env-file', str(tmp_path/'missing'), '--dossier', str(tmp_path/'missing-dossier')]) == 2
    assert 'только для AI Tunnel' in capsys.readouterr().err
    adapter = fixture_adapter('openai', lambda req: None)
    adapter.capabilities = replace(adapter.capabilities, output_limit_policy='aitunnel_test')
    with pytest.raises(ValueError):
        check_adapter(adapter)
    asyncio.run(adapter.aclose())


def test_cancelled_siblings_preserve_unknown_attempt_usage(retriever, personas):
    adapter = fixture_adapter('aitunnel', lambda req: None)
    adapter.settings = replace(adapter.settings, aitunnel_test_mode=True)
    started = 0
    async def action(value):
        nonlocal started
        all_started = asyncio.Event()
        async def generate(req):
            nonlocal started
            started += 1
            if started == 5:
                all_started.set()
            await all_started.wait()
            if req.persona_id == 'peter_thiel':
                raise ProviderRequestError('provider_model_mismatch')
            await asyncio.Future()  # Sibling terminal failure must cancel this.
        value.generate = generate
        council = Council('Career?', personas, tuple(retriever.sources.values()), retriever, value)
        # This regression isolates the initial-position barrier, independently
        # of the preceding sequential note filter and typed tool planning.
        async def no_notes(_):
            return {'next': 'tools'}
        async def no_tools(_):
            return {'next': 'analyze'}
        council.select_notes, council.read_tools = no_notes, no_tools
        await council.run()
        trace = council.trace()
        assert trace['status'] == 'failed' and trace['attempts'] == 5
        assert len(trace['usage']) == 5
        assert {e['attempt_id'] for e in trace['events']} == {u['attempt_id'] for u in trace['usage']}
        assert sum(e.get('error') == 'CancelledError' for e in trace['events']) == 4
        assert all(not u['accepted'] and u['output_tokens'] is None and
                   u['output_limit_exceeded'] is None and u['requested_output_tokens'] == 2000
                   for u in trace['usage'])
        assert not trace['initial_positions'] and not trace['decisions']
    asyncio.run(use(adapter, action))


@pytest.mark.parametrize('failure,stage,code', [('quote', 'citations', 'citation_selection_shape'),
                                              ('unseen', 'citations', 'citation_selection_not_shown'),
                                              ('schema', 'schema', 'schema_invalid'),
                                              ('json', 'provider', 'response_json')])
def test_validation_diagnostics_are_specific_and_secret_free(failure, stage, code, retriever, personas):
    class Invalid(ScriptedAdapter):
        async def generate(self, request):
            if failure == 'json':
                raise json.JSONDecodeError(SECRET, SECRET, 0)
            reply = await super().generate(request)
            payload = json.loads(reply.payload_json)
            if failure == 'schema':
                payload['recommendation'] = {'untrusted': SECRET}
            elif failure == 'unseen':
                payload['arguments'][0]['citations'][0]['evidence_id'] = 'not-shown'
            else:
                payload['arguments'][0]['citations'][0]['quote'] = SECRET
            return replace(reply, payload_json=canonical(payload))
    async def action():
        council = Council('Career?', personas, tuple(retriever.sources.values()), retriever, Invalid())
        persona = personas.personas[2]
        packet, seen = council.context('initial', persona, Position)
        with pytest.raises(RuntimeError):
            await council.call('initial', persona, Position, packet, seen, lambda _: None)
        assert len(council.events) == 2
        assert all(e['validation_stage'] == stage and e['validation_code'] == code for e in council.events)
        assert SECRET not in canonical(council.trace()) and SECRET not in render(council.trace())
    asyncio.run(action())


def test_report_distinguishes_valid_response_from_uncommitted_barrier():
    trace = {'mode': 'model', 'status': 'failed', 'reason': 'barrier failure', 'question': 'Career?',
             'events': [{'stage': 'initial', 'persona': 'peter_thiel', 'accepted': True},
                        {'stage': 'initial', 'persona': 'robert_reich', 'accepted': False,
                         'validation_code': 'citation_quote_not_exact'},
                        {'stage': 'initial', 'persona': 'marcus_aurelius', 'accepted': False,
                         'error': 'CancelledError'}]}
    report = render(trace)
    assert 'Ответ персоны прошёл проверку, но общий этап пяти позиций не завершён' in report
    assert 'Цитата не совпадает с дословным фрагментом источника.' in report
    assert 'Запрос отменён; ответ не завершён.' in report


@pytest.mark.parametrize('provider', ['openai', 'aitunnel'])
def test_cli_model_lifecycle_without_real_credentials(provider, retriever, tmp_path, monkeypatch):
    module = importlib.import_module('council.main')
    env_file = tmp_path / '.env'
    env_file.write_text(f'LLM_PROVIDER={provider}\nLLM_MODEL={MODEL}\n'
                        f'OPENAI_API_KEY={SECRET}\nAITUNNEL_API_KEY={SECRET}\n', encoding='utf-8')
    for key in ('LLM_PROVIDER', 'LLM_MODEL', 'OPENAI_API_KEY', 'AITUNNEL_API_KEY'):
        monkeypatch.delenv(key, raising=False)
    adapter = scripted_http_adapter(provider, 'agree')
    monkeypatch.setattr(module, 'make_adapter', lambda settings: adapter)
    monkeypatch.setattr(module, 'Encoder', lambda *args: SimpleNamespace(config=args[0], events=[]))
    monkeypatch.setattr(module, 'Sources', lambda *args, **kwargs: SimpleNamespace(
        events=[], load=lambda dossier: tuple(retriever.sources.values())))
    monkeypatch.setattr(module.Retriever, 'prepare', lambda sources, encoder: retriever)
    assert module.main(['--mode', 'model', '--env-file', str(env_file), '--output', str(tmp_path / 'out')]) == 0
    trace_path = next((tmp_path / 'out').glob('*/trace.json'))
    raw = trace_path.read_text(encoding='utf-8')
    trace = json.loads(raw)
    assert trace['mode'] == 'model' and trace['provider'] == provider and trace['status'] == 'consensus'
    assert (trace_path.parent / 'report.md').is_file() and adapter.client.is_closed
    assert SECRET not in raw


def test_already_done_expired_inner_error_is_consumed():
    errors = []
    class Failed(ScriptedAdapter):
        async def generate(self, value):
            # Simulate a child finishing with an error while the loop cannot process expiry.
            time.sleep(.01)
            raise ValueError('fixture failure')
    async def scenario():
        asyncio.get_running_loop().set_exception_handler(lambda loop, context: errors.append(context))
        with pytest.raises(asyncio.TimeoutError):
            await invoke(Failed(), request(), .001)
        gc.collect()
        await asyncio.sleep(.01)
    asyncio.run(scenario())
    assert not errors


@pytest.mark.parametrize('status,expected', [(401, 1), (429, 2), (400, 1), (503, 2)])
@pytest.mark.parametrize('body_error', [False, True])
def test_runtime_terminal_and_transient_retries(status, expected, body_error, retriever, personas):
    calls = {}
    async def handler(req):
        persona = json.loads(req.content)['messages'][1]['content']
        calls[persona] = calls.get(persona, 0) + 1
        return httpx.Response(200 if body_error else status, json={
            'error': {'code': status, 'message': SECRET},
            'model': MODEL, 'usage': {'prompt_tokens': 100, 'completion_tokens': 50, 'cost_rub': .125}})
    async def action(adapter):
        council = Council('Career?', personas, tuple(retriever.sources.values()), retriever, adapter)
        await council.run()
        assert council.status == 'failed' and not council.positions
        assert max(calls.values()) == expected
        assert all(not u['accepted'] for u in council.usage)
        if body_error:
            assert any(u['output_tokens'] == 50 for u in council.usage)
        assert any(e.get('provider_error') for e in council.events)
        assert SECRET not in canonical(council.trace())
    asyncio.run(use(fixture_adapter('aitunnel', handler), action))


def test_server_policy_cannot_masquerade_as_reliable():
    class Fake:
        mode = 'model'
        capabilities = Capabilities(True, True, 8192, True, MODEL, 'server_enforced', 'aitunnel')
    with pytest.raises(ValueError):
        check_adapter(Fake())


@pytest.mark.parametrize('upstream,field', [('openai', 'max_completion_tokens'), ('anthropic', 'max_tokens')])
def test_catalog_selects_output_cap_field(upstream, field):
    wires = []
    async def handler(req):
        if req.url.path == '/public/aitunnel/models':
            return httpx.Response(200, json={'chat': {MODEL: {
                'provider': upstream, 'context_size': 8192, 'max_output': 4096}}})
        wires.append(json.loads(req.content))
        return httpx.Response(200, json=response('aitunnel'))
    adapter = ProviderAdapter(Settings('aitunnel', MODEL, SECRET), transport=httpx.MockTransport(handler))
    async def action(value):
        await invoke(value, request(), 1)
        assert value.catalog_metadata['upstream_provider'] == upstream
    asyncio.run(use(adapter, action))
    assert wires[0][field] == 2000
    assert set(wires[0]).intersection({'max_tokens', 'max_completion_tokens'}) == {field}


def test_wire_overflow_without_cropping():
    adapter = ProviderAdapter(Settings('openai', MODEL, SECRET), transport=httpx.MockTransport(lambda req: None))
    async def action(value):
        with pytest.raises(Incomplete):
            value._encoded({'schema': 'x' * 131072})
    asyncio.run(use(adapter, action))
