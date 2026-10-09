import asyncio
import copy
import json

import pytest

from council.feedback import pack_feedback, unpack_feedback
from council.runtime import Council
from council.schemas import (Citation, CompactProposal, CompactVote, ObjectionInput,
                             Obligation, Proposal, Vote, canonical)
from council.scripted import ScriptedAdapter
from council.model import Response
from council.citations import catalog, resolve_output


def completed_packet(retriever, personas):
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, ScriptedAdapter('revise'))
    asyncio.run(c.run())
    assert c.status == 'consensus'
    return {'previous_votes': {k: v.model_dump(mode='json') for k, v in c.votes[1].items()},
            'obligations': [o.model_dump(mode='json') for o in c.obligations], 'conflicts': []}


def test_feedback_roundtrip_preserves_all_supported_qualifications(retriever, personas):
    packet = completed_packet(retriever, personas)
    for owner, vote in packet['previous_votes'].items():
        vote['claim_assessments'][0].update(
            rationale=f'{owner}: supported only as a potential edge; the market evidence is stale.',
            caveat_ref='v1/k1', condition_text='Exact Unicode condition: Lisa’s agreement — not assumed.\r\n')
    before = canonical(packet)
    packed = pack_feedback(packet)
    assert canonical(packet) == before
    assert canonical(unpack_feedback(packed)) == before
    assert len(packed['vote_targets']) == len(packed['vote_conditions']) == 1
    assert all(len(v['claim_assessments'][0]) == 6 for v in packed['previous_votes'].values())
    assert all(owner in v['claim_assessments'][0][2] for owner, v in packed['previous_votes'].items())
    assert len(canonical(packed).encode('utf-8')) < len(before.encode('utf-8'))


@pytest.mark.parametrize('change', ['duplicate', 'owner', 'version', 'blocking', 'citation'])
def test_ledger_reference_requires_unique_full_equality(retriever, personas, change):
    packet = completed_packet(retriever, personas)
    packed = pack_feedback(packet)
    owner = 'warren_buffett'
    assert packed['previous_votes'][owner]['new_objections'] == [{'objection_ref': 'o1'}]
    changed = copy.deepcopy(packet)
    if change == 'duplicate':
        changed['obligations'].append(dict(changed['obligations'][0], id='other'))
    elif change == 'citation':
        changed['obligations'][0]['citations'] = [{'chunk_id': 'e3', 'quote': 'Budget planning.'}]
    else:
        key, value = {'owner': ('owner', 'peter_thiel'), 'version': ('origin_version', 2),
                      'blocking': ('blocking', False)}[change]
        changed['obligations'][0][key] = value
    result = pack_feedback(changed)
    assert result['previous_votes'][owner]['new_objections'] == changed['previous_votes'][owner]['new_objections']
    assert canonical(unpack_feedback(result)) == canonical(changed)


def test_feedback_versions_rows_and_collisions_fail_closed(retriever, personas, monkeypatch):
    packet = completed_packet(retriever, personas)
    packed = pack_feedback(packet)
    bad = copy.deepcopy(packed)
    bad['feedback_layout']['version'] = 2
    with pytest.raises(ValueError, match='layout version'):
        unpack_feedback(bad)
    bad = copy.deepcopy(packed)
    bad['previous_votes']['peter_thiel']['criterion_checks'][0].pop()
    with pytest.raises(ValueError, match='row width'):
        unpack_feedback(bad)
    import council.feedback as module
    monkeypatch.setattr(module, 'digest', lambda _: 'x' * 64)
    packet['previous_votes']['peter_thiel']['target_digest'] = 'another'
    with pytest.raises(ValueError, match='reference collision'):
        pack_feedback(packet)


def test_original_negative_source_pinned_before_feedback_packing(retriever, personas):
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, ScriptedAdapter('revise'))
    asyncio.run(c.run())
    owner = 'warren_buffett'
    item = ObjectionInput(text='Budget source needs attention.', citations=(Citation(chunk_id='e3', quote='Budget planning.'),))
    c.votes[1][owner] = c.votes[1][owner].model_copy(update={'new_objections': (item,)})
    c.obligations.append(Obligation(id='o2', owner=owner, origin_version=1,
                                  text=item.text, blocking=item.blocking, citations=item.citations))
    c.ranked = ['e0', 'e1']
    packet, seen = c.context('review', personas.personas[0], Vote)
    assert 'e3' in seen
    assert packet['previous_votes'][owner]['new_objections'] == [{'objection_ref': 'o2'}]
    assert 'Budget source needs attention.' in canonical(packet['obligations'])


@pytest.mark.parametrize('stage,field,size', [('draft', 'recommendation', 401), ('review', 'rationale', 241)])
def test_generation_bounds_use_repair_without_rewriting_original_dto(retriever, personas, stage, field, size):
    class LargeOnce(ScriptedAdapter):
        async def generate(self, request):
            p = json.loads((await super().generate(request)).payload_json)
            if request.stage == stage and 'repair' not in request.payload():
                if field == 'recommendation':
                    p[field]['text'] = 'x' * size
                    context = request.payload()
                    seen = {row['chunk_id'] for row in context['evidence']}
                    resolved = resolve_output(p, catalog(context, retriever.evidence, seen))
                    assert Proposal.model_validate_json(canonical(resolved))
                else:
                    p[field] = 'x' * size
                    assert Vote.model_validate_json(canonical(p))
            return Response(canonical(p))
    adapter = LargeOnce()
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, adapter)
    asyncio.run(c.run())
    assert c.status == 'consensus'
    failed = [e for e in c.events if e.get('stage') == stage and e.get('validation_code') == 'schema_invalid']
    assert len(failed) == (1 if stage == 'draft' else 5)
    assert all('string_too_long' in e['schema_error_types'] for e in failed)
    assert type(c.decisions[0].payload) is Proposal
    assert all(type(v) is Vote for v in c.votes[1].values())
