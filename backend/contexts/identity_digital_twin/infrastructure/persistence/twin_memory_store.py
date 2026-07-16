from __future__ import annotations
from contexts.identity_digital_twin.domain.aggregates.identity_digital_twin_platform import DigitalTwin, TwinSnapshot, TwinSimulation, TwinDriftAlert
from contexts.identity_digital_twin.domain.ports.twin_repositories import ITwinRepository, ISnapshotRepository, ISimulationRepository, IDriftAlertRepository
class InMemoryTwinStore:
    twins: dict[str, DigitalTwin] = {}; snapshots: dict[str, TwinSnapshot] = {}; simulations: dict[str, TwinSimulation] = {}; alerts: dict[str, TwinDriftAlert] = {}; counters: dict[str, int] = {}
    @classmethod
    def reset(cls): cls.twins.clear(); cls.snapshots.clear(); cls.simulations.clear(); cls.alerts.clear(); cls.counters.clear()
    @classmethod
    def next(cls, tenant_id: str, prefix: str) -> str:
        key=f"{tenant_id}:{prefix}"; cls.counters[key]=cls.counters.get(key, 0)+1; return f"{prefix}-{tenant_id}-{cls.counters[key]:04d}"
class InMemoryTwinRepository(ITwinRepository):
    async def save(self, twin): InMemoryTwinStore.twins[f"{twin.tenant_id}:{twin.twin_ref}"]=twin
    async def find_by_ref(self, tenant_id, twin_ref): return InMemoryTwinStore.twins.get(f"{tenant_id}:{twin_ref}")
    async def list_by_tenant(self, tenant_id, *, limit=100): return [x for x in InMemoryTwinStore.twins.values() if x.tenant_id == tenant_id][:limit]
    def next_ref(self, tenant_id): return InMemoryTwinStore.next(tenant_id, "twin")
class InMemorySnapshotRepository(ISnapshotRepository):
    async def save(self, item): InMemoryTwinStore.snapshots[f"{item.tenant_id}:{item.snapshot_ref}"]=item
    async def list_by_twin(self, tenant_id, twin_ref, *, limit=50): return [x for x in InMemoryTwinStore.snapshots.values() if x.tenant_id == tenant_id and x.twin_ref == twin_ref][-limit:]
    def next_ref(self, tenant_id): return InMemoryTwinStore.next(tenant_id, "snapshot")
class InMemorySimulationRepository(ISimulationRepository):
    async def save(self, item): InMemoryTwinStore.simulations[f"{item.tenant_id}:{item.simulation_ref}"]=item
    async def list_by_twin(self, tenant_id, twin_ref, *, limit=50): return [x for x in InMemoryTwinStore.simulations.values() if x.tenant_id == tenant_id and x.twin_ref == twin_ref][-limit:]
    def next_ref(self, tenant_id): return InMemoryTwinStore.next(tenant_id, "simulation")
class InMemoryDriftAlertRepository(IDriftAlertRepository):
    async def save(self, item): InMemoryTwinStore.alerts[f"{item.tenant_id}:{item.alert_ref}"]=item
    async def list_by_tenant(self, tenant_id, *, limit=100): return [x for x in InMemoryTwinStore.alerts.values() if x.tenant_id == tenant_id][-limit:]
    def next_ref(self, tenant_id): return InMemoryTwinStore.next(tenant_id, "drift")
