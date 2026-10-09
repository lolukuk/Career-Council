from __future__ import annotations

from pathlib import Path

import pytest

from council.retrieval import Retriever
from council.schemas import Evidence, Source, digest
from council.sources import load_personas


class FixtureEncoder:
    def queries(self, queries, **kwargs):
        return [[1.0, 0.0] for _ in queries]


@pytest.fixture
def personas():
    return load_personas(Path('council/data/personas.md'))


@pytest.fixture
def retriever():
    kinds = ('profile', 'document', 'note', 'task', 'subtask', 'document')
    texts = ('Family constraints and resources.', 'Hiring opportunity coding portfolio.',
             'Coding is satisfying.', 'Budget planning.', 'Interview portfolio.',
             'Contradictory market risk.')
    sources = tuple(Source(source_id=f's{i}', kind=k, origin=f'fixture/{i}', location='/',
                           captured_at='fixture', text=t, content_digest=digest(t))
                    for i, (k, t) in enumerate(zip(kinds, texts)))
    evidence = tuple(Evidence(chunk_id=f'e{i}', source_id=s.source_id, text=s.text, start=0,
                              end=len(s.text), digest=digest(s.text)) for i, s in enumerate(sources))
    obj = Retriever(sources, evidence, [[1.0, 0.0] for _ in evidence], FixtureEncoder())
    obj.embedding_config = {'model': 'fixture', 'normalized': True}
    return obj
