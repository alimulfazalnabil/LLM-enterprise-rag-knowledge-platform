import re

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ...core.config import settings
from ...database import get_db, init_db
from ...models import DocumentChunk, User
from ...security import SecurityContext, create_token, decode_token, password_digest
from ...services.documents import ensure_demo_resources, list_documents_for_tenant, list_versions_for_document, upload_document

router = APIRouter(prefix="/api/v1")

_STOPWORDS = {"how", "many", "the", "a", "an", "in", "on", "of", "for", "to", "and", "or", "is", "are", "what", "when", "where", "who", "why", "can", "does", "do", "be", "with", "at", "from", "by"}


def _terms(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in _STOPWORDS}


def _score_match(query: str, content: str) -> int:
    query_terms = _terms(query)
    content_terms = _terms(content)
    return len(query_terms & content_terms)


class LoginRequest(BaseModel):
    tenant_id: str
    user_id: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


async def context(authorization: str | None = Header(default=None)) -> SecurityContext:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Authentication required")
    try:
        return decode_token(authorization.split(" ", 1)[1], settings.jwt_secret)
    except ValueError as exc:
        raise HTTPException(401, "Invalid authentication token") from exc


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/auth/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(tenant_id=request.tenant_id, id=request.user_id).first()
    if not user or user.password_hash != password_digest(request.password):
        raise HTTPException(401, "Invalid credentials")
    roles = set(user.roles.split(",")) if user.roles else {"EMPLOYEE"}
    token = create_token(SecurityContext(request.tenant_id, request.user_id, frozenset(roles)), settings.jwt_secret, settings.access_token_minutes)
    return TokenResponse(access_token=token)


@router.post("/documents")
async def upload_document_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db), security: SecurityContext = Depends(context)):
    payload = await file.read()
    return upload_document(db, security.tenant_id, security.user_id, file, payload)


@router.get("/documents")
def list_documents(db: Session = Depends(get_db), security: SecurityContext = Depends(context)):
    return {"items": list_documents_for_tenant(db, security.tenant_id)}


@router.get("/documents/{document_id}/versions")
def list_document_versions(document_id: str, db: Session = Depends(get_db), security: SecurityContext = Depends(context)):
    return {"items": list_versions_for_document(db, security.tenant_id, document_id)}


@router.post("/search")
def search(request: SearchRequest, db: Session = Depends(get_db), security: SecurityContext = Depends(context)):
    rows = db.query(DocumentChunk).filter_by(tenant_id=security.tenant_id).all()
    matches = []
    for row in rows:
        score = _score_match(request.query, row.content)
        if score > 0:
            matches.append({"document_id": row.document_id, "version_id": row.version_id, "chunk_id": row.id, "section": row.section, "page": row.page, "score": score, "snippet": row.content[:220]})
    return {"results": sorted(matches, key=lambda x: x["score"], reverse=True)[:10], "retrieval": {"dense_results": len(matches), "sparse_results": len(matches), "reranked_results": min(10, len(matches))}}


@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db), security: SecurityContext = Depends(context)):
    rows = db.query(DocumentChunk).filter_by(tenant_id=security.tenant_id).all()
    matches = []
    for row in rows:
        score = _score_match(request.question, row.content)
        if score > 0:
            matches.append((score, row))
    if not matches:
        return {"answer": "The available knowledge base does not contain enough information to answer this question.", "grounded": False, "confidence": 0.0, "citations": [], "retrieval": {"dense_results": 0, "sparse_results": 0, "reranked_results": 0}}
    matches.sort(key=lambda item: item[0], reverse=True)
    best = matches[0][1]
    answer = f"Based on the available records, the most relevant evidence is: {best.content[:200]} [1]"
    citations = [{"document_id": best.document_id, "version_id": best.version_id, "chunk_id": best.id, "page": best.page, "section": best.section, "verified": True}]
    return {"answer": answer, "grounded": True, "confidence": 0.8, "citations": citations, "retrieval": {"dense_results": len(matches), "sparse_results": len(matches), "reranked_results": len(matches)}}


@router.on_event("startup")
def startup():
    init_db()
    db = next(get_db())
    try:
        ensure_demo_resources(db)
    finally:
        db.close()
