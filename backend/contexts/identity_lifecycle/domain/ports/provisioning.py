"""P201-A2 ports — provisioning + Workflow approval (identity_lifecycle SoR)."""
from __future__ import annotations

from typing import Protocol


class IIdentityUserProvisioner(Protocol):
    async def provision_user(
        self,
        *,
        tenant_id: str,
        email: str,
        display_name: str,
        external_id: str,
        correlation_id: str,
    ) -> dict: ...


class IWorkflowApprovalPort(Protocol):
    async def ensure_registration_approval_definition(self, tenant_id: str) -> None: ...

    async def start_registration_approval(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        registration_ref: str,
        started_by: str,
        assignee_id: str | None = None,
    ) -> dict: ...
