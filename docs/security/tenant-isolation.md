# Tenant Isolation

Tenant identity is carried in the signed security context. Every retrieval path scopes chunks by `tenant_id` before scoring, fusion, reranking, compression, citation verification, or response serialization. API document listing applies the same scope. PostgreSQL Row-Level Security should be enabled in the production profile as a second database boundary.

The security test suite includes a cross-tenant retrieval check using an exact query against a hidden tenant's content.
