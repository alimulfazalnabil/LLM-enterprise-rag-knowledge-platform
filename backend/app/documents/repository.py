from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class IngestionStatus(StrEnum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


@dataclass
class DocumentRecord:
    id: str
    tenant_id: str
    filename: str
    status: IngestionStatus


_DOCUMENTS: list[DocumentRecord] = [
    DocumentRecord(id='doc_a_1', tenant_id='tenant_a', filename='handbook_a.pdf', status=IngestionStatus.COMPLETED),
    DocumentRecord(id='doc_b_1', tenant_id='tenant_b', filename='handbook_b.pdf', status=IngestionStatus.COMPLETED),
]


def list_documents_for_tenant(tenant_id: str) -> list[DocumentRecord]:
    return [d for d in _DOCUMENTS if d.tenant_id == tenant_id]


def get_document_for_tenant(doc_id: str, tenant_id: str) -> DocumentRecord | None:
    for doc in _DOCUMENTS:
        if doc.id == doc_id and doc.tenant_id == tenant_id:
            return doc
    return None


def create_document_for_tenant(tenant_id: str, filename: str) -> DocumentRecord:
    next_id = f'doc_{tenant_id}_{len(_DOCUMENTS)+1}'
    record = DocumentRecord(id=next_id, tenant_id=tenant_id, filename=filename, status=IngestionStatus.PENDING)
    _DOCUMENTS.append(record)
    return record


def delete_document_for_tenant(doc_id: str, tenant_id: str) -> bool:
    for i, doc in enumerate(_DOCUMENTS):
        if doc.id == doc_id and doc.tenant_id == tenant_id:
            _DOCUMENTS.pop(i)
            return True
    return False
