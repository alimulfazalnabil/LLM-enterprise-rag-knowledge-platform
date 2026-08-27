from enum import StrEnum
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

class IngestionStatus(StrEnum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

class DocumentResponse(BaseModel):
    id: str
    tenant_id: str
    filename: str
    status: IngestionStatus = Field(default=IngestionStatus.PENDING)

@router.post('')
def upload_document() -> DocumentResponse:
    return DocumentResponse(id='doc_1', tenant_id='tenant_a', filename='sample.pdf')

@router.get('')
def list_documents() -> list[DocumentResponse]:
    return [DocumentResponse(id='doc_1', tenant_id='tenant_a', filename='sample.pdf', status=IngestionStatus.COMPLETED)]

@router.get('/{doc_id}')
def get_document(doc_id: str) -> DocumentResponse:
    return DocumentResponse(id=doc_id, tenant_id='tenant_a', filename='sample.pdf', status=IngestionStatus.COMPLETED)

@router.delete('/{doc_id}')
def delete_document(doc_id: str) -> dict[str, str]:
    return {'deleted_document_id': doc_id}

@router.post('/{doc_id}/versions')
def create_version(doc_id: str) -> dict[str, str]:
    return {'document_id': doc_id, 'version_id': 'v2'}

@router.get('/{doc_id}/versions')
def list_versions(doc_id: str) -> dict[str, list[str]]:
    return {'document_id': doc_id, 'versions': ['v1']}

@router.post('/{doc_id}/reindex')
def reindex(doc_id: str) -> dict[str, str]:
    return {'document_id': doc_id, 'status': 'queued'}
