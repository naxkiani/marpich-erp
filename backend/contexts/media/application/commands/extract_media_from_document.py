from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExtractMediaFromDocumentCommand:
    tenant_id: str
    correlation_id: str
    document_id: str
    file_name: str
