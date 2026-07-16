"""Registration & onboarding application service (P201-A)."""
from __future__ import annotations

import uuid

from contexts.identity_lifecycle.application.service import IdentityLifecycleApplicationService
from contexts.identity_lifecycle.domain.aggregates.registration_onboarding import (
    ApprovalMode,
    IdentityRegistration,
    RegistrationChannel,
    RegistrationStatus,
)
from contexts.identity_lifecycle.domain.events.identity_lifecycle_integration_events import (
    LifecycleActivationRequestedIntegration,
    LifecycleIdentityCreatedIntegration,
    LifecycleOnboardingStartedIntegration,
    LifecycleProfileInitializedIntegration,
    LifecycleProvisioningRequestedIntegration,
    LifecycleRegistrationApprovedIntegration,
    LifecycleRegistrationDuplicateDetectedIntegration,
    LifecycleRegistrationRejectedIntegration,
    LifecycleRegistrationRequestedIntegration,
    LifecycleRegistrationValidatedIntegration,
    LifecycleWelcomeGeneratedIntegration,
)
from contexts.identity_lifecycle.domain.ports.registration_repositories import (
    IIdentityRegistrationRepository,
)
from contexts.identity_lifecycle.domain.services import registration_onboarding_engine as eng
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class RegistrationOnboardingApplicationService:
    def __init__(
        self,
        registrations: IIdentityRegistrationRepository,
        lifecycle: IdentityLifecycleApplicationService,
    ) -> None:
        self._regs = registrations
        self._lifecycle = lifecycle

    def surface(self) -> dict:
        return {
            **eng.catalog(),
            "apis": [
                "/api/v1/identity-lifecycle/eilmp/surface",
                "/api/v1/identity-lifecycle/registration/catalog",
                "/api/v1/identity-lifecycle/registration/register",
            ],
            "sor": "identity_lifecycle",
            "forbidden_sibling": "eilmp",
        }

    async def register_identity(
        self,
        tenant_id: str,
        *,
        email: str,
        display_name: str,
        identity_type: str = "employee",
        channel: str = RegistrationChannel.REST_API.value,
        source: str = "api",
        method: str = "self_registration",
        national_id: str = "",
        employee_number: str = "",
        phone: str = "",
        organization_ref: str = "",
        approval_mode: str = ApprovalMode.AUTOMATIC.value,
        zt_context: dict | None = None,
        metadata: dict | None = None,
        correlation_id: str = "",
        actor_id: str | None = None,
        auto_advance: bool = True,
    ) -> Result[dict]:
        policy = await self._lifecycle._policy_params(tenant_id)
        if not policy["registration_enabled"]:
            return Result.fail("identity_lifecycle.errors.registration_disabled")

        zt = eng.evaluate_zero_trust(zt_context)
        if not zt["passed"]:
            return Result.fail("identity_lifecycle.errors.zero_trust_blocked")

        corr = correlation_id or str(uuid.uuid4())
        reg = IdentityRegistration.request(
            tenant_id=tenant_id,
            registration_ref=self._regs.next_registration_ref(tenant_id),
            identity_type=identity_type,
            channel=channel,
            email=email,
            display_name=display_name,
            source=source,
            method=method,
            national_id=national_id,
            employee_number=employee_number,
            phone=phone,
            organization_ref=organization_ref,
            approval_mode=approval_mode,
            zt_context=zt_context,
            metadata=metadata,
        )
        reg.risk_score = float(zt["risk_score"])
        reg.trust_level = str(zt["trust_level"])
        await self._regs.save(reg)
        await publish_integration_event(
            LifecycleRegistrationRequestedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=corr,
                registration_ref=reg.registration_ref,
                identity_type=reg.identity_type,
                email=reg.email,
            )
        )

        if auto_advance:
            validated = await self.validate_registration(
                tenant_id, reg.registration_ref, correlation_id=corr, actor_id=actor_id
            )
            if not validated.succeeded:
                return validated
            dup = await self.detect_duplicates(
                tenant_id, reg.registration_ref, correlation_id=corr
            )
            if not dup.succeeded:
                return dup
            reg = await self._regs.find_by_ref(tenant_id, reg.registration_ref)
            assert reg is not None
            if reg.duplicate_matches:
                return Result.ok(
                    {
                        **reg.to_dict(),
                        "ai": eng.ai_registration_hints(reg, reg.duplicate_matches),
                        "blocked_on": "duplicate_review",
                    }
                )
            if reg.approval_mode == ApprovalMode.AUTOMATIC.value and reg.risk_score < 50:
                approved = await self.approve_registration(
                    tenant_id,
                    reg.registration_ref,
                    correlation_id=corr,
                    actor_id=actor_id or "system",
                )
                if not approved.succeeded:
                    return approved
                return Result.ok(approved.unwrap())

        refreshed = await self._regs.find_by_ref(tenant_id, reg.registration_ref)
        assert refreshed is not None
        return Result.ok(
            {
                **refreshed.to_dict(),
                "ai": eng.ai_registration_hints(refreshed, refreshed.duplicate_matches),
                "zt": zt,
            }
        )

    async def validate_registration(
        self,
        tenant_id: str,
        registration_ref: str,
        *,
        correlation_id: str = "",
        actor_id: str | None = None,
    ) -> Result[dict]:
        reg = await self._regs.find_by_ref(tenant_id, registration_ref)
        if not reg:
            return Result.fail("identity_lifecycle.errors.registration_not_found")
        reg.touch(RegistrationStatus.PENDING_VALIDATION.value)
        errors = eng.validate_registration_input(reg)
        reg.validation_errors = errors
        if errors:
            reg.touch(RegistrationStatus.REQUESTED.value)
            await self._regs.save(reg)
            return Result.fail("identity_lifecycle.errors.validation_failed:" + ",".join(errors))
        reg.touch(RegistrationStatus.VALIDATED.value)
        await self._regs.save(reg)
        await publish_integration_event(
            LifecycleRegistrationValidatedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or str(uuid.uuid4()),
                registration_ref=reg.registration_ref,
            )
        )
        return Result.ok(reg.to_dict())

    async def detect_duplicates(
        self,
        tenant_id: str,
        registration_ref: str,
        *,
        threshold: float = 0.85,
        correlation_id: str = "",
    ) -> Result[dict]:
        reg = await self._regs.find_by_ref(tenant_id, registration_ref)
        if not reg:
            return Result.fail("identity_lifecycle.errors.registration_not_found")
        existing = await self._regs.list_by_tenant(tenant_id)
        cases_result = await self._lifecycle.list_cases(tenant_id)
        cases = cases_result.unwrap() if cases_result.succeeded else []
        matches = eng.detect_duplicates(
            candidate=reg, existing=existing, cases=cases, threshold=threshold
        )
        reg.duplicate_matches = matches
        if matches:
            reg.touch(RegistrationStatus.DUPLICATE_REVIEW.value)
            await publish_integration_event(
                LifecycleRegistrationDuplicateDetectedIntegration(
                    tenant_id=TenantId(tenant_id),
                    correlation_id=correlation_id or str(uuid.uuid4()),
                    registration_ref=reg.registration_ref,
                    match_count=len(matches),
                )
            )
        else:
            reg.touch(RegistrationStatus.PENDING_APPROVAL.value)
        await self._regs.save(reg)
        return Result.ok(
            {
                "registration_ref": reg.registration_ref,
                "matches": matches,
                "status": reg.status,
                "ai": eng.ai_registration_hints(reg, matches),
            }
        )

    async def approve_registration(
        self,
        tenant_id: str,
        registration_ref: str,
        *,
        correlation_id: str = "",
        actor_id: str | None = None,
        force: bool = False,
    ) -> Result[dict]:
        reg = await self._regs.find_by_ref(tenant_id, registration_ref)
        if not reg:
            return Result.fail("identity_lifecycle.errors.registration_not_found")
        if reg.status == RegistrationStatus.REJECTED.value:
            return Result.fail("identity_lifecycle.errors.already_rejected")
        if reg.duplicate_matches and not force:
            return Result.fail("identity_lifecycle.errors.duplicates_unresolved")
        if reg.status not in {
            RegistrationStatus.PENDING_APPROVAL.value,
            RegistrationStatus.VALIDATED.value,
            RegistrationStatus.DUPLICATE_REVIEW.value,
        }:
            if reg.status != RegistrationStatus.APPROVED.value:
                # allow re-entry only from gated statuses
                if reg.status not in {
                    RegistrationStatus.REQUESTED.value,
                    RegistrationStatus.PENDING_VALIDATION.value,
                }:
                    pass
        corr = correlation_id or str(uuid.uuid4())
        case_result = await self._lifecycle.register(
            tenant_id,
            email=reg.email,
            display_name=reg.display_name,
            identity_ref=None,
            user_id=None,
            correlation_id=corr,
            actor_id=actor_id,
        )
        if not case_result.succeeded:
            return Result.fail(case_result.error or "identity_lifecycle.errors.case_create_failed")
        case = case_result.unwrap()
        # enrich case metadata via transition metadata path — store on registration
        reg.case_ref = case["case_ref"]
        reg.approved_by = actor_id
        reg.touch(RegistrationStatus.APPROVED.value)
        await self._regs.save(reg)
        await publish_integration_event(
            LifecycleRegistrationApprovedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=corr,
                registration_ref=reg.registration_ref,
                case_ref=reg.case_ref or "",
                approved_by=actor_id or "",
            )
        )
        await publish_integration_event(
            LifecycleIdentityCreatedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=corr,
                registration_ref=reg.registration_ref,
                case_ref=reg.case_ref or "",
                identity_type=reg.identity_type,
            )
        )
        return Result.ok(reg.to_dict())

    async def reject_registration(
        self,
        tenant_id: str,
        registration_ref: str,
        *,
        reason: str = "",
        correlation_id: str = "",
        actor_id: str | None = None,
    ) -> Result[dict]:
        reg = await self._regs.find_by_ref(tenant_id, registration_ref)
        if not reg:
            return Result.fail("identity_lifecycle.errors.registration_not_found")
        reg.rejected_reason = reason
        reg.approved_by = actor_id
        reg.touch(RegistrationStatus.REJECTED.value)
        await self._regs.save(reg)
        await publish_integration_event(
            LifecycleRegistrationRejectedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or str(uuid.uuid4()),
                registration_ref=reg.registration_ref,
                reason=reason,
            )
        )
        return Result.ok(reg.to_dict())

    async def initialize_profile(
        self,
        tenant_id: str,
        registration_ref: str,
        *,
        correlation_id: str = "",
    ) -> Result[dict]:
        reg = await self._regs.find_by_ref(tenant_id, registration_ref)
        if not reg:
            return Result.fail("identity_lifecycle.errors.registration_not_found")
        if reg.status not in {
            RegistrationStatus.APPROVED.value,
            RegistrationStatus.PROFILE_INITIALIZED.value,
        }:
            return Result.fail("identity_lifecycle.errors.not_approved")
        reg.profile = eng.build_initial_profile(reg)
        reg.touch(RegistrationStatus.PROFILE_INITIALIZED.value)
        await self._regs.save(reg)
        await publish_integration_event(
            LifecycleProfileInitializedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or str(uuid.uuid4()),
                registration_ref=reg.registration_ref,
            )
        )
        return Result.ok(reg.to_dict())

    async def start_onboarding(
        self,
        tenant_id: str,
        registration_ref: str,
        *,
        correlation_id: str = "",
    ) -> Result[dict]:
        reg = await self._regs.find_by_ref(tenant_id, registration_ref)
        if not reg:
            return Result.fail("identity_lifecycle.errors.registration_not_found")
        if reg.status not in {
            RegistrationStatus.PROFILE_INITIALIZED.value,
            RegistrationStatus.ONBOARDING.value,
            RegistrationStatus.APPROVED.value,
        }:
            return Result.fail("identity_lifecycle.errors.profile_required")
        if not reg.profile:
            reg.profile = eng.build_initial_profile(reg)
        reg.onboarding = eng.build_onboarding_checklist(reg)
        reg.touch(RegistrationStatus.ONBOARDING.value)
        await self._regs.save(reg)
        corr = correlation_id or str(uuid.uuid4())
        await publish_integration_event(
            LifecycleOnboardingStartedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=corr,
                registration_ref=reg.registration_ref,
            )
        )
        await publish_integration_event(
            LifecycleWelcomeGeneratedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=corr,
                registration_ref=reg.registration_ref,
            )
        )
        return Result.ok(reg.to_dict())

    async def request_provisioning(
        self,
        tenant_id: str,
        registration_ref: str,
        *,
        correlation_id: str = "",
    ) -> Result[dict]:
        reg = await self._regs.find_by_ref(tenant_id, registration_ref)
        if not reg:
            return Result.fail("identity_lifecycle.errors.registration_not_found")
        if reg.status not in {
            RegistrationStatus.ONBOARDING.value,
            RegistrationStatus.PROVISIONING_REQUESTED.value,
        }:
            return Result.fail("identity_lifecycle.errors.onboarding_required")
        corr = correlation_id or str(uuid.uuid4())
        reg.onboarding["provisioning"] = {
            "requested": True,
            "delegate_to": ["identity", "directory"],
            "case_ref": reg.case_ref,
        }
        reg.touch(RegistrationStatus.PROVISIONING_REQUESTED.value)
        await self._regs.save(reg)
        await publish_integration_event(
            LifecycleProvisioningRequestedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=corr,
                registration_ref=reg.registration_ref,
                case_ref=reg.case_ref or "",
                identity_type=reg.identity_type,
            )
        )
        reg.touch(RegistrationStatus.ACTIVATION_REQUESTED.value)
        await self._regs.save(reg)
        await publish_integration_event(
            LifecycleActivationRequestedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=corr,
                registration_ref=reg.registration_ref,
                case_ref=reg.case_ref or "",
            )
        )
        return Result.ok(reg.to_dict())

    async def get_registration(
        self, tenant_id: str, registration_ref: str
    ) -> Result[dict]:
        reg = await self._regs.find_by_ref(tenant_id, registration_ref)
        if not reg:
            return Result.fail("identity_lifecycle.errors.registration_not_found")
        return Result.ok(reg.to_dict())

    async def get_status(self, tenant_id: str, registration_ref: str) -> Result[dict]:
        reg = await self._regs.find_by_ref(tenant_id, registration_ref)
        if not reg:
            return Result.fail("identity_lifecycle.errors.registration_not_found")
        return Result.ok(
            {
                "registration_ref": reg.registration_ref,
                "status": reg.status,
                "case_ref": reg.case_ref,
                "duplicate_matches": reg.duplicate_matches,
                "risk_score": reg.risk_score,
                "trust_level": reg.trust_level,
                "onboarding_status": (reg.onboarding or {}).get("checklist"),
            }
        )
