from __future__ import annotations

from typing import Protocol, Any


class BM25Index(Protocol):
    async def search(self, tenant_id: str, query: str, top_k: int) -> list[dict[str, Any]]: ...
