# ADR-007 Redis Async Ingestion

## Context
Uploads should not block API.
## Decision
Queue ingestion jobs via Redis-backed workers.
## Alternatives
Synchronous ingestion.
## Trade-offs
Operational complexity for better responsiveness.
## Consequences
Need retries, idempotency, and dead-letter handling.