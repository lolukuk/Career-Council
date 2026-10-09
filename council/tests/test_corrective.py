import asyncio
import json

import pytest
from pydantic import ValidationError

from council.context import build_context
from council.model import Response
from council.retrieval import Retriever
from council.runtime import Council
from council.schemas import Config, Evidence, Position, ToolAction, canonical, digest
from council.scripted import ScriptedAdapter
from council.sources import Sources
from council.task_tools import SnapshotTools
from conftest import FixtureEncoder
from test_sources import API, dossier


def prepared(tmp_path, notes, api=None):
    root = dossier(tmp_path)
    (root / 'notes.json').write_text(canonical(notes), encoding='utf-8')
    reader = Sources(Config(), api=api or API(), sleep=lambda _: None)
    sources = reader.load(root)
    evidence = tuple(Evidence(chunk_id=f'e{i}', source_id=s.source_id, text=s.text,
                              start=0, end=len(s.text), digest=digest(s.text)) for i, s in enumerate(sources))
    return reader, Retriever(sources, evidence, [[1., 0.] for _ in evidence], FixtureEncoder())


@pytest.mark.parametrize('notes,expected', [([], 0),
    ([{'note_id': 'noise', 'content': 'Replace furnace filter and reschedule dentist.'}], 0),
    ([{'note_id': 'noise', 'content': 'Replace furnace filter.'},
      {'note_id': 'signal', 'content': 'Software career with coding.'}], 1),
    ([{'note_id': f'noise{i}', 'content': f'Dentist appointment {i}, furnace filter.'} for i in range(300)], 0),
    ([{'note_id': f'noise{i}', 'content': f'Dentist appointment {i}, furnace filter.'} for i in range(298)] +
     [{'note_id': 'signal', 'content': 'Software career with coding.'},
      {'note_id': 'counter', 'content': 'Software career risk: family income before quitting.'}], 2)])
def test_empty_noise_mixed_selection(tmp_path, personas, notes, expected):
    _, r = prepared(tmp_path, notes)
    c = Council('Software career?', personas, tuple(r.sources.values()), r, ScriptedAdapter())
    asyncio.run(c.select_notes({}))
    assert len(c.relevant_notes) == expected
    packet, _ = c.context('initial', personas.personas[0], Position)
    shown_notes = {e['chunk_id'] for e in packet['evidence'] if r.sources[e['source_id']].kind == 'note'}
    assert shown_notes <= c.relevant_notes
    assert len(c.note_selection['shortlist']) <= 20


def test_successfully_empty_task_inventory(tmp_path):
    api = API()
    api.get_tasks = lambda: []
    reader, r = prepared(tmp_path, [], api)
    assert not any(s.kind in ('note', 'subtask') for s in r.sources.values())
    assert all(s.origin == 'tasker:get_tasks' and json.loads(s.text) == []
               for s in r.sources.values() if s.kind == 'task')
    tools = SnapshotTools(tuple(r.sources.values()), r.evidence)
    result, _ = tools.dispatch(ToolAction(name='get_tasks'))
    assert result['records'] == [] and all(e['text'] == '[]' for e in result['evidence'])
    assert reader.events[-1]['ok'] is True


def test_tools_provenance_scope_and_snapshot(tmp_path):
    api = API()
    reader, r = prepared(tmp_path, [], api)
    calls = list(api.calls)
    tools = SnapshotTools(tuple(r.sources.values()), r.evidence)
    for name in ('get_tasks', 'get_task_details', 'get_subtasks'):
        action = ToolAction(name=name, task_id=None if name == 'get_tasks' else 't1')
        result, hash_ = tools.dispatch(action)
        assert result['evidence'] and hash_ == digest(result)
        assert all(e['origin'].startswith('tasker:') for e in result['evidence'])
        if name == 'get_tasks':
            assert all(e['origin'] == 'tasker:get_tasks' for e in result['evidence'])
            assert 'description' not in canonical(result)
    assert api.calls == calls and reader.calls == 3
    with pytest.raises(ValueError):
        tools.dispatch(ToolAction(name='get_task_details', task_id='foreign'))
    with pytest.raises(ValidationError):
        ToolAction(name='delete_task', task_id='t1')
    with pytest.raises(ValidationError):
        ToolAction(name='get_tasks', task_id='t1')


def test_tool_loop_limit_and_advisor_isolation(tmp_path, personas):
    _, r = prepared(tmp_path, [])
    class AlwaysRead(ScriptedAdapter):
        async def generate(self, request):
            if request.stage == 'tools':
                self.requests.append(request)
                return Response(canonical({'name': 'get_tasks', 'task_id': None}))
            return await super().generate(request)
    c = Council('Career?', personas, tuple(r.sources.values()), r, AlwaysRead())
    asyncio.run(c.select_notes({}))
    asyncio.run(c.read_tools({}))
    assert c.tools.dispatches == 15 and c.attempts == 15
    assert all(len(results) == 3 for results in c.tool_results.values())
    for request in c.adapter.requests:
        packet = request.payload()
        assert not {'positions', 'previous_votes', 'advisor_tool_results'} & packet.keys()
        assert 'available_tools' in packet
        assert all('evidence' not in result and 'evidence_ids' in result
                   for result in packet.get('tool_results', []))
    assert all(e['snapshot_id'] == c.snapshot_id for e in c.events if 'tool_dispatch' in e)


def test_filter_unknown_id_is_not_valid_empty(tmp_path, personas):
    _, r = prepared(tmp_path, [{'note_id': 'n1', 'content': 'Career'}])
    class Foreign(ScriptedAdapter):
        async def generate(self, request):
            if request.stage == 'notes':
                return Response(canonical({'relevant_chunk_ids': ['foreign']}))
            return await super().generate(request)
    c = Council('Career?', personas, tuple(r.sources.values()), r, Foreign())
    asyncio.run(c.run())
    assert c.status == 'failed' and c.note_selection['status'] == 'pending'
    assert c.events[-1]['validation_code'] == 'note_selection_ids'


def test_filtered_counterevidence_remains_transitively_pinned(retriever, personas):
    from council.schemas import Argument, Citation
    argument = Argument(text='Personal doubt', basis='source',
                        citations=(Citation(chunk_id='e2', quote='Coding'),))
    packet, seen = build_context('draft', question='Career?', snapshot_id='s', persona=personas,
        positions={'p': argument}, decision=None, obligations=(), conflicts=(), previous_votes={},
        retriever=retriever, ranked=['e1'], relevant_notes=frozenset(), cap=10000)
    assert 'e2' in seen
