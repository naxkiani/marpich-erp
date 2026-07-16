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
    PhysicalLocationAssignedIntegration,
    VersionCreatedIntegration,
)
from contexts.documents.domain.ports.content_signer import IDocumentContentSigner
from contexts.documents.domain.ports.repositories import (
    IDocumentRepository,
    IFolderRepository,
    ISignatureRepository,
    IVersionRepository,
)
from contexts.documents.domain.services.document_verification_engine import (
    build_watermark,
    generate_qr_token,
    verify_qr_token,
)
from contexts.documents.domain.value_objects.physical_location import PhysicalLocation
from shared.application.ports.authorization import IAuthorizationEvaluator
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
        content_signer: IDocumentContentSigner,
        authz: IAuthorizationEvaluator | None = None,
    ) -> None:
        self._folders = folders
        self._documents = documents
        self._versions = versions
        self._signatures = signatures
        self._platform_events = platform_events
        self._content_signer = content_signer
        self._authz = authz

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
        document.set_qr_token(
            generate_qr_token(
                tenant_id=tenant_id,
                document_id=str(document.id),
                version_number=version.version_number,
                checksum=version.checksum,
            )
        )

        await self._documents.save(document)
        await self._versions.save(version)

        if self._authz and created_by:
            await self._authz.write_relation(
                tenant_id,
                subject_type="user",
                subject_id=created_by,
                relation="owner",
                object_type="document",
                object_id=str(document.id),
            )

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
        document.set_qr_token(
            generate_qr_token(
                tenant_id=tenant_id,
                document_id=str(document.id),
                version_number=version.version_number,
                checksum=version.checksum,
            )
        )
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
        token = document.qr_token or document.metadata.get("qr_token")
        return Result.ok(
            {
                "document": document.to_dict(),
                "versions": [v.to_dict() for v in versions],
                "signatures": [s.to_dict() for s in signatures],
                "verify_path": f"/api/v1/documents/verify/{token}" if token else None,
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
                "qr_token": document.qr_token or document.metadata.get("qr_token"),
            }
        )

    async def preview_document(
        self,
        *,
        tenant_id: str,
        document_id: str,
        principal_id: str,
        sensitivity: str = "high",
    ) -> Result[dict]:
        """Serve-time preview — watermark via AuthZ obligation; never mutates stored bytes."""
        download = await self.download_current(tenant_id, document_id)
        if not download.succeeded:
            return download
        payload = download.unwrap()
        watermark = None
        obligations: list[str] = []
        if self._authz:
            decision = await self._authz.check_access(
                tenant_id,
                principal_id=principal_id,
                resource=f"marpich://documents/file/{document_id}",
                action="export",
                permission_code="documents.read",
                context={"export": True, "sensitivity": sensitivity},
            )
            if not decision.allowed:
                return Result.fail("documents.errors.forbidden")
            obligations = list(decision.obligations)
            if "data.watermark" in obligations:
                watermark = build_watermark(
                    tenant_id=tenant_id,
                    actor_id=principal_id,
                    document_id=document_id,
                )
        else:
            # Fail-safe for demos without AuthZ wiring: apply watermark on high sensitivity
            if sensitivity in {"high", "critical"}:
                watermark = build_watermark(
                    tenant_id=tenant_id,
                    actor_id=principal_id,
                    document_id=document_id,
                )
                obligations = ["data.watermark"]
        return Result.ok(
            {
                **payload,
                "watermark": watermark,
                "obligations": obligations,
                "stored_mutated": False,
            }
        )

    async def verify_public_token(self, token: str) -> Result[dict]:
        parsed = verify_qr_token(token)
        if not parsed:
            return Result.fail("documents.errors.invalid_qr_token")

        document = await self._documents.find_by_qr_token(token)
        if not document:
            # Token HMAC valid but document missing / rotated — still report integrity failure
            return Result.fail("documents.errors.document_not_found")

        version = None
        if document.current_version_id:
            version = await self._versions.find_by_id(document.tenant_id, document.current_version_id)
        if not version:
            return Result.fail("documents.errors.version_not_found")

        checksum_ok = (
            version.checksum == parsed["checksum"]
            and version.version_number == parsed["version_number"]
            and str(document.id) == parsed["document_id"]
            and document.tenant_id == parsed["tenant_id"]
        )
        signatures = await self._signatures.find_by_document(document.tenant_id, document.id)
        latest_sig = signatures[-1].to_dict() if signatures else None
        crypto_ok = True
        if latest_sig and latest_sig.get("signature_hash"):
            crypto_ok = self._content_signer.verify(
                document_id=str(document.id),
                version_checksum=latest_sig.get("content_checksum") or version.checksum,
                signer_id=latest_sig.get("requester_id") or "",
                signature=latest_sig["signature_hash"],
                algorithm=latest_sig.get("algorithm"),
                key_id=latest_sig.get("key_id")
                or (document.metadata.get("last_signature") or {}).get("key_id"),
            )
        return Result.ok(
            {
                "valid": bool(checksum_ok and crypto_ok),
                "tenant_id": document.tenant_id,
                "document_id": str(document.id),
                "title": document.title,
                "status": document.status.value,
                "version_number": version.version_number,
                "checksum": version.checksum,
                "checksum_matches": bool(checksum_ok),
                "signature_valid": bool(crypto_ok) if latest_sig else None,
                "signature": latest_sig,
                "qr_token": token,
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

        version = await self._versions.find_by_id(tenant_id, document.current_version_id)
        if not version:
            return Result.fail("documents.errors.version_not_found")

        evidence = self._content_signer.sign(
            document_id=str(document.id),
            version_checksum=version.checksum,
            signer_id=requester_id,
        )
        request = SignatureRequest.create(
            tenant_id=tenant_id,
            document_id=document.id,
            version_id=document.current_version_id,
            requester_id=requester_id,
            signers=signers,
        )
        request.mark_signed(
            algorithm=evidence["algorithm"],
            signature_hash=evidence["signature"],
            content_checksum=version.checksum,
            key_id=evidence.get("key_id"),
        )
        document.set_qr_token(
            generate_qr_token(
                tenant_id=tenant_id,
                document_id=str(document.id),
                version_number=version.version_number,
                checksum=version.checksum,
            )
        )
        document.metadata = {
            **document.metadata,
            "last_signature": evidence,
        }
        await self._signatures.save(request)
        await self._documents.save(document)

        await publish_integration_event(
            DocumentSignedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=document.id,
                signature_request_id=request.id,
                signers=signers,
                algorithm=evidence["algorithm"],
                key_id=evidence.get("key_id"),
                content_checksum=version.checksum,
            )
        )
        return Result.ok({**request.to_dict(), "qr_token": document.qr_token, "evidence": evidence})

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

    async def delete_document(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        document_id: str,
        principal_id: str,
        context: dict | None = None,
    ) -> Result[dict]:
        """Owner-only delete (ReBAC) via AuthZ PEP — soft-deletes via archive."""
        if self._authz:
            ctx = {
                "object_type": "document",
                "object_id": document_id,
                "relation": "owner",
                "mutating": True,
                **(context or {}),
            }
            decision = await self._authz.check_access(
                tenant_id,
                principal_id=principal_id,
                resource=f"marpich://documents/file/{document_id}",
                action="delete",
                permission_code="documents.file.delete",
                context=ctx,
            )
            if not decision.allowed:
                return Result.fail("documents.errors.forbidden")
        return await self.archive_document(tenant_id, correlation_id, document_id)

    async def assign_physical_location(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        document_id: str,
        site_code: str,
        room: str = "",
        cabinet: str = "",
        shelf: str = "",
        box: str = "",
        file_ref: str = "",
    ) -> Result[dict]:
        document = await self._documents.find_by_id(tenant_id, UniqueId.from_string(document_id))
        if not document:
            return Result.fail("documents.errors.document_not_found")
        try:
            location = PhysicalLocation(
                site_code=site_code,
                room=room,
                cabinet=cabinet,
                shelf=shelf,
                box=box,
                file_ref=file_ref,
            )
            document.assign_physical_location(location)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._documents.save(document)
        await publish_integration_event(
            PhysicalLocationAssignedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=document.id,
                site_code=location.site_code,
                room=location.room,
                cabinet=location.cabinet,
                shelf=location.shelf,
                box=location.box,
                file_ref=location.file_ref,
            )
        )
        return Result.ok(document.to_dict())

    async def get_physical_location(self, tenant_id: str, document_id: str) -> Result[dict]:
        document = await self._documents.find_by_id(tenant_id, UniqueId.from_string(document_id))
        if not document:
            return Result.fail("documents.errors.document_not_found")
        location = document.physical_location()
        return Result.ok(
            {
                "document_id": str(document.id),
                "physical_location": location.to_dict() if location else None,
            }
        )

    async def get_root_folder(self, tenant_id: str) -> Result[dict]:
        root = await self._folders.find_root(tenant_id)
        if not root:
            return Result.fail("documents.errors.root_not_found")
        return Result.ok(root.to_dict())
