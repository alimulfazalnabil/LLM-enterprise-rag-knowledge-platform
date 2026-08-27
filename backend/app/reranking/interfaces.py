from typing import Protocol

from app.retrieval.schemas import RetrievalResult


class Reranker(Protocol):
    def rerank(self, query: str, candidates: list[RetrievalResult], top_k: int) -> list[RetrievalResult]: ...
