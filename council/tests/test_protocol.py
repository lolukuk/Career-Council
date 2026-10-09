from __future__ import annotations

import asyncio
import json

import pytest

from council.model import Response
from council.runtime import Council, guard, scoped_proposal, validate_vote
from council.schemas import Config, Decision, Proposal, ROSTER, Vote, canonical, digest
from council.scripted import ScriptedAdapter


def run(retriever, personas, adapter=None, **kwargs):
    council = Council('Career?', personas, tuple(retriever.sources.values()), retriever,
                      adapter or ScriptedAdapter(), **kwargs)
    return asyncio.run(council.run())


@pytest.mark.parametrize('scenario,status,rounds', [('agree', 'consensus', 1), ('revise', 'consensus', 2), ('disagree', 'no_consensus', 3)])
def test_outcomes_and_isolation(retriever, personas, scenario, status, rounds):
    adapter = ScriptedAdapter(scenario)
    c = run(retriever, personas, adapter)
    assert c.status == status, c.events
    assert len(c.decisions) == rounds
    initials = [r for r in adapter.requests if r.stage == 'initial']
    assert len(initials) == 5 and set(c.positions) == set(ROSTER)
    for request in initials:
        p = request.payload()
        assert not {'positions', 'decision', 'previous_votes'} & p.keys()
    for version in range(1, rounds+1):
        reviews = [r for r in adapter.requests if r.stage == 'review' and r.version == version]
        assert len(reviews) == 5
        packets = [r.payload() for r in reviews]
        assert len({canonical(p['evidence']) for p in packets}) == 1
        assert all(set(p['positions']) == set(ROSTER) for p in packets)
        assert all(p['decision']['digest'] == c.decisions[version-1].digest for p in packets)
        assert all(len(p['previous_votes']) == (0 if version == 1 else 5) for p in packets)
    if scenario == 'revise':
        assert c.objection_checks['o1'][2]['status'] == 'resolved'
    if scenario == 'disagree':
        assert c.objection_checks['o1'][3]['status'] == 'upheld'


class Mutated(ScriptedAdapter):
    def __init__(self, mutate):
        super().__init__()
        self.mutate = mutate

    async def generate(self, request):
        response = await super().generate(request)
        p = json.loads(response.payload_json)
        if request.stage == 'review' and request.persona_id == 'peter_thiel':
            self.mutate(p)
        return Response(canonical(p))


@pytest.mark.parametrize('mutate,expected', [
    (lambda p: p.update(target_digest='old'), 'failed'),
    (lambda p: p.update(run_id='foreign'), 'failed'),
    (lambda p: p.update(verdict='abstain'), 'no_consensus'),
    (lambda p: p.update(verdict='conditional_approve'), 'failed'),
    (lambda p: p.update(criterion_checks=[]), 'failed'),
    (lambda p: p['claim_assessments'][0].update(status='unsupported'), 'no_consensus'),
    (lambda p: p['payload_assessment'].update(status='unsupported', unregistered_assertions=['steps: hidden fact']), 'no_consensus'),
    (lambda p: p.update(change_explanation=' '), 'failed'),
    (lambda p: p['claim_assessments'].append(p['claim_assessments'][0]), 'failed'),
    (lambda p: p['claim_assessments'][0].update(status='qualified', caveat_ref='v0/k1', condition_text='fake'), 'failed')])
def test_false_consensus_rejected(retriever, personas, mutate, expected):
    c = run(retriever, personas, Mutated(mutate))
    assert c.status == expected
    assert c.status != 'consensus'


def test_five_guard_roster_exact(retriever, personas):
    c = run(retriever, personas)
    votes = c.votes[1]
    assert not guard({k: v for k, v in votes.items() if k != 'peter_thiel'}, c.decisions[0], c.positions, (), ())[0]
    assert not guard(dict(votes, fake=votes['peter_thiel']), c.decisions[0], c.positions, (), ())[0]


