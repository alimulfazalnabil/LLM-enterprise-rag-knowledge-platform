# ADR-004 Reciprocal Rank Fusion

## Context
Need robust rank fusion.
## Decision
Use RRF for dense+sparse candidate combination.
## Alternatives
Weighted sum on normalized scores.
## Trade-offs
Simple, stable, model-agnostic; less interpretable raw score semantics.
## Consequences
Tune rrf_k and candidate depth.