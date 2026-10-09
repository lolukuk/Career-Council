from __future__ import annotations

import hashlib
import json
import re
import time
import threading
from datetime import datetime, timezone
from pathlib import Path

from .schemas import Cancelled, Config, Incomplete, NAMES, ROSTER, Persona, PersonaConfig, Source, canonical, digest
from .tools import tasker


def load_personas(path: Path) -> PersonaConfig:
    raw = path.read_bytes()
    if len(raw) > 65536:
        raise Incomplete('persona configuration too large')
    text = raw.decode('utf-8-sig')
    entries = re.findall(r'^\d+\. \*\*(.+?)\*\*\s*—\s*(.*?)(?=^\d+\. \*\*|^Swap figures|\Z)', text, re.M | re.S)
    if tuple(name for name, _ in entries) != NAMES:
        raise ValueError('personas.md must contain exactly the given five personas in order')
    return PersonaConfig(source_digest=hashlib.sha256(raw).hexdigest(), personas=tuple(
        Persona(id=id_, name=name, description=' '.join(desc.split()))
        for id_, (name, desc) in zip(ROSTER, entries)))


class Sources:
    def __init__(self, config: Config, api=tasker, sleep=time.sleep, clock=time.monotonic, cancel=None):
        self.config, self.api, self.sleep, self.clock = config, api, sleep, clock
        self.calls = 0
        self.records = []
        self.total = 0
        self.events = []
        self.started = clock()
        self.cancel = cancel or threading.Event()

    def check(self):
        if self.cancel.is_set():
            raise Cancelled('source preparation cancelled')
        if self.clock() - self.started > self.config.preparation_timeout:
            raise Incomplete('preparation deadline')

    def read(self, path):
        self.check()
        if not path.is_file() or path.stat().st_size > self.config.max_file_bytes:
            raise Incomplete('missing or oversized mandatory input')
        raw = path.read_bytes()
        if len(raw) > self.config.max_file_bytes:
            raise Incomplete('input grew beyond limit')
        self.total += len(raw)
        if self.total > self.config.max_source_bytes:
            raise Incomplete('source byte budget')
        return raw.decode('utf-8-sig')

    def add(self, id_, kind, origin, location, text, date=None):
        self.check()
        if len(self.records) >= self.config.max_sources:
            raise Incomplete('source count budget')
        if not text.strip():
            raise Incomplete('empty mandatory source')
        if len(text.encode('utf-8')) > self.config.max_file_bytes:
            raise Incomplete('tool record byte budget')
        if any(r.source_id == id_ for r in self.records):
            raise ValueError('duplicate source ID')
        self.records.append(Source(source_id=id_, kind=kind, origin=origin, location=location,
                                   captured_at=datetime.now(timezone.utc).isoformat(), source_date=date,
                                   text=text, content_digest=digest(text)))

    def call(self, name, *args):
        for attempt in range(3):
            self.check()
            if self.calls >= self.config.max_tasker_calls:
                raise Incomplete('tasker call budget')
            self.calls += 1
            try:
                value = getattr(self.api, name)(*args)
                size = len(canonical(value).encode('utf-8'))
                self.total += size
                if size > self.config.max_file_bytes or self.total > self.config.max_source_bytes:
                    raise Incomplete('tool response byte budget')
                self.events.append({'tool': name, 'args': args, 'attempt': attempt + 1, 'ok': True})
                return value
            except tasker.TaskerServiceError:
                self.events.append({'tool': name, 'args': args, 'attempt': attempt + 1, 'ok': False})
                if attempt == 2:
                    raise Incomplete('mandatory tasker read exhausted') from None
                self.sleep((0.1, 0.3)[attempt])

    def load(self, root: Path):
        self.add('profile', 'profile', 'user_kb.md', '/', self.read(root / 'user_kb.md'))
        documents = sorted((root / 'corpus').glob('*.md'))
        if not documents:
            raise Incomplete('missing document corpus')
        for path in documents:
            self.add('doc:' + path.stem, 'document', str(path.relative_to(root)), '/', self.read(path))
        notes = json.loads(self.read(root / 'notes.json'))
        if not isinstance(notes, list):
            raise ValueError('invalid notes inventory')
        for i, note in enumerate(notes):
            if not isinstance(note, dict) or not isinstance(note.get('note_id'), str):
                raise ValueError('invalid note')
            self.add('note:' + note['note_id'], 'note', 'notes.json', f'/{i}', canonical(note), note.get('date'))
        tasks = self.call('get_tasks')
        if not isinstance(tasks, list):
            raise ValueError('invalid task inventory')
        ids = [t.get('task_id') for t in tasks if isinstance(t, dict)]
        if len(ids) != len(tasks) or any(not isinstance(id_, str) or not id_ for id_ in ids) or len(ids) != len(set(ids)):
            raise ValueError('invalid task inventory IDs')
        self.add('tasker:inventory', 'task', 'tasker:get_tasks', '/inventory', canonical(tasks))
        for id_ in ids:
            detail = self.call('get_task_details', id_)
            if not isinstance(detail, dict) or detail.get('task_id') != id_ or 'subtasks' in detail:
                raise ValueError('task identity/scope mismatch')
            self.add('task:' + id_, 'task', 'tasker:get_task_details', '/' + id_, canonical(detail))
            children = self.call('get_subtasks', id_)
            if not isinstance(children, list):
                raise ValueError('invalid subtasks')
            child_ids = set()
            for child in children:
                if not isinstance(child, dict):
                    raise ValueError('invalid subtask')
                cid = child.get('subtask_id')
                if not isinstance(cid, str) or not cid or cid in child_ids or child.get('task_id', id_) != id_:
                    raise ValueError('subtask parent/ID mismatch')
                child_ids.add(cid)
                self.add('subtask:' + id_ + ':' + cid, 'subtask', 'tasker:get_subtasks', '/' + id_ + '/' + cid, canonical(child))
        return tuple(self.records)
