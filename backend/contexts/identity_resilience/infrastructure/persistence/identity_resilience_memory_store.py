"""In-memory identity resilience persistence."""
from __future__ import annotations

from contexts.identity_resilience.domain.aggregates.identity_resilience_platform import (
    FailoverEvent,
    RegionDescriptor,
    ResilienceProfile,
    WorkerDeployment,
    WorkerRole,
)
from contexts.identity_resilience.domain.ports.identity_resilience_repositories import (
    IFailoverEventRepository,
    IRegionRepository,
    IResilienceProfileRepository,
    IWorkerDeploymentRepository,
)


class InMemoryIdentityResilienceStore:
    profiles: dict[str, ResilienceProfile] = {}
    regions: dict[str, RegionDescriptor] = {}
    workers: dict[str, WorkerDeployment] = {}
    failovers: dict[str, FailoverEvent] = {}
    profile_counter: dict[str, int] = {}
    region_counter: dict[str, int] = {}
    worker_counter: dict[str, int] = {}
    failover_counter: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls.profiles.clear()
        cls.regions.clear()
        cls.workers.clear()
        cls.failovers.clear()
        cls.profile_counter.clear()
        cls.region_counter.clear()
        cls.worker_counter.clear()
        cls.failover_counter.clear()


class InMemoryResilienceProfileRepository(IResilienceProfileRepository):
    async def find_by_tenant(self, tenant_id: str) -> ResilienceProfile | None:
        return InMemoryIdentityResilienceStore.profiles.get(tenant_id)

    async def save(self, profile: ResilienceProfile) -> None:
        InMemoryIdentityResilienceStore.profiles[profile.tenant_id] = profile

    def next_profile_ref(self, tenant_id: str) -> str:
        n = InMemoryIdentityResilienceStore.profile_counter.get(tenant_id, 0) + 1
        InMemoryIdentityResilienceStore.profile_counter[tenant_id] = n
        return f"resilience-profile-{tenant_id}-{n:04d}"


class InMemoryRegionRepository(IRegionRepository):
    async def save(self, region: RegionDescriptor) -> None:
        InMemoryIdentityResilienceStore.regions[region.region_ref] = region

    async def list_by_tenant(self, tenant_id: str) -> list[RegionDescriptor]:
        return [r for r in InMemoryIdentityResilienceStore.regions.values() if r.tenant_id == tenant_id]

    async def find_by_region_id(self, tenant_id: str, region_id: str) -> RegionDescriptor | None:
        for region in InMemoryIdentityResilienceStore.regions.values():
            if region.tenant_id == tenant_id and region.region_id == region_id:
                return region
        return None

    def next_region_ref(self, tenant_id: str) -> str:
        n = InMemoryIdentityResilienceStore.region_counter.get(tenant_id, 0) + 1
        InMemoryIdentityResilienceStore.region_counter[tenant_id] = n
        return f"region-{tenant_id}-{n:04d}"


class InMemoryWorkerDeploymentRepository(IWorkerDeploymentRepository):
    async def save(self, worker: WorkerDeployment) -> None:
        InMemoryIdentityResilienceStore.workers[worker.worker_ref] = worker

    async def list_by_tenant(self, tenant_id: str) -> list[WorkerDeployment]:
        return [w for w in InMemoryIdentityResilienceStore.workers.values() if w.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, worker_ref: str) -> WorkerDeployment | None:
        worker = InMemoryIdentityResilienceStore.workers.get(worker_ref)
        if worker and worker.tenant_id == tenant_id:
            return worker
        return None

    async def find_leader(self, tenant_id: str, worker_type: str) -> WorkerDeployment | None:
        for worker in InMemoryIdentityResilienceStore.workers.values():
            if (
                worker.tenant_id == tenant_id
                and worker.worker_type == worker_type
                and worker.role == WorkerRole.LEADER.value
            ):
                return worker
        return None

    def next_worker_ref(self, tenant_id: str) -> str:
        n = InMemoryIdentityResilienceStore.worker_counter.get(tenant_id, 0) + 1
        InMemoryIdentityResilienceStore.worker_counter[tenant_id] = n
        return f"worker-{tenant_id}-{n:04d}"


class InMemoryFailoverEventRepository(IFailoverEventRepository):
    async def save(self, event: FailoverEvent) -> None:
        InMemoryIdentityResilienceStore.failovers[event.failover_ref] = event

    async def list_by_tenant(self, tenant_id: str) -> list[FailoverEvent]:
        return [f for f in InMemoryIdentityResilienceStore.failovers.values() if f.tenant_id == tenant_id]

    def next_failover_ref(self, tenant_id: str) -> str:
        n = InMemoryIdentityResilienceStore.failover_counter.get(tenant_id, 0) + 1
        InMemoryIdentityResilienceStore.failover_counter[tenant_id] = n
        return f"failover-{tenant_id}-{n:04d}"
