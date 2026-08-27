# ADR-005 Cross-Encoder Reranking

## Context
Need better top-k relevance.
## Decision
Use cross-encoder reranker stage.
## Alternatives
No reranking.
## Trade-offs
Higher latency for better relevance.
## Consequences
Batching and timeout controls required.