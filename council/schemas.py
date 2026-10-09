from __future__ import annotations

import hashlib
import json
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ROSTER = ('peter_thiel', 'warren_buffett', 'robert_reich',
          'nassim_nicholas_taleb', 'marcus_aurelius')
NAMES = ('Peter Thiel', 'Warren Buffett', 'Robert Reich',
         'Nassim Nicholas Taleb', 'Marcus Aurelius')
Text = Annotated[str, Field(min_length=1, max_length=1500)]
Short = Annotated[str, Field(min_length=1, max_length=600)]
Id = Annotated[str, Field(min_length=1, max_length=160)]


def canonical(value) -> str:
    if isinstance(value, BaseModel):
        value = value.model_dump(mode='json')
    def encode(item):
        if isinstance(item, BaseModel):
            return item.model_dump(mode='json')
        raise TypeError('not JSON serializable')
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False, default=encode)


def digest(value) -> str:
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


class DTO(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid', frozen=True)

    @field_validator('*')
    @classmethod
    def nonblank(cls, value, info):
        if isinstance(value, str) and not value.strip() and info.field_name != 'change_summary':
            raise ValueError('required text must contain a nonwhitespace character')
        return value


class Config(DTO):
    max_rounds: Annotated[int, Field(ge=1, le=10)] = 3
    max_attempts: Annotated[int, Field(ge=1, le=100)] = 50
    model_timeout: Annotated[float, Field(gt=0, allow_inf_nan=False)] = 45.0
    deadline: Annotated[float, Field(gt=0, allow_inf_nan=False)] = 600.0
    context_bytes: Annotated[int, Field(ge=1000, le=1_000_000)] = 32768
    output_tokens: Annotated[int, Field(ge=100, le=8000)] = 2000
    preparation_timeout: Annotated[float, Field(gt=0, allow_inf_nan=False)] = 300.0
    max_sources: Annotated[int, Field(ge=1, le=5000)] = 5000
    max_file_bytes: Annotated[int, Field(ge=1, le=8388608)] = 8388608
    max_source_bytes: Annotated[int, Field(ge=1, le=67108864)] = 67108864
    max_chunks: Annotated[int, Field(ge=1, le=20000)] = 20000
    chunk_bytes: Annotated[int, Field(ge=64, le=4096)] = 4096
    max_dimensions: Annotated[int, Field(ge=1, le=1024)] = 1024
    max_tasker_calls: Annotated[int, Field(ge=1, le=100)] = 100


class Persona(DTO):
    id: Id
    name: Short
    description: Text


class PersonaConfig(DTO):
    source_digest: Id
    personas: tuple[Persona, ...]

    @model_validator(mode='after')
    def roster(self):
        if tuple(p.id for p in self.personas) != ROSTER or tuple(p.name for p in self.personas) != NAMES:
            raise ValueError('fixed persona roster mismatch')
        return self


class Source(DTO):
    source_id: Id
    kind: Literal['profile', 'note', 'document', 'task', 'subtask']
    origin: Id
    location: Id
    captured_at: Id
    source_date: str | None = None
    text: Annotated[str, Field(min_length=1, max_length=8388608)]
    content_digest: Id


class Evidence(DTO):
    chunk_id: Id
    source_id: Id
    text: Annotated[str, Field(min_length=1, max_length=4096)]
    start: Annotated[int, Field(ge=0)]
    end: Annotated[int, Field(gt=0)]
    digest: Id
    section: Annotated[str, Field(max_length=600)] = '/'


class Citation(DTO):
    chunk_id: Id
    quote: Annotated[str, Field(min_length=1, max_length=400)]


class Argument(DTO):
    text: Annotated[str, Field(min_length=1, max_length=800)]
    basis: Literal['source', 'assumption']
    citations: Annotated[tuple[Citation, ...], Field(max_length=5)] = ()
    impact: Short = 'Основание рекомендации.'

    @model_validator(mode='after')
    def basis_refs(self):
        if (self.basis == 'source') != bool(self.citations):
            raise ValueError('source needs citations; assumption must be disclosed without source citations')
        return self


class Criterion(DTO):
    id: Id
    text: Short
    blocking: bool = True


class ConflictInput(DTO):
    text: Short
    citations: tuple[Citation, Citation]

    @model_validator(mode='after')
    def distinct(self):
        if self.citations[0] == self.citations[1]:
            raise ValueError('conflict requires two distinct assertions')
        return self


class Position(DTO):
    recommendation: Text
    arguments: Annotated[tuple[Argument, ...], Field(min_length=1, max_length=5)]
    criteria: Annotated[tuple[Criterion, ...], Field(min_length=1, max_length=4)]
    strongest_counterargument: Text
    missing_data: Annotated[tuple[Short, ...], Field(max_length=5)] = ()
    conflicts: Annotated[tuple[ConflictInput, ...], Field(max_length=2)] = ()


class CompactArgument(Argument):
    text: Annotated[str, Field(min_length=1, max_length=200)]
    impact: Annotated[str, Field(min_length=1, max_length=80)] = 'Основание рекомендации.'


class CompactCriterion(Criterion):
    text: Annotated[str, Field(min_length=1, max_length=240)]


class CompactPosition(Position):
    """Generation subset; accepted state is normalized to the original Position."""
    recommendation: Annotated[str, Field(min_length=1, max_length=200)]
    arguments: Annotated[tuple[CompactArgument, ...], Field(min_length=1, max_length=2)]
    criteria: Annotated[tuple[CompactCriterion, ...], Field(min_length=1, max_length=1)]
    strongest_counterargument: Annotated[str, Field(min_length=1, max_length=240)]
    missing_data: Annotated[tuple[Annotated[str, Field(min_length=1, max_length=100)], ...], Field(max_length=3)] = ()


class NoteSelection(DTO):
    relevant_chunk_ids: Annotated[tuple[Id, ...], Field(max_length=20)] = ()


class ToolAction(DTO):
    name: Literal['get_tasks', 'get_task_details', 'get_subtasks', 'finish']
    task_id: Id | None = None

    @model_validator(mode='after')
    def arguments(self):
        needs_id = self.name in ('get_task_details', 'get_subtasks')
        if needs_id != (self.task_id is not None):
            raise ValueError('tool argument mismatch')
        return self


class Claim(Argument):
    id: Id


class Section(DTO):
    text: Text
    claim_refs: Annotated[tuple[Id, ...], Field(min_length=1, max_length=8)]
    caveat_refs: Annotated[tuple[Id, ...], Field(max_length=8)] = ()


class Caveat(DTO):
    id: Id
    text: Short
    claim_refs: Annotated[tuple[Id, ...], Field(min_length=1, max_length=8)]


class Response(DTO):
    id: Id
    text: Short
    claim_refs: Annotated[tuple[Id, ...], Field(min_length=1, max_length=8)]
    caveat_ref: Id | None = None


class Proposal(DTO):
    recommendation: Section
    steps: Annotated[tuple[Section, ...], Field(min_length=1, max_length=8)]
    claims: Annotated[tuple[Claim, ...], Field(min_length=1, max_length=8)]
    alternatives: Annotated[tuple[Short, ...], Field(max_length=5)] = ()
    caveats: Annotated[tuple[Caveat, ...], Field(max_length=8)] = ()
    missing_data: Annotated[tuple[Short, ...], Field(max_length=5)] = ()
    objection_responses: Annotated[tuple[Response, ...], Field(max_length=150)] = ()
    conflict_responses: Annotated[tuple[Response, ...], Field(max_length=30)] = ()
    change_summary: Annotated[str, Field(max_length=1500)] = ''


class CompactSection(Section):
    text: Annotated[str, Field(min_length=1, max_length=240)]


class CompactRecommendation(Section):
    text: Annotated[str, Field(min_length=1, max_length=400)]


class CompactClaim(Claim):
    text: Annotated[str, Field(min_length=1, max_length=240)]
    impact: Annotated[str, Field(min_length=1, max_length=100)] = 'Основание рекомендации.'


class CompactCaveat(Caveat):
    text: Annotated[str, Field(min_length=1, max_length=300)]


class CompactResponse(Response):
    text: Annotated[str, Field(min_length=1, max_length=240)]


class CompactProposal(Proposal):
    recommendation: CompactRecommendation
    steps: Annotated[tuple[CompactSection, ...], Field(min_length=1, max_length=8)]
    claims: Annotated[tuple[CompactClaim, ...], Field(min_length=1, max_length=8)]
    alternatives: Annotated[tuple[Annotated[str, Field(min_length=1, max_length=160)], ...], Field(max_length=5)] = ()
    caveats: Annotated[tuple[CompactCaveat, ...], Field(max_length=8)] = ()
    missing_data: Annotated[tuple[Annotated[str, Field(min_length=1, max_length=160)], ...], Field(max_length=5)] = ()
    objection_responses: Annotated[tuple[CompactResponse, ...], Field(max_length=150)] = ()
    conflict_responses: Annotated[tuple[CompactResponse, ...], Field(max_length=30)] = ()
    change_summary: Annotated[str, Field(max_length=240)] = ''


class Decision(DTO):
    run_id: Id
    snapshot_id: Id
    version: Annotated[int, Field(ge=1)]
    digest: Id
    payload: Proposal


class Check(DTO):
    id: Id
    status: Literal['satisfied', 'unmet', 'resolved', 'upheld', 'supported', 'qualified',
                    'unsupported', 'uncertainty_in_decision', 'unresolved']
    rationale: Short
    claim_ref: Id | None = None
    caveat_ref: Id | None = None
    condition_text: Short | None = None


class PayloadAssessment(DTO):
    status: Literal['supported', 'unsupported']
    unregistered_assertions: Annotated[tuple[Short, ...], Field(max_length=8)] = ()
    rationale: Short


class ObjectionInput(DTO):
    text: Short
    blocking: bool = True
    citations: Annotated[tuple[Citation, ...], Field(max_length=5)] = ()


class Vote(DTO):
    run_id: Id
    snapshot_id: Id
    target_version: Annotated[int, Field(ge=1)]
    target_digest: Id
    verdict: Literal['approve', 'object', 'abstain']
    rationale: Text
    criterion_checks: Annotated[tuple[Check, ...], Field(max_length=4)]
    objection_checks: Annotated[tuple[Check, ...], Field(max_length=150)] = ()
    conflict_checks: Annotated[tuple[Check, ...], Field(max_length=30)] = ()
    claim_assessments: Annotated[tuple[Check, ...], Field(min_length=1, max_length=8)]
    payload_assessment: PayloadAssessment
    new_objections: Annotated[tuple[ObjectionInput, ...], Field(max_length=3)] = ()
    new_conflicts: Annotated[tuple[ConflictInput, ...], Field(max_length=2)] = ()
    change_explanation: Text
    evidence_requests: Annotated[tuple[Short, ...], Field(max_length=2)] = ()


class CompactCheck(Check):
    rationale: Annotated[str, Field(min_length=1, max_length=120)]


class CompactPayloadAssessment(PayloadAssessment):
    rationale: Annotated[str, Field(min_length=1, max_length=240)]
    unregistered_assertions: Annotated[tuple[Annotated[str, Field(min_length=1, max_length=160)], ...], Field(max_length=8)] = ()


class CompactObjection(ObjectionInput):
    text: Annotated[str, Field(min_length=1, max_length=300)]


class CompactVote(Vote):
    rationale: Annotated[str, Field(min_length=1, max_length=240)]
    change_explanation: Annotated[str, Field(min_length=1, max_length=240)]
    criterion_checks: Annotated[tuple[CompactCheck, ...], Field(max_length=4)]
    objection_checks: Annotated[tuple[CompactCheck, ...], Field(max_length=150)] = ()
    conflict_checks: Annotated[tuple[CompactCheck, ...], Field(max_length=30)] = ()
    claim_assessments: Annotated[tuple[CompactCheck, ...], Field(min_length=1, max_length=8)]
    payload_assessment: CompactPayloadAssessment
    new_objections: Annotated[tuple[CompactObjection, ...], Field(max_length=3)] = ()
    evidence_requests: Annotated[tuple[Annotated[str, Field(min_length=1, max_length=160)], ...], Field(max_length=2)] = ()


class Obligation(DTO):
    id: Id
    owner: Id
    origin_version: Annotated[int, Field(ge=0)]
    text: Short
    blocking: bool = True
    citations: Annotated[tuple[Citation, ...], Field(max_length=5)] = ()


class Conflict(DTO):
    id: Id
    owner: Id
    origin_version: Annotated[int, Field(ge=0)]
    text: Short
    citations: tuple[Citation, Citation]


class Incomplete(RuntimeError):
    """A mandatory source, budget or context constraint prevents a complete run."""


class Cancelled(RuntimeError):
    pass


def exact_ids(items, expected):
    ids = [i.id for i in items]
    if len(ids) != len(set(ids)) or set(ids) != set(expected):
        raise ValueError('duplicate/missing/foreign check IDs')


def citation_refs(value):
    value = value.model_dump(mode='json') if isinstance(value, BaseModel) else value
    if isinstance(value, dict):
        if set(value) == {'chunk_id', 'quote'}:
            yield Citation.model_validate(value)
        else:
            for child in value.values():
                yield from citation_refs(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            yield from citation_refs(child)
