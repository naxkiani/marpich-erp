"""Documents application service."""
from __future__ import annotations

import hashlib

from contexts.documents.application.commands.bootstrap_root_folder import BootstrapRootFolderCommand
from contexts.documents.application.ports.platform_events import IDocumentsPlatformAdapter
from contexts.documents.domain.aggregates.document import Document, DocumentStatus
from contexts.documents.domain.aggregates.document_version import DocumentVersion
from contexts.documents.domain.aggregates.folder import Folder
from contexts.documents.domain.aggregates.signature_request import SignatureRequest
from contexts.documents.domain.events.integration_events import (
    DocumentArchivedIntegration,
    DocumentSignedIntegration,
    DocumentUploadedIntegration,
    VersionCreatedIntegration,
)
from contexts.documents.domain.ports.repositories import (
    IDocumentRepository,
    IFolderRepository,
    ISignatureRepository,
    IVersionRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


def _checksum(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


class DocumentsApplicationService:
    def __init__(
        self,
        folders: IFolderRepository,
        documents: IDocumentRepository,
        versions: IVersionRepository,
        signatures: ISignatureRepository,
        platform_events: IDocumentsPlatformAdapter,
    ) -> None:
        self._folders = folders
        self._documents = documents
        self._versions = versions
        self._signatures = signatures
        self._platform_events = platform_events

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        command = await self._platform_events.parse_tenant_provisioned(envelope)
        await self.bootstrap_root_folder(command)

    async def bootstrap_root_folder(self, command: BootstrapRootFolderCommand) -> Result[dict]:
        existing = await self._folders.find_root(command.tenant_id)
        if existing:
            return Result.ok(existing.to_dict())

        folder = Folder.create(
            tenant_id=command.tenant_id,
            name=command.name,
            parent_id=None,
            is_root=True,
        )
        await self._folders.save(folder)
        return Result.ok(folder.to_dict())

    async def create_folder(
        self,
        *,
        tenant_id: str,
        parent_id: str | None,
        name: str,
    ) -> Result[dict]:
        parent_uid: UniqueId | None = None
        if parent_id:
            parent = await self._folders.find_by_id(tenant_id, UniqueId.from_string(parent_id))
            if not parent:
                return Result.fail("documents.errors.parent_not_found")
            parent_uid = parent.id
        else:
            root = await self._folders.find_root(tenant_id)
            if not root:
                return Result.fail("documents.errors.root_not_found")
            parent_uid = root.id

        folder = Folder.create(tenant_id=tenant_id, name=name, parent_id=parent_uid)
        await self._folders.save(folder)
        return Result.ok(folder.to_dict())

    async def get_folder_contents(self, tenant_id: str, folder_id: str) -> Result[dict]:
        folder = await self._folders.find_by_id(tenant_id, UniqueId.from_string(folder_id))
        if not folder:
            return Result.fail("documents.errors.folder_not_found")

        subfolders = await self._folders.list_children(tenant_id, folder.id)
        docs = await self._documents.list_by_folder(tenant_id, folder.id)
        return Result.ok(
            {
                "folder": folder.to_dict(),
                "subfolders": [f.to_dict() for f in subfolders],
                "documents": [d.to_dict() for d in docs],
            }
        )

    async def create_document(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        folder_id: str,
        title: str,
        description: str,
        file_name: str,
        content_type: str,
        content: str,
        metadata: dict | None,
        created_by: str | None,
    ) -> Result[dict]:
        folder = await self._folders.find_by_id(tenant_id, UniqueId.from_string(folder_id))
        if not folder:
            return Result.fail("documents.errors.folder_not_found")

        document = Document.create(
            tenant_id=tenant_id,
            folder_id=folder.id,
            title=title,
            description=description,
            metadata=metadata,
            created_by=created_by,
        )
        version = DocumentVersion.create(
            tenant_id=tenant_id,
            document_id=document.id,
            version_number=1,
            file_name=file_name,
            content_type=content_type,
            content=content,
            checksum=_checksum(content),
            created_by=created_by,
        )
        document.set_current_version(version.id)

        await self._documents.save(document)
        await self._versions.save(version)

        await publish_integration_event(
            DocumentUploadedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=document.id,
                version_id=version.id,
                folder_id=folder.id,
                title=document.title,
                file_name=version.file_name,
            )
        )
        await publish_integration_event(
            VersionCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=document.id,
                version_id=version.id,
                version_number=version.version_number,
                file_name=version.file_name,
            )
        )
        return Result.ok(
            {
                "document": document.to_dict(),
                "current_version": version.to_dict(),
            }
        )

    async def add_version(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        document_id: str,
        file_name: str,
        content_type: str,
        content: str,
        created_by: str | None,
    ) -> Result[dict]:
        document = await self._documents.find_by_id(tenant_id, UniqueId.from_string(document_id))
        if not document:
            return Result.fail("documents.errors.document_not_found")
        if document.status == DocumentStatus.ARCHIVED:
            return Result.fail("documents.errors.document_archived")

        version_number = await self._versions.next_version_number(tenant_id, document.id)
        version = DocumentVersion.create(
            tenant_id=tenant_id,
            document_id=document.id,
            version_number=version_number,
            file_name=file_name,
            content_type=content_type,
            content=content,
            checksum=_checksum(content),
            created_by=created_by,
        )
        document.set_current_version(version.id)
        await self._versions.save(version)
        await self._documents.save(document)

        await publish_integration_event(
            VersionCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=document.id,
                version_id=version.id,
                version_number=version.version_number,
                file_name=version.file_name,
            )
        )
        return Result.ok(version.to_dict())

    async def get_document(self, tenant_id: str, document_id: str) -> Result[dict]:
        document = await self._documents.find_by_id(tenant_id, UniqueId.from_string(document_id))
        if not document:
            return Result.fail("documents.errors.document_not_found")

        versions = await self._versions.list_by_document(tenant_id, document.id)
        signatures = await self._signatures.find_by_document(tenant_id, document.id)
        return Result.ok(
            {
                "document": document.to_dict(),
                "versions": [v.to_dict() for v in versions],
                "signatures": [s.to_dict() for s in signatures],
            }
        )

    async def download_current(self, tenant_id: str, document_id: str) -> Result[dict]:
        document = await self._documents.find_by_id(tenant_id, UniqueId.from_string(document_id))
        if not document or not document.current_version_id:
            return Result.fail("documents.errors.document_not_found")

        version = await self._versions.find_by_id(tenant_id, document.current_version_id)
        if not version:
            return Result.fail("documents.errors.version_not_found")

        return Result.ok(
            {
                "file_name": version.file_name,
                "content_type": version.content_type,
                "checksum": version.checksum,
                "content": version.content,
            }
        )

    async def request_signature(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        document_id: str,
        signers: list[str],
        requester_id: str,
    ) -> Result[dict]:
        document = await self._documents.find_by_id(tenant_id, UniqueId.from_string(document_id))
        if not document or not document.current_version_id:
            return Result.fail("documents.errors.document_not_found")
        if document.status == DocumentStatus.ARCHIVED:
            return Result.fail("documents.errors.document_archived")
        if not signers:
            return Result.fail("documents.errors.signers_required")

        request = SignatureRequest.create(
            tenant_id=tenant_id,
            document_id=document.id,
            version_id=document.current_version_id,
            requester_id=requester_id,
            signers=signers,
        )
        request.mark_signed()
        await self._signatures.save(request)

        await publish_integration_event(
            DocumentSignedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=document.id,
                signature_request_id=request.id,
                signers=signers,
            )
        )
        return Result.ok(request.to_dict())

    async def archive_document(
        self, tenant_id: str, correlation_id: str, document_id: str
    ) -> Result[dict]:
        document = await self._documents.find_by_id(tenant_id, UniqueId.from_string(document_id))
        if not document:
            return Result.fail("documents.errors.document_not_found")
        if document.status == DocumentStatus.ARCHIVED:
            return Result.ok(document.to_dict())

        document.archive()
        await self._documents.save(document)

        await publish_integration_event(
            DocumentArchivedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=document.id,
                title=document.title,
            )
        )
        return Result.ok(document.to_dict())

    async def get_root_folder(self, tenant_id: str) -> Result[dict]:
        root = await self._folders.find_root(tenant_id)
        if not root:
            return Result.fail("documents.errors.root_not_found")
        return Result.ok(root.to_dict())
