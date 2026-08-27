from collections import defaultdict

from app.retrieval.schemas import RetrievalResult


def reciprocal_rank_fusion(rankings: list[list[RetrievalResult]], rrf_k: int = 60, top_k: int = 20) -> list[RetrievalResult]:
    score_map: dict[tuple[str, str, str], float] = defaultdict(float)
    exemplar: dict[tuple[str, str, str], RetrievalResult] = {}

    for ranking in rankings:
        for rank, item in enumerate(ranking, start=1):
            key = (item.document_id, item.version_id, item.chunk_id)
            score_map[key] += 1.0 / (rrf_k + rank)
            exemplar[key] = item

    ordered = sorted(score_map.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    fused: list[RetrievalResult] = []
    for key, score in ordered:
        base = exemplar[key]
        fused.append(
            RetrievalResult(
                tenant_id=base.tenant_id,
                document_id=base.document_id,
                version_id=base.version_id,
                chunk_id=base.chunk_id,
                score=score,
                metadata=base.metadata,
            )
        )
    return fused
