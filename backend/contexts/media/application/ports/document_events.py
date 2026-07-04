from __future__ import annotations

from typing import Protocol

from contexts.media.application.commands.extract_media_from_document import (
    ExtractMediaFromDocumentCommand,
)


class IDocumentEventAdapter(Protocol):
    async def parse_document_uploaded(
        self, envelope: dict
    ) -> ExtractMediaFromDocumentCommand | None: ...