class RegressedSafeguard(ScriptedAdapter):
    def __init__(self):
        super().__init__('revise')

    async def generate(self, request):
        response = await super().generate(request)
        p = json.loads(response.payload_json)
        if request.stage == 'review' and request.version == 2 and request.persona_id == 'peter_thiel':
            p['verdict'] = 'object'
            p['new_objections'] = [{'text': 'Нужна ещё проверка преимуществ.'}]
        if request.stage == 'draft' and request.version == 3:
            p['recommendation']['text'] = 'Уволиться немедленно.'
        if request.stage == 'review' and request.version == 3 and request.persona_id == 'warren_buffett':
            p['objection_checks'] = []  # V2 resolution must never carry into V3.
        return Response(canonical(p))


def test_resolved_history_pending_again(retriever, personas):
    c = run(retriever, personas, RegressedSafeguard())
    assert c.objection_checks['o1'][2]['status'] == 'resolved'
    assert len(c.decisions) == 3 and c.status == 'failed'
    assert 'o1' in [o.id for o in c.obligations]


class ConflictRevision(ScriptedAdapter):
    def __init__(self, remove=False):
        super().__init__('conflict')
        self.remove = remove

    async def generate(self, request):
        response = await super().generate(request)
        p = json.loads(response.payload_json)
        if request.stage == 'review' and request.version == 1 and request.persona_id == 'peter_thiel':
            p['verdict'] = 'object'
            p['new_objections'] = [{'text': 'Нужна дополнительная проверка.'}]
            # Drop the negative side from ranking; it still belongs to pinned closure.
        if self.remove and request.stage == 'draft' and request.version == 2:
            p['caveats'] = []
        return Response(canonical(p))


def test_whole_round_conflict_and_negative_pinning(retriever, personas):
    c = run(retriever, personas, ConflictRevision())
    assert c.status == 'consensus' and len(c.decisions) == 2
    conflict = c.conflicts[0]
    assert set(c.conflict_checks['f1']) == {1, 2}
    # Packet reconstruction after losing both rank positions still pins the pair.
    c.ranked = ['e4']
    packet, seen = c.context('review', personas.personas[2], Vote)
    assert {x.chunk_id for x in conflict.citations} <= seen
    assert packet['conflicts'][0]['id'] == 'f1'


def test_conflict_caveat_cannot_disappear(retriever, personas):
    c = run(retriever, personas, ConflictRevision(remove=True))
    assert c.status == 'failed' and len(c.decisions) == 1


def test_attempt_and_context_budgets(retriever, personas):
    c = run(retriever, personas, config=Config(max_attempts=4))
    assert c.status == 'incomplete' and c.attempts == 4
    c = run(retriever, personas, config=Config(context_bytes=1000))
    assert c.status == 'incomplete' and not c.decisions


def test_source_instructions_cannot_change_state(retriever, personas):
    # Source data may be malicious. A protocol-shaped output still cannot set terminal.
    class Injected(ScriptedAdapter):
        async def generate(self, request):
            p = json.loads((await super().generate(request)).payload_json)
            if request.stage == 'initial':
                p['consensus'] = True
                p['next_agent'] = 'fake'
            return Response(canonical(p))
    c = run(retriever, personas, Injected())
    assert c.status == 'failed' and not c.decisions


@pytest.mark.parametrize('group,scenario', [('criterion_checks', 'agree'), ('claim_assessments', 'agree'),
                                          ('objection_checks', 'revise'), ('conflict_checks', 'conflict')])
def test_each_check_group_requires_nonblank_reason(retriever, personas, group, scenario):
    class BlankChecks(ScriptedAdapter):
        async def generate(self, request):
            p = json.loads((await super().generate(request)).payload_json)
            if request.stage == 'review':
                for check in p[group]:
                    check['rationale'] = ' \t\n'
            return Response(canonical(p))
    c = run(retriever, personas, BlankChecks(scenario))
    assert c.status == 'failed'
    assert not any(e.get('guard') is True for e in c.events)


