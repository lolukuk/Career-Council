from __future__ import annotations

import json
from pathlib import Path

import pytest

from council.schemas import Config, Incomplete, ROSTER
from council.sources import Sources, load_personas
from council.tools.tasker import TaskerServiceError


class API:
    def __init__(self, fail=0, detail_id='t1', parent='t1'):
        self.fail, self.detail_id, self.parent, self.calls = fail, detail_id, parent, []

    def get_tasks(self):
        self.calls.append(('list',))
        if self.fail:
            self.fail -= 1
            raise TaskerServiceError()
        return [{'task_id': 't1'}]

    def get_task_details(self, id_):
        self.calls.append(('detail', id_))
        return {'task_id': self.detail_id, 'description': 'Plan'}

    def get_subtasks(self, id_):
        self.calls.append(('children', id_))
        return [{'subtask_id': 'c1', 'task_id': self.parent, 'title': 'Do'}]


def dossier(tmp_path):
    (tmp_path / 'corpus').mkdir()
    (tmp_path / 'user_kb.md').write_text('Profile', encoding='utf-8')
    (tmp_path / 'corpus' / 'doc.md').write_text('Document', encoding='utf-8')
    (tmp_path / 'notes.json').write_text(json.dumps([{'note_id': 'n1', 'content': 'Note'}]))
    return tmp_path


def test_fixed_frozen_personas(personas, tmp_path):
    assert tuple(p.id for p in personas.personas) == ROSTER
    raw = Path('council/data/personas.md').read_text(encoding='utf-8')
    p = tmp_path / 'personas.md'
    p.write_text(raw.replace('Peter Thiel', 'Unknown'))
    with pytest.raises(ValueError):
        load_personas(p)
    assert personas.personas[0].name == 'Peter Thiel'


def test_tasker_hierarchy_retry(tmp_path):
    api = API(fail=1)
    reader = Sources(Config(), api=api, sleep=lambda _: None)
    records = reader.load(dossier(tmp_path))
    assert api.calls == [('list',), ('list',), ('detail', 't1'), ('children', 't1')]
    assert {r.kind for r in records} == {'profile', 'document', 'note', 'task', 'subtask'}


@pytest.mark.parametrize('detail,parent', [('wrong', 't1'), ('t1', 'wrong')])
def test_tool_scope_rejected(tmp_path, detail, parent):
    with pytest.raises(ValueError):
        Sources(Config(), api=API(detail_id=detail, parent=parent)).load(dossier(tmp_path))


def test_tasker_exhausted_is_gap(tmp_path):
    with pytest.raises(Incomplete):
        Sources(Config(), api=API(fail=3), sleep=lambda _: None).load(dossier(tmp_path))


def test_keyerror_not_retried(tmp_path):
    api = API()
    def detail(id_):
        api.calls.append(('detail', id_))
        raise KeyError(id_)
    api.get_task_details = detail
    with pytest.raises(KeyError):
        Sources(Config(), api=api).load(dossier(tmp_path))
    assert api.calls == [('list',), ('detail', 't1')]


def test_source_bytes_bounded(tmp_path):
    with pytest.raises(Incomplete):
        Sources(Config(max_file_bytes=3), api=API()).load(dossier(tmp_path))


def test_duplicate_tasks_rejected(tmp_path):
    api = API()
    api.get_tasks = lambda: [{'task_id': 't1'}, {'task_id': 't1'}]
    with pytest.raises(ValueError):
        Sources(Config(), api=api).load(dossier(tmp_path))
