from __future__ import annotations

import asyncio
import json
import threading
import time
import uuid
from dataclasses import replace
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from pydantic import ValidationError

from .citations import (CITATION_STAGES, PROTOCOL, SelectionError, catalog, project_packet,
                        resolve_output, response_schema)
from .context import build_context, validate_citations
from .model import Request, TransientModelError, check_adapter, discard_task, invoke, output_token_ceiling
from .prompts import PERSONA_VOICES, STAGE_HINTS, bounded_policy
from .packing import VERSION as CONTEXT_TABLE_VERSION, context_payload
from .schemas import (Cancelled, Claim, CompactPosition, CompactProposal, CompactVote, Config, Conflict, Criterion, Decision, Incomplete,
                      NoteSelection, Obligation, Position, Proposal, ROSTER, ToolAction, Vote, canonical, digest, exact_ids)
from .task_tools import SnapshotTools

ASPECTS = ('undervalued opportunity differentiated portfolio', 'circle of competence margin of safety budget',
           'worker employer risk benefits healthcare stability', 'fragility optionality capped downside',
           'control duty family obligations ambition fear')

# Only backend literals enter repair/audit; never retain rejected model prose.
PROTOCOL_REPAIRS = {
    'assumption lacks applicable caveat': ('assumption_missing_caveat', 'claims',
        'Each assumption claim needs a specific caveat explicitly listing its local ID in claim_refs. '
        'State its actual uncertainty; never relabel it as source or fabricate support to pass.'),
    'vote identity mismatch': ('vote_identity', 'target_digest',
        'Copy run_id, snapshot_id, target_version and target_digest exactly from decision.'),
    'duplicate/missing/foreign check IDs': ('check_ids', 'checks',
        'Include exactly one check for each required current ID: own criteria, own objections/conflicts '
        'and every decision claim. No other IDs or duplicates.'),
    'empty reasoning': ('vote_reasoning', 'rationale',
        'Supply nonblank rationale, change_explanation and payload_assessment rationale.'),
    'missing/foreign/stale caveat or condition text': ('caveat_condition', 'condition_text',
        'Use a current decision caveat and copy its exact text into condition_text. '
        'Do not rewrite the condition or invent a caveat.'),
    'invalid criterion check': ('criterion_status', 'criterion_checks',
        'Criterion status must be satisfied or unmet; unknown conditions remain unmet.'),
    'invalid claim assessment': ('claim_status', 'claim_assessments',
        'Claim status must be supported, qualified or unsupported, based on actual support.'),
    'caveat does not apply to claim': ('caveat_claim', 'claim_assessments',
        'A qualified assessment must select a current caveat whose claim_refs contains that claim ID '
        'and copy its exact text. Otherwise assess unsupported; do not invent linkage.'),
    'assumption cannot be treated as established fact': ('assumption_as_fact', 'claim_assessments',
        'An assumption cannot be supported as fact. Use qualified with an applicable current caveat '
        'and exact condition_text, or unsupported. Preserve your independent verdict.'),
    'invalid objection check': ('objection_status', 'objection_checks',
        'Objection status must be resolved or upheld; assess only objections you own.'),
    'resolution needs current response basis': ('objection_basis', 'objection_checks',
        'Resolved requires a claim_ref from the current response to that objection; otherwise uphold.'),
    'invalid conflict disposition': ('conflict_status', 'conflict_checks',
        'Conflict status must be uncertainty_in_decision or unresolved; assess only conflicts you own.'),
    'conflict disposition needs current response and applicable caveat': ('conflict_basis', 'conflict_checks',
        'Use the current conflict response claim_ref and caveat_ref, an applicable linked caveat '
        'and exact condition_text; otherwise mark unresolved.'),
}


def generation_schema(stage, schema):
    return {('initial', Position): CompactPosition, ('draft', Proposal): CompactProposal,
            ('review', Vote): CompactVote}.get((stage, schema), schema)


