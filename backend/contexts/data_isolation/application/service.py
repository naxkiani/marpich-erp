"""Data isolation application service."""
from __future__ import annotations

import uuid

from contexts.data_isolation.domain.aggregates.data_isolation_platform import IsolationProfile, Principal
from contexts.data_isolation.domain.events.data_isolation_integration_events import (
    PrincipalSyncedIntegration,
    RlsVerifiedIntegration,
)
from contexts.data_isolation.domain.ports.data_isolation_repositories import (
    IIdentityPrincipalSource,
    IIsolationProfileRepository,
    IPrincipalRepository,
)
from contexts.data_isolation.domain.services import data_isolation_engine as engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.database.rls_context import get_current_principal_id, get_current_tenant_id
from shared.infrastructure.messaging.event_bus import publish_integration_event
from shared.infrastructure.settings import settings, use_rls


class DataIsolationApplicationService:
    def __init__(
        self,
        profiles: IIsolationProfileRepository,
        principals: IPrincipalRepository,
        identity_source: IIdentityPrincipalSource,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._principals = principals
        self._identity = identity_source
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "rls_enabled": profile.rls_enabled if profile else True,
            "principal_partitioning_enabled": True,
            "tenant_context_required": profile.enforce_tenant_context if profile else True,
        }
        pmap = {
            "data_isolation.rls.enabled": ("rls_enabled", "enabled"),
            "data_isolation.principal_partitioning.enabled": ("principal_partitioning_enabled", "enabled"),
            "data_isolation.tenant_context.required": ("tenant_context_required", "required"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> IsolationProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = IsolationProfile.create(
            tenant_id=tenant_id,
            profile_ref=self._profiles.next_profile_ref(tenant_id),
            partition_modulus=settings.marpich_principal_partition_modulus,
        )
        await self._profiles.save(profile)
        return profile

    async def handle_tenant_provisioned(self, event: dict) -> None:
        tenant_id = event.get("tenant_id") or event.get("payload", {}).get("tenant_id")
        if tenant_id:
            await self.seed(tenant_id)

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": engine.list_capability_catalog(),
            "policy_keys": engine.list_policy_keys(),
            "rls_policies": engine.list_rls_policies(),
            "dependency_map": engine.dependency_map(),
            "runtime": {
                "postgres_rls_enabled": use_rls(),
                "partition_modulus": settings.marpich_principal_partition_modulus,
            },
        })

    async def seed(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        return Result.ok({"seeded": True, "profile_ref": profile.profile_ref})

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        principal_rows = await self._principals.list_by_tenant(tenant_id)
        dashboard = engine.build_dashboard(
            profile=profile.to_dict(),
            principals=[p.to_dict() for p in principal_rows],
            policies=engine.list_rls_policies(),
            partition_modulus=profile.principal_partition_modulus,
        )
        return Result.ok(dashboard)

    async def list_principals(self, tenant_id: str) -> Result[list[dict]]:
        rows = await self._principals.list_by_tenant(tenant_id)
        return Result.ok([row.to_dict() for row in rows])

    async def sync_principals(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        users = await self._identity.list_users(tenant_id)
        created = 0
        synced = 0
        for user in users:
            synced += 1
            user_id = str(user.get("id", ""))
            if not user_id:
                continue
            existing = await self._principals.find_by_user_id(tenant_id, user_id)
            if existing:
                continue
            bucket = engine.partition_bucket(tenant_id, profile.principal_partition_modulus)
            principal = Principal.register_user(
                tenant_id=tenant_id,
                principal_ref=self._principals.next_principal_ref(tenant_id),
                user_id=user_id,
                email=str(user.get("email", "")),
                display_name=str(user.get("display_name", user.get("email", "User"))),
                partition_bucket=bucket,
            )
            await self._principals.save(principal)
            created += 1
        await publish_integration_event(
            PrincipalSyncedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                synced_count=synced,
                created_count=created,
            )
        )
        return Result.ok({"synced": synced, "created": created})

    async def verify_isolation(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        policies = engine.list_rls_policies()
        bound_tenant = get_current_tenant_id()
        bound_principal = get_current_principal_id()
        passed = True
        checks = []
        for item in policies:
            ok = profile.rls_enabled
            checks.append({**item, "configured": ok})
            passed = passed and ok
        if profile.enforce_tenant_context and use_rls():
            context_ok = bound_tenant == tenant_id.lower()
            checks.append({
                "check": "tenant_context_bound",
                "expected": tenant_id.lower(),
                "actual": bound_tenant,
                "passed": context_ok,
            })
            passed = passed and context_ok
        await publish_integration_event(
            RlsVerifiedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                tenant_id_checked=tenant_id,
                policies_checked=len(policies),
                passed=passed,
            )
        )
        return Result.ok({
            "tenant_id": tenant_id,
            "passed": passed,
            "rls_enabled": profile.rls_enabled,
            "postgres_rls_runtime": use_rls(),
            "tenant_context": {"tenant_id": bound_tenant, "principal_id": bound_principal},
            "checks": checks,
        })

    async def get_partition_map(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        principals = await self._principals.list_by_tenant(tenant_id)
        distribution: dict[int, int] = {}
        for principal in principals:
            distribution[principal.partition_bucket] = distribution.get(principal.partition_bucket, 0) + 1
        return Result.ok({
            "tenant_id": tenant_id,
            "partition_modulus": profile.principal_partition_modulus,
            "tenant_bucket": engine.partition_bucket(tenant_id, profile.principal_partition_modulus),
            "distribution": distribution,
            "principals_total": len(principals),
        })