class AssumptionDraft(ScriptedAdapter):
    """Protocol fixture: explicit linking is produced by the model stub, never backend repair."""
    def __init__(self, persistent=False, unsupported=False, bad_review_once=False):
        super().__init__()
        self.persistent, self.unsupported = persistent, unsupported
        self.bad_review_once = bad_review_once

    async def generate(self, request):
        p = json.loads((await super().generate(request)).payload_json)
        context = request.payload()
        if request.stage == 'draft':
            p['claims'].append({'id': 'c2', 'text': 'A trial may produce useful information.',
                                'basis': 'assumption', 'citations': []})
            # Reproduce saved live: a caveat exists but points only to a source claim.
            p['caveats'] = [{'id': 'k1', 'text': 'The trial may yield no useful evidence.',
                            'claim_refs': ['c1'] if self.persistent or 'repair' not in context else ['c2']}]
        if request.stage == 'review':
            claim = next(c for c in context['decision']['payload']['claims'] if c['basis'] == 'assumption')
            check = next(c for c in p['claim_assessments'] if c['id'] == claim['id'])
            if self.unsupported:
                check.update(status='unsupported', rationale='The assumption remains unsupported.')
            elif not self.bad_review_once or 'repair' in context:
                caveat = context['decision']['payload']['caveats'][0]
                check.update(status='qualified', caveat_ref=caveat['id'], condition_text=caveat['text'])
        return Response(canonical(p))


@pytest.mark.parametrize('persistent', [False, True])
def test_uncaveated_assumption_repaired_before_review_barrier(retriever, personas, persistent):
    adapter = AssumptionDraft(persistent=persistent)
    c = run(retriever, personas, adapter)
    drafts = [r for r in adapter.requests if r.stage == 'draft']
    assert len(drafts) == 2
    repair = json.loads(drafts[1].payload_json)['repair']
    assert repair['validation_code'] == 'assumption_missing_caveat'
    assert repair['protocol_path'] == 'claims'
    assert drafts[0].request_id != drafts[1].request_id
    assert drafts[0].snapshot_id == drafts[1].snapshot_id
    assert 'claim_refs' in repair['instruction']
    if persistent:
        assert c.status == 'failed' and not c.decisions
        assert not any(r.stage == 'review' for r in adapter.requests)
    else:
        assert c.status == 'consensus'
        decision = c.decisions[0]
        assert 'v1/c2' in decision.payload.caveats[0].claim_refs
        assert all(v.claim_assessments[1].status == 'qualified' for v in c.votes[1].values())


def test_linked_caveat_does_not_force_assumption_acceptance(retriever, personas):
    c = run(retriever, personas, AssumptionDraft(unsupported=True))
    assert c.status == 'no_consensus' and len(c.decisions) == 3
    assert all(v.claim_assessments[1].status == 'unsupported' for v in c.votes[3].values())


def test_assumption_vote_uses_specific_safe_repair(retriever, personas):
    adapter = AssumptionDraft(bad_review_once=True)
    c = run(retriever, personas, adapter)
    assert c.status == 'consensus'
    failures = [e for e in c.events if e.get('validation_code') == 'assumption_as_fact']
    assert len(failures) == 5 and all(e['protocol_path'] == 'claim_assessments' for e in failures)
    repairs = [r.payload()['repair'] for r in adapter.requests
               if r.stage == 'review' and 'repair' in r.payload()]
    assert len(repairs) == 5 and all('applicable current caveat' in r['instruction'] for r in repairs)


def test_vote_identity_repair_does_not_echo_rejected_value(retriever, personas):
    class BadIdentityOnce(ScriptedAdapter):
        async def generate(self, request):
            p = json.loads((await super().generate(request)).payload_json)
            if request.stage == 'review' and 'repair' not in request.payload():
                p['target_digest'] = 'untrusted-private-text'
            return Response(canonical(p))
    adapter = BadIdentityOnce()
    c = run(retriever, personas, adapter)
    assert c.status == 'consensus'
    errors = [e for e in c.events if e.get('validation_code') == 'vote_identity']
    assert len(errors) == 5
    assert 'untrusted-private-text' not in canonical(c.trace())
    repairs = [r.payload()['repair'] for r in adapter.requests
               if r.stage == 'review' and 'repair' in r.payload()]
    assert all(r['protocol_path'] == 'target_digest' for r in repairs)
    assert 'untrusted-private-text' not in canonical(repairs)
