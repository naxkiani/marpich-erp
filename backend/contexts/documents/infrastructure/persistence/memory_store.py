"""In-memory documents repositories."""
from __future__ import annotations

from contexts.documents.domain.aggregates.document import Document
from contexts.documents.domain.aggregates.document_version import DocumentVersion
from contexts.documents.domain.aggregates.folder import Folder
from contexts.documents.domain.aggregates.signature_request import SignatureRequest
from contexts.documents.domain.ports.repositories import (
    IDocumentRepository,
    IFolderRepository,
    ISignatureRepository,
    IVersionRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class DocumentsMemoryStore:
    folders: dict[str, Folder] = {}
    documents: dict[str, Document] = {}
    versions: dict[str, DocumentVersion] = {}
    signatures: dict[str, SignatureRequest] = {}

    @classmethod
    def reset(cls) -> None:
        cls.folders.clear()
        cls.documents.clear()
        cls.versions.clear()
        cls.signatures.clear()


class InMemoryFolderRepository(IFolderRepository):
    async def save(self, folder: Folder) -> None:
        DocumentsMemoryStore.folders[str(folder.id)] = folder

    async def find_by_id(self, tenant_id: str, folder_id: UniqueId) -> Folder | None:
        folder = DocumentsMemoryStore.folders.get(str(folder_id))
        return folder if folder and folder.tenant_id == tenant_id else None

    async def find_root(self, tenant_id: str) -> Folder | None:
        for folder in DocumentsMemoryStore.folders.values():
            if folder.tenant_id == tenant_id and folder.is_root:
                return folder
        return None

    async def list_children(self, tenant_id: str, parent_id: UniqueId | None) -> list[Folder]:
        return [
            f
            for f in DocumentsMemoryStore.folders.values()
            if f.tenant_id == tenant_id and f.parent_id == parent_id
        ]


class InMemoryDocumentRepository(IDocumentRepository):
    async def save(self, document: Document) -> None:
        DocumentsMemoryStore.documents[str(document.id)] = document

    async def find_by_id(self, tenant_id: str, document_id: UniqueId) -> Document | None:
        doc = DocumentsMemoryStore.documents.get(str(document_id))
        return doc if doc and doc.tenant_id == tenant_id else None

    async def list_by_folder(self, tenant_id: str, folder_id: UniqueId) -> list[Document]:
        return [
            d
            for d in DocumentsMemoryStore.documents.values()
            if d.tenant_id == tenant_id and str(d.folder_id) == str(folder_id)
        ]


class InMemoryVersionRepository(IVersionRepository):
    async def save(self, version: DocumentVersion) -> None:
        DocumentsMemoryStore.versions[str(version.id)] = version

    async def find_by_id(self, tenant_id: str, version_id: UniqueId) -> DocumentVersion | None:
        version = DocumentsMemoryStore.versions.get(str(version_id))
        return version if version and version.tenant_id == tenant_id else None

    async def list_by_document(self, tenant_id: str, document_id: UniqueId) -> list[DocumentVersion]:
        versions = [
            v
            for v in DocumentsMemoryStore.versions.values()
            if v.tenant_id == tenant_id and str(v.document_id) == str(document_id)
        ]
        return sorted(versions, key=lambda v: v.version_number)

    async def next_version_number(self, tenant_id: str, document_id: UniqueId) -> int:
        versions = await self.list_by_document(tenant_id, document_id)
        return (versions[-1].version_number + 1) if versions else 1


class InMemorySignatureRepository(ISignatureRepository):
    async def save(self, request: SignatureRequest) -> None:
        DocumentsMemoryStore.signatures[str(request.id)] = request

    async def find_by_document(
        self, tenant_id: str, document_id: UniqueId
    ) -> list[SignatureRequest]:
        return [
            s
            for s in DocumentsMemoryStore.signatures.values()
            if s.tenant_id == tenant_id and str(s.document_id) == str(document_id)
        ]
