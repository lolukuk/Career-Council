from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from council.retrieval import Encoder, Retriever, tokens
from council.schemas import Cancelled, Config, Incomplete, Source, digest
from council.runtime import Council
from council.scripted import ScriptedAdapter


def test_actual_dense_paraphrase_and_no_truncation(tmp_path):
    texts = ('Automobile maintenance specialist fixes vehicles.',
             'Rare QXZ791 lexical identifier.',
             'An unrelated grocery list with milk and eggs.',
             'Long source ' + 'budget constraints and portfolio ' * 300)
    sources = tuple(Source(source_id=f's{i}', kind='document', origin='fixture', location='/',
                           captured_at='fixture', text=t, content_digest=digest(t)) for i, t in enumerate(texts))
    encoder = Encoder(Config(), Path('council/.cache/models'))
    retriever = Retriever.prepare(sources, encoder)
    order = retriever.search(['car mechanic repairs automobiles', 'QXZ791'])
    branches = retriever.coverage[-1]['branches']
    assert not set(tokens(texts[0])) & set(tokens('car mechanic repairs automobiles'))
    assert retriever.evidence[branches[0]['dense'][0][0]].source_id == 's0'
    assert retriever.evidence[branches[1]['bm25'][0][0]].source_id == 's1'
    assert retriever.embedding_config['model'] == 'sentence-transformers/all-MiniLM-L6-v2'
    for s in sources:
        chunks = sorted([e for e in retriever.evidence.values() if e.source_id == s.source_id], key=lambda e: e.start)
        assert ''.join(e.text for e in chunks) == s.text
    assert len([e for e in retriever.evidence.values() if e.source_id == 's3']) > 1


def test_native_windows_worker_cancel_and_late_result(tmp_path):
    assert os.name == 'nt', 'This prototype evidence requires native Windows.'
    response = tmp_path / 'response.json'
    cancelled = threading.Event()
    encoder = Encoder(Config(), tmp_path, cancelled)
    # Deliberately slow native helper also attempts to write a late result.
    code = 'import time,pathlib; time.sleep(10); pathlib.Path(__import__("sys").argv[1]).write_text("{}")'
    timer = threading.Timer(.3, cancelled.set)
    timer.start()
    started = time.monotonic()
    try:
        with pytest.raises(Cancelled):
            encoder.managed([sys.executable, '-c', code, str(response)], response, 20.0)
    finally:
        timer.cancel()
    event = encoder.events[-1]
    assert event['stopped'] and event['cancelled'] and time.monotonic() - started < 5
    assert not response.exists()
    # Popen.wait proves the child PID exited; no late output is accepted after cancellation.
    assert event['returncode'] is not None


def test_discussion_deadline_stops_actual_query_child(retriever, personas, tmp_path):
    import asyncio
    response = tmp_path / 'late.json'
    encoder = Encoder(Config(), tmp_path)
    received = []
    class SlowNativeQuery:
        def queries(self, texts, *, deadline=None, cancel=None):
            received.append(deadline)
            code = 'import time,pathlib,sys; time.sleep(10); pathlib.Path(sys.argv[1]).write_text("{}")'
            result = encoder.managed([sys.executable, '-c', code, str(response)], response,
                                     max(0.0, deadline-time.monotonic()), cancel)
            return result['vectors']
    retriever.encoder = SlowNativeQuery()
    c = Council('Career?', personas, tuple(retriever.sources.values()), retriever, ScriptedAdapter(),
                Config(deadline=.05))
    started = time.monotonic()
    asyncio.run(c.run())
    assert c.status == 'incomplete' and c.attempts == 0
    assert time.monotonic() - started < .3
    # Native cleanup is bounded separately and measured, not inferred from coroutine completion.
    until = time.monotonic() + 1
    while not encoder.events and time.monotonic() < until:
        time.sleep(.01)
    assert received and received[0] == c.started + c.config.deadline
    assert encoder.events and encoder.events[-1]['stopped'] and encoder.events[-1]['returncode'] is not None
    assert not response.exists() and not retriever.coverage
