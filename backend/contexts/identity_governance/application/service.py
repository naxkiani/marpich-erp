"""Enterprise Identity Governance Platform application service."""
from __future__ import annotations

from contexts.identity_governance.domain.aggregates.identity_governance_platform import (
    AccessRequest,
    AccessReview,
    EmergencyAccessGrant,
    GovernanceAuditEntry,
    IdentityGovernanceProfile,
    PrivilegeCertification,
    RequestStatus,
    TemporaryAccessGrant,
)
from contexts.identity_governance.domain.events.identity_governance_integration_events import (
    AccessRequestApprovedIntegration,
    AccessRequestSubmittedIntegration,
    AccessReviewCompletedIntegration,
    EmergencyAccessGrantedIntegration,
    SodViolationDetectedIntegration,
)
from contexts.identity_governance.domain.ports.identity_governance_repositories import (
    IAccessRequestRepository,
    IAccessReviewRepository,
    IEmergencyAccessGrantRepository,
    IGovernanceAuditEntryRepository,
    IIdentityGovernanceProfileRepository,
    IPrivilegeCertificationRepository,
    ITemporaryAccessGrantRepository,
)
from contexts.identity_governance.domain.services import identity_governance_engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class IdentityGovernanceApplicationService:
    def __init__(
        self,
        profiles: IIdentityGovernanceProfileRepository,
        access_requests: IAccessRequestRepository,
        access_reviews: IAccessReviewRepository,
        certifications: IPrivilegeCertificationRepository,
        temporary_grants: ITemporaryAccessGrantRepository,
        emergency_grants: IEmergencyAccessGrantRepository,
        audit_entries: IGovernanceAuditEntryRepository,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._access_requests = access_requests
        self._access_reviews = access_reviews
        self._certifications = certifications
        self._temporary_grants = temporary_grants
        self._emergency_grants = emergency_grants
        self._audit = audit_entries
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        params = {
            "access_review_frequency_days": 90,
            "certification_required": True,
            "sod_enforcement": True,
            "temporary_access_max_hours": 72,
            "emergency_access_max_hours": 4,
        }
        pmap = {
            "identity_governance.access_review.frequency_days": ("access_review_frequency_days", "frequency_days"),
            "identity_governance.certification.required": ("certification_required", "required"),
            "identity_governance.sod.enforcement": ("sod_enforcement", "enforcement"),
            "identity_governance.temporary_access.max_hours": ("temporary_access_max_hours", "max_hours"),
            "identity_governance.emergency_access.max_hours": ("emergency_access_max_hours", "max_hours"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(
                tenant_id=tenant_id, domain="tax", policy_key=key, facts={}
            )
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _record_audit(
        self,
        tenant_id: str,
        *,
        action: str,
        actor_id: str,
        resource_type: str,
        resource_ref: str,
        details: dict | None = None,
    ) -> None:
        entry = GovernanceAuditEntry.record(
            tenant_id=tenant_id,
            entry_ref=self._audit.next_entry_ref(tenant_id),
            action=action,
            actor_id=actor_id,
            resource_type=resource_type,
            resource_ref=resource_ref,
            details=details,
        )
        await self._audit.save(entry)

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": identity_governance_engine.list_capability_catalog(),
            "sod_rules": identity_governance_engine.list_sod_rules(),
            "policy_keys": identity_governance_engine.list_policy_keys(),
            "shared_service": True,
            "delegation": {
                "identity_user_role_management": True,
                "workflow_approval": True,
                "audit_trail": True,
                "local_identity_duplication": False,
            },
        })

    async def get_dependency_map(self) -> Result[dict]:
        return Result.ok(identity_governance_engine.dependency_map())

    async def seed(self, tenant_id: str) -> Result[dict]:
        existing = await self._profiles.find_by_tenant(tenant_id)
        if existing:
            return Result.ok({
                "seeded": False,
                "profile": existing.to_dict(),
                "access_requests": len(await self._access_requests.list_by_tenant(tenant_id)),
            })

        params = await self._policy_params(tenant_id)
        ref = self._profiles.next_profile_ref(tenant_id)
        profile = IdentityGovernanceProfile.create(tenant_id=tenant_id, profile_ref=ref)
        profile.access_review_frequency_days = int(params.get("access_review_frequency_days", 90))
        profile.certification_required = bool(params.get("certification_required", True))
        profile.sod_enforcement = bool(params.get("sod_enforcement", True))
        profile.temporary_access_max_hours = int(params.get("temporary_access_max_hours", 72))
        profile.emergency_access_max_hours = int(params.get("emergency_access_max_hours", 4))
        await self._profiles.save(profile)

        review_ref = self._access_reviews.next_review_ref(tenant_id)
        review = AccessReview.schedule(
            tenant_id=tenant_id,
            review_ref=review_ref,
            title="Quarterly Access Review",
            reviewer_id="governance-admin",
            scope_user_ids=["user-finance-1", "user-treasury-1"],
        )
        await self._access_reviews.save(review)

        requests_seeded = 0
        for seed_req in identity_governance_engine.DEFAULT_SEED_ACCESS_REQUESTS:
            sod = identity_governance_engine.check_segregation_of_duties(
                existing_roles=[], requested_roles=seed_req["requested_roles"]
            )
            request_ref = self._access_requests.next_request_ref(tenant_id)
            req = AccessRequest.submit(
                tenant_id=tenant_id,
                request_ref=request_ref,
                requester_id="user-requester",
                target_user_id=seed_req["target_user_id"],
                requested_roles=seed_req["requested_roles"],
                justification=seed_req["justification"],
                sod_valid=sod["valid"],
            )
            await self._access_requests.save(req)
            requests_seeded += 1

        cert_ref = self._certifications.next_certification_ref(tenant_id)
        cert = PrivilegeCertification.initiate(
            tenant_id=tenant_id,
            certification_ref=cert_ref,
            user_id="user-finance-1",
            role_ids=["finance_viewer"],
        )
        await self._certifications.save(cert)

        return Result.ok({
            "seeded": True,
            "profile": profile.to_dict(),
            "access_requests_seeded": requests_seeded,
            "access_reviews_seeded": 1,
            "certifications_seeded": 1,
        })

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        return Result.ok(
            identity_governance_engine.build_dashboard(
                profile=profile.to_dict() if profile else None,
                access_requests=[r.to_dict() for r in await self._access_requests.list_by_tenant(tenant_id)],
                access_reviews=[r.to_dict() for r in await self._access_reviews.list_by_tenant(tenant_id)],
                certifications=[c.to_dict() for c in await self._certifications.list_by_tenant(tenant_id)],
                temporary_grants=[g.to_dict() for g in await self._temporary_grants.list_by_tenant(tenant_id)],
                emergency_grants=[g.to_dict() for g in await self._emergency_grants.list_by_tenant(tenant_id)],
                audit_entries=[e.to_dict() for e in await self._audit.list_by_tenant(tenant_id)],
            )
        )

    async def check_sod(
        self,
        tenant_id: str,
        *,
        existing_roles: list[str],
        requested_roles: list[str],
    ) -> Result[dict]:
        result = identity_governance_engine.check_segregation_of_duties(
            existing_roles=existing_roles, requested_roles=requested_roles
        )
        if not result["valid"]:
            await publish_integration_event(
                SodViolationDetectedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id="sod-check",
                    request_ref="",
                    conflicts=result["conflicts"],
                )
            )
        return Result.ok(result)

    async def submit_access_request(
        self,
        tenant_id: str,
        *,
        requester_id: str,
        target_user_id: str,
        requested_roles: list[str],
        justification: str,
        existing_roles: list[str] | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        sod = identity_governance_engine.check_segregation_of_duties(
            existing_roles=existing_roles or [],
            requested_roles=requested_roles,
        )
        if bool(params.get("sod_enforcement", True)) and not sod["valid"]:
            return Result.fail("sod_violation")

        request_ref = self._access_requests.next_request_ref(tenant_id)
        req = AccessRequest.submit(
            tenant_id=tenant_id,
            request_ref=request_ref,
            requester_id=requester_id,
            target_user_id=target_user_id,
            requested_roles=requested_roles,
            justification=justification,
            sod_valid=sod["valid"],
        )
        await self._access_requests.save(req)

        corr = correlation_id or request_ref
        await publish_integration_event(
            AccessRequestSubmittedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                request_ref=request_ref,
                target_user_id=target_user_id,
                requested_roles=requested_roles,
            )
        )
        await self._record_audit(
            tenant_id, action="access_request.submitted", actor_id=requester_id,
            resource_type="access_request", resource_ref=request_ref,
        )
        return Result.ok(req.to_dict())

    async def list_access_requests(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._access_requests.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in items])

    async def approve_access_request(
        self,
        tenant_id: str,
        request_ref: str,
        *,
        approver_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        req = await self._access_requests.find_by_ref(tenant_id, request_ref)
        if not req:
            return Result.fail("request_not_found")
        if req.status != RequestStatus.PENDING.value:
            return Result.fail("request_not_pending")
        if not req.sod_valid:
            return Result.fail("sod_violation")

        req.approve(approver_id)
        await self._access_requests.save(req)

        corr = correlation_id or request_ref
        await publish_integration_event(
            AccessRequestApprovedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                request_ref=request_ref,
                approver_id=approver_id,
            )
        )
        await self._record_audit(
            tenant_id, action="access_request.approved", actor_id=approver_id,
            resource_type="access_request", resource_ref=request_ref,
        )
        return Result.ok(req.to_dict())

    async def reject_access_request(
        self,
        tenant_id: str,
        request_ref: str,
        *,
        approver_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        req = await self._access_requests.find_by_ref(tenant_id, request_ref)
        if not req:
            return Result.fail("request_not_found")
        req.reject(approver_id)
        await self._access_requests.save(req)
        await self._record_audit(
            tenant_id, action="access_request.rejected", actor_id=approver_id,
            resource_type="access_request", resource_ref=request_ref,
        )
        return Result.ok(req.to_dict())

    async def schedule_access_review(
        self,
        tenant_id: str,
        *,
        title: str,
        reviewer_id: str,
        scope_user_ids: list[str],
    ) -> Result[dict]:
        review_ref = self._access_reviews.next_review_ref(tenant_id)
        review = AccessReview.schedule(
            tenant_id=tenant_id,
            review_ref=review_ref,
            title=title,
            reviewer_id=reviewer_id,
            scope_user_ids=scope_user_ids,
        )
        await self._access_reviews.save(review)
        return Result.ok(review.to_dict())

    async def list_access_reviews(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._access_reviews.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in items])

    async def complete_access_review(
        self,
        tenant_id: str,
        review_ref: str,
        *,
        findings: list[dict],
        reviewer_id: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        review = await self._access_reviews.find_by_ref(tenant_id, review_ref)
        if not review:
            return Result.fail("review_not_found")
        review.complete(findings)
        await self._access_reviews.save(review)

        corr = correlation_id or review_ref
        await publish_integration_event(
            AccessReviewCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                review_ref=review_ref,
                findings_count=len(findings),
            )
        )
        await self._record_audit(
            tenant_id, action="access_review.completed", actor_id=reviewer_id,
            resource_type="access_review", resource_ref=review_ref,
            details={"findings_count": len(findings)},
        )
        return Result.ok(review.to_dict())

    async def initiate_certification(
        self,
        tenant_id: str,
        *,
        user_id: str,
        role_ids: list[str],
    ) -> Result[dict]:
        cert_ref = self._certifications.next_certification_ref(tenant_id)
        cert = PrivilegeCertification.initiate(
            tenant_id=tenant_id,
            certification_ref=cert_ref,
            user_id=user_id,
            role_ids=role_ids,
        )
        await self._certifications.save(cert)
        return Result.ok(cert.to_dict())

    async def list_certifications(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._certifications.list_by_tenant(tenant_id)
        return Result.ok([c.to_dict() for c in items])

    async def certify_privileges(
        self,
        tenant_id: str,
        certification_ref: str,
        *,
        certifier_id: str,
        notes: str = "",
    ) -> Result[dict]:
        cert = await self._certifications.find_by_ref(tenant_id, certification_ref)
        if not cert:
            return Result.fail("certification_not_found")
        cert.certify(certifier_id, notes)
        await self._certifications.save(cert)
        await self._record_audit(
            tenant_id, action="privilege.certified", actor_id=certifier_id,
            resource_type="certification", resource_ref=certification_ref,
        )
        return Result.ok(cert.to_dict())

    async def grant_temporary_access(
        self,
        tenant_id: str,
        *,
        user_id: str,
        roles: list[str],
        granted_by: str,
        hours: int | None = None,
        justification: str = "",
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        max_hours = int(params.get("temporary_access_max_hours", 72))
        grant_hours = min(hours or max_hours, max_hours)
        sod = identity_governance_engine.check_segregation_of_duties(
            existing_roles=[], requested_roles=roles
        )
        if bool(params.get("sod_enforcement", True)) and not sod["valid"]:
            return Result.fail("sod_violation")

        grant_ref = self._temporary_grants.next_grant_ref(tenant_id)
        grant = TemporaryAccessGrant.grant(
            tenant_id=tenant_id,
            grant_ref=grant_ref,
            user_id=user_id,
            roles=roles,
            granted_by=granted_by,
            expires_at=identity_governance_engine.compute_expiry(hours=grant_hours),
            justification=justification,
        )
        await self._temporary_grants.save(grant)
        await self._record_audit(
            tenant_id, action="temporary_access.granted", actor_id=granted_by,
            resource_type="temporary_access", resource_ref=grant_ref,
        )
        return Result.ok(grant.to_dict())

    async def list_temporary_access(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._temporary_grants.list_by_tenant(tenant_id)
        return Result.ok([g.to_dict() for g in items])

    async def grant_emergency_access(
        self,
        tenant_id: str,
        *,
        user_id: str,
        roles: list[str],
        granted_by: str,
        incident_ref: str = "",
        justification: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        max_hours = int(params.get("emergency_access_max_hours", 4))

        grant_ref = self._emergency_grants.next_grant_ref(tenant_id)
        grant = EmergencyAccessGrant.grant(
            tenant_id=tenant_id,
            grant_ref=grant_ref,
            user_id=user_id,
            roles=roles,
            granted_by=granted_by,
            expires_at=identity_governance_engine.compute_expiry(hours=max_hours),
            incident_ref=incident_ref,
            justification=justification,
        )
        await self._emergency_grants.save(grant)

        corr = correlation_id or grant_ref
        await publish_integration_event(
            EmergencyAccessGrantedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                grant_ref=grant_ref,
                user_id=user_id,
                incident_ref=incident_ref,
            )
        )
        await self._record_audit(
            tenant_id, action="emergency_access.granted", actor_id=granted_by,
            resource_type="emergency_access", resource_ref=grant_ref,
            details={"incident_ref": incident_ref},
        )
        return Result.ok(grant.to_dict())

    async def list_emergency_access(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._emergency_grants.list_by_tenant(tenant_id)
        return Result.ok([g.to_dict() for g in items])

    async def list_audit_log(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._audit.list_by_tenant(tenant_id)
        return Result.ok([e.to_dict() for e in items])

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope.get("tenant_id", "")
        if tenant_id:
            await self.seed(tenant_id)
