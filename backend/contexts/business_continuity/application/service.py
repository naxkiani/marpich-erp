"""Enterprise Business Continuity Platform application service."""
from __future__ import annotations

from contexts.business_continuity.domain.aggregates.continuity_platform import (
    BackupStrategy,
    ContinuityPlan,
    ContinuityTenantProfile,
    CriticalityTier,
    FailoverRecord,
    PlanType,
    RecoveryTest,
)
from contexts.business_continuity.domain.events.continuity_integration_events import (
    ContinuityPlanCreatedIntegration,
    EmergencyOpsActivatedIntegration,
    FailoverCompletedIntegration,
    FailoverInitiatedIntegration,
    RecoveryTestCompletedIntegration,
)
from contexts.business_continuity.domain.ports.continuity_repositories import (
    IBackupStrategyRepository,
    IContinuityPlanRepository,
    IContinuityTenantProfileRepository,
    IFailoverRecordRepository,
    IRecoveryTestRepository,
)
from contexts.business_continuity.domain.services import continuity_engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BusinessContinuityApplicationService:
    def __init__(
        self,
        profiles: IContinuityTenantProfileRepository,
        plans: IContinuityPlanRepository,
        backups: IBackupStrategyRepository,
        failovers: IFailoverRecordRepository,
        tests: IRecoveryTestRepository,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._plans = plans
        self._backups = backups
        self._failovers = failovers
        self._tests = tests
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        params = {
            "default_rpo_hours": 4,
            "default_rto_hours": 8,
            "auto_trigger_threshold": 3,
            "test_frequency_days": 90,
            "replication_lag_threshold": 30,
        }
        pmap = {
            "continuity.rpo.default_hours": ("default_rpo_hours", "default_hours"),
            "continuity.rto.default_hours": ("default_rto_hours", "default_hours"),
            "continuity.failover.auto_trigger_threshold": ("auto_trigger_threshold", "threshold"),
            "continuity.testing.frequency_days": ("test_frequency_days", "frequency_days"),
            "continuity.ha.replication_lag_threshold": ("replication_lag_threshold", "lag_threshold"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(
                tenant_id=tenant_id, domain="tax", policy_key=key, facts={}
            )
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": continuity_engine.list_capability_catalog(),
            "criticality_tiers": continuity_engine.list_criticality_tiers(),
            "policy_keys": continuity_engine.list_policy_keys(),
            "shared_service": True,
            "delegation": {
                "data_protection_backup_encryption": True,
                "security_incident_emergency_ops": True,
                "workflow_emergency_lock": True,
                "local_continuity_duplication": False,
            },
        })

    async def get_dependency_map(self) -> Result[dict]:
        return Result.ok(continuity_engine.dependency_map())

    async def seed(self, tenant_id: str) -> Result[dict]:
        existing = await self._profiles.find_by_tenant(tenant_id)
        if existing:
            return Result.ok({
                "seeded": False,
                "profile": existing.to_dict(),
                "plans": len(await self._plans.list_by_tenant(tenant_id)),
            })

        params = await self._policy_params(tenant_id)
        ref = self._profiles.next_profile_ref(tenant_id)
        profile = ContinuityTenantProfile.create(
            tenant_id=tenant_id,
            profile_ref=ref,
            enabled_tiers=[t.value for t in CriticalityTier],
        )
        profile.default_rpo_hours = int(params.get("default_rpo_hours", 4))
        profile.default_rto_hours = int(params.get("default_rto_hours", 8))
        profile.test_frequency_days = int(params.get("test_frequency_days", 90))
        await self._profiles.save(profile)

        plans_seeded = 0
        for seed_plan in continuity_engine.DEFAULT_SEED_PLANS:
            plan_ref = self._plans.next_plan_ref(tenant_id)
            plan = ContinuityPlan.create(
                tenant_id=tenant_id,
                plan_ref=plan_ref,
                title=seed_plan["title"],
                plan_type=seed_plan["plan_type"],
                criticality_tier=seed_plan["criticality_tier"],
                rpo_hours=seed_plan["rpo_hours"],
                rto_hours=seed_plan["rto_hours"],
                recovery_steps=seed_plan.get("recovery_steps", []),
                delegated_to=seed_plan.get("delegated_to"),
            )
            await self._plans.save(plan)
            plans_seeded += 1

        backups_seeded = 0
        for seed_backup in continuity_engine.DEFAULT_SEED_BACKUPS:
            strategy_ref = self._backups.next_strategy_ref(tenant_id)
            strategy = BackupStrategy.define(
                tenant_id=tenant_id,
                strategy_ref=strategy_ref,
                name=seed_backup["name"],
                backup_type=seed_backup["backup_type"],
                frequency_hours=seed_backup["frequency_hours"],
                retention_days=seed_backup["retention_days"],
                rpo_hours=seed_backup["rpo_hours"],
            )
            await self._backups.save(strategy)
            backups_seeded += 1

        return Result.ok({
            "seeded": True,
            "profile": profile.to_dict(),
            "plans_seeded": plans_seeded,
            "backups_seeded": backups_seeded,
            "enabled_tiers": len(profile.enabled_tiers),
        })

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = await self._policy_params(tenant_id)
        plans = [p.to_dict() for p in await self._plans.list_by_tenant(tenant_id)]
        backups = [b.to_dict() for b in await self._backups.list_by_tenant(tenant_id)]
        failovers = [f.to_dict() for f in await self._failovers.list_by_tenant(tenant_id)]
        tests = [t.to_dict() for t in await self._tests.list_by_tenant(tenant_id)]
        return Result.ok(
            continuity_engine.build_dashboard(
                profile=profile.to_dict() if profile else None,
                plans=plans,
                backups=backups,
                failovers=failovers,
                tests=tests,
                lag_threshold=int(params.get("replication_lag_threshold", 30)),
            )
        )

    async def list_plans(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._plans.list_by_tenant(tenant_id)
        return Result.ok([p.to_dict() for p in items])

    async def create_plan(
        self,
        tenant_id: str,
        *,
        title: str,
        plan_type: str,
        criticality_tier: str,
        rpo_hours: int | None = None,
        rto_hours: int | None = None,
        recovery_steps: list[str] | None = None,
        owner_id: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        if plan_type not in {t.value for t in PlanType}:
            return Result.fail("invalid_plan_type")
        if criticality_tier not in {t.value for t in CriticalityTier}:
            return Result.fail("invalid_criticality_tier")

        params = await self._policy_params(tenant_id)
        profile = await self._profiles.find_by_tenant(tenant_id)
        default_rpo = profile.default_rpo_hours if profile else int(params.get("default_rpo_hours", 4))
        default_rto = profile.default_rto_hours if profile else int(params.get("default_rto_hours", 8))

        plan_ref = self._plans.next_plan_ref(tenant_id)
        plan = ContinuityPlan.create(
            tenant_id=tenant_id,
            plan_ref=plan_ref,
            title=title,
            plan_type=plan_type,
            criticality_tier=criticality_tier,
            rpo_hours=rpo_hours if rpo_hours is not None else default_rpo,
            rto_hours=rto_hours if rto_hours is not None else default_rto,
            recovery_steps=recovery_steps or [],
            owner_id=owner_id,
        )
        await self._plans.save(plan)

        corr = correlation_id or plan_ref
        await publish_integration_event(
            ContinuityPlanCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                plan_ref=plan_ref,
                plan_type=plan_type,
                criticality_tier=criticality_tier,
            )
        )
        return Result.ok(plan.to_dict())

    async def list_backups(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._backups.list_by_tenant(tenant_id)
        return Result.ok([b.to_dict() for b in items])

    async def create_backup(
        self,
        tenant_id: str,
        *,
        name: str,
        backup_type: str,
        frequency_hours: int,
        retention_days: int,
        rpo_hours: int,
        encrypted: bool = True,
    ) -> Result[dict]:
        strategy_ref = self._backups.next_strategy_ref(tenant_id)
        strategy = BackupStrategy.define(
            tenant_id=tenant_id,
            strategy_ref=strategy_ref,
            name=name,
            backup_type=backup_type,
            frequency_hours=frequency_hours,
            retention_days=retention_days,
            rpo_hours=rpo_hours,
            encrypted=encrypted,
        )
        await self._backups.save(strategy)
        return Result.ok(strategy.to_dict())

    async def get_rpo_rto(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        plans = [p.to_dict() for p in await self._plans.list_by_tenant(tenant_id)]
        backups = [b.to_dict() for b in await self._backups.list_by_tenant(tenant_id)]
        return Result.ok(
            continuity_engine.build_rpo_rto_summary(
                plans=plans,
                backups=backups,
                profile=profile.to_dict() if profile else None,
            )
        )

    async def get_high_availability(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        failovers = [f.to_dict() for f in await self._failovers.list_by_tenant(tenant_id)]
        return Result.ok(
            continuity_engine.compute_ha_status(
                profile=profile.to_dict() if profile else None,
                failovers=failovers,
            )
        )

    async def get_replication(self, tenant_id: str) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        backups = [b.to_dict() for b in await self._backups.list_by_tenant(tenant_id)]
        return Result.ok(
            continuity_engine.compute_replication_status(
                strategies=backups,
                lag_threshold_seconds=int(params.get("replication_lag_threshold", 30)),
            )
        )

    async def initiate_failover(
        self,
        tenant_id: str,
        *,
        source_system: str,
        target_system: str,
        trigger_reason: str,
        initiated_by: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        profile = await self._profiles.find_by_tenant(tenant_id)
        rto_target = profile.default_rto_hours if profile else int(params.get("default_rto_hours", 8))

        failover_ref = self._failovers.next_failover_ref(tenant_id)
        record = FailoverRecord.initiate(
            tenant_id=tenant_id,
            failover_ref=failover_ref,
            source_system=source_system,
            target_system=target_system,
            trigger_reason=trigger_reason,
            rto_target_hours=rto_target,
            initiated_by=initiated_by,
        )
        record.complete()
        await self._failovers.save(record)

        corr = correlation_id or failover_ref
        await publish_integration_event(
            FailoverInitiatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                failover_ref=failover_ref,
                source_system=source_system,
                target_system=target_system,
            )
        )
        await publish_integration_event(
            FailoverCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                failover_ref=failover_ref,
                status=record.status,
            )
        )
        return Result.ok(record.to_dict())

    async def list_failovers(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._failovers.list_by_tenant(tenant_id)
        return Result.ok([f.to_dict() for f in items])

    async def activate_emergency_ops(
        self,
        tenant_id: str,
        *,
        plan_ref: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        plan = None
        if plan_ref:
            plan = await self._plans.find_by_ref(tenant_id, plan_ref)
        else:
            plans = await self._plans.list_by_tenant(tenant_id)
            for p in plans:
                if p.plan_type == PlanType.EMERGENCY_OPS.value:
                    plan = p
                    break

        if not plan:
            return Result.fail("emergency_ops_plan_not_found")

        corr = correlation_id or plan.plan_ref
        await publish_integration_event(
            EmergencyOpsActivatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                plan_ref=plan.plan_ref,
                title=plan.title,
            )
        )
        return Result.ok({
            "activated": True,
            "plan": plan.to_dict(),
            "delegates_to": "security_incident",
            "workflow_emergency_lock_available": True,
        })

    async def schedule_test(
        self,
        tenant_id: str,
        *,
        plan_ref: str,
        test_type: str = "full",
        executed_by: str = "",
    ) -> Result[dict]:
        plan = await self._plans.find_by_ref(tenant_id, plan_ref)
        if not plan:
            return Result.fail("plan_not_found")

        test_ref = self._tests.next_test_ref(tenant_id)
        test = RecoveryTest.schedule(
            tenant_id=tenant_id,
            test_ref=test_ref,
            plan_ref=plan_ref,
            test_type=test_type,
            executed_by=executed_by,
        )
        await self._tests.save(test)
        return Result.ok(test.to_dict())

    async def run_test(
        self,
        tenant_id: str,
        test_ref: str,
        *,
        correlation_id: str = "",
    ) -> Result[dict]:
        tests = await self._tests.list_by_tenant(tenant_id)
        test = next((t for t in tests if t.test_ref == test_ref), None)
        if not test:
            return Result.fail("test_not_found")

        plan = await self._plans.find_by_ref(tenant_id, test.plan_ref)
        if not plan:
            return Result.fail("plan_not_found")

        simulation = continuity_engine.simulate_recovery_test(
            plan=plan.to_dict(), test_type=test.test_type
        )
        test.run(
            rto_achieved=simulation["rto_achieved_hours"],
            rpo_achieved=simulation["rpo_achieved_hours"],
            rto_target=simulation["rto_target_hours"],
            rpo_target=simulation["rpo_target_hours"],
        )
        test.findings = simulation.get("findings", [])
        await self._tests.save(test)

        corr = correlation_id or test_ref
        await publish_integration_event(
            RecoveryTestCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                test_ref=test_ref,
                plan_ref=test.plan_ref,
                passed=test.passed,
            )
        )
        return Result.ok(test.to_dict())

    async def list_tests(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._tests.list_by_tenant(tenant_id)
        return Result.ok([t.to_dict() for t in items])

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope.get("tenant_id", "")
        if tenant_id:
            await self.seed(tenant_id)
