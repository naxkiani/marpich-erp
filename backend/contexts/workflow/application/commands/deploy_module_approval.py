"""Command from platform.module.activated integration event."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeployModuleApprovalCommand:
    tenant_id: str
    correlation_id: str
    module_id: str
