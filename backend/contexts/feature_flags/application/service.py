"""Feature flag application service."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.feature_flags.application.constants.default_flags import DEFAULT_FLAGS
from contexts.feature_flags.domain.aggregates.feature_flag import FeatureFlag
from contexts.feature_flags.domain.events.integration_events import (
    EmergencyDisabledIntegration,
    FlagCreatedIntegration,
    FlagUpdatedIntegration,
    RollbackAppliedIntegration,
    RolloutUpdatedIntegration,
)
from contexts.feature_flags.domain.ports.repositories import IFeatureFlagRepository
from contexts.feature_flags.domain.services.evaluator import evaluate_flag
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class FeatureFlagApplicationService:
    def __init__(self, flags: IFeatureFlagRepository) -> None:
        self._flags = flags

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        industry_pack = (envelope.get("payload") or {}).get("industry_pack", "")
        for key, name, default_enabled, industry_overrides in DEFAULT_FLAGS:
            if await self._flags.exists(tenant_id, key):
                continue
            rules = {}
            if industry_overrides and industry_pack in industry_overrides:
                rules[industry_pack] = industry_overrides[industry_pack]
            flag = FeatureFlag.create(
                tenant_id=tenant_id,
                key=key,
                name=name,
                default_enabled=default_enabled,
                industry_rules=rules,
            )
            await self._flags.save(flag)
            await publish_integration_event(
                FlagCreatedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=f"flag-seed-{key}",
                    flag_key=key,
                )
            )

    async def list_flags(self, tenant_id: str) -> Result[list[dict]]:
        flags = await self._flags.list_by_tenant(tenant_id)
        return Result.ok([f.to_dict() for f in sorted(flags, key=lambda x: x.key)])

    async def get_flag(self, tenant_id: str, key: str) -> Result[dict]:
        flag = await self._flags.find_by_key(tenant_id, key)
        if not flag:
            return Result.fail("feature_flags.errors.not_found")
        data = flag.to_dict()
        data["history"] = flag.history
        return Result.ok(data)

    async def create_flag(
        self,
        *,
        tenant_id: str,
        key: str,
        name: str,
        default_enabled: bool,
        correlation_id: str,
    ) -> Result[dict]:
        if await self._flags.exists(tenant_id, key):
            return Result.fail("feature_flags.errors.key_exists")
        flag = FeatureFlag.create(
            tenant_id=tenant_id, key=key, name=name, default_enabled=default_enabled
        )
        await self._flags.save(flag)
        await publish_integration_event(
            FlagCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                flag_key=key,
            )
        )
        return Result.ok(flag.to_dict())

    async def update_flag(
        self,
        *,
        tenant_id: str,
        key: str,
        default_enabled: bool | None = None,
        tenant_rules: dict | None = None,
        organization_rules: dict | None = None,
        user_rules: dict | None = None,
        environment_rules: dict | None = None,
        country_rules: dict | None = None,
        industry_rules: dict | None = None,
        correlation_id: str,
    ) -> Result[dict]:
        flag = await self._flags.find_by_key(tenant_id, key)
        if not flag:
            return Result.fail("feature_flags.errors.not_found")
        if default_enabled is not None:
            flag.default_enabled = default_enabled
        if tenant_rules is not None:
            flag.tenant_rules = tenant_rules
        if organization_rules is not None:
            flag.organization_rules = organization_rules
        if user_rules is not None:
            flag.user_rules = user_rules
        if environment_rules is not None:
            flag.environment_rules = environment_rules
        if country_rules is not None:
            flag.country_rules = country_rules
        if industry_rules is not None:
            flag.industry_rules = industry_rules
        flag.bump_version("updated")
        await self._flags.save(flag)
        await publish_integration_event(
            FlagUpdatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                flag_key=key,
                version=flag.version,
            )
        )
        return Result.ok(flag.to_dict())

    async def evaluate(
        self, tenant_id: str, keys: list[str], context: dict | None = None
    ) -> Result[dict]:
        ctx = dict(context or {})
        ctx.setdefault("tenant_id", tenant_id)
        results = {}
        for key in keys:
            flag = await self._flags.find_by_key(tenant_id, key)
            if not flag:
                results[key] = {
                    "enabled": False,
                    "variant_id": None,
                    "reason": "default",
                    "flag_version": 0,
                }
                continue
            results[key] = evaluate_flag(flag, ctx)
        return Result.ok(results)

    async def update_rollout(
        self, tenant_id: str, key: str, percentage: int, stage: str, correlation_id: str
    ) -> Result[dict]:
        flag = await self._flags.find_by_key(tenant_id, key)
        if not flag:
            return Result.fail("feature_flags.errors.not_found")
        flag.update_rollout(percentage, stage)
        await self._flags.save(flag)
        await publish_integration_event(
            RolloutUpdatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                flag_key=key,
                percentage=percentage,
                stage=stage,
            )
        )
        return Result.ok(flag.to_dict())

    async def configure_ab_test(
        self, tenant_id: str, key: str, variants: list[dict], correlation_id: str
    ) -> Result[dict]:
        flag = await self._flags.find_by_key(tenant_id, key)
        if not flag:
            return Result.fail("feature_flags.errors.not_found")
        flag.configure_ab_test(variants)
        await self._flags.save(flag)
        await publish_integration_event(
            FlagUpdatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                flag_key=key,
                version=flag.version,
            )
        )
        return Result.ok(flag.to_dict())

    async def emergency_disable(
        self, tenant_id: str, key: str, reason: str, correlation_id: str
    ) -> Result[dict]:
        flag = await self._flags.find_by_key(tenant_id, key)
        if not flag:
            return Result.fail("feature_flags.errors.not_found")
        flag.set_emergency_disable(reason)
        await self._flags.save(flag)
        await publish_integration_event(
            EmergencyDisabledIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                flag_key=key,
                reason=reason,
            )
        )
        return Result.ok(flag.to_dict())

    async def emergency_enable(
        self, tenant_id: str, key: str, correlation_id: str
    ) -> Result[dict]:
        flag = await self._flags.find_by_key(tenant_id, key)
        if not flag:
            return Result.fail("feature_flags.errors.not_found")
        flag.clear_emergency_disable()
        await self._flags.save(flag)
        await publish_integration_event(
            FlagUpdatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                flag_key=key,
                version=flag.version,
            )
        )
        return Result.ok(flag.to_dict())

    async def get_history(self, tenant_id: str, key: str) -> Result[list[dict]]:
        flag = await self._flags.find_by_key(tenant_id, key)
        if not flag:
            return Result.fail("feature_flags.errors.not_found")
        return Result.ok(flag.history)

    async def rollback(
        self, tenant_id: str, key: str, target_version: int, correlation_id: str
    ) -> Result[dict]:
        flag = await self._flags.find_by_key(tenant_id, key)
        if not flag:
            return Result.fail("feature_flags.errors.not_found")
        if not flag.rollback_to(target_version):
            return Result.fail("feature_flags.errors.version_not_found")
        await self._flags.save(flag)
        await publish_integration_event(
            RollbackAppliedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                flag_key=key,
                target_version=target_version,
            )
        )
        return Result.ok(flag.to_dict())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        flags = await self._flags.list_by_tenant(tenant_id)
        cutoff = datetime.now(UTC) - timedelta(hours=24)
        recent = []
        for flag in flags:
            for entry in flag.history:
                updated = entry.get("updated_at")
                if updated and updated >= cutoff.isoformat():
                    recent.append({"flag_key": flag.key, **entry})
        scope_counts = {
            "tenant": sum(1 for f in flags if f.tenant_rules),
            "organization": sum(1 for f in flags if f.organization_rules),
            "user": sum(1 for f in flags if f.user_rules),
            "environment": sum(1 for f in flags if f.environment_rules),
            "country": sum(1 for f in flags if f.country_rules),
            "industry": sum(1 for f in flags if f.industry_rules),
        }
        return Result.ok(
            {
                "total_flags": len(flags),
                "emergency_disabled": sum(1 for f in flags if f.emergency_disabled),
                "canary_active": sum(1 for f in flags if f.rollout_stage == "canary"),
                "ab_tests_running": sum(1 for f in flags if f.ab_test_enabled),
                "scope_breakdown": scope_counts,
                "recent_changes": sorted(recent, key=lambda x: x.get("updated_at", ""), reverse=True)[:20],
                "flags": [f.to_dict() for f in flags],
            }
        )
