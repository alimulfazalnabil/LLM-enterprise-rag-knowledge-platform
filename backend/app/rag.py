from dataclasses import dataclass
import re
from .retrieval import RankedChunk


@dataclass(frozen=True)
class Citation:
    document_id: str
    version_id: str
    chunk_id: str
    section: str
    page: int | None
    verified: bool


def compress_context(results: list[RankedChunk], max_sentences: int = 2) -> list[RankedChunk]:
    compressed = []
    for result in results:
        sentences = re.split(r"(?<=[.!?])\s+", result.chunk.content.strip())
        content = " ".join(sentences[:max_sentences])
        chunk = result.chunk.__class__(**{**result.chunk.__dict__, "content": content})
        compressed.append(RankedChunk(chunk, result.score, result.source))
    return compressed


def verify_citations(results: list[RankedChunk], tenant_id: str) -> list[Citation]:
    return [Citation(r.chunk.document_id, r.chunk.version_id, r.chunk.chunk_id, r.chunk.section, r.chunk.page, r.chunk.tenant_id == tenant_id) for r in results if r.chunk.tenant_id == tenant_id]


def grounded_answer(question: str, results: list[RankedChunk], citations: list[Citation]) -> tuple[str, bool]:
    if not results or not citations:
        return "The available knowledge base does not contain enough information to answer this question.", False
    evidence = " ".join(result.chunk.content for result in results)
    answer = f"Based on the available knowledge base: {evidence} [1]"
    return answer, True
