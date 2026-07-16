"""Identity lifecycle application service."""
from __future__ import annotations

import secrets
import uuid
from datetime import UTC, datetime, timedelta

from contexts.identity_lifecycle.domain.aggregates.identity_lifecycle_platform import (
    ConsentRecord,
    LifecycleAction,
    LifecycleAuditEntry,
    LifecycleCase,
    LifecycleInvitation,
    LifecycleProfile,
    LifecycleState,
    LifecycleTransition,
    VerificationTask,
)
from contexts.identity_lifecycle.domain.events.identity_lifecycle_integration_events import (
    LifecycleCaseOpenedIntegration,
    LifecycleConsentRecordedIntegration,
    LifecycleIdentityDeletedIntegration,
    LifecycleStateChangedIntegration,
    LifecycleVerificationCompletedIntegration,
)
from contexts.identity_lifecycle.domain.ports.identity_lifecycle_repositories import (
    IConsentRecordRepository,
    ILifecycleAuditRepository,
    ILifecycleCaseRepository,
    ILifecycleInvitationRepository,
    ILifecycleProfileRepository,
    ILifecycleTransitionRepository,
    IVerificationTaskRepository,
)
from contexts.identity_lifecycle.domain.services import ai_lifecycle_assistant
from contexts.identity_lifecycle.domain.services import identity_lifecycle_engine as engine
from contexts.identity_lifecycle.domain.services import lifecycle_workflow_engine as workflow
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class IdentityLifecycleApplicationService:
    def __init__(
        self,
        profiles: ILifecycleProfileRepository,
        cases: ILifecycleCaseRepository,
        transitions: ILifecycleTransitionRepository,
        verifications: IVerificationTaskRepository,
        consents: IConsentRecordRepository,
        audits: ILifecycleAuditRepository,
        invitations: ILifecycleInvitationRepository,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._cases = cases
        self._transitions = transitions
        self._verifications = verifications
        self._consents = consents
        self._audits = audits
        self._invitations = invitations
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "registration_enabled": profile.registration_enabled if profile else True,
            "invitation_enabled": profile.invitation_enabled if profile else True,
            "kyc_required": profile.kyc_required if profile else False,
            "aml_required": profile.aml_required if profile else False,
            "consent_required": profile.consent_required if profile else True,
            "soft_delete_retention_days": profile.soft_delete_retention_days if profile else 30,
            "ai_assistant_enabled": True,
        }
        pmap = {
            "identity_lifecycle.registration.enabled": ("registration_enabled", "enabled"),
            "identity_lifecycle.invitation.enabled": ("invitation_enabled", "enabled"),
            "identity_lifecycle.kyc.required": ("kyc_required", "required"),
            "identity_lifecycle.aml.required": ("aml_required", "required"),
            "identity_lifecycle.consent.required": ("consent_required", "required"),
            "identity_lifecycle.soft_delete.retention_days": ("soft_delete_retention_days", "days"),
            "identity_lifecycle.ai_assistant.enabled": ("ai_assistant_enabled", "enabled"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> LifecycleProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = LifecycleProfile.create(
            tenant_id=tenant_id,
            profile_ref=self._profiles.next_profile_ref(tenant_id),
        )
        await self._profiles.save(profile)
        return profile

    async def _audit(
        self,
        tenant_id: str,
        *,
        case_ref: str,
        action: str,
        actor_id: str | None,
        details: dict | None = None,
    ) -> None:
        entry = LifecycleAuditEntry.log(
            tenant_id=tenant_id,
            audit_ref=self._audits.next_audit_ref(tenant_id),
            case_ref=case_ref,
            action=action,
            actor_id=actor_id,
            details=details,
        )
        await self._audits.save(entry)

    async def _transition(
        self,
        tenant_id: str,
        case: LifecycleCase,
        action: str,
        *,
        actor_id: str | None = None,
        reason: str = "",
        correlation_id: str,
        metadata: dict | None = None,
    ) -> Result[LifecycleCase]:
        new_state = workflow.resolve_transition(case.state, action)
        if not new_state:
            return Result.fail("identity_lifecycle.errors.invalid_transition")
        from_state = case.state
        case.transition(new_state)
        await self._cases.save(case)
        transition = LifecycleTransition.record(
            tenant_id=tenant_id,
            transition_ref=self._transitions.next_transition_ref(tenant_id),
            case_ref=case.case_ref,
            action=action,
            from_state=from_state,
            to_state=new_state,
            actor_id=actor_id,
            reason=reason,
            metadata=metadata,
        )
        await self._transitions.save(transition)
        await self._audit(
            tenant_id,
            case_ref=case.case_ref,
            action=action,
            actor_id=actor_id,
            details={"from_state": from_state, "to_state": new_state, "reason": reason},
        )
        await publish_integration_event(
            LifecycleStateChangedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                case_ref=case.case_ref,
                action=action,
                from_state=from_state,
                to_state=new_state,
            )
        )
        return Result.ok(case)

    async def handle_tenant_provisioned(self, event: dict) -> None:
        tenant_id = event.get("tenant_id") or event.get("payload", {}).get("tenant_id")
        if tenant_id:
            await self.seed(tenant_id)

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": engine.list_capability_catalog(),
            "policy_keys": engine.list_policy_keys(),
            "verification_types": engine.list_verification_types(),
            "lifecycle_actions": workflow.list_workflow_actions(),
            "lifecycle_states": workflow.list_lifecycle_states(),
            "workflow_graph": workflow.build_workflow_graph(),
            "dependency_map": engine.dependency_map(),
        })

    async def seed(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        return Result.ok({"seeded": True, "profile_ref": profile.profile_ref})

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        cases = await self._cases.list_by_tenant(tenant_id)
        verifications = []
        for case in cases:
            verifications.extend(await self._verifications.list_by_case(tenant_id, case.case_ref))
        audits = await self._audits.list_by_tenant(tenant_id)
        return Result.ok(
            engine.build_dashboard(
                profile=profile.to_dict(),
                cases=[c.to_dict() for c in cases],
                verifications=[v.to_dict() for v in verifications],
                audits=[a.to_dict() for a in audits],
            )
        )

    async def list_cases(self, tenant_id: str) -> Result[list[dict]]:
        cases = await self._cases.list_by_tenant(tenant_id)
        return Result.ok([c.to_dict() for c in cases])

    async def get_case(self, tenant_id: str, case_ref: str) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        verifications = await self._verifications.list_by_case(tenant_id, case_ref)
        consents = await self._consents.list_by_case(tenant_id, case_ref)
        transitions = await self._transitions.list_by_case(tenant_id, case_ref)
        return Result.ok({
            "case": case.to_dict(),
            "verifications": [v.to_dict() for v in verifications],
            "consents": [c.to_dict() for c in consents],
            "transitions": [t.to_dict() for t in transitions],
        })

    async def register(
        self,
        tenant_id: str,
        *,
        email: str,
        display_name: str,
        identity_ref: str | None = None,
        user_id: str | None = None,
        correlation_id: str,
        actor_id: str | None = None,
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["registration_enabled"]:
            return Result.fail("identity_lifecycle.errors.registration_disabled")
        case_ref = self._cases.next_case_ref(tenant_id)
        case = LifecycleCase.open(
            tenant_id=tenant_id,
            case_ref=case_ref,
            identity_ref=identity_ref or f"id-{uuid.uuid4().hex[:12]}",
            email=email,
            display_name=display_name,
            user_id=user_id,
        )
        await self._cases.save(case)
        await self._audit(
            tenant_id,
            case_ref=case_ref,
            action=LifecycleAction.REGISTRATION.value,
            actor_id=actor_id,
            details={"email": email},
        )
        await publish_integration_event(
            LifecycleCaseOpenedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                case_ref=case_ref,
                identity_ref=case.identity_ref,
                email=case.email,
            )
        )
        return Result.ok(case.to_dict())

    async def invite(
        self,
        tenant_id: str,
        case_ref: str,
        *,
        correlation_id: str,
        actor_id: str | None = None,
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["invitation_enabled"]:
            return Result.fail("identity_lifecycle.errors.invitation_disabled")
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        result = await self._transition(
            tenant_id,
            case,
            LifecycleAction.INVITATION.value,
            actor_id=actor_id,
            correlation_id=correlation_id,
        )
        if not result.succeeded:
            return result
        case = result.unwrap()
        token = secrets.token_urlsafe(32)
        invitation = LifecycleInvitation.issue(
            tenant_id=tenant_id,
            invitation_ref=self._invitations.next_invitation_ref(tenant_id),
            case_ref=case_ref,
            email=case.email,
            token=token,
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )
        await self._invitations.save(invitation)
        return Result.ok({**case.to_dict(), "invitation": invitation.to_dict()})

    async def run_verification(
        self,
        tenant_id: str,
        case_ref: str,
        verification_type: str,
        *,
        correlation_id: str,
        actor_id: str | None = None,
        payload: dict | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        valid_types = {v["type"] for v in engine.list_verification_types()}
        if verification_type not in valid_types:
            return Result.fail("identity_lifecycle.errors.invalid_verification_type")

        action_map = {
            "email_verification": LifecycleAction.EMAIL_VERIFICATION.value,
            "phone_verification": LifecycleAction.PHONE_VERIFICATION.value,
            "government_id_verification": LifecycleAction.GOVERNMENT_ID_VERIFICATION.value,
            "kyc": LifecycleAction.KYC.value,
            "aml": LifecycleAction.AML.value,
            "background_verification": LifecycleAction.BACKGROUND_VERIFICATION.value,
            "identity_verification": LifecycleAction.IDENTITY_VERIFICATION.value,
        }
        action = action_map.get(verification_type, LifecycleAction.IDENTITY_VERIFICATION.value)

        task = VerificationTask.create(
            tenant_id=tenant_id,
            task_ref=self._verifications.next_task_ref(tenant_id),
            case_ref=case_ref,
            verification_type=verification_type,
        )
        passed = bool(payload.get("verified", True)) if payload else True
        if passed:
            task.mark_passed(payload or {"verified": True})
        else:
            task.mark_failed(str(payload.get("reason", "verification_failed") if payload else "verification_failed"))
        await self._verifications.save(task)

        if passed:
            await self._transition(
                tenant_id,
                case,
                action,
                actor_id=actor_id,
                correlation_id=correlation_id,
            )

        await publish_integration_event(
            LifecycleVerificationCompletedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                case_ref=case_ref,
                verification_type=verification_type,
                status=task.status,
            )
        )
        updated = await self._cases.find_by_ref(tenant_id, case_ref)
        return Result.ok({"task": task.to_dict(), "case": updated.to_dict() if updated else {}})

    async def activate(
        self,
        tenant_id: str,
        case_ref: str,
        *,
        correlation_id: str,
        actor_id: str | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        policy = await self._policy_params(tenant_id)
        required = workflow.required_verifications_for_activation(
            policy["kyc_required"],
            policy["aml_required"],
        )
        verifications = await self._verifications.list_by_case(tenant_id, case_ref)
        passed = {v.verification_type for v in verifications if v.status == "passed"}
        missing = [r for r in required if r not in passed]
        if missing:
            return Result.fail("identity_lifecycle.errors.verifications_incomplete")
        if policy["consent_required"]:
            consents = await self._consents.list_by_case(tenant_id, case_ref)
            if not any(c.granted for c in consents):
                return Result.fail("identity_lifecycle.errors.consent_required")
        result = await self._transition(
            tenant_id,
            case,
            LifecycleAction.ACCOUNT_ACTIVATION.value,
            actor_id=actor_id,
            correlation_id=correlation_id,
        )
        if not result.succeeded:
            return result
        return Result.ok(result.unwrap().to_dict())

    async def suspend(
        self,
        tenant_id: str,
        case_ref: str,
        *,
        reason: str,
        correlation_id: str,
        actor_id: str | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        result = await self._transition(
            tenant_id,
            case,
            LifecycleAction.SUSPENSION.value,
            actor_id=actor_id,
            reason=reason,
            correlation_id=correlation_id,
        )
        if not result.succeeded:
            return result
        return Result.ok(result.unwrap().to_dict())

    async def temporary_disable(
        self,
        tenant_id: str,
        case_ref: str,
        *,
        reason: str,
        correlation_id: str,
        actor_id: str | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        result = await self._transition(
            tenant_id,
            case,
            LifecycleAction.TEMPORARY_DISABLE.value,
            actor_id=actor_id,
            reason=reason,
            correlation_id=correlation_id,
        )
        if not result.succeeded:
            return result
        return Result.ok(result.unwrap().to_dict())

    async def reactivate(
        self,
        tenant_id: str,
        case_ref: str,
        *,
        correlation_id: str,
        actor_id: str | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        result = await self._transition(
            tenant_id,
            case,
            LifecycleAction.REACTIVATION.value,
            actor_id=actor_id,
            correlation_id=correlation_id,
        )
        if not result.succeeded:
            return result
        return Result.ok(result.unwrap().to_dict())

    async def merge_identities(
        self,
        tenant_id: str,
        case_ref: str,
        *,
        target_case_ref: str,
        correlation_id: str,
        actor_id: str | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        target = await self._cases.find_by_ref(tenant_id, target_case_ref)
        if not case or not target:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        result = await self._transition(
            tenant_id,
            case,
            LifecycleAction.MERGE_IDENTITIES.value,
            actor_id=actor_id,
            correlation_id=correlation_id,
            metadata={"merged_into": target_case_ref},
        )
        if not result.succeeded:
            return result
        merged = result.unwrap()
        merged.merged_into = target_case_ref
        await self._cases.save(merged)
        return Result.ok(merged.to_dict())

    async def split_identity(
        self,
        tenant_id: str,
        case_ref: str,
        *,
        new_identity_ref: str,
        correlation_id: str,
        actor_id: str | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        result = await self._transition(
            tenant_id,
            case,
            LifecycleAction.SPLIT_IDENTITY.value,
            actor_id=actor_id,
            correlation_id=correlation_id,
            metadata={"new_identity_ref": new_identity_ref},
        )
        if not result.succeeded:
            return result
        return Result.ok(result.unwrap().to_dict())

    async def archive(
        self,
        tenant_id: str,
        case_ref: str,
        *,
        reason: str,
        correlation_id: str,
        actor_id: str | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        result = await self._transition(
            tenant_id,
            case,
            LifecycleAction.IDENTITY_ARCHIVE.value,
            actor_id=actor_id,
            reason=reason,
            correlation_id=correlation_id,
        )
        if not result.succeeded:
            return result
        return Result.ok(result.unwrap().to_dict())

    async def recover(
        self,
        tenant_id: str,
        case_ref: str,
        *,
        correlation_id: str,
        actor_id: str | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        result = await self._transition(
            tenant_id,
            case,
            LifecycleAction.IDENTITY_RECOVERY.value,
            actor_id=actor_id,
            correlation_id=correlation_id,
        )
        if not result.succeeded:
            return result
        activated = await self._transition(
            tenant_id,
            result.unwrap(),
            LifecycleAction.REACTIVATION.value,
            actor_id=actor_id,
            correlation_id=correlation_id,
        )
        if not activated.succeeded:
            return activated
        return Result.ok(activated.unwrap().to_dict())

    async def delete_identity(
        self,
        tenant_id: str,
        case_ref: str,
        *,
        deletion_type: str,
        correlation_id: str,
        actor_id: str | None = None,
        reason: str = "",
    ) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        action = (
            LifecycleAction.HARD_DELETE.value
            if deletion_type == "hard"
            else LifecycleAction.SOFT_DELETE.value
        )
        result = await self._transition(
            tenant_id,
            case,
            action,
            actor_id=actor_id,
            reason=reason,
            correlation_id=correlation_id,
        )
        if not result.succeeded:
            return result
        await publish_integration_event(
            LifecycleIdentityDeletedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                case_ref=case_ref,
                deletion_type=deletion_type,
            )
        )
        return Result.ok(result.unwrap().to_dict())

    async def record_consent(
        self,
        tenant_id: str,
        case_ref: str,
        *,
        purpose: str,
        granted: bool,
        version: str = "1.0",
        correlation_id: str,
        actor_id: str | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        if granted:
            consent = ConsentRecord.grant(
                tenant_id=tenant_id,
                consent_ref=self._consents.next_consent_ref(tenant_id),
                case_ref=case_ref,
                purpose=purpose,
                version=version,
            )
        else:
            consents = await self._consents.list_by_case(tenant_id, case_ref)
            existing = next((c for c in consents if c.purpose == purpose and c.granted), None)
            if not existing:
                return Result.fail("identity_lifecycle.errors.consent_not_found")
            existing.revoke()
            consent = existing
        await self._consents.save(consent)
        if case.state in {
            LifecycleState.REGISTERED.value,
            LifecycleState.INVITED.value,
        }:
            await self._transition(
                tenant_id,
                case,
                LifecycleAction.CONSENT_MANAGEMENT.value,
                actor_id=actor_id,
                correlation_id=correlation_id,
            )
        else:
            await self._audit(
                tenant_id,
                case_ref=case_ref,
                action=LifecycleAction.CONSENT_MANAGEMENT.value,
                actor_id=actor_id,
                details={"purpose": purpose, "granted": granted},
            )
        await publish_integration_event(
            LifecycleConsentRecordedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                case_ref=case_ref,
                purpose=purpose,
                granted=granted,
            )
        )
        updated = await self._cases.find_by_ref(tenant_id, case_ref)
        return Result.ok({"consent": consent.to_dict(), "case": updated.to_dict() if updated else {}})

    async def list_audit(self, tenant_id: str, case_ref: str) -> Result[list[dict]]:
        entries = await self._audits.list_by_case(tenant_id, case_ref)
        return Result.ok([e.to_dict() for e in entries])

    async def get_workflow(self, tenant_id: str, case_ref: str) -> Result[dict]:
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        transitions = await self._transitions.list_by_case(tenant_id, case_ref)
        available = [
            a["action"]
            for a in workflow.list_workflow_actions()
            if workflow.can_transition(case.state, a["action"])
        ]
        return Result.ok({
            "current_state": case.state,
            "transitions": [t.to_dict() for t in transitions],
            "available_actions": available,
            "workflow_graph": workflow.build_workflow_graph(),
        })

    async def assistant_recommend(
        self,
        tenant_id: str,
        case_ref: str,
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["ai_assistant_enabled"]:
            return Result.fail("identity_lifecycle.errors.assistant_disabled")
        case = await self._cases.find_by_ref(tenant_id, case_ref)
        if not case:
            return Result.fail("identity_lifecycle.errors.case_not_found")
        verifications = await self._verifications.list_by_case(tenant_id, case_ref)
        consents = await self._consents.list_by_case(tenant_id, case_ref)
        return Result.ok(
            ai_lifecycle_assistant.recommend_next_actions(
                current_state=case.state,
                verifications=[v.to_dict() for v in verifications],
                consents=[c.to_dict() for c in consents],
                kyc_required=policy["kyc_required"],
                aml_required=policy["aml_required"],
                consent_required=policy["consent_required"],
            )
        )
