# ADR-003: Hybrid Retrieval

## Context
Vector search misses exact identifiers; lexical search misses paraphrases.

## Decision
Combine dense and BM25 retrieval through Reciprocal Rank Fusion.

## Alternatives
Use one retrieval mode or rely on a hosted search service.

## Trade-offs
Two indexes and more latency are exchanged for broader recall and controllable behavior.

## Consequences
Each path requires authorization filters and independent observability.
