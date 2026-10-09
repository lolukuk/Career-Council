"""Requested 1200/300 measurement, real dense encoder and explicit fixture filter.

Run from project_1 with its venv; psutil is measurement-only, not an app dependency.
"""
import asyncio
import json
import threading
import time
import uuid
from pathlib import Path

import psutil

from council.model import Request
from council.prompts import STAGE_HINTS
from council.retrieval import Encoder, Retriever
from council.runtime import Council
from council.schemas import Config, Position, Source, canonical, digest
from council.scripted import ScriptedAdapter
from council.sources import Sources, load_personas


def source(id_, kind, text):
    return Source(source_id=id_, kind=kind, origin='synthetic-scale/' + id_, location='/',
                  captured_at='scale-fixture', text=text, content_digest=digest(text))


cfg, root = Config(), Path('council')
reader = Sources(cfg)
original = reader.load(root / 'data')
docs = [s for s in original if s.kind == 'document']
notes = [s for s in original if s.kind == 'note']
others = [s for s in original if s.kind not in ('document', 'note')]
gold_docs = [source('doc:scale-opportunity', 'document', 'Mechanical engineer transitioning into software development: use industrial automation knowledge and a coding portfolio to test employment prospects.'),
             source('doc:scale-risk', 'document', 'Mechanical engineer switching to software development faces uncertain employment. Coding as a hobby is not proof of professional fit; avoid resigning before testing income and family obligations.')]
gold_notes = [source('note:scale-positive', 'note', 'I enjoy coding after my mechanical engineering shift and want a software career experiment.'),
              source('note:scale-negative', 'note', 'Software career fear: I must preserve family income and test whether full-time coding differs from my hobby.')]
docs += gold_docs
notes += gold_notes
while len(docs) < 1200:
    i = len(docs)
    docs.append(source(f'doc:scale-noise-{i}', 'document', f'Botanical inventory specimen {i}: leaf pigmentation, soil moisture, plant height and gardening supplies.'))
while len(notes) < 300:
    i = len(notes)
    notes.append(source(f'note:scale-noise-{i}', 'note', f'Dentist appointment {i}, furnace filter shopping, watering plants.'))
sources = tuple(others + docs + notes)
stop, proc = threading.Event(), psutil.Process()
peak = {'parent_rss': proc.memory_info().rss, 'tree_rss': proc.memory_info().rss}


def sample():
    while not stop.wait(.1):
        try:
            parent = proc.memory_info().rss
            total = parent
            for child in proc.children(recursive=True):
                try:
                    total += child.memory_info().rss
                except psutil.Error:
                    pass
            peak['parent_rss'] = max(peak['parent_rss'], parent)
            peak['tree_rss'] = max(peak['tree_rss'], total)
        except psutil.Error:
            pass


thread = threading.Thread(target=sample, daemon=True)
thread.start()
started = time.perf_counter()
encoder = Encoder(cfg, root / '.cache/models')
r = Retriever.prepare(sources, encoder)
index_seconds = time.perf_counter() - started
q = "I'm thinking about switching careers from mechanical engineering to software development. Help me think through this decision."
c = Council(q, load_personas(root / 'data/personas.md'), sources, r, ScriptedAdapter(), cfg)
asyncio.run(c.select_notes({}))
packet, seen = c.context('initial', c.personas.personas[0], Position)
req = Request('initial', c.personas.personas[0].id, c.run_id, c.snapshot_id, 0, '0' * 32, '0' * 32,
              c.stage_policy('initial', c.personas.personas[0]), canonical(packet), canonical(Position.model_json_schema()), cfg.output_tokens)
shown = {r.evidence[e].source_id for e in seen}
shortlist = {r.evidence[e].source_id for e in c.note_selection['shortlist']}
selected = {r.evidence[e].source_id for e in c.relevant_notes}
dg, ng = {s.source_id for s in gold_docs}, {s.source_id for s in gold_notes}
checks = {'documents': len(docs) == 1200, 'notes': len(notes) == 300,
          'gold_docs': dg <= shown, 'gold_note_shortlist': ng <= shortlist, 'gold_note_context': ng <= shown,
          'no_selected_noise': not any('scale-noise' in s for s in selected),
          'bounded_request': len(req.serialized().encode('utf-8')) <= 32768,
          'shortlist': len(c.note_selection['shortlist']) <= 20}
stop.set()
thread.join()
out = root / 'output' / ('scale-' + uuid.uuid4().hex)
out.mkdir()
result = {'kind': 'synthetic_scale_not_live_quality', 'status': 'PASS' if all(checks.values()) else 'FAIL',
          'checks': checks, 'documents': len(docs), 'notes': len(notes), 'sources': len(sources),
          'chunks': len(r.evidence), 'index_seconds': index_seconds, 'index_cache_hit': not any('operation' in e for e in encoder.events) and len(encoder.events) == 1,
          'elapsed_seconds': time.perf_counter() - started, 'peak_sampled_memory_bytes': peak,
          'sampling_interval_seconds': .1, 'serialized_request_bytes': len(req.serialized().encode('utf-8')),
          'gold_document_hits': sorted(dg & shown), 'gold_note_shortlist_hits': sorted(ng & shortlist),
          'gold_note_context_hits': sorted(ng & shown), 'shown_sources': sorted(shown),
          'selected_noise_sources': sorted(s for s in selected if 'scale-noise' in s),
          'note_selection': c.note_selection, 'model_mode': 'scripted_filter_fixture', 'no_paid_calls': True,
          'embedding_config': r.embedding_config, 'encoder_events': encoder.events, 'api_calls': reader.calls}
(out / 'metadata.json').write_text(canonical(result), encoding='utf-8')
(out / 'report.md').write_text('# Проверка масштаба 1200/300\n\nНастоящий dense encoder, синтетический корпус, scripted фильтр; это не live качество.\n\n' + json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(canonical({'artifact': str(out.resolve()), 'status': result['status'], 'checks': checks,
                 'request_bytes': result['serialized_request_bytes'], 'seconds': result['elapsed_seconds'], 'memory': peak}))
raise SystemExit(0 if result['status'] == 'PASS' else 1)
