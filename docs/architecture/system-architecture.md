# System Architecture

```mermaid
flowchart LR
 Client[React client] --> API[FastAPI gateway]
 API --> Auth[JWT and RBAC]
 API --> Retrieval[Authorized hybrid retrieval]
 API --> Docs[Document API]
 Retrieval --> Dense[Dense adapter]
 Retrieval --> Sparse[BM25 adapter]
 Dense --> Fusion[RRF fusion]
 Sparse --> Fusion
 Fusion --> Rank[Reranker]
 Rank --> Compress[Context compression]
 Compress --> Verify[Citation verification]
 Verify --> LLM[Provider abstraction]
 Docs --> Queue[Redis queue]
 Queue --> Worker[Ingestion worker]
```

The current local profile uses an in-memory store and deterministic retrieval so the demo is runnable without credentials. Production profiles should replace these adapters with PostgreSQL/pgvector, Redis, object storage, and configured model providers.
