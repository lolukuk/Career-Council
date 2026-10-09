import pytest


def test_both_branches_and_rare_lexical(retriever):
    order = retriever.search(['portfolio'])
    branches = retriever.coverage[-1]['branches'][0]
    assert branches['bm25'] and branches['dense']
    assert order[0] in ('e1', 'e4')
    assert 'e5' in order


def test_no_dense_fallback(retriever):
    def unavailable(_, **kwargs):
        raise RuntimeError('unavailable')
    retriever.encoder.queries = unavailable
    with pytest.raises(RuntimeError):
        retriever.search(['coding'])


def test_tie_is_stable(retriever):
    assert retriever.search(['notpresent']) == sorted(retriever.evidence)


def test_query_limit(retriever):
    with pytest.raises(ValueError):
        retriever.search(['q'] * 11)
