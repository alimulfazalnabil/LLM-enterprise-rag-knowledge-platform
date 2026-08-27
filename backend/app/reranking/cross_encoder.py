from __future__ import annotations

from typing import Any


class CrossEncoderReranker:
    async def rerank(self, query: str, candidates: list[dict[str, Any]], top_k: int = 8) -> list[dict[str, Any]]:
        scored = sorted(candidates, key=lambda c: c.get('score', c.get('rrf_score', 0.0)), reverse=True)
        return scored[:top_k]