def scoped_proposal(proposal, version, obligations, conflicts):
    data = proposal.model_dump(mode='json')
    claims = [c.id for c in proposal.claims]
    caveats = [c.id for c in proposal.caveats]
    if len(claims) != len(set(claims)) or len(caveats) != len(set(caveats)):
        raise ValueError('duplicate claim/caveat ID')
    if any('/' in id_ for id_ in claims + caveats):
        raise ValueError('proposal uses local IDs only')
    exact_ids(proposal.objection_responses, [o.id for o in obligations])
    exact_ids(proposal.conflict_responses, [c.id for c in conflicts])

    def visit(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key == 'claim_refs':
                    if not set(child) <= set(claims) or len(child) != len(set(child)):
                        raise ValueError('foreign/duplicate section claim refs')
                    value[key] = [f'v{version}/{id_}' for id_ in child]
                elif key == 'caveat_refs':
                    if not set(child) <= set(caveats) or len(child) != len(set(child)):
                        raise ValueError('foreign/duplicate caveat refs')
                    value[key] = [f'v{version}/{id_}' for id_ in child]
                elif key == 'caveat_ref' and child is not None:
                    if child not in caveats:
                        raise ValueError('foreign caveat ref')
                    value[key] = f'v{version}/{child}'
                else:
                    visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
    visit(data)
    for claim in data['claims']:
        claim['id'] = f"v{version}/{claim['id']}"
    for caveat in data['caveats']:
        caveat['id'] = f"v{version}/{caveat['id']}"
    if version > 1 and not proposal.change_summary.strip():
        raise ValueError('revision requires change summary')
    covered = {ref for caveat in data['caveats'] for ref in caveat['claim_refs']}
    if any(claim['basis'] == 'assumption' and claim['id'] not in covered for claim in data['claims']):
        raise ValueError('assumption lacks applicable caveat')
    return Proposal.model_validate_json(canonical(data))


def validate_vote(vote, owner, decision, positions, obligations, conflicts):
    if (vote.run_id, vote.snapshot_id, vote.target_version, vote.target_digest) != (
            decision.run_id, decision.snapshot_id, decision.version, decision.digest):
        raise ValueError('vote identity mismatch')
    criteria = {c.id: c for c in positions[owner].criteria}
    own_objections = {o.id: o for o in obligations if o.owner == owner}
    own_conflicts = {c.id: c for c in conflicts if c.owner == owner}
    claims = {c.id: c for c in decision.payload.claims}
    caveats = {c.id: c for c in decision.payload.caveats}
    exact_ids(vote.criterion_checks, criteria)
    exact_ids(vote.objection_checks, own_objections)
    exact_ids(vote.conflict_checks, own_conflicts)
    exact_ids(vote.claim_assessments, claims)
    if any(not x.strip() for x in (vote.rationale, vote.change_explanation, vote.payload_assessment.rationale)):
        raise ValueError('empty reasoning')

    def caveat(check):
        c = caveats.get(check.caveat_ref)
        if c is None or check.condition_text != c.text:
            raise ValueError('missing/foreign/stale caveat or condition text')
        return c

    for check in vote.criterion_checks:
        if check.status not in ('satisfied', 'unmet'):
            raise ValueError('invalid criterion check')
    for check in vote.claim_assessments:
        if check.status not in ('supported', 'qualified', 'unsupported'):
            raise ValueError('invalid claim assessment')
        if check.status == 'qualified':
            if check.id not in caveat(check).claim_refs:
                raise ValueError('caveat does not apply to claim')
        if claims[check.id].basis == 'assumption' and check.status == 'supported':
            raise ValueError('assumption cannot be treated as established fact')
    responses = {r.id: r for r in decision.payload.objection_responses}
    for check in vote.objection_checks:
        if check.status not in ('resolved', 'upheld'):
            raise ValueError('invalid objection check')
        if check.status == 'resolved' and check.claim_ref not in responses[check.id].claim_refs:
            raise ValueError('resolution needs current response basis')
    responses = {r.id: r for r in decision.payload.conflict_responses}
    for check in vote.conflict_checks:
        if check.status not in ('uncertainty_in_decision', 'unresolved'):
            raise ValueError('invalid conflict disposition')
        if check.status == 'uncertainty_in_decision':
            response = responses[check.id]
            if check.caveat_ref != response.caveat_ref or check.claim_ref not in response.claim_refs or check.claim_ref not in caveat(check).claim_refs:
                raise ValueError('conflict disposition needs current response and applicable caveat')


def guard(votes, decision, positions, obligations, conflicts):
    if set(votes) != set(ROSTER) or set(positions) != set(ROSTER):
        return False, ['missing/foreign participant']
    reasons = []
    for owner, vote in votes.items():
        validate_vote(vote, owner, decision, positions, obligations, conflicts)
        if vote.verdict != 'approve':
            reasons.append(owner + ':' + vote.verdict)
        if vote.new_objections or vote.new_conflicts:
            reasons.append(owner + ':new obligation')
        if vote.payload_assessment.status != 'supported' or vote.payload_assessment.unregistered_assertions:
            reasons.append(owner + ':unsupported payload')
        if any(c.status == 'unsupported' for c in vote.claim_assessments):
            reasons.append(owner + ':unsupported claim')
        blocking = {c.id for c in positions[owner].criteria if c.blocking}
        if any(c.id in blocking and c.status != 'satisfied' for c in vote.criterion_checks):
            reasons.append(owner + ':unmet criterion')
        if any(c.status != 'resolved' and next(o for o in obligations if o.id == c.id).blocking for c in vote.objection_checks):
            reasons.append(owner + ':upheld objection')
        if any(c.status != 'uncertainty_in_decision' for c in vote.conflict_checks):
            reasons.append(owner + ':unresolved conflict')
    return not reasons, reasons


class GraphState(TypedDict):
    next: str


class Council:
    def __init__(self, question, personas, sources, retriever, adapter, config=None, cancel=None):
        check_adapter(adapter)  # Before building model payloads/disclosure.
        self.config = config or Config()
        self.policy = bounded_policy(self.config.output_tokens)
        self.generation_schema_digest = digest(response_schema(CompactPosition))
        self.generation_schema_digests = {stage: digest(response_schema(schema)) for stage, schema in
            (('initial', CompactPosition), ('draft', CompactProposal), ('review', CompactVote))}
        self.initial_position_bytes = 1600
        self.stage_hints, self.persona_voices = dict(STAGE_HINTS), dict(PERSONA_VOICES)
        self.question, self.personas, self.sources, self.retriever, self.adapter = question, personas, sources, retriever, adapter
        self.cancel = cancel or threading.Event()
        self.run_id = uuid.uuid4().hex
        self.snapshot_id = digest({'sources': [(s.source_id, s.content_digest) for s in sources],
                                   'personas': personas, 'config': self.config, 'question': question,
                                   'policy_digest': digest(self.policy),
                                   'stage_hints': self.stage_hints, 'persona_voices': self.persona_voices,
                                   'citation_protocol': PROTOCOL,
                                   'context_table_version': CONTEXT_TABLE_VERSION,
                                   'generation_schema_digest': self.generation_schema_digest,
                                   'generation_schema_digests': self.generation_schema_digests,
                                   'initial_position_bytes': self.initial_position_bytes,
                                   'model': {'provider': adapter.capabilities.provider,
                                             'identity': adapter.capabilities.identity,
                                             'accounting_policy': adapter.capabilities.accounting_policy,
                                             'output_limit_policy': adapter.capabilities.output_limit_policy,
                                             'accepted_output_token_ceiling': output_token_ceiling(adapter.capabilities, self.config.output_tokens),
                                             'context_budget': adapter.capabilities.context_window,
                                             'reasoning_effort': getattr(getattr(adapter, 'settings', None), 'reasoning_effort', None),
                                             'catalog': getattr(adapter, 'catalog_metadata', None)}})
        self.positions, self.decisions, self.votes = {}, [], {}
        self.obligations, self.conflicts = [], []
        self.objection_checks, self.conflict_checks = {}, {}
        self.events, self.usage, self.ranked = [], [], []
        self.status, self.reason, self.started = 'created', '', time.monotonic()
        self.attempts = 0
        self.active_attempts = set()
        self.tools = SnapshotTools(sources, retriever.evidence)
        self.tool_results = {id_: [] for id_ in ROSTER}
        self.relevant_notes = frozenset()
        self.note_selection = {'shortlist': [], 'selected': [], 'status': 'pending'}

    def active(self):
        if self.cancel.is_set():
            raise Cancelled('user cancellation')
        if time.monotonic() - self.started > self.config.deadline:
            raise Incomplete('discussion deadline')
        if self.status in ('consensus', 'no_consensus', 'failed', 'incomplete', 'cancelled'):
            raise Cancelled('late result for terminal run')

    def stage_policy(self, stage, persona):
        voice = self.persona_voices.get(getattr(persona, 'id', ''), '') if stage in ('initial', 'review') else ''
        return self.policy + '\n' + self.stage_hints.get(stage, '') + ('\n' + voice if voice else '')

    def context(self, stage, persona, schema):
        schema = generation_schema(stage, schema)
        version = len(self.decisions) + (1 if stage == 'draft' else 0)
        empty = Request(stage, getattr(persona, 'id', 'coordinator'), self.run_id, self.snapshot_id,
                        version, '0'*32, '0'*32, self.stage_policy(stage, persona),
                        '', canonical(response_schema(schema)), self.config.output_tokens)
        return build_context(stage, question=self.question, snapshot_id=self.snapshot_id, persona=persona,
            positions=self.positions, decision=self.decisions[-1] if self.decisions else None,
            obligations=self.obligations, conflicts=self.conflicts,
            previous_votes=self.votes.get(version - 1, {}), retriever=self.retriever,
            ranked=self.ranked, cap=self.config.context_bytes,
            optional_cap=self.config.context_bytes - 1024,
            measure=lambda payload: len(replace(empty, payload_json=context_payload(json.loads(payload)),
                response_schema_json=canonical(response_schema(schema,
                    [e['evidence_id'] for row in json.loads(payload)['evidence'] for e in row['excerpts']])
                    if stage in CITATION_STAGES else response_schema(schema))).serialized().encode('utf-8')),
            relevant_notes=self.relevant_notes,
            tool_results=self.tool_results.get(getattr(persona, 'id', ''), ()) if stage in ('initial', 'tools') else (),
            project=(lambda p: project_packet(p, self.retriever.evidence,
                     persona.id if stage == 'review' else None)) if stage in CITATION_STAGES else None)

    async def call(self, stage, persona, schema, packet, seen, validate):
        schema = generation_schema(stage, schema)
        allowed = catalog(packet, self.retriever.evidence, seen) if stage in CITATION_STAGES else None
        base = Request(stage, getattr(persona, 'id', 'coordinator'), self.run_id, self.snapshot_id,
                       len(self.decisions) + (stage == 'draft'), uuid.uuid4().hex, '',
                       self.stage_policy(stage, persona),
                       context_payload(packet), canonical(response_schema(schema, list(allowed) if allowed is not None else None)),
                       self.config.output_tokens)
        feedback = None
        for attempt in range(2):
            self.active()
            if self.attempts >= self.config.max_attempts:
                raise Incomplete('model attempt budget')
            if feedback is not None:
                repair_packet = dict(packet, repair=feedback)
                request = replace(base, request_id=uuid.uuid4().hex,
                                  payload_json=context_payload(repair_packet), attempt_id=uuid.uuid4().hex)
            else:
                request = replace(base, attempt_id=uuid.uuid4().hex)
            if len(request.serialized().encode('utf-8')) > self.config.context_bytes:
                raise Incomplete('complete serialized request byte budget')
            self.attempts += 1  # Reserve a dispatchable attempt before awaiting.
            event = {'stage': stage, 'persona': request.persona_id, 'version': request.version,
                     'request_id': request.request_id, 'attempt_id': request.attempt_id,
                     'context_digest': digest(json.loads(request.payload_json)),
                     'base_request_id': base.request_id, 'base_context_digest': digest(packet),
                     'response_schema_digest': digest(json.loads(request.response_schema_json)),
                     'evidence_ids': sorted(seen), 'attempt': attempt + 1,
                     'serialized_bytes': len(request.serialized().encode('utf-8'))}
            event['validation_stage'] = 'provider'
            self.events.append(event)
            usage = None

            def record_usage(response=None, error=None):
                nonlocal usage
                if usage is not None:
                    return
                metadata = (response.metadata if response is not None else getattr(error, 'safe_metadata', None)) or {}
                usage = {'attempt_id': request.attempt_id, 'accepted': False,
                         'input_tokens': response.input_tokens if response else metadata.get('input_tokens'),
                         'output_tokens': response.output_tokens if response else metadata.get('output_tokens'),
                         'http_dispatches': metadata.get('http_dispatches'),
                         'preflight_count': metadata.get('preflight_count'),
                         'returned_model': metadata.get('returned_model'),
                         'cost_rub': metadata.get('cost_rub'),
                         'requested_output_tokens': request.output_tokens}
                received = usage['output_tokens']
                usage['output_limit_exceeded'] = received > request.output_tokens if type(received) is int else None
                self.usage.append(usage)

            expires = min(time.monotonic() + self.config.model_timeout, self.started + self.config.deadline)
            self.active_attempts.add(request.attempt_id)
            try:
                # Poll cancellation independently from a cooperatively cancellable async adapter.
                task = asyncio.create_task(invoke(self.adapter, request, self.config.model_timeout))
                try:
                    while not task.done():
                        self.active()
                        if time.monotonic() >= expires:
                            raise asyncio.TimeoutError('attempt expired')
                        await asyncio.wait({task}, timeout=.05)
                    if time.monotonic() >= expires or request.attempt_id not in self.active_attempts:
                        raise asyncio.TimeoutError('late attempt result')
                    response = task.result()
                finally:
                    # Expire before cancellation; suppressed cancellation cannot revive it.
                    self.active_attempts.discard(request.attempt_id)
                    if not task.done():
                        task.cancel()
                        task.add_done_callback(discard_task)
                    else:
                        discard_task(task)  # Consume an already-expired error, never its payload.
                self.active()
                record_usage(response)
                event['validation_stage'] = 'response_contract'
                if not isinstance(response.payload_json, str) or len(response.payload_json.encode('utf-8')) > 65536:
                    raise ValueError('model output byte budget')
                if self.adapter.mode == 'model' and (type(response.input_tokens) is not int or type(response.output_tokens) is not int or response.input_tokens < 0 or response.output_tokens < 0 or response.output_tokens > output_token_ceiling(self.adapter.capabilities, request.output_tokens)):
                    raise ValueError('missing/excessive provider usage')
                event['validation_stage'] = 'schema'
                if allowed is not None:
                    try:
                        raw = json.loads(response.payload_json)
                    except json.JSONDecodeError:
                        schema.model_validate_json(response.payload_json)  # Original safe JSON diagnostics.
                    if stage == 'initial':
                        # Measure the wire content, independent of adapter formatting.
                        # The production adapter already canonicalizes its response.
                        event['initial_wire_bytes'] = len(canonical(raw).encode('utf-8'))
                        if isinstance(raw, dict):
                            event['initial_field_bytes'] = {
                                key: len(canonical(raw[key]).encode('utf-8'))
                                for key in ('recommendation', 'arguments', 'criteria',
                                            'strongest_counterargument', 'missing_data', 'conflicts')
                                if key in raw}
                        if event['initial_wire_bytes'] > self.initial_position_bytes:
                            event['validation_stage'] = 'response_contract'
                            raise ValueError('initial position byte budget')
                    event['validation_stage'] = 'citations'
                    selected_ids = []
                    resolved = resolve_output(raw, allowed, selected_ids)
                    event['validation_stage'] = 'schema'
                    dto = schema.model_validate_json(canonical(resolved))
                else:
                    dto = schema.model_validate_json(response.payload_json)
                event['validation_stage'] = 'citations'
                validate_citations(dto, self.retriever.evidence, seen)
                event['validation_stage'] = 'protocol'
                validate(dto)
                if isinstance(dto, CompactVote):
                    dto = Vote.model_validate_json(canonical(dto))
                if allowed is not None:
                    event['selected_evidence_ids'] = list(dict.fromkeys(selected_ids))
                usage['accepted'] = True
                event['accepted'] = True
                return dto
            except asyncio.CancelledError as exc:
                # A sibling failure cancels this task before an envelope arrives.
                # Preserve the reserved attempt with unknown usage, never zero.
                record_usage(error=exc)
                event['accepted'] = False
                event['error'] = 'CancelledError'
                raise
            except (ValueError, TransientModelError, asyncio.TimeoutError) as exc:
                record_usage(error=exc)
                event['accepted'] = False
                event['error'] = type(exc).__name__  # No provider secrets/error body.
                # Fixed local categories only: never retain exception text, raw
                # model output, Pydantic inputs, or provider error-body details.
                categories = {'unseen/unknown citation': 'citation_not_shown',
                              'initial position byte budget': 'position_byte_budget',
                              'invalid evidence digest/quote': 'citation_digest_or_quote',
                              'invalid evidence digest': 'evidence_digest',
                              'nonexact citation quote': 'citation_quote_not_exact',
                              'duplicate/missing/foreign check IDs': 'check_ids',
                              'provider_invalid_usage_total': 'usage_total',
                              'provider_missing_usage': 'usage_missing',
                              'provider_invalid_text': 'response_text',
                              'provider_invalid_json': 'response_json',
                              'provider_invalid_envelope': 'response_envelope'}
                categories.update({'unknown task ID': 'tool_unknown_task',
                                   'unknown/duplicate note selection': 'note_selection_ids',
                                   'tool argument mismatch': 'tool_arguments'})
                categories.update({message: repair[0] for message, repair in PROTOCOL_REPAIRS.items()})
                if isinstance(exc, SelectionError):
                    event['validation_code'] = exc.code
                    event['citation_path'] = exc.path
                elif isinstance(exc, ValidationError):
                    event['validation_code'] = 'schema_invalid'
                    event['schema_error_types'] = sorted({e['type'] for e in exc.errors(
                        include_input=False, include_context=False, include_url=False)})[:10]
                    def fields(node):
                        if isinstance(node, dict):
                            return set(node.get('properties', {})) | set().union(*(fields(v) for v in node.values()))
                        if isinstance(node, list):
                            return set().union(*(fields(v) for v in node))
                        return set()
                    trusted_fields = fields(response_schema(schema))
                    event['schema_error_paths'] = [list(e['loc']) for e in exc.errors(
                        include_input=False, include_context=False, include_url=False)
                        if all((isinstance(x, str) and x in trusted_fields) or
                               (type(x) is int and 0 <= x <= 150) for x in e['loc'])][:5]
                elif type(exc) is ValueError:
                    event['validation_code'] = categories.get(str(exc), 'validation_rejected')
                elif isinstance(exc, json.JSONDecodeError):
                    event['validation_code'] = 'response_json'
                else:
                    event['validation_code'] = ('timeout' if isinstance(exc, asyncio.TimeoutError) else
                                                'transient' if isinstance(exc, TransientModelError) else
                                                'validation_rejected')
                if getattr(exc, 'safe_code', None):
                    event['provider_error'] = exc.safe_code
                if isinstance(exc, ValueError):
                    feedback = {'base_request_id': base.request_id,
                                'validation_stage': event['validation_stage'],
                                'validation_code': event['validation_code']}
                    if type(exc) is ValueError and str(exc) in PROTOCOL_REPAIRS:
                        _, path, instruction = PROTOCOL_REPAIRS[str(exc)]
                        event['protocol_path'] = path
                        feedback.update(protocol_path=path, instruction=instruction)
                        if str(exc) == 'assumption lacks applicable caveat':
                            # Address validated DTO locations, never rejected prose or IDs.
                            indices = [i for i, claim in enumerate(dto.claims)
                                       if claim.basis == 'assumption' and
                                       not any(claim.id in caveat.claim_refs for caveat in dto.caveats)]
                            event['assumption_claim_indices'] = indices
                            feedback['assumption_claim_indices'] = indices
                            feedback['instruction'] = ('At each zero-based claims index listed here, keep the '
                                'assumption and author its concrete uncertainty in caveats; claim_refs must '
                                'contain that exact local claim.id. Inspect EVERY assumption, including claims '
                                'supporting steps or responses. Generic caveats linked only to other claims '
                                'do not apply. Do not fabricate facts or relabel the basis to evade this check.')
                    if 'schema_error_types' in event:
                        feedback['schema_error_types'] = event['schema_error_types']
                        feedback['schema_error_paths'] = event['schema_error_paths']
                        if 'string_too_long' in event['schema_error_types']:
                            feedback['instruction'] = ('For every reported field obey its schema maxLength in CHARACTERS, '
                                'not tokens. Rewrite concise complete reasoning; retain material qualifications '
                                'and never shorten exact condition_text or change the independent verdict.')
                    if event['validation_code'] == 'position_byte_budget':
                        feedback.update(maximum_utf8_bytes=self.initial_position_bytes,
                            actual_utf8_bytes=event['initial_wire_bytes'],
                            field_utf8_bytes=event.get('initial_field_bytes', {}),
                            prose_targets={'recommendation': 120, 'argument_text': 120,
                                           'argument_impact': 40, 'criterion_text': 160,
                                           'strongest_counterargument': 140, 'missing_item': 70},
                            instruction='Return the complete concise initial JSON within this byte limit. '
                                        'Shorten the largest prose fields using the character targets; '
                                        'they are guidance, not permission to omit material information. '
                                        'Keep supporting IDs, strongest counterargument, unknowns and all required conditions; '
                                        'use short sentences, never truncate or invent facts.')
                    if isinstance(exc, SelectionError):
                        feedback.update(citation_path=exc.path,
                            instruction='At this citation return only evidence_id selected from shown excerpts. '
                                        'Choose direct support for the assertion; otherwise disclose an assumption. '
                                        'The list below is a subset, not a relevance ranking; all shown IDs remain valid.',
                            allowed_evidence_ids=list(allowed)[:8])
                if attempt == 1:
                    raise RuntimeError('model response invalid/exhausted: ' + type(exc).__name__) from None
            except Exception as exc:
                record_usage(error=exc)
                event['accepted'] = False
                event['error'] = type(exc).__name__
                if getattr(exc, 'safe_code', None):
                    event['provider_error'] = exc.safe_code
                raise

    async def search(self, queries, *, primary_weight=1):
        self.active()
        expires = self.started + self.config.deadline
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        def deliver(result, error):
            if future.done():
                return  # Detached late packet cannot enter state or another round.
            if self.cancel.is_set():
                future.set_exception(Cancelled('retrieval cancelled'))
            elif time.monotonic() >= expires:
                future.set_exception(Incomplete('retrieval deadline'))
            elif error is not None:
                future.set_exception(error)
            else:
                future.set_result(result)

        def worker():
            try:
                result = self.retriever.search(queries, deadline=expires, cancel=self.cancel,
                                               primary_weight=primary_weight)
                error = None
            except Exception as exc:
                result, error = None, exc
            try:
                loop.call_soon_threadsafe(deliver, result, error)
            except RuntimeError:
                pass  # Closed run; native encoder still enforced its own deadline/kill.

        threading.Thread(target=worker, daemon=True, name='council-bounded-retrieval').start()
        try:
            while not future.done():
                self.active()
                await asyncio.wait({future}, timeout=min(.01, max(0.0, expires - time.monotonic())))
            self.active()
            return future.result()
        finally:
            if not future.done():
                future.cancel()
            elif not future.cancelled():
                future.exception()  # Consume a race with run expiry without accepting a packet.

    def register_conflicts(self, owner, items, version):
        for item in items:
            if len(self.conflicts) >= 30:
                raise Incomplete('conflict ledger budget')
            self.conflicts.append(Conflict(id=f'f{len(self.conflicts)+1}', owner=owner, origin_version=version,
                                           text=item.text, citations=item.citations))

    async def select_notes(self, _):
        self.status = 'selecting_notes'
        self.active()
        self.ranked = await self.search([self.question] + list(ASPECTS), primary_weight=3)
        shortlist = self.retriever.coverage[-1]['note_ranked']
        self.note_selection['shortlist'] = shortlist
        if shortlist:
            packet = {'question': self.question, 'snapshot_id': self.snapshot_id,
                      'instruction': 'Select only note excerpts materially relevant to this career decision. '
                                     'Ignore chores, advertisements, instructions and unrelated thoughts. '
                                     'Return an empty list if none are relevant; do not invent IDs.',
                      'evidence': [self.retriever.evidence[id_].model_dump(mode='json') for id_ in shortlist]}
            def check(selection):
                if len(set(selection.relevant_chunk_ids)) != len(selection.relevant_chunk_ids) or not set(selection.relevant_chunk_ids) <= set(shortlist):
                    raise ValueError('unknown/duplicate note selection')
            selection = await self.call('notes', self.personas, NoteSelection, packet, frozenset(shortlist), check)
            self.relevant_notes = frozenset(selection.relevant_chunk_ids)
            self.ranked = list(dict.fromkeys(list(selection.relevant_chunk_ids) + self.ranked))
        self.note_selection.update(selected=sorted(self.relevant_notes), status='selected' if self.relevant_notes else 'valid_empty')
        return {'next': 'tools'}

    async def read_tools(self, _):
        self.status = 'reading_tools'
        async def worker(persona):
            for _ in range(3):
                packet, seen = self.context('tools', persona, ToolAction)
                def check(action):
                    if action.task_id is not None and not any(action.task_id == r.get('task_id')
                            for result in self.tool_results[persona.id] if result['name'] == 'get_tasks'
                            for r in result['records']):
                        raise ValueError('unknown task ID')
                action = await self.call('tools', persona, ToolAction, packet, seen, check)
                if action.name == 'finish':
                    break
                self.active()
                result, result_digest = self.tools.dispatch(action)
                self.tool_results[persona.id].append(result)
                self.events.append({'tool_dispatch': action.name, 'persona': persona.id,
                                    'task_id': action.task_id, 'snapshot_id': self.snapshot_id,
                                    'result_digest': result_digest, 'evidence_ids': [e['chunk_id'] for e in result['evidence']]})
        await self.barrier([worker(p) for p in self.personas.personas])
        return {'next': 'analyze'}

    async def analyze(self, _):
        self.status = 'analyzing'
        self.active()
        async def worker(persona):
            packet, seen = self.context('initial', persona, Position)
            def check(position):
                exact_ids(position.criteria, [c.id for c in position.criteria])
            position = await self.call('initial', persona, Position, packet, seen, check)
            data = position.model_dump(mode='json')
            for i, criterion in enumerate(data['criteria'], 1):
                criterion['id'] = persona.id + f'/c{i}'
            return persona.id, Position.model_validate_json(canonical(data))
        results = await self.barrier([worker(p) for p in self.personas.personas])
        if len(results) != 5 or len({id_ for id_, _ in results}) != 5:
            raise ValueError('position barrier roster')
        self.positions = dict(results)
        for owner, p in results:
            self.register_conflicts(owner, p.conflicts, 0)
        return {'next': 'draft'}

    async def barrier(self, coroutines):
        tasks = [asyncio.create_task(c) for c in coroutines]
        try:
            return await asyncio.gather(*tasks)
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

    async def draft(self, _):
        self.active()
        self.status = 'drafting'
        packet, seen = self.context('draft', self.personas, Proposal)
        version = len(self.decisions) + 1
        proposal = await self.call('draft', self.personas, Proposal, packet, seen,
                                  lambda p: scoped_proposal(p, version, self.obligations, self.conflicts))
        proposal = scoped_proposal(proposal, version, self.obligations, self.conflicts)
        identity = {'run_id': self.run_id, 'snapshot_id': self.snapshot_id, 'version': version, 'payload': proposal}
        self.decisions.append(Decision(**identity, digest=digest(identity)))
        return {'next': 'review'}

    async def review(self, _):
        self.active()
        self.status = 'reviewing'
        decision = self.decisions[-1]
        packets = [self.context('review', p, Vote) for p in self.personas.personas]
        # Identical evidence packet for all reviewers, with own framework only.
        common = set.intersection(*(set(seen) for _, seen in packets))
        async def worker(persona, packet):
            packet['evidence'] = [e for e in packet['evidence'] if e['chunk_id'] in common]
            vote = await self.call('review', persona, Vote, packet, frozenset(common),
                                   lambda v: validate_vote(v, persona.id, decision, self.positions, self.obligations, self.conflicts))
            return persona.id, vote
        results = await self.barrier([worker(p, packet) for p, (packet, _) in zip(self.personas.personas, packets)])
        self.votes[decision.version] = dict(results)
        return {'next': 'check'}

    async def check(self, _):
        self.active()
        self.status = 'checking'
        decision = self.decisions[-1]
        votes = self.votes[decision.version]
        agreed, reasons = guard(votes, decision, self.positions, self.obligations, self.conflicts)
        self.events.append({'guard': agreed, 'version': decision.version, 'reasons': reasons})
        for owner, vote in votes.items():
            for check in vote.objection_checks:
                self.objection_checks.setdefault(check.id, {})[decision.version] = check.model_dump(mode='json')
            for check in vote.conflict_checks:
                self.conflict_checks.setdefault(check.id, {})[decision.version] = check.model_dump(mode='json')
            for item in vote.new_objections:
                if len(self.obligations) >= 150:
                    raise Incomplete('objection ledger budget')
                self.obligations.append(Obligation(id=f'o{len(self.obligations)+1}', owner=owner,
                    origin_version=decision.version, text=item.text, blocking=item.blocking, citations=item.citations))
            self.register_conflicts(owner, vote.new_conflicts, decision.version)
        self.active()  # Cancellation/deadline wins over terminal unanimity.
        if agreed:
            self.status, self.reason = 'consensus', 'Все пять явно согласовали одну версию.'
            return {'next': 'end'}
        if len(self.decisions) >= self.config.max_rounds:
            self.status, self.reason = 'no_consensus', '; '.join(reasons)
            return {'next': 'end'}
        queries = list(dict.fromkeys(q for v in votes.values() for q in v.evidence_requests if len(q) <= 300))[:10]
        rejected = [q for v in votes.values() for q in v.evidence_requests if len(q) > 300]
        if rejected:
            self.events.append({'retrieval_requests_rejected': len(rejected)})
        if queries:
            self.ranked = await self.search(queries)
        return {'next': 'draft'}

    async def run(self):
        graph = StateGraph(GraphState)
        for name in ('select_notes', 'read_tools', 'analyze', 'draft', 'review', 'check'):
            graph.add_node(name, getattr(self, name))
        graph.add_edge(START, 'select_notes')
        graph.add_edge('select_notes', 'read_tools')
        graph.add_edge('read_tools', 'analyze')
        graph.add_edge('analyze', 'draft')
        graph.add_edge('draft', 'review')
        graph.add_edge('review', 'check')
        graph.add_conditional_edges('check', lambda s: s['next'], {'draft': 'draft', 'end': END})
        try:
            await graph.compile().ainvoke({'next': 'analyze'}, {'recursion_limit': 10 + self.config.max_rounds * 4})
        except Cancelled:
            self.status, self.reason = 'cancelled', 'Обсуждение отменено; поздние результаты не учитываются.'
        except Incomplete as exc:
            self.status, self.reason = 'incomplete', str(exc)
        except Exception as exc:
            self.status, self.reason = 'failed', getattr(exc, 'safe_code', None) or (type(exc).__name__ + ': protocol/source/model failure')
        return self

    def trace(self):
        return {'schema_version': 1, 'run_id': self.run_id, 'snapshot_id': self.snapshot_id,
                'mode': self.adapter.mode, 'model': self.adapter.capabilities.identity,
                'provider': self.adapter.capabilities.provider,
                'accounting_policy': self.adapter.capabilities.accounting_policy,
                'output_limit_policy': self.adapter.capabilities.output_limit_policy,
                'requested_output_tokens': self.config.output_tokens,
                'accepted_output_token_ceiling': output_token_ceiling(self.adapter.capabilities, self.config.output_tokens),
                'model_context_budget': self.adapter.capabilities.context_window,
                'reliable_token_accounting': self.adapter.capabilities.reliable_token_accounting,
                'reasoning_effort': getattr(getattr(self.adapter, 'settings', None), 'reasoning_effort', None),
                'policy_digest': digest(self.policy),
                'citation_protocol': PROTOCOL,
                'context_table_version': CONTEXT_TABLE_VERSION,
                'generation_schema_digest': self.generation_schema_digest,
                'generation_schema_digests': self.generation_schema_digests,
                'initial_position_bytes': self.initial_position_bytes,
                'stage_hints': self.stage_hints, 'persona_voices': self.persona_voices,
                'catalog_metadata': getattr(self.adapter, 'catalog_metadata', None),
                'status': self.status, 'reason': self.reason, 'question': self.question,
                'config': self.config.model_dump(mode='json'), 'persona_config': self.personas.model_dump(mode='json'),
                'manifest': [s.model_dump(mode='json') for s in self.sources],
                'evidence_store': {k: v.model_dump(mode='json') for k, v in self.retriever.evidence.items()},
                'initial_positions': {k: v.model_dump(mode='json') for k, v in self.positions.items()},
                'decisions': [d.model_dump(mode='json') for d in self.decisions],
                'votes_by_version': {str(v): {k: x.model_dump(mode='json') for k, x in votes.items()} for v, votes in self.votes.items()},
                'objection_ledger': [o.model_dump(mode='json') for o in self.obligations],
                'conflict_ledger': [c.model_dump(mode='json') for c in self.conflicts],
                'objection_checks_by_version': self.objection_checks, 'conflict_checks_by_version': self.conflict_checks,
                'coverage': self.retriever.coverage, 'embedding_config': self.retriever.embedding_config,
                'note_selection': self.note_selection, 'snapshot_tool_dispatches': self.tools.dispatches,
                'advisor_tool_results': self.tool_results,
                'events': self.events, 'usage': self.usage, 'attempts': self.attempts,
                'elapsed': time.monotonic() - self.started}
