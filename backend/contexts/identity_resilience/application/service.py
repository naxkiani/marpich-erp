"""Identity resilience application service."""
from __future__ import annotations

import uuid

from contexts.identity_resilience.domain.aggregates.identity_resilience_platform import (
    FailoverEvent,
    RegionDescriptor,
    ResilienceProfile,
    WorkerDeployment,
    WorkerRole,
    WorkerType,
)
from contexts.identity_resilience.domain.events.identity_resilience_integration_events import (
    FailoverCompletedIntegration,
    FailoverInitiatedIntegration,
    RegionHealthChangedIntegration,
    WorkerRegisteredIntegration,
)
from contexts.identity_resilience.domain.ports.identity_resilience_repositories import (
    IDirectoryWorkerPort,
    IFailoverEventRepository,
    IRegionRepository,
    IRiskWorkerPort,
    IResilienceProfileRepository,
    IWorkerDeploymentRepository,
)
from contexts.identity_resilience.domain.services import identity_resilience_engine as engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event
from shared.infrastructure.settings import settings


class IdentityResilienceApplicationService:
    def __init__(
        self,
        profiles: IResilienceProfileRepository,
        regions: IRegionRepository,
        workers: IWorkerDeploymentRepository,
        failovers: IFailoverEventRepository,
        directory_workers: IDirectoryWorkerPort,
        risk_workers: IRiskWorkerPort,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._regions = regions
        self._workers = workers
        self._failovers = failovers
        self._directory_workers = directory_workers
        self._risk_workers = risk_workers
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "multi_region_enabled": profile.multi_region_enabled if profile else True,
            "auto_failover": profile.auto_failover if profile else True,
            "heartbeat_timeout_seconds": profile.heartbeat_timeout_seconds if profile else 60,
            "replication_lag_threshold_seconds": profile.replication_lag_threshold_seconds if profile else 30,
        }
        pmap = {
            "identity_resilience.multi_region.enabled": ("multi_region_enabled", "enabled"),
            "identity_resilience.failover.auto_trigger": ("auto_failover", "enabled"),
            "identity_resilience.worker.heartbeat_timeout_seconds": ("heartbeat_timeout_seconds", "timeout"),
            "identity_resilience.replication.lag_threshold_seconds": ("replication_lag_threshold_seconds", "threshold"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> ResilienceProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = ResilienceProfile.create(
            tenant_id=tenant_id,
            profile_ref=self._profiles.next_profile_ref(tenant_id),
        )
        await self._profiles.save(profile)
        return profile

    async def handle_tenant_provisioned(self, event: dict) -> None:
        tenant_id = event.get("tenant_id") or event.get("payload", {}).get("tenant_id")
        if tenant_id:
            await self.seed(tenant_id)

    async def handle_worker_activity(self, event: dict) -> None:
        tenant_id = str(event.get("tenant_id") or "")
        if not tenant_id:
            return
        payload = event.get("payload") or event
        event_name = str(event.get("event_name", ""))
        if event_name == "directory.sync.completed":
            leader = await self._workers.find_leader(tenant_id, WorkerType.DIRECTORY_SYNC.value)
            if leader:
                leader.heartbeat()
                await self._workers.save(leader)
        elif event_name == "identity_risk.score.computed":
            leader = await self._workers.find_leader(tenant_id, WorkerType.RISK_SCORING.value)
            if leader:
                leader.heartbeat()
                await self._workers.save(leader)

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": engine.list_capability_catalog(),
            "policy_keys": engine.list_policy_keys(),
            "default_regions": engine.list_default_regions(),
            "worker_types": engine.list_worker_types(),
            "dependency_map": engine.dependency_map(),
            "runtime": {"local_region_id": settings.marpich_region_id},
        })

    async def seed(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        existing = await self._regions.list_by_tenant(tenant_id)
        if not existing:
            for item in engine.list_default_regions():
                region = RegionDescriptor.register(
                    tenant_id=tenant_id,
                    region_ref=self._regions.next_region_ref(tenant_id),
                    region_id=item["region_id"],
                    display_name=item["display_name"],
                    is_primary=item.get("is_primary", False),
                )
                await self._regions.save(region)
        return Result.ok({"seeded": True, "profile_ref": profile.profile_ref})

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        region_rows = await self._regions.list_by_tenant(tenant_id)
        worker_rows = await self._workers.list_by_tenant(tenant_id)
        failover_rows = await self._failovers.list_by_tenant(tenant_id)
        dashboard = engine.build_dashboard(
            profile=profile.to_dict(),
            regions=[r.to_dict() for r in region_rows],
            workers=[w.to_dict() for w in worker_rows],
            failovers=[f.to_dict() for f in failover_rows],
        )
        return Result.ok(dashboard)

    async def list_regions(self, tenant_id: str) -> Result[list[dict]]:
        rows = await self._regions.list_by_tenant(tenant_id)
        return Result.ok([row.to_dict() for row in rows])

    async def register_region(
        self,
        tenant_id: str,
        *,
        region_id: str,
        display_name: str,
        is_primary: bool = False,
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["multi_region_enabled"]:
            return Result.fail("identity_resilience.errors.multi_region_disabled")
        existing = await self._regions.find_by_region_id(tenant_id, region_id)
        if existing:
            return Result.ok(existing.to_dict())
        region = RegionDescriptor.register(
            tenant_id=tenant_id,
            region_ref=self._regions.next_region_ref(tenant_id),
            region_id=region_id,
            display_name=display_name,
            is_primary=is_primary,
        )
        await self._regions.save(region)
        return Result.ok(region.to_dict())

    async def deploy_worker(
        self,
        tenant_id: str,
        *,
        worker_type: str,
        region_id: str,
        role: str = WorkerRole.STANDBY.value,
    ) -> Result[dict]:
        await self._ensure_profile(tenant_id)
        region = await self._regions.find_by_region_id(tenant_id, region_id)
        if not region:
            return Result.fail("identity_resilience.errors.region_not_found")
        if role == WorkerRole.LEADER.value:
            current_leader = await self._workers.find_leader(tenant_id, worker_type)
            if current_leader:
                current_leader.demote_standby()
                await self._workers.save(current_leader)
        worker = WorkerDeployment.deploy(
            tenant_id=tenant_id,
            worker_ref=self._workers.next_worker_ref(tenant_id),
            worker_type=worker_type,
            region_id=region_id,
            role=role,
        )
        worker.heartbeat()
        await self._workers.save(worker)
        await publish_integration_event(
            WorkerRegisteredIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                worker_ref=worker.worker_ref,
                worker_type=worker.worker_type,
                region_id=worker.region_id,
            )
        )
        return Result.ok(worker.to_dict())

    async def list_workers(self, tenant_id: str) -> Result[list[dict]]:
        rows = await self._workers.list_by_tenant(tenant_id)
        return Result.ok([row.to_dict() for row in rows])

    async def heartbeat(self, tenant_id: str, worker_ref: str) -> Result[dict]:
        worker = await self._workers.find_by_ref(tenant_id, worker_ref)
        if not worker:
            return Result.fail("identity_resilience.errors.worker_not_found")
        worker.heartbeat()
        await self._workers.save(worker)
        return Result.ok(worker.to_dict())

    async def check_replication_health(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        policy = await self._policy_params(tenant_id)
        threshold = int(policy["replication_lag_threshold_seconds"])
        regions = await self._regions.list_by_tenant(tenant_id)
        results = []
        for region in regions:
            lag = region.replication_lag_seconds if region.region_id == settings.marpich_region_id else region.replication_lag_seconds
            # Simulate lag for non-primary regions in dev
            if not region.is_primary and lag == 0:
                lag = 5 if region.region_id != settings.marpich_region_id else 0
            previous_health = region.health
            region.update_health(lag_seconds=lag, threshold=threshold)
            await self._regions.save(region)
            results.append(region.to_dict())
            if region.health != previous_health:
                await publish_integration_event(
                    RegionHealthChangedIntegration(
                        tenant_id=TenantId(tenant_id),
                        correlation_id=str(uuid.uuid4()),
                        region_id=region.region_id,
                        health=region.health,
                        replication_lag_seconds=region.replication_lag_seconds,
                    )
                )
        return Result.ok({"regions": results, "threshold_seconds": threshold, "profile_ref": profile.profile_ref})

    async def initiate_failover(
        self,
        tenant_id: str,
        *,
        worker_type: str,
        reason: str = "leader_heartbeat_timeout",
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["auto_failover"] and reason == "leader_heartbeat_timeout":
            return Result.fail("identity_resilience.errors.auto_failover_disabled")
        leader = await self._workers.find_leader(tenant_id, worker_type)
        if not leader:
            return Result.fail("identity_resilience.errors.no_leader")
        workers = await self._workers.list_by_tenant(tenant_id)
        target_data = engine.select_failover_target(
            [w.to_dict() for w in workers],
            worker_type=worker_type,
            exclude_region_id=leader.region_id,
        )
        if not target_data:
            return Result.fail("identity_resilience.errors.no_failover_target")
        target = await self._workers.find_by_ref(tenant_id, target_data["worker_ref"])
        if not target:
            return Result.fail("identity_resilience.errors.no_failover_target")

        failover = FailoverEvent.initiate(
            tenant_id=tenant_id,
            failover_ref=self._failovers.next_failover_ref(tenant_id),
            worker_type=worker_type,
            from_region_id=leader.region_id,
            to_region_id=target.region_id,
            reason=reason,
        )
        await self._failovers.save(failover)

        leader.mark_offline()
        leader.demote_standby()
        target.promote_leader()
        target.heartbeat()
        await self._workers.save(leader)
        await self._workers.save(target)

        correlation_id = str(uuid.uuid4())
        await publish_integration_event(
            FailoverInitiatedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                failover_ref=failover.failover_ref,
                worker_type=worker_type,
                from_region_id=leader.region_id,
                to_region_id=target.region_id,
            )
        )
        failover.complete()
        await self._failovers.save(failover)
        await publish_integration_event(
            FailoverCompletedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                failover_ref=failover.failover_ref,
                worker_type=worker_type,
                to_region_id=target.region_id,
            )
        )
        return Result.ok({
            "failover": failover.to_dict(),
            "new_leader": target.to_dict(),
            "previous_leader": leader.to_dict(),
        })

    async def run_health_check(self, tenant_id: str) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        timeout = int(policy["heartbeat_timeout_seconds"])
        workers = await self._workers.list_by_tenant(tenant_id)
        stale_leaders: list[str] = []
        failovers: list[dict] = []
        for worker in workers:
            if worker.role != WorkerRole.LEADER.value:
                continue
            if engine.is_heartbeat_stale(worker.last_heartbeat_at, timeout_seconds=timeout):
                worker.mark_offline()
                await self._workers.save(worker)
                stale_leaders.append(worker.worker_type)
        for worker_type in stale_leaders:
            if policy["auto_failover"]:
                result = await self.initiate_failover(
                    tenant_id,
                    worker_type=worker_type,
                    reason="leader_heartbeat_timeout",
                )
                if result.succeeded:
                    failovers.append(result.unwrap())
        replication = (await self.check_replication_health(tenant_id)).unwrap()
        return Result.ok({
            "stale_leaders": stale_leaders,
            "failovers": failovers,
            "replication": replication,
        })

    async def run_directory_sync_ha(self, tenant_id: str) -> Result[dict]:
        leader = await self._workers.find_leader(tenant_id, WorkerType.DIRECTORY_SYNC.value)
        if not leader:
            return Result.fail("identity_resilience.errors.no_directory_leader")
        if leader.region_id != settings.marpich_region_id:
            return Result.ok({"delegated": False, "reason": "not_local_region_leader", "leader_region": leader.region_id})
        result = await self._directory_workers.run_sync_worker(tenant_id)
        leader.heartbeat()
        await self._workers.save(leader)
        return Result.ok({"delegated": True, "leader_region": leader.region_id, "sync_result": result})

    async def list_failovers(self, tenant_id: str) -> Result[list[dict]]:
        rows = await self._failovers.list_by_tenant(tenant_id)
        return Result.ok([row.to_dict() for row in rows])
