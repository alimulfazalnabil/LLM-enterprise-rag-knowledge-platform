from __future__ import annotations

from typing import Any


class HybridRetrievalEngine:
    def __init__(self, vector_store, bm25_index, reranker):
        self.vector_store = vector_store
        self.bm25_index = bm25_index
        self.reranker = reranker

    async def retrieve(
        self,
        tenant_id: str,
        query: str,
        query_embedding: list[float],
        dense_top_k: int = 20,
        sparse_top_k: int = 20,
        fusion_top_k: int = 30,
        rerank_top_k: int = 8,
    ) -> list[dict[str, Any]]:
        dense_results = await self.vector_store.similarity_search(
            tenant_id=tenant_id,
            embedding=query_embedding,
            top_k=dense_top_k,
        )
        sparse_results = await self.bm25_index.search(
            tenant_id=tenant_id,
            query=query,
            top_k=sparse_top_k,
        )
        fused = self._rrf(dense_results, sparse_results, top_k=fusion_top_k)
        reranked = await self.reranker.rerank(query=query, candidates=fused, top_k=rerank_top_k)
        return reranked

    def _rrf(self, dense: list[dict[str, Any]], sparse: list[dict[str, Any]], k: int = 60, top_k: int = 30) -> list[dict[str, Any]]:
        scores: dict[str, float] = {}
        doc_map: dict[str, dict[str, Any]] = {}

        for rank, doc in enumerate(dense):
            did = doc['chunk_id']
            doc_map[did] = doc
            scores[did] = scores.get(did, 0.0) + (1.0 / (k + rank + 1))

        for rank, doc in enumerate(sparse):
            did = doc['chunk_id']
            doc_map[did] = doc
            scores[did] = scores.get(did, 0.0) + (1.0 / (k + rank + 1))

        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [{**doc_map[did], 'rrf_score': score} for did, score in sorted_docs[:top_k]]
