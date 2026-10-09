import asyncio
import json
from dataclasses import replace

import pytest

from council.citations import (SelectionError, catalog, excerpts, project_packet,
                               resolve_output, response_schema)
from council.context import validate_citations
from council.model import Response
from council.providers import restore_defaults, transport_schema
from council.runtime import Council, guard
from council.schemas import Citation, CompactPosition, Evidence, Position, Vote, canonical, digest
from council.scripted import ScriptedAdapter


def test_exact_excerpts_unicode_crlf_json_and_bounds():
    text = '# Heading\r\n\r\nФакт: $42,000 — семейный резерв.\r\nВторая строка.\r\n\r\n' + 'слово ' * 150 + '\n{"quote":"a\\nb"}'
    chunk = Evidence(chunk_id='e', source_id='s', text=text, start=0, end=len(text), digest=digest(text))
    rows = excerpts(chunk)
    assert ''.join(r['text'] for r in rows) == text
    assert len(rows) > 3 and len({r['evidence_id'] for r in rows}) == len(rows)
    start = 0
    for row in rows:
        assert row['evidence_id'].startswith('q') and len(row['evidence_id']) == 13
        assert row['text'] == text[start:start + len(row['text'])] and 1 <= len(row['text']) <= 400
        start += len(row['text'])
    assert any('Факт: $42,000' in r['text'] and '\r\nВторая' in r['text'] for r in rows)


def test_id_resolution_is_local_and_digest_checked(retriever):
    packet = project_packet({'evidence': [{'chunk_id': 'e1', 'source_id': 's1',
                                           'text': retriever.evidence['e1'].text}]}, retriever.evidence)
    allowed = catalog(packet, retriever.evidence, {'e1'})
    id_ = next(iter(allowed))
    citation = Citation.model_validate(resolve_output({'evidence_id': id_}, allowed))
    validate_citations(citation, retriever.evidence, {'e1'})
    for bad in ('unknown', excerpts(retriever.evidence['e0'])[0]['evidence_id'], 'e1:0:1'):
        with pytest.raises(SelectionError, match='citation_selection_not_shown'):
            resolve_output({'evidence_id': bad}, allowed)
    with pytest.raises(SelectionError, match='citation_not_shown'):
        catalog(packet, retriever.evidence, {'e0'})
    foreign_source = json.loads(canonical(packet))
    foreign_source['evidence'][0]['source_id'] = 'unregistered-source'
    with pytest.raises(SelectionError, match='citation_selection_invalid'):
        catalog(foreign_source, retriever.evidence, {'e1'})
    changed = dict(retriever.evidence, e1=retriever.evidence['e1'].model_copy(update={'text': 'tampered'}))
    with pytest.raises(SelectionError, match='evidence_digest'):
        catalog(packet, changed, {'e1'})
    packet['evidence'][0]['excerpts'][0]['text'] = 'substitute'
    with pytest.raises(SelectionError, match='citation_selection_invalid'):
        catalog(packet, retriever.evidence, {'e1'})


@pytest.mark.parametrize('value', [{'chunk_id': 'e1', 'quote': 'Hiring'},
    {'evidence_id': 'e1:0:1', 'quote': 'fabricated'}, {'evidence_id': 1}])
def test_no_free_quote_fallback_or_extra_keys(value):
    with pytest.raises(SelectionError, match='citation_selection_shape'):
        resolve_output({'arguments': [{'citations': [value]}]}, {})


def test_wire_schema_preserves_internal_dto_and_defaults():
    original = Position.model_json_schema()
    wire = response_schema(Position)
    assert 'quote' in original['$defs']['Citation']['properties']
    assert set(wire['$defs']['Citation']['properties']) == {'evidence_id'}
    assert wire['$defs']['Citation']['additionalProperties'] is False
    transport = transport_schema(wire)
    assert transport['$defs']['Citation']['required'] == ['evidence_id']
    assert restore_defaults({'missing_data': None}, wire, wire) == {}
    limited = response_schema(Position, ['qabc', 'qdef'])
    assert transport_schema(limited)['$defs']['Citation']['properties']['evidence_id']['enum'] == ['qabc', 'qdef']


