# ADR-010 Citation Verification

## Context
LLM citations can be incorrect or unauthorized.
## Decision
Verify citation existence, authorization, and mapping post-generation.
## Alternatives
Trust model citations directly.
## Trade-offs
Extra latency for trustworthiness.
## Consequences
Citation verification status returned in responses.