"""Documents repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.documents.domain.aggregates.document import Document
from contexts.documents.domain.aggregates.document_version import DocumentVersion
from contexts.documents.domain.aggregates.folder import Folder
from contexts.documents.domain.aggregates.signature_request import SignatureRequest
from shared.domain.value_objects.unique_id import UniqueId


class IFolderRepository(ABC):
    @abstractmethod
    async def save(self, folder: Folder) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, folder_id: UniqueId) -> Folder | None: ...

    @abstractmethod
    async def find_root(self, tenant_id: str) -> Folder | None: ...

    @abstractmethod
    async def list_children(self, tenant_id: str, parent_id: UniqueId | None) -> list[Folder]: ...


class IDocumentRepository(ABC):
    @abstractmethod
    async def save(self, document: Document) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, document_id: UniqueId) -> Document | None: ...

    @abstractmethod
    async def list_by_folder(self, tenant_id: str, folder_id: UniqueId) -> list[Document]: ...


class IVersionRepository(ABC):
    @abstractmethod
    async def save(self, version: DocumentVersion) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, version_id: UniqueId) -> DocumentVersion | None: ...

    @abstractmethod
    async def list_by_document(self, tenant_id: str, document_id: UniqueId) -> list[DocumentVersion]: ...

    @abstractmethod
    async def next_version_number(self, tenant_id: str, document_id: UniqueId) -> int: ...


class ISignatureRepository(ABC):
    @abstractmethod
    async def save(self, request: SignatureRequest) -> None: ...

    @abstractmethod
    async def find_by_document(
        self, tenant_id: str, document_id: UniqueId
    ) -> list[SignatureRequest]: ...
