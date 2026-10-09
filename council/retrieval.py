from __future__ import annotations

import json
import math
import re
import subprocess
import sys
import tempfile
import threading
import time
from collections import Counter
from pathlib import Path

from .schemas import Cancelled, Config, Evidence, Incomplete, canonical, digest


class Encoder:
    def __init__(self, config: Config, cache: Path, cancel=None):
        self.config, self.cache = config, cache.resolve()
        self.cancel = cancel or threading.Event()
        self.events = []

    def managed(self, command, response: Path, timeout, cancel=None):
        cancellation = cancel or self.cancel
        started = time.monotonic()
        # No visible helper window on Windows. Never trust worker-provided paths.
        with tempfile.TemporaryFile() as log:
            process = subprocess.Popen(command, stdout=log, stderr=log,
                                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            try:
                while process.poll() is None:
                    if cancellation.wait(0.01):
                        raise Cancelled('encoder cancelled')
                    if time.monotonic() - started > timeout:
                        raise Incomplete('encoder timeout')
                if cancellation.is_set():
                    raise Cancelled('late encoder result rejected')
                if process.returncode != 0:
                    log.seek(0, 2)
                    log.seek(max(0, log.tell() - 2000))
                    detail = log.read().decode('utf-8', errors='replace')
                    raise RuntimeError('encoder worker failed: ' + detail)
                if not response.is_file() or response.stat().st_size > 64 * 1024 * 1024:
                    raise RuntimeError('missing/oversized encoder output')
                return json.loads(response.read_text(encoding='utf-8'))
            finally:
                if process.poll() is None:
                    process.kill()
                process.wait(timeout=5)
                self.events.append({'pid': process.pid, 'returncode': process.returncode,
                                    'elapsed': time.monotonic() - started, 'stopped': process.poll() is not None,
                                    'cancelled': cancellation.is_set()})

    def request(self, operation, *, deadline=None, cancel=None, **payload):
        cancellation = cancel or self.cancel
        expires = min(time.monotonic() + self.config.preparation_timeout, deadline or float('inf'))
        if cancellation.is_set():
            raise Cancelled('encoder cancelled before dispatch')
        if time.monotonic() >= expires:
            raise Incomplete('encoder deadline before dispatch')
        with tempfile.TemporaryDirectory(prefix='council-encoder-') as directory:
            input_path, output_path = Path(directory) / 'request.json', Path(directory) / 'response.json'
            data = {'operation': operation, 'cache': str(self.cache),
                    'chunk_bytes': self.config.chunk_bytes, 'max_chunks': self.config.max_chunks, **payload}
            input_path.write_text(canonical(data), encoding='utf-8')
            result = self.managed([sys.executable, '-m', 'council.embedding_worker', '--request', str(input_path),
                                   '--response', str(output_path)], output_path,
                                  max(0.0, expires - time.monotonic()), cancellation)
        if cancellation.is_set():
            raise Cancelled('late encoder result rejected')
        if time.monotonic() >= expires:
            raise Incomplete('late encoder result rejected after deadline')
        vectors = result['vectors']
        if not vectors or any(not isinstance(v, list) or not v or len(v) > self.config.max_dimensions or
                              any(not isinstance(x, (int, float)) or not math.isfinite(x) for x in v) for v in vectors):
            raise ValueError('invalid embedding dimensions/values')
        if len({len(v) for v in vectors}) != 1:
            raise ValueError('inconsistent vector dimensions')
        return result

    def index(self, sources):
        from .embedding_worker import MODEL, REVISION
        payload = [{'source_id': s.source_id, 'text': s.text} for s in sources]
        key = digest({'sources': payload, 'model': MODEL, 'revision': REVISION,
                      'chunk_bytes': self.config.chunk_bytes, 'chunking': 'tokenizer-paragraphs-v1',
                      'max_chunks': self.config.max_chunks, 'max_dimensions': self.config.max_dimensions})
        path = self.cache.parent / ('index-' + key + '.json')
        if path.is_file() and path.stat().st_size <= 64 * 1024 * 1024:
            stored = json.loads(path.read_text(encoding='utf-8'))
            if stored['digest'] == digest(stored['result']):
                return stored['result']
            raise ValueError('embedding cache integrity')
        result = self.request('index', sources=payload)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(canonical({'digest': digest(result), 'result': result}), encoding='utf-8')
        return result

    def queries(self, texts, *, deadline=None, cancel=None):
        return self.request('query', texts=list(texts), deadline=deadline, cancel=cancel)['vectors']


def tokens(text):
    return re.findall(r'\w+', text.lower())


class Retriever:
    def __init__(self, sources, evidence, vectors, encoder):
        self.sources = {s.source_id: s for s in sources}
        self.evidence = {e.chunk_id: e for e in evidence}
        if len(self.evidence) != len(evidence) or len(vectors) != len(evidence) or not evidence:
            raise ValueError('index alignment')
        self.ids = list(self.evidence)
        self.vectors, self.encoder = vectors, encoder
        self.tf = [Counter(tokens(e.text)) for e in evidence]
        self.df = Counter(t for counts in self.tf for t in counts)
        self.avg = sum(sum(c.values()) for c in self.tf) / len(self.tf)
        self.coverage = []

    @classmethod
    def prepare(cls, sources, encoder):
        result = encoder.index(sources)
        if len(result['rows']) != len(result['vectors']):
            raise ValueError('encoder rows/vector mismatch')
        evidence = []
        registry = {s.source_id: s for s in sources}
        for i, row in enumerate(result['rows']):
            source = registry[row['source_id']]
            if source.text[row['start']:row['end']] != row['text']:
                raise ValueError('worker offsets mismatch')
            evidence.append(Evidence(chunk_id=f'e{i:05d}', digest=digest(row['text']), **row))
        # Full coverage: worker cannot silently omit a source tail/whitespace.
        for source in sources:
            chunks = sorted((e for e in evidence if e.source_id == source.source_id), key=lambda e: e.start)
            cursor = 0
            for e in chunks:
                if e.start != cursor:
                    raise ValueError('encoder missing/overlapping text')
                cursor = e.end
            if cursor != len(source.text):
                raise ValueError('encoder truncated source')
        obj = cls(sources, tuple(evidence), result['vectors'], encoder)
        obj.embedding_config = {k: v for k, v in result.items() if k not in ('rows', 'vectors')}
        return obj

    def search(self, queries, *, deadline=None, cancel=None, primary_weight=1):
        def active():
            if cancel is not None and cancel.is_set():
                raise Cancelled('retrieval cancelled')
            if deadline is not None and time.monotonic() >= deadline:
                raise Incomplete('retrieval deadline')
        active()
        if not queries or len(queries) > 10 or any(len(q) > 1500 for q in queries):
            raise ValueError('query budget')
        query_vectors = self.encoder.queries(queries, deadline=deadline, cancel=cancel)
        active()
        if len(query_vectors) != len(queries):
            raise ValueError('query vector alignment')
        fused = Counter()
        note_fused = Counter()
        note_lexical = Counter()
        branches = []
        n = len(self.ids)
        for query_index, (query, qv) in enumerate(zip(queries, query_vectors)):
            weight = primary_weight if query_index == 0 else 1
            lexical = []
            dense = []
            for i, counts in enumerate(self.tf):
                active()
                length = sum(counts.values())
                score = sum(math.log(1 + (n - self.df[t] + .5) / (self.df[t] + .5)) *
                            counts[t] * 2.5 / (counts[t] + 1.5 * (.25 + .75 * length / max(self.avg, 1)))
                            for t in tokens(query) if counts[t])
                if score > 0:
                    lexical.append((self.ids[i], score))
                if len(qv) != len(self.vectors[i]):
                    raise ValueError('query dimensions mismatch')
                dense.append((self.ids[i], sum(a*b for a, b in zip(qv, self.vectors[i]))))
            def dedup(branch):
                seen_digests = set()
                result = []
                for row in sorted(branch, key=lambda row: (-row[1], row[0])):
                    hash_ = self.evidence[row[0]].digest
                    if hash_ not in seen_digests:
                        seen_digests.add(hash_)
                        result.append(row)
                return result[:20]
            ranked = [dedup(branch) for branch in (lexical, dense)]
            for branch_index, branch in enumerate((lexical, dense)):
                note_branch = dedup([row for row in branch
                    if self.sources[self.evidence[row[0]].source_id].kind == 'note'])
                for rank, (id_, _) in enumerate(note_branch, 1):
                    note_fused[id_] += weight / (60 + rank)
                    if branch_index == 0:
                        note_lexical[id_] += weight / (60 + rank)
            branches.append({'query': query, 'bm25': ranked[0], 'dense': ranked[1]})
            for branch in ranked:
                for rank, (id_, _) in enumerate(branch, 1):
                    fused[id_] += weight / (60 + rank)
        order = sorted(fused, key=lambda id_: (-fused[id_], id_))
        # Keep origins of duplicate content rather than merging its provenance away.
        origins = {}
        for e in self.evidence.values():
            origins.setdefault(e.digest, []).append(e.chunk_id)
        active()
        # Reserve a small lexical lane so tied/weak dense rankings cannot
        # bury explicit signals under hundreds of unrelated personal notes.
        lexical_lane = sorted(note_lexical, key=lambda id_: (-note_lexical[id_], id_))[:5]
        note_order = list(dict.fromkeys(lexical_lane + sorted(note_fused, key=lambda id_: (-note_fused[id_], id_))))[:20]
        self.coverage.append({'branches': branches, 'ranked': order,
                              'primary_query_weight': primary_weight,
                              'note_ranked': note_order,
                              'duplicate_origins': {d: ids for d, ids in origins.items() if len(ids) > 1}})
        return order
