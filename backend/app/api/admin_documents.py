# =============================================================================
# forge / app / api / admin_documents
# =============================================================================
# Description : Admin document upload, list, delete, and reindex routes.
# Layer       : API
# Feature     : F007 — Basic RAG Foundation
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status

from app.core.auth import require_admin
from app.core.exceptions import NotFoundError
from app.models.admin import AdminUser
from app.models.document import DocumentRecord
from app.services.rag_service import RAGService

router = APIRouter(prefix="/api/admin/documents", tags=["admin-documents"])

AdminUserDep = Annotated[AdminUser, Depends(require_admin)]
UploadFileDep = Annotated[UploadFile, File(...)]

_rag: RAGService | None = None


def _get_rag() -> RAGService:
    global _rag  # noqa: PLW0603
    if _rag is None:
        _rag = RAGService()
    return _rag


@router.get("", response_model=list[DocumentRecord])
async def list_documents(_admin: AdminUserDep) -> list[DocumentRecord]:
    """List uploaded knowledge documents."""
    _ = _admin
    return _get_rag().list_documents()


@router.post("", response_model=DocumentRecord, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFileDep,
    _admin: AdminUserDep,
) -> DocumentRecord:
    """Upload and ingest a document for RAG."""
    _ = _admin
    raw = await file.read()
    mime_type = file.content_type or "text/plain"
    filename = file.filename or "upload.txt"
    return await _get_rag().ingest_document(filename, mime_type, raw)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: UUID,
    _admin: AdminUserDep,
) -> None:
    """Delete a document and its chunks."""
    _ = _admin
    try:
        _get_rag().delete_document(document_id)
    except NotFoundError:
        raise


@router.post("/{document_id}/reindex", response_model=DocumentRecord)
async def reindex_document(
    document_id: UUID,
    file: UploadFileDep,
    _admin: AdminUserDep,
) -> DocumentRecord:
    """Replace document content and re-embed chunks."""
    _ = _admin
    _get_rag().delete_document(document_id)
    raw = await file.read()
    mime_type = file.content_type or "text/plain"
    filename = file.filename or "upload.txt"
    return await _get_rag().ingest_document(filename, mime_type, raw)
