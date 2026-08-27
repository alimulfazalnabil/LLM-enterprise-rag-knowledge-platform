import hashlib
import os
import re
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..models import Document, DocumentChunk, DocumentVersion, Tenant, User
from ..security import password_digest


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _chunk_text(text: str, max_chars: int = 1200) -> list[str]:
    cleaned = text.strip()
    if not cleaned:
        return []
    if len(cleaned) <= max_chars:
        return [cleaned]

    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", cleaned) if part.strip()]
    if not sentences:
        return [cleaned[:max_chars].strip()]

    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        candidate = f"{current} {sentence}".strip() if current else sentence
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            chunks.append(current)
        current = sentence
    if current:
        chunks.append(current)

    if not chunks:
        return [cleaned[:max_chars].strip()]
    return chunks


def ensure_demo_resources(db: Session) -> None:
    tenant = db.query(Tenant).filter_by(id="demo").first()
    if tenant is None:
        tenant = Tenant(id="demo", name="Demo Tenant")
        db.add(tenant)

    user = db.query(User).filter_by(id="alice", tenant_id="demo").first()
    if user is None:
        db.add(User(id="alice", tenant_id="demo", email="alice@demo.local", password_hash=password_digest("demo-password"), roles="EMPLOYEE"))
    else:
        if user.password_hash != password_digest("demo-password") or user.roles != "EMPLOYEE":
            user.password_hash = password_digest("demo-password")
            user.roles = "EMPLOYEE"

    if db.query(DocumentChunk).filter_by(tenant_id="demo").count() == 0:
        document_one = Document(
            id="doc-remote-work",
            tenant_id="demo",
            filename="remote-work-policy.txt",
            mime_type="text/plain",
            storage_uri="/tmp/demo/doc-remote-work.txt",
            status="COMPLETED",
            checksum="demo-remote-work",
        )
        document_two = Document(
            id="doc-security-retention",
            tenant_id="demo",
            filename="security-retention.txt",
            mime_type="text/plain",
            storage_uri="/tmp/demo/doc-security-retention.txt",
            status="COMPLETED",
            checksum="demo-security-retention",
        )
        db.add_all([document_one, document_two])
        db.flush()

        version_one = DocumentVersion(id="ver-remote-work", document_id="doc-remote-work", tenant_id="demo", version_number=1, filename="remote-work-policy.txt", checksum="demo-remote-work", mime_type="text/plain", status="COMPLETED")
        version_two = DocumentVersion(id="ver-security-retention", document_id="doc-security-retention", tenant_id="demo", version_number=1, filename="security-retention.txt", checksum="demo-security-retention", mime_type="text/plain", status="COMPLETED")
        db.add_all([version_one, version_two])
        db.flush()

        db.add_all([
            DocumentChunk(id="chunk-remote-work", tenant_id="demo", document_id="doc-remote-work", version_id="ver-remote-work", section="Remote Work Policy", subsection="", page=4, content="Employees may work remotely up to three days each week with manager approval.", token_count=18),
            DocumentChunk(id="chunk-security-retention", tenant_id="demo", document_id="doc-security-retention", version_id="ver-security-retention", section="Logging and Retention", subsection="", page=12, content="Security logs must be retained for seven years and access is audited quarterly.", token_count=21),
            DocumentChunk(id="chunk-secret-other", tenant_id="other", document_id="doc-secret", version_id="ver-secret", section="Confidential", subsection="", page=1, content="Tenant-specific confidential information.", token_count=4),
        ])

    db.commit()


def upload_document(db: Session, tenant_id: str, user_id: str, file: UploadFile, content: bytes) -> dict:
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(413, "File exceeds configured upload limit")

    filename = file.filename or "document.txt"
    checksum = _sha256(content)
    existing_document = db.query(Document).filter_by(tenant_id=tenant_id, filename=filename).order_by(Document.created_at.desc()).first()

    if existing_document is not None:
        document = existing_document
        version_number = db.query(DocumentVersion).filter_by(document_id=document.id).count() + 1
    else:
        document = Document(
            id=str(uuid4()),
            tenant_id=tenant_id,
            filename=filename,
            mime_type=file.content_type or "application/octet-stream",
            storage_uri="",
            status="COMPLETED",
            checksum=checksum,
        )
        db.add(document)
        db.flush()
        version_number = 1

    document_id = document.id
    version_id = str(uuid4())
    storage_uri = f"/tmp/{tenant_id}/{document_id}/{version_id}.bin"
    os.makedirs(os.path.dirname(storage_uri), exist_ok=True)
    with open(storage_uri, "wb") as handle:
        handle.write(content)

    document.storage_uri = storage_uri
    document.mime_type = file.content_type or "application/octet-stream"
    document.checksum = checksum
    document.status = "COMPLETED"

    version = DocumentVersion(
        id=version_id,
        document_id=document_id,
        tenant_id=tenant_id,
        version_number=version_number,
        filename=filename,
        checksum=checksum,
        mime_type=file.content_type or "application/octet-stream",
        status="COMPLETED",
    )
    db.add(version)
    db.flush()

    text = content.decode("utf-8", errors="replace")
    chunk_texts = _chunk_text(text)
    for index, chunk_text in enumerate(chunk_texts, start=1):
        chunk = DocumentChunk(
            id=str(uuid4()),
            tenant_id=tenant_id,
            document_id=document_id,
            version_id=version_id,
            section="Uploaded Document",
            subsection=f"Part {index}" if len(chunk_texts) > 1 else "",
            page=1,
            content=chunk_text,
            token_count=max(1, len(chunk_text.split())),
        )
        db.add(chunk)
    db.commit()

    return {"document_id": document_id, "version_id": version_id, "status": "COMPLETED"}


def list_documents_for_tenant(db: Session, tenant_id: str) -> list[dict]:
    rows = db.query(Document).filter_by(tenant_id=tenant_id).all()
    return [{"document_id": row.id, "filename": row.filename, "status": row.status} for row in rows]


def list_versions_for_document(db: Session, tenant_id: str, document_id: str) -> list[dict]:
    rows = db.query(DocumentVersion).filter_by(tenant_id=tenant_id, document_id=document_id).order_by(DocumentVersion.version_number.asc()).all()
    return [{"version_id": row.id, "version_number": row.version_number, "status": row.status, "checksum": row.checksum} for row in rows]
