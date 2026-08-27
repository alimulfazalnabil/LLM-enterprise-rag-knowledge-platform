from typing import Protocol

from app.retrieval.schemas import RetrievalResult


class VectorStore(Protocol):
    def search(self, query_embedding: list[float], tenant_id: str, top_k: int) -> list[RetrievalResult]: ...


class BM25Store(Protocol):
    def search(self, query: str, tenant_id: str, top_k: int) -> list[RetrievalResult]: ...


class RetrievalStrategy(Protocol):
    def retrieve(self, query: str, tenant_id: str) -> list[RetrievalResult]: ...
