"""Documents integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class DocumentUploadedIntegration(IntegrationEvent):
    document_id: UniqueId
    version_id: UniqueId
    folder_id: UniqueId
    title: str
    file_name: str

    @property
    def event_name(self) -> str:
        return "documents.document.uploaded"

    @property
    def source_context(self) -> str:
        return "documents"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "document_id": str(self.document_id),
            "version_id": str(self.version_id),
            "folder_id": str(self.folder_id),
            "title": self.title,
            "file_name": self.file_name,
        }


@dataclass(frozen=True, kw_only=True)
class VersionCreatedIntegration(IntegrationEvent):
    document_id: UniqueId
    version_id: UniqueId
    version_number: int
    file_name: str

    @property
    def event_name(self) -> str:
        return "documents.version.created"

    @property
    def source_context(self) -> str:
        return "documents"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "document_id": str(self.document_id),
            "version_id": str(self.version_id),
            "version_number": self.version_number,
            "file_name": self.file_name,
        }


@dataclass(frozen=True, kw_only=True)
class DocumentSignedIntegration(IntegrationEvent):
    document_id: UniqueId
    signature_request_id: UniqueId
    signers: list[str]

    @property
    def event_name(self) -> str:
        return "documents.document.signed"

    @property
    def source_context(self) -> str:
        return "documents"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "document_id": str(self.document_id),
            "signature_request_id": str(self.signature_request_id),
            "signers": self.signers,
        }


@dataclass(frozen=True, kw_only=True)
class DocumentArchivedIntegration(IntegrationEvent):
    document_id: UniqueId
    title: str

    @property
    def event_name(self) -> str:
        return "documents.document.archived"

    @property
    def source_context(self) -> str:
        return "documents"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {"document_id": str(self.document_id), "title": self.title}


@dataclass(frozen=True, kw_only=True)
class PhysicalLocationAssignedIntegration(IntegrationEvent):
    document_id: UniqueId
    site_code: str
    room: str
    cabinet: str
    shelf: str
    box: str
    file_ref: str

    @property
    def event_name(self) -> str:
        return "documents.physical_location.assigned"

    @property
    def source_context(self) -> str:
        return "documents"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "document_id": str(self.document_id),
            "site_code": self.site_code,
            "room": self.room,
            "cabinet": self.cabinet,
            "shelf": self.shelf,
            "box": self.box,
            "file_ref": self.file_ref,
        }
