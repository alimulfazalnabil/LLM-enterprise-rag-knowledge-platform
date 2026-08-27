# Architecture

## 1. System architecture
```mermaid
flowchart LR
  UI[React Frontend] --> API[FastAPI]
  API --> AUTH[Auth/RBAC]
  API --> APP[Application Services]
  APP --> RET[Retrieval]
  APP --> GEN[Generation]
  RET --> PG[(PostgreSQL + pgvector)]
  RET --> BM25[BM25 Index]
  APP --> REDIS[(Redis Queue)]
  APP --> OBJ[(Object Storage)]
```

## 2. Document ingestion
```mermaid
flowchart LR
  U[Upload] --> V[Validation]
  V --> O[Object Storage]
  O --> Q[Redis Queue]
  Q --> W[Worker]
  W --> P[Parser+Chunker]
  P --> E[Embeddings]
  E --> I[Indexing]
```

## 3. RAG pipeline
```mermaid
flowchart LR
  Q[Query] --> D[Dense]
  Q --> S[BM25]
  D --> F[RRF]
  S --> F
  F --> R[Reranker]
  R --> C[Compression]
  C --> L[LLM]
  L --> CV[Citation Verification]
```

## 4. Hybrid retrieval
```mermaid
flowchart TD
  A[Dense top N] --> C[Candidate Pool]
  B[Sparse top N] --> C
  C --> D[RRF]
```

## 5. Tenant isolation
```mermaid
flowchart LR
  CTX[Security Context tenant_id] --> RET[Retrieval Query Filter]
  RET --> RES[Authorized Results Only]
```

## 6. Authentication/RBAC
```mermaid
flowchart LR
  U[User] --> JWT[JWT]
  JWT --> RBAC[Role + Permission Check]
  RBAC --> API[Endpoint Access]
```

## 7. Citation verification
```mermaid
flowchart LR
  A[Answer] --> X[Extract citations]
  X --> M[Map to chunk metadata]
  M --> T[Tenant authorization]
  T --> V[Verification status]
```

## 8. Azure deployment
```mermaid
flowchart LR
  I[Internet] --> F[Front Door/WAF]
  F --> APIM[API Management]
  APIM --> AKS[AKS/ACA]
  AKS --> DB[Azure PostgreSQL]
  AKS --> R[Azure Cache for Redis]
  AKS --> B[Blob Storage]
  AKS --> AOAI[Azure OpenAI]
```

## 9. Kubernetes deployment
```mermaid
flowchart LR
  Ingress --> Service --> Deployment
  Deployment --> ConfigMap
  Deployment --> SecretRef
  Deployment --> HPA
```

## 10. CI/CD
```mermaid
flowchart LR
  PR[Pull Request] --> CI[Lint/Test/Security/Build]
  CI --> CD[Deploy]
  CD --> Verify[Deployment Verification]
```
