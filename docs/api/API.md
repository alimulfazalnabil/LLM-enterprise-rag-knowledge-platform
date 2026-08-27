# API

FastAPI's interactive contract is available at `/docs` when the API is running.

## Authentication
`POST /api/v1/auth/login` accepts `{tenant_id, user_id, password}` and returns a bearer token. The local demo user is `demo/alice` with password `demo-password`.

## Search
`POST /api/v1/search` with `{query}` returns tenant-scoped hybrid retrieval results and retrieval counts.

## Chat
`POST /api/v1/chat` with `{question}` returns a grounded answer, verified citations, confidence semantics, and retrieval counts.

## Documents
`GET /api/v1/documents` lists only documents visible in the authenticated tenant. `POST /api/v1/documents` accepts a multipart upload and creates a versioned local chunk.
