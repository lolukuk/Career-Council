"""Read tools over the immutable snapshot captured by Sources through the API.

No model-selected filesystem access, direct JSON-file reads or writes. The API
capture and its retries remain owned by Sources; dispatch never re-fetches a
different observation halfway through a discussion.
"""
import json

from .schemas import ToolAction, canonical, digest


class SnapshotTools:
    def __init__(self, sources, evidence):
        self._sources = {s.source_id: s for s in sources
                         if s.kind in ('task', 'subtask') and s.origin.startswith('tasker:')}
        self._evidence = evidence
        self._tasks = {json.loads(s.text)['task_id']: s.source_id for s in self._sources.values()
                       if s.origin == 'tasker:get_task_details'}
        self.dispatches = 0

    def dispatch(self, action: ToolAction):
        if action.name == 'finish':
            raise ValueError('finish is not a tool')
        if action.task_id is not None and action.task_id not in self._tasks:
            raise ValueError('unknown task ID')
        if action.name == 'get_tasks':
            ids = [id_ for id_, s in self._sources.items() if s.origin == 'tasker:get_tasks']
            records = json.loads(self._sources[ids[0]].text) if ids else []
        elif action.name == 'get_task_details':
            ids = [self._tasks[action.task_id]]
            records = [json.loads(self._sources[ids[0]].text)]
        else:
            ids = [id_ for id_, s in self._sources.items()
                   if s.kind == 'subtask' and s.location.startswith('/' + action.task_id + '/')]
            records = [json.loads(self._sources[id_].text) for id_ in ids]
        evidence = [dict(e.model_dump(mode='json'), origin=self._sources[e.source_id].origin,
                         location=self._sources[e.source_id].location,
                         source_digest=self._sources[e.source_id].content_digest)
                    for e in self._evidence.values() if e.source_id in ids]
        self.dispatches += 1
        result = {'name': action.name, 'task_id': action.task_id, 'records': records,
                  'evidence': evidence, 'snapshot_reads': self.dispatches}
        return json.loads(canonical(result)), digest(result)