def test_input_projection_preserves_exact_retained_span_and_provenance(retriever):
    original = {'positions': {'a': {'citations': [{'chunk_id': 'e1', 'quote': 'opportunity'}]}},
                'evidence': [{'chunk_id': 'e1', 'source_id': 's1', 'text': retriever.evidence['e1'].text,
                              'origin': 'fixture/1', 'location': '/'}]}
    before = canonical(original)
    packet = project_packet(original, retriever.evidence)
    assert canonical(original) == before
    id_ = packet['positions']['a']['citations'][0]['source_span']
    chunk, start, end = id_.split(':')
    shown_text = ''.join(e['text'] for e in packet['evidence'][0]['excerpts'])
    assert chunk == 'e1' and shown_text[int(start):int(end)] == 'opportunity'
    assert packet['evidence_sources']['s1'] == {'origin': 'fixture/1', 'location': '/'}
    # Audit reference is not authorization to select an unlisted subspan.
    with pytest.raises(SelectionError, match='citation_selection_not_shown'):
        resolve_output({'evidence_id': id_}, catalog(packet, retriever.evidence, {'e1'}))


@pytest.mark.parametrize('quote', ['Hiring opportunity', 'Hiring  opportunity', 'hiring opportunity'])
def test_original_exact_quote_guard_unchanged(retriever, quote):
    citation = Citation(chunk_id='e1', quote=quote)
    if quote == 'Hiring opportunity':
        validate_citations(citation, retriever.evidence, {'e1'})
    else:
        with pytest.raises(ValueError, match='nonexact citation quote'):
            validate_citations(citation, retriever.evidence, {'e1'})


def test_safe_targeted_repair_and_selected_trace(retriever, personas):
    class BadThenGood(ScriptedAdapter):
        async def generate(self, request):
            response = await super().generate(request)
            if request.stage == 'initial' and 'repair' not in request.payload():
                data = json.loads(response.payload_json)
                data['arguments'][0]['citations'][0]['evidence_id'] = 'untrusted-secret-unknown'
                return replace(response, payload_json=canonical(data))
            return response
    adapter = BadThenGood()
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, adapter)
    asyncio.run(c.run())
    assert c.status == 'consensus', c.reason
    repaired = [r for r in adapter.requests if 'repair' in r.payload()]
    assert len(repaired) == 5
    for request in repaired:
        payload = request.payload()
        feedback = payload.pop('repair')
        assert feedback['citation_path'] == '$.arguments[0].citations[0]'
        allowed = catalog(payload, retriever.evidence, {e['chunk_id'] for e in payload['evidence']})
        assert set(feedback['allowed_evidence_ids']) <= allowed.keys()
        assert request.request_id != feedback['base_request_id']
        assert len(request.serialized().encode('utf-8')) <= c.config.context_bytes
    assert 'untrusted-secret' not in canonical(c.trace())
    assert all(e.get('selected_evidence_ids') for e in c.events if e.get('accepted') and e['stage'] == 'initial')


def test_identical_text_keeps_actual_selected_offset_in_trace(retriever, personas):
    text = 'same\n\nsame\n\n'
    retriever.evidence['e0'] = Evidence(chunk_id='e0', source_id='s0', text=text,
        start=0, end=len(text), digest=digest(text))
    retriever.sources['s0'] = retriever.sources['s0'].model_copy(update={'text': text, 'content_digest': digest(text)})
    adapter = ScriptedAdapter()
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, adapter)
    asyncio.run(c.run())
    assert c.status == 'consensus'
    options = excerpts(retriever.evidence['e0'])
    assert len(options) == 2 and options[0]['text'] == options[1]['text']
    initials = [e for e in c.events if e.get('stage') == 'initial' and e.get('accepted')]
    assert len(initials) == 5
    assert all(e['selected_evidence_ids'] == [options[0]['evidence_id']] for e in initials)


