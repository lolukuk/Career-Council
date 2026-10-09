import pytest

from council.context import build_context, validate_citations
from council.schemas import Argument, Citation, Incomplete


def packet(retriever, personas, **kwargs):
    args = dict(question='Career?', snapshot_id='s', persona=personas.personas[0], positions={},
                decision=None, obligations=(), conflicts=(), previous_votes={}, retriever=retriever,
                ranked=retriever.search(['coding']), cap=10000)
    args.update(kwargs)
    return build_context('initial', **args)


def test_initial_allowlist(retriever, personas):
    payload, seen = packet(retriever, personas)
    assert not {'positions', 'decision', 'previous_votes', 'obligations'} & payload.keys()
    assert len(seen) == 6
    assert payload['persona']['id'] == 'peter_thiel'
    assert all(not {'digest', 'source_digest', 'start', 'end'} & e.keys() for e in payload['evidence'])
    assert all(retriever.evidence[e['chunk_id']].text == e['text'] for e in payload['evidence'])


def test_exact_seen_quotes(retriever):
    cite = Citation(chunk_id='e5', quote='Contradictory')
    with pytest.raises(ValueError):
        validate_citations(cite, retriever.evidence, {'e1'})
    validate_citations(cite, retriever.evidence, {'e5'})
    with pytest.raises(ValueError):
        validate_citations(Citation(chunk_id='e5', quote='fabricated'), retriever.evidence, {'e5'})


def test_transitive_evidence_is_pinned(retriever, personas):
    argument = Argument(text='Counterevidence', basis='source', citations=(Citation(chunk_id='e5', quote='Contradictory'),))
    payload, seen = build_context('draft', question='Career?', snapshot_id='s', persona=personas,
                                 positions={'p': argument}, decision=None, obligations=(), conflicts=(),
                                 previous_votes={}, retriever=retriever, ranked=['e1'], cap=10000)
    assert 'e5' in seen
    with pytest.raises(Incomplete):
        build_context('draft', question='Career?', snapshot_id='s', persona=personas,
                      positions={'p': argument}, decision=None, obligations=(), conflicts=(),
                      previous_votes={}, retriever=retriever, ranked=['e1'], cap=100)
