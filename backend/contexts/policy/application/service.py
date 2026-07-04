"""Policy application service."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.policy.application.constants.default_policies import (
    DEFAULT_POLICY_TEMPLATES,
    default_effective_from,
)
from contexts.policy.application.constants.domains import INDUSTRY_PACK_TO_DOMAIN, POLICY_DOMAINS
from contexts.policy.domain.aggregates.policy import Policy
from contexts.policy.domain.aggregates.policy_version import PolicyStatus, PolicyVersion
from contexts.policy.domain.events.integration_events import (
    EvaluationDeniedIntegration,
    SimulationExecutedIntegration,
    VersionActivatedIntegration,
    VersionRolledBackIntegration,
    VersionSubmittedIntegration,
)
from contexts.policy.domain.ports.repositories import IPolicyRepository, IPolicyVersionRepository
from contexts.policy.domain.services.policy_evaluator import evaluate_version, run_test_cases
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class PolicyApplicationService:
    def __init__(
        self,
        policies: IPolicyRepository,
        versions: IPolicyVersionRepository,
    ) -> None:
        self._policies = policies
        self._versions = versions

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        industry_pack = envelope.get("payload", {}).get("industry_pack") or envelope.get(
            "industry_pack", ""
        )
        domain = INDUSTRY_PACK_TO_DOMAIN.get(str(industry_pack).lower())
        if not domain:
            return
        templates = DEFAULT_POLICY_TEMPLATES.get(domain, [])
        for template in templates:
            existing = await self._policies.find_by_key(tenant_id, domain, template["key"])
            if existing:
                continue
            await self._create_policy_from_template(
                tenant_id=tenant_id,
                domain=domain,
                template=template,
                activate=True,
            )

    async def handle_workflow_process_completed(self, envelope: dict) -> None:
        payload = envelope.get("payload") or {}
        policy_id = payload.get("policy_id")
        version = payload.get("version")
        outcome = payload.get("outcome", payload.get("status"))
        tenant_id = envelope.get("tenant_id", "")
        if not policy_id or version is None or not tenant_id:
            return

        ver = await self._versions.find_by_policy_and_version(tenant_id, policy_id, int(version))
        if not ver or ver.status != PolicyStatus.PENDING_APPROVAL:
            return

        if outcome in ("approved", "completed", "success"):
            await self._activate_version(tenant_id, policy_id, int(version), actor_id=envelope.get("user_id"))
        else:
            ver.reject_to_draft()
            await self._versions.save(ver)

    async def list_domains(self) -> Result[list[dict]]:
        return Result.ok([{"id": d[0], "name": d[1]} for d in POLICY_DOMAINS])

    async def list_policies(
        self, tenant_id: str, *, domain: str | None = None
    ) -> Result[list[dict]]:
        policies = await self._policies.list_by_tenant(tenant_id, domain=domain)
        items = []
        for policy in policies:
            versions = await self._versions.list_by_policy(tenant_id, str(policy.id))
            active = next((v for v in versions if v.status == PolicyStatus.ACTIVE), None)
            items.append(
                {
                    **policy.to_dict(),
                    "active_version": active.version if active else None,
                    "version_count": len(versions),
                }
            )
        return Result.ok(items)

    async def get_policy(self, tenant_id: str, policy_id: str) -> Result[dict]:
        policy = await self._policies.find_by_id(tenant_id, UniqueId.from_string(policy_id))
        if not policy:
            return Result.fail("policy.errors.not_found")
        versions = await self._versions.list_by_policy(tenant_id, policy_id)
        active = next((v for v in versions if v.status == PolicyStatus.ACTIVE), None)
        return Result.ok(
            {
                **policy.to_dict(),
                "active_version": active.to_dict() if active else None,
                "versions": [v.to_dict() for v in sorted(versions, key=lambda x: x.version)],
            }
        )

    async def list_versions(self, tenant_id: str, policy_id: str) -> Result[list[dict]]:
        policy = await self._policies.find_by_id(tenant_id, UniqueId.from_string(policy_id))
        if not policy:
            return Result.fail("policy.errors.not_found")
        versions = await self._versions.list_by_policy(tenant_id, policy_id)
        return Result.ok([v.to_dict() for v in sorted(versions, key=lambda x: x.version)])

    async def create_policy(
        self,
        *,
        tenant_id: str,
        domain: str,
        key: str,
        name: str,
        description: str | None,
        effective_from: datetime,
        priority: int,
        conditions: list[dict],
        rules: list[dict],
        exceptions: list[dict] | None,
        expires_at: datetime | None,
        approval_required: bool,
        actor_id: str | None,
    ) -> Result[dict]:
        existing = await self._policies.find_by_key(tenant_id, domain, key)
        if existing:
            return Result.fail("policy.errors.key_exists")

        policy = Policy.create(
            tenant_id=tenant_id,
            domain=domain,
            key=key,
            name=name,
            description=description,
        )
        version = PolicyVersion.create_draft(
            policy_id=str(policy.id),
            tenant_id=tenant_id,
            version=1,
            effective_from=effective_from,
            priority=priority,
            conditions=conditions,
            rules=rules,
            exceptions=exceptions,
            expires_at=expires_at,
            approval_required=approval_required,
            workflow_key=f"policy.{domain}.{key}.publish",
            metadata={"created_by": actor_id} if actor_id else {},
        )
        await self._policies.save(policy)
        await self._versions.save(version)
        return Result.ok({**policy.to_dict(), "draft_version": version.to_dict()})

    async def create_version(
        self,
        *,
        tenant_id: str,
        policy_id: str,
        effective_from: datetime,
        priority: int,
        conditions: list[dict],
        rules: list[dict],
        exceptions: list[dict] | None,
        expires_at: datetime | None,
        approval_required: bool,
        actor_id: str | None,
        change_reason: str | None,
    ) -> Result[dict]:
        policy = await self._policies.find_by_id(tenant_id, UniqueId.from_string(policy_id))
        if not policy:
            return Result.fail("policy.errors.not_found")

        next_ver = await self._versions.next_version_number(tenant_id, policy_id)
        version = PolicyVersion.create_draft(
            policy_id=policy_id,
            tenant_id=tenant_id,
            version=next_ver,
            effective_from=effective_from,
            priority=priority,
            conditions=conditions,
            rules=rules,
            exceptions=exceptions,
            expires_at=expires_at,
            approval_required=approval_required,
            workflow_key=f"policy.{policy.domain}.{policy.key}.publish",
            metadata={
                **({"created_by": actor_id} if actor_id else {}),
                **({"change_reason": change_reason} if change_reason else {}),
            },
        )
        await self._versions.save(version)
        return Result.ok(version.to_dict())

    async def update_draft_version(
        self,
        *,
        tenant_id: str,
        policy_id: str,
        version: int,
        effective_from: datetime | None,
        expires_at: datetime | None,
        priority: int | None,
        conditions: list[dict] | None,
        rules: list[dict] | None,
        exceptions: list[dict] | None,
    ) -> Result[dict]:
        ver = await self._versions.find_by_policy_and_version(tenant_id, policy_id, version)
        if not ver:
            return Result.fail("policy.errors.version_not_found")
        try:
            ver.update_draft(
                effective_from=effective_from,
                expires_at=expires_at,
                priority=priority,
                conditions=conditions,
                rules=rules,
                exceptions=exceptions,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._versions.save(ver)
        return Result.ok(ver.to_dict())

    async def evaluate(
        self,
        *,
        tenant_id: str,
        domain: str,
        policy_key: str,
        facts: dict,
        as_of: datetime | None = None,
    ) -> Result[dict]:
        as_of = as_of or datetime.now(UTC)
        version = await self._versions.find_active_for_key(tenant_id, domain, policy_key, as_of)
        if not version:
            await publish_integration_event(
                EvaluationDeniedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=f"policy-deny-{domain}-{policy_key}",
                    domain=domain,
                    policy_key=policy_key,
                    reason="no_active_policy",
                )
            )
            return Result.ok(
                {
                    "matched": False,
                    "policy_id": None,
                    "version": None,
                    "outcome": None,
                    "parameters": {},
                    "applied_exception": None,
                    "evaluation_trace": [{"step": "lookup", "result": False}],
                }
            )
        result = evaluate_version(version, facts, as_of=as_of, require_active=True)
        return Result.ok(result)

    async def simulate(
        self,
        *,
        tenant_id: str,
        domain: str,
        policy_key: str,
        facts: dict,
        candidate_versions: list[int] | None,
        as_of: datetime | None,
        correlation_id: str,
    ) -> Result[dict]:
        policy = await self._policies.find_by_key(tenant_id, domain, policy_key)
        if not policy:
            return Result.fail("policy.errors.not_found")

        versions = await self._versions.list_by_policy(tenant_id, str(policy.id))
        if candidate_versions:
            versions = [v for v in versions if v.version in candidate_versions]

        comparisons = [
            evaluate_version(v, facts, as_of=as_of, require_active=False) for v in versions
        ]
        await publish_integration_event(
            SimulationExecutedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                domain=domain,
                policy_key=policy_key,
                version_count=len(comparisons),
            )
        )
        return Result.ok({"policy_id": str(policy.id), "comparisons": comparisons})

    async def run_tests(
        self, tenant_id: str, policy_id: str, version: int, test_cases: list[dict]
    ) -> Result[dict]:
        ver = await self._versions.find_by_policy_and_version(tenant_id, policy_id, version)
        if not ver:
            return Result.fail("policy.errors.version_not_found")
        results = run_test_cases(ver, test_cases)
        passed = all(r["passed"] for r in results)
        return Result.ok({"passed": passed, "results": results})

    async def submit_approval(
        self,
        *,
        tenant_id: str,
        policy_id: str,
        version: int,
        correlation_id: str,
        actor_id: str | None,
    ) -> Result[dict]:
        policy = await self._policies.find_by_id(tenant_id, UniqueId.from_string(policy_id))
        if not policy:
            return Result.fail("policy.errors.not_found")
        ver = await self._versions.find_by_policy_and_version(tenant_id, policy_id, version)
        if not ver:
            return Result.fail("policy.errors.version_not_found")
        try:
            ver.submit_for_approval()
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._versions.save(ver)
        await publish_integration_event(
            VersionSubmittedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                actor_user_id=actor_id,
                policy_id=policy_id,
                version=version,
                domain=policy.domain,
                policy_key=policy.key,
            )
        )
        return Result.ok(ver.to_dict())

    async def activate_version(
        self, tenant_id: str, policy_id: str, version: int, *, actor_id: str | None = None
    ) -> Result[dict]:
        try:
            ver = await self._activate_version(tenant_id, policy_id, version, actor_id=actor_id)
        except ValueError as exc:
            return Result.fail(str(exc))
        return Result.ok(ver.to_dict())

    async def rollback(
        self,
        *,
        tenant_id: str,
        policy_id: str,
        target_version: int,
        reason: str,
        correlation_id: str,
        actor_id: str | None,
    ) -> Result[dict]:
        policy = await self._policies.find_by_id(tenant_id, UniqueId.from_string(policy_id))
        if not policy:
            return Result.fail("policy.errors.not_found")

        target = await self._versions.find_by_policy_and_version(
            tenant_id, policy_id, target_version
        )
        if not target:
            return Result.fail("policy.errors.version_not_found")

        versions = await self._versions.list_by_policy(tenant_id, policy_id)
        current = next((v for v in versions if v.status == PolicyStatus.ACTIVE), None)
        from_version = current.version if current else target_version

        if current:
            current.mark_rolled_back()
            await self._versions.save(current)

        await self._versions.supersede_active(tenant_id, policy_id, except_version=target_version)
        target.activate()
        target.metadata = {**target.metadata, "rollback_reason": reason, "rolled_back_by": actor_id}
        await self._versions.save(target)

        await publish_integration_event(
            VersionRolledBackIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                actor_user_id=actor_id,
                policy_id=policy_id,
                from_version=from_version,
                to_version=target_version,
                reason=reason,
            )
        )
        return Result.ok(target.to_dict())

    async def get_history(self, tenant_id: str, policy_id: str) -> Result[list[dict]]:
        policy = await self._policies.find_by_id(tenant_id, UniqueId.from_string(policy_id))
        if not policy:
            return Result.fail("policy.errors.not_found")
        versions = await self._versions.list_by_policy(tenant_id, policy_id)
        history = []
        for ver in sorted(versions, key=lambda v: v.version):
            history.append(
                {
                    "version": ver.version,
                    "status": ver.status.value,
                    "effective_from": ver.effective_from.isoformat(),
                    "metadata": ver.metadata,
                    "created_at": ver.created_at.isoformat(),
                }
            )
        return Result.ok(history)

    async def _activate_version(
        self, tenant_id: str, policy_id: str, version: int, *, actor_id: str | None
    ) -> PolicyVersion:
        policy = await self._policies.find_by_id(tenant_id, UniqueId.from_string(policy_id))
        if not policy:
            raise ValueError("policy.errors.not_found")
        ver = await self._versions.find_by_policy_and_version(tenant_id, policy_id, version)
        if not ver:
            raise ValueError("policy.errors.version_not_found")
        await self._versions.supersede_active(tenant_id, policy_id, except_version=version)
        ver.activate()
        if actor_id:
            ver.metadata = {**ver.metadata, "approved_by": actor_id}
        await self._versions.save(ver)
        await publish_integration_event(
            VersionActivatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"policy-activate-{policy_id}-v{version}",
                actor_user_id=actor_id,
                policy_id=policy_id,
                version=version,
                domain=policy.domain,
                policy_key=policy.key,
            )
        )
        return ver

    async def _create_policy_from_template(
        self,
        *,
        tenant_id: str,
        domain: str,
        template: dict,
        activate: bool,
    ) -> None:
        policy = Policy.create(
            tenant_id=tenant_id,
            domain=domain,
            key=template["key"],
            name=template["name"],
        )
        version = PolicyVersion.create_draft(
            policy_id=str(policy.id),
            tenant_id=tenant_id,
            version=1,
            effective_from=default_effective_from(),
            priority=template.get("priority", 100),
            conditions=template.get("conditions", []),
            rules=template.get("rules", []),
            exceptions=template.get("exceptions"),
            approval_required=template.get("approval_required", False),
            metadata={"seeded": True},
        )
        if activate and not version.approval_required:
            version.activate()
        await self._policies.save(policy)
        await self._versions.save(version)
        if version.status == PolicyStatus.ACTIVE:
            await publish_integration_event(
                VersionActivatedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=f"policy-seed-{policy.key}",
                    policy_id=str(policy.id),
                    version=1,
                    domain=domain,
                    policy_key=policy.key,
                )
            )