def test_effective_enum_matches_each_measured_request(retriever, personas):
    adapter = ScriptedAdapter('revise')
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, adapter)
    asyncio.run(c.run())
    assert c.status == 'consensus'
    for request in adapter.requests:
        if request.stage not in ('initial', 'draft', 'review'):
            continue
        packet = request.payload()
        shown = [e['evidence_id'] for row in packet['evidence'] for e in row['excerpts']]
        wire = json.loads(request.response_schema_json)
        assert wire['$defs']['Citation']['properties']['evidence_id']['enum'] == shown
        assert len(request.serialized().encode('utf-8')) <= c.config.context_bytes
    with pytest.raises(Exception, match='no selectable evidence'):
        response_schema(Position, [])


def test_opaque_id_collision_fails_closed(retriever, monkeypatch):
    import council.citations as module
    original_digest = module.digest
    monkeypatch.setattr(module, 'digest', lambda x: 'f' * 64 if isinstance(x, list) else original_digest(x))
    packet = project_packet({'evidence': [dict(e.model_dump(mode='json')) for e in
                                         (retriever.evidence['e0'], retriever.evidence['e1'])]}, retriever.evidence)
    with pytest.raises(SelectionError, match='citation_selection_invalid'):
        catalog(packet, retriever.evidence, {'e0', 'e1'})


def test_compact_generation_is_stricter_than_unchanged_state_dto():
    from pydantic import ValidationError
    data = {'recommendation': 'Verify a bounded career experiment.',
            'arguments': [{'text': 'Budget remains unknown.', 'basis': 'assumption'}] * 3,
            'criteria': [{'id': 'c1', 'text': 'Budget AND schedule AND family consent must all be confirmed.'}],
            'strongest_counterargument': 'A slower transition can delay opportunity.'}
    assert len(Position.model_validate_json(canonical(data)).arguments) == 3
    with pytest.raises(ValidationError):
        CompactPosition.model_validate_json(canonical(data))
    data['arguments'] = data['arguments'][:2]
    assert len(CompactPosition.model_validate_json(canonical(data)).arguments) == 2
    data['criteria'].append({'id': 'c2', 'text': 'Second criterion.'})
    with pytest.raises(ValidationError):
        CompactPosition.model_validate_json(canonical(data))


def test_review_drops_uncited_tool_prefetch_but_keeps_cited_source(retriever, personas):
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, ScriptedAdapter())
    persona = personas.personas[0]
    c.tool_results[persona.id] = [{'name': 'get_task_details', 'records': [],
                                  'evidence': [retriever.evidence['e3'].model_dump(mode='json')]}]
    _, initial_seen = c.context('initial', persona, Position)
    _, review_seen = c.context('review', persona, Vote)
    assert 'e3' in initial_seen and 'e3' not in review_seen
    c.positions[persona.id] = Position.model_validate_json(canonical({
        'recommendation': 'Read the recorded budget task.',
        'arguments': [{'text': 'A budget task is recorded.', 'basis': 'source',
                       'citations': [{'chunk_id': 'e3', 'quote': 'Budget planning.'}]}],
        'criteria': [{'id': 'c1', 'text': 'Verify actual budget first.'}],
        'strongest_counterargument': 'The task is not proof that the budget is complete.'}))
    _, seen = c.context('review', persona, Vote)
    assert 'e3' in seen


def test_review_keeps_peer_uncertainty_and_full_owner_criteria(retriever, personas):
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, ScriptedAdapter())
    asyncio.run(c.run())
    own = personas.personas[0]
    packet, _ = c.context('review', own, Vote)
    assert packet['positions'][own.id]['criteria'] == c.positions[own.id].model_dump(mode='json')['criteria']
    for owner, position in c.positions.items():
        if owner != own.id:
            assert 'criteria' not in packet['positions'][owner]
        assert packet['positions'][owner]['missing_data'] == list(position.missing_data)
        assert packet['positions'][owner]['strongest_counterargument'] == position.strongest_counterargument


