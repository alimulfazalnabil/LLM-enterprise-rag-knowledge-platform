from dataclasses import dataclass
import math
import re
from collections import Counter


@dataclass(frozen=True)
class Chunk:
    tenant_id: str
    document_id: str
    version_id: str
    chunk_id: str
    content: str
    section: str = ""
    page: int | None = None


@dataclass(frozen=True)
class RankedChunk:
    chunk: Chunk
    score: float
    source: str


def _terms(text: str) -> list[str]:
    return re.findall(r"[a-z0-9][a-z0-9_-]+", text.lower())


def lexical_search(query: str, chunks: list[Chunk], tenant_id: str, top_k: int) -> list[RankedChunk]:
    # Tenant filtering is deliberately the first operation in every retrieval path.
    scoped = [item for item in chunks if item.tenant_id == tenant_id]
    query_terms = Counter(_terms(query))
    scored: list[RankedChunk] = []
    for chunk in scoped:
        terms = Counter(_terms(chunk.content))
        score = sum((1 + math.log(terms[t])) * weight for t, weight in query_terms.items() if terms[t])
        if score:
            scored.append(RankedChunk(chunk, score, "bm25"))
    return sorted(scored, key=lambda result: result.score, reverse=True)[:top_k]


def dense_search(query: str, chunks: list[Chunk], tenant_id: str, top_k: int) -> list[RankedChunk]:
    scoped = [item for item in chunks if item.tenant_id == tenant_id]
    query_terms = set(_terms(query))
    scored = []
    for chunk in scoped:
        terms = set(_terms(chunk.content))
        score = len(query_terms & terms) / max(1, len(query_terms | terms))
        if score:
            scored.append(RankedChunk(chunk, score, "dense"))
    return sorted(scored, key=lambda result: result.score, reverse=True)[:top_k]


def reciprocal_rank_fusion(*result_sets: list[RankedChunk], top_k: int = 20, k: int = 60) -> list[RankedChunk]:
    scores: dict[str, float] = {}
    entries: dict[str, RankedChunk] = {}
    for result_set in result_sets:
        for rank, result in enumerate(result_set, start=1):
            key = result.chunk.chunk_id
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            entries[key] = result
    return [RankedChunk(entries[key].chunk, score, "rrf") for key, score in sorted(scores.items(), key=lambda pair: pair[1], reverse=True)[:top_k]]


def rerank(query: str, candidates: list[RankedChunk], top_k: int) -> list[RankedChunk]:
    query_terms = set(_terms(query))
    scored = [(len(query_terms & set(_terms(result.chunk.content))), result) for result in candidates]
    return [RankedChunk(result.chunk, float(score), "cross-encoder") for score, result in sorted(scored, key=lambda pair: pair[0], reverse=True)[:top_k]]
