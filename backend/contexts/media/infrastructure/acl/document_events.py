"""ACL — documents events."""
from __future__ import annotations

from contexts.media.application.commands.extract_media_from_document import (
    ExtractMediaFromDocumentCommand,
)
from contexts.media.application.constants.media_extensions import MEDIA_EXTENSIONS


class DocumentEventAdapter:
    async def parse_document_uploaded(
        self, envelope: dict
    ) -> ExtractMediaFromDocumentCommand | None:
        payload = envelope["payload"]
        file_name = payload.get("file_name", "").lower()
        if not any(file_name.endswith(ext) for ext in MEDIA_EXTENSIONS):
            return None
        return ExtractMediaFromDocumentCommand(
            tenant_id=envelope["tenant_id"],
            correlation_id=envelope["correlation_id"],
            document_id=payload["document_id"],
            file_name=payload.get("file_name", "asset"),
        )


async def on_document_uploaded(envelope: dict) -> ExtractMediaFromDocumentCommand | None:
    return await DocumentEventAdapter().parse_document_uploaded(envelope)
