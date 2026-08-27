from __future__ import annotations

from typing import Protocol, Any


class VectorStore(Protocol):
    async def similarity_search(self, tenant_id: str, embedding: list[float], top_k: int) -> list[dict[str, Any]]: ...
