# ADR-003 Hybrid Retrieval

## Context
Vector-only misses exact tokens.
## Decision
Combine dense + BM25.
## Alternatives
Dense only or sparse only.
## Trade-offs
Higher complexity; better recall/precision balance.
## Consequences
RRF fusion and reranking become required.