from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BootstrapRootFolderCommand:
    tenant_id: str
    correlation_id: str
    name: str
