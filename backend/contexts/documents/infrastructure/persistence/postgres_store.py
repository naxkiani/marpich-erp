"""PostgreSQL repositories — Documents bounded context."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select

from contexts.documents.domain.aggregates.document import Document, DocumentStatus
from contexts.documents.domain.aggregates.document_version import DocumentVersion
from contexts.documents.domain.aggregates.folder import Folder
from contexts.documents.domain.aggregates.signature_request import SignatureRequest, SignatureStatus
from contexts.documents.domain.ports.repositories import (
    IDocumentRepository,
    IFolderRepository,
    ISignatureRepository,
    IVersionRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    DocumentRow,
    DocumentVersionRow,
    FolderRow,
    SignatureRequestRow,
)


class PostgresFolderRepository(IFolderRepository):
    async def save(self, folder: Folder) -> None:
        async with session_scope() as session:
            row = await session.get(FolderRow, UUID(str(folder.id)))
            if row is None:
                session.add(
                    FolderRow(
                        id=UUID(str(folder.id)),
                        tenant_id=folder.tenant_id,
                        parent_id=UUID(str(folder.parent_id)) if folder.parent_id else None,
                        name=folder.name,
                        is_root=folder.is_root,
                        created_at=folder.created_at,
                    )
                )
            else:
                row.name = folder.name

    async def find_by_id(self, tenant_id: str, folder_id: UniqueId) -> Folder | None:
        async with session_scope() as session:
            row = await session.get(FolderRow, UUID(str(folder_id)))
            if row and row.tenant_id == tenant_id:
                return _folder_from_row(row)
            return None

    async def find_root(self, tenant_id: str) -> Folder | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(FolderRow).where(FolderRow.tenant_id == tenant_id, FolderRow.is_root.is_(True))
            )
            return _folder_from_row(row) if row else None

    async def list_children(self, tenant_id: str, parent_id: UniqueId | None) -> list[Folder]:
        async with session_scope() as session:
            if parent_id is None:
                stmt = select(FolderRow).where(
                    FolderRow.tenant_id == tenant_id,
                    FolderRow.parent_id.is_(None),
                )
            else:
                stmt = select(FolderRow).where(
                    FolderRow.tenant_id == tenant_id,
                    FolderRow.parent_id == UUID(str(parent_id)),
                )
            rows = (await session.scalars(stmt)).all()
        return [_folder_from_row(r) for r in rows]


class PostgresDocumentRepository(IDocumentRepository):
    async def save(self, document: Document) -> None:
        async with session_scope() as session:
            row = await session.get(DocumentRow, UUID(str(document.id)))
            if row is None:
                session.add(
                    DocumentRow(
                        id=UUID(str(document.id)),
                        tenant_id=document.tenant_id,
                        folder_id=UUID(str(document.folder_id)),
                        title=document.title,
                        description=document.description,
                        current_version_id=(
                            UUID(str(document.current_version_id))
                            if document.current_version_id
                            else None
                        ),
                        status=document.status.value,
                        doc_metadata=document.metadata,
                        created_by=document.created_by,
                        created_at=document.created_at,
                    )
                )
            else:
                row.title = document.title
                row.description = document.description
                row.current_version_id = (
                    UUID(str(document.current_version_id)) if document.current_version_id else None
                )
                row.status = document.status.value
                row.doc_metadata = document.metadata

    async def find_by_id(self, tenant_id: str, document_id: UniqueId) -> Document | None:
        async with session_scope() as session:
            row = await session.get(DocumentRow, UUID(str(document_id)))
            if row and row.tenant_id == tenant_id:
                return _document_from_row(row)
            return None

    async def list_by_folder(self, tenant_id: str, folder_id: UniqueId) -> list[Document]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(DocumentRow).where(
                        DocumentRow.tenant_id == tenant_id,
                        DocumentRow.folder_id == UUID(str(folder_id)),
                    )
                )
            ).all()
        return [_document_from_row(r) for r in rows]


class PostgresVersionRepository(IVersionRepository):
    async def save(self, version: DocumentVersion) -> None:
        async with session_scope() as session:
            row = await session.get(DocumentVersionRow, UUID(str(version.id)))
            if row is None:
                session.add(
                    DocumentVersionRow(
                        id=UUID(str(version.id)),
                        tenant_id=version.tenant_id,
                        document_id=UUID(str(version.document_id)),
                        version_number=version.version_number,
                        file_name=version.file_name,
                        content_type=version.content_type,
                        content=version.content,
                        checksum=version.checksum,
                        storage_key=version.storage_key,
                        created_by=version.created_by,
                        created_at=version.created_at,
                    )
                )

    async def find_by_id(self, tenant_id: str, version_id: UniqueId) -> DocumentVersion | None:
        async with session_scope() as session:
            row = await session.get(DocumentVersionRow, UUID(str(version_id)))
            if row and row.tenant_id == tenant_id:
                return _version_from_row(row)
            return None

    async def list_by_document(self, tenant_id: str, document_id: UniqueId) -> list[DocumentVersion]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(DocumentVersionRow)
                    .where(
                        DocumentVersionRow.tenant_id == tenant_id,
                        DocumentVersionRow.document_id == UUID(str(document_id)),
                    )
                    .order_by(DocumentVersionRow.version_number)
                )
            ).all()
        return [_version_from_row(r) for r in rows]

    async def next_version_number(self, tenant_id: str, document_id: UniqueId) -> int:
        async with session_scope() as session:
            current = await session.scalar(
                select(func.max(DocumentVersionRow.version_number)).where(
                    DocumentVersionRow.tenant_id == tenant_id,
                    DocumentVersionRow.document_id == UUID(str(document_id)),
                )
            )
        return (current or 0) + 1


class PostgresSignatureRepository(ISignatureRepository):
    async def save(self, request: SignatureRequest) -> None:
        async with session_scope() as session:
            row = await session.get(SignatureRequestRow, UUID(str(request.id)))
            if row is None:
                session.add(
                    SignatureRequestRow(
                        id=UUID(str(request.id)),
                        tenant_id=request.tenant_id,
                        document_id=UUID(str(request.document_id)),
                        version_id=UUID(str(request.version_id)),
                        requester_id=request.requester_id,
                        signers=request.signers,
                        status=request.status.value,
                        created_at=request.created_at,
                        completed_at=request.completed_at,
                    )
                )
            else:
                row.status = request.status.value
                row.completed_at = request.completed_at

    async def find_by_document(
        self, tenant_id: str, document_id: UniqueId
    ) -> list[SignatureRequest]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(SignatureRequestRow).where(
                        SignatureRequestRow.tenant_id == tenant_id,
                        SignatureRequestRow.document_id == UUID(str(document_id)),
                    )
                )
            ).all()
        return [_signature_from_row(r) for r in rows]


def _folder_from_row(row: FolderRow) -> Folder:
    return Folder(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        parent_id=UniqueId(str(row.parent_id)) if row.parent_id else None,
        name=row.name,
        is_root=row.is_root,
        created_at=row.created_at,
    )


def _document_from_row(row: DocumentRow) -> Document:
    return Document(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        folder_id=UniqueId(str(row.folder_id)),
        title=row.title,
        description=row.description,
        current_version_id=UniqueId(str(row.current_version_id)) if row.current_version_id else None,
        status=DocumentStatus(row.status),
        metadata=row.doc_metadata,
        created_by=row.created_by,
        created_at=row.created_at,
    )


def _version_from_row(row: DocumentVersionRow) -> DocumentVersion:
    return DocumentVersion(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        document_id=UniqueId(str(row.document_id)),
        version_number=row.version_number,
        file_name=row.file_name,
        content_type=row.content_type,
        content=row.content,
        checksum=row.checksum,
        storage_key=row.storage_key,
        created_by=row.created_by,
        created_at=row.created_at,
    )


def _signature_from_row(row: SignatureRequestRow) -> SignatureRequest:
    return SignatureRequest(
        id=UniqueId(str(row.id)),
        tenant_id=row.tenant_id,
        document_id=UniqueId(str(row.document_id)),
        version_id=UniqueId(str(row.version_id)),
        requester_id=row.requester_id,
        signers=row.signers,
        status=SignatureStatus(row.status),
        created_at=row.created_at,
        completed_at=row.completed_at,
    )
