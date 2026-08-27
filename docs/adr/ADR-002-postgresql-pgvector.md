# ADR-002 PostgreSQL + pgvector

## Context
Need transactional + vector data.
## Decision
Use PostgreSQL + pgvector.
## Alternatives
Dedicated vector DB only.
## Trade-offs
Simple architecture with SQL joins; may need specialized scaling later.
## Consequences
Unified storage for metadata + vectors.