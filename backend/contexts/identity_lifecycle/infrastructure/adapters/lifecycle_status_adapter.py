"""IIdentityLifecycleStatus adapter (P201-A)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from shared.application.ports.identity_lifecycle import (
    IdentityLifecycleStatus,
    IIdentityLifecycleStatus,
)

if TYPE_CHECKING:
    from contexts.identity_lifecycle.application.registration_service import (
        RegistrationOnboardingApplicationService,
    )
    from contexts.identity_lifecycle.application.service import (
        IdentityLifecycleApplicationService,
    )


class IdentityLifecycleStatusAdapter(IIdentityLifecycleStatus):
    def __init__(
        self,
        *,
        registrations: RegistrationOnboardingApplicationService,
        lifecycle: IdentityLifecycleApplicationService,
    ) -> None:
        self._registrations = registrations
        self._lifecycle = lifecycle

    async def get_registration_status(
        self, *, tenant_id: str, registration_ref: str
    ) -> IdentityLifecycleStatus | None:
        result = await self._registrations.get_registration(tenant_id, registration_ref)
        if not result.succeeded:
            return None
        data = result.unwrap()
        return IdentityLifecycleStatus(
            tenant_id=tenant_id,
            subject_ref=registration_ref,
            subject_kind="registration",
            status=str(data.get("status") or "unknown"),
            identity_type=str(data.get("identity_type") or ""),
            case_ref=data.get("case_ref"),
            risk_score=float(data.get("risk_score") or 0),
            trust_level=str(data.get("trust_level") or "unknown"),
            attributes={
                "email": data.get("email"),
                "channel": data.get("channel"),
            },
        )

    async def get_case_status(
        self, *, tenant_id: str, case_ref: str
    ) -> IdentityLifecycleStatus | None:
        result = await self._lifecycle.get_case(tenant_id, case_ref)
        if not result.succeeded:
            return None
        case = result.unwrap().get("case") or {}
        return IdentityLifecycleStatus(
            tenant_id=tenant_id,
            subject_ref=case_ref,
            subject_kind="lifecycle_case",
            status=str(case.get("state") or "unknown"),
            identity_type=str((case.get("metadata") or {}).get("identity_type") or ""),
            case_ref=case_ref,
            attributes={"email": case.get("email"), "identity_ref": case.get("identity_ref")},
        )
