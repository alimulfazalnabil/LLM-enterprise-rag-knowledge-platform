from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.auth.deps import require_documents_delete, require_documents_read, require_documents_write
from app.documents.repository import (
    IngestionStatus,
    create_document_for_tenant,
    delete_document_for_tenant,
    get_document_for_tenant,
    list_documents_for_tenant,
)
from app.security.rbac import SecurityContext

router = APIRouter()

class DocumentResponse(BaseModel):
    id: str
    tenant_id: str
    filename: str
    status: IngestionStatus = IngestionStatus.PENDING


class UploadRequest(BaseModel):
    filename: str

@router.post('')
def upload_document(
    payload: UploadRequest,
    context: SecurityContext = Depends(require_documents_write),
) -> DocumentResponse:
    created = create_document_for_tenant(context.tenant_id, payload.filename)
    return DocumentResponse(**created.__dict__)

@router.get('')
def list_documents(
    context: SecurityContext = Depends(require_documents_read),
) -> list[DocumentResponse]:
    return [DocumentResponse(**r.__dict__) for r in list_documents_for_tenant(context.tenant_id)]

@router.get('/{doc_id}')
def get_document(
    doc_id: str,
    context: SecurityContext = Depends(require_documents_read),
) -> DocumentResponse:
    doc = get_document_for_tenant(doc_id, context.tenant_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Document not found')
    return DocumentResponse(**doc.__dict__)

@router.delete('/{doc_id}')
def delete_document(
    doc_id: str,
    context: SecurityContext = Depends(require_documents_delete),
) -> dict[str, str]:
    if not delete_document_for_tenant(doc_id, context.tenant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Document not found')
    return {'deleted_document_id': doc_id}

@router.post('/{doc_id}/versions')
def create_version(
    doc_id: str,
    context: SecurityContext = Depends(require_documents_write),
) -> dict[str, str]:
    if not get_document_for_tenant(doc_id, context.tenant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Document not found')
    return {'document_id': doc_id, 'version_id': 'v2'}

@router.get('/{doc_id}/versions')
def list_versions(
    doc_id: str,
    context: SecurityContext = Depends(require_documents_read),
) -> dict[str, list[str]]:
    if not get_document_for_tenant(doc_id, context.tenant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Document not found')
    return {'document_id': doc_id, 'versions': ['v1']}

@router.post('/{doc_id}/reindex')
def reindex(
    doc_id: str,
    context: SecurityContext = Depends(require_documents_write),
) -> dict[str, str]:
    if not get_document_for_tenant(doc_id, context.tenant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Document not found')
    return {'document_id': doc_id, 'status': 'queued'}