def test_initial_byte_budget_has_bounded_specific_repair(retriever, personas):
    class LargeOnce(ScriptedAdapter):
        async def generate(self, request):
            reply = await super().generate(request)
            if request.stage == 'initial' and 'repair' not in request.payload():
                data = json.loads(reply.payload_json)
                data['recommendation'] = 'x' * 2000
                return replace(reply, payload_json=canonical(data))
            return reply
    adapter = LargeOnce()
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, adapter)
    asyncio.run(c.run())
    assert c.status == 'consensus'
    failed = [e for e in c.events if e.get('validation_code') == 'position_byte_budget']
    assert len(failed) == 5 and all(e['validation_stage'] == 'response_contract' for e in failed)
    repairs = [r.payload()['repair'] for r in adapter.requests
               if r.stage == 'initial' and 'repair' in r.payload()]
    assert len(repairs) == 5 and all(x['maximum_utf8_bytes'] == 1600 for x in repairs)
    assert all(x['actual_utf8_bytes'] > 1600 and
               x['field_utf8_bytes']['recommendation'] == 2002 for x in repairs)
    assert all(x['prose_targets']['argument_text'] == 120 for x in repairs)
    assert all(set(e['initial_field_bytes']) <= {
        'recommendation', 'arguments', 'criteria', 'strongest_counterargument',
        'missing_data', 'conflicts'} for e in failed)


def test_initial_wire_budget_is_independent_of_adapter_whitespace(retriever, personas):
    class Pretty(ScriptedAdapter):
        async def generate(self, request):
            reply = await super().generate(request)
            if request.stage == 'initial':
                data = json.loads(reply.payload_json)
                assert len(canonical(data).encode('utf-8')) <= 1600
                pretty = json.dumps(data, ensure_ascii=False, indent=24)
                assert len(pretty.encode('utf-8')) > 1600
                return replace(reply, payload_json=pretty)
            return reply
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, Pretty())
    asyncio.run(c.run())
    assert c.status == 'consensus'
    initial = [e for e in c.events if e.get('stage') == 'initial']
    assert len(initial) == 5 and all(e['initial_wire_bytes'] <= 1600 for e in initial)


def test_initial_field_bounds_do_not_rewrite_original_positions():
    from pydantic import ValidationError
    data = {'recommendation': 'Verify the actual budget before a reversible career experiment.',
            'arguments': [{'text': 'Hiring prospects remain unknown.', 'basis': 'assumption'}],
            'criteria': [{'id': 'c1', 'text': 'Budget AND family consent must be established.'}],
            'strongest_counterargument': 'Waiting can delay learning.', 'missing_data': ['Actual expenses.']}
    assert CompactPosition.model_validate_json(canonical(data))
    for path, maximum in [(('recommendation',), 200), (('strongest_counterargument',), 240),
                          (('arguments', 0, 'text'), 200), (('arguments', 0, 'impact'), 80),
                          (('criteria', 0, 'text'), 240), (('missing_data', 0), 100)]:
        changed = json.loads(canonical(data))
        target = changed
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = 'x' * (maximum + 1)
        assert Position.model_validate_json(canonical(changed))
        with pytest.raises(ValidationError):
            CompactPosition.model_validate_json(canonical(changed))


def test_exact_but_irrelevant_evidence_cannot_override_unsupported_review(retriever, personas):
    class Unsupported(ScriptedAdapter):
        async def generate(self, request):
            reply = await super().generate(request)
            data = json.loads(reply.payload_json)
            if request.stage == 'draft':
                data['claims'][0]['text'] = 'The user has guaranteed employment tomorrow.'
            if request.stage == 'review':
                data['claim_assessments'][0].update(status='unsupported', rationale='Exact profile excerpt does not prove employment.')
                data['payload_assessment'].update(status='unsupported', rationale='Unsupported forecast.')
            return replace(reply, payload_json=canonical(data))
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, Unsupported())
    asyncio.run(c.run())
    assert c.status == 'no_consensus' and len(c.decisions) == 3
    assert not guard(c.votes[3], c.decisions[2], c.positions, c.obligations, c.conflicts)[0]
    assert all(not e['guard'] for e in c.events if 'guard' in e)
