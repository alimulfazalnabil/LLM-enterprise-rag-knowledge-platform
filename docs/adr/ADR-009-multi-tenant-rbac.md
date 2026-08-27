# ADR-009 Multi-Tenant RBAC

## Context
Strict tenant isolation and least privilege needed.
## Decision
Centralized RBAC + tenant-aware filtering at retrieval boundaries.
## Alternatives
UI-only filtering.
## Trade-offs
More backend checks; strong data isolation.
## Consequences
All domain objects carry tenant_id.