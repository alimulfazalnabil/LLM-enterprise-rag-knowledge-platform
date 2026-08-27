from app.retrieval.rrf import reciprocal_rank_fusion
from app.retrieval.schemas import RetrievalResult


def _r(doc: str, rank_score: float) -> RetrievalResult:
    return RetrievalResult(
        tenant_id='tenant_a',
        document_id=doc,
        version_id='v1',
        chunk_id=f'{doc}_c1',
        score=rank_score,
        metadata={},
    )


def test_rrf_prioritizes_items_seen_in_multiple_rankings() -> None:
    dense = [_r('doc_1', 0.9), _r('doc_2', 0.8)]
    sparse = [_r('doc_2', 1.2), _r('doc_1', 1.0)]

    fused = reciprocal_rank_fusion([dense, sparse], rrf_k=60, top_k=2)

    assert len(fused) == 2
    assert {f.document_id for f in fused} == {'doc_1', 'doc_2'}
