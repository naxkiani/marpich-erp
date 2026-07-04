"""Command from platform.module.activated."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MergeModuleConfigCommand:
    tenant_id: str
    correlation_id: str
    module_id: str
