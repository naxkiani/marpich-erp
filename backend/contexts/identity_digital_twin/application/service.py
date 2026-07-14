"""Application orchestration for the Enterprise Identity Digital Twin Platform."""
from __future__ import annotations
from contexts.identity_digital_twin.domain.aggregates.identity_digital_twin_platform import DigitalTwin, TwinSnapshot, TwinSimulation, TwinDriftAlert
from contexts.identity_digital_twin.domain.events.twin_integration_events import TwinCreatedIntegration, TwinSynchronizedIntegration, TwinSimulationCompletedIntegration, TwinDriftDetectedIntegration
from contexts.identity_digital_twin.domain.services import twin_engine, twin_simulation_engine, twin_drift_engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event
class IdentityDigitalTwinApplicationService:
    def __init__(self, twins, snapshots, simulations, alerts, policy_evaluator: IPolicyEvaluator): self._twins, self._snapshots, self._simulations, self._alerts, self._policy = twins, snapshots, simulations, alerts, policy_evaluator
    async def _params(self, tenant_id: str) -> dict:
        values={"enabled": True, "simulation_enabled": True, "drift_threshold": 1}
        for key, target, field in (("twin.enabled","enabled","enabled"),("twin.simulation.enabled","simulation_enabled","enabled"),("twin.drift.threshold","drift_threshold","threshold")):
            decision=await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters: values[target]=decision.parameters[field]
        return values
    async def create(self, tenant_id: str, *, identity_ref: str, attributes: dict | None = None, correlation_id: str = "") -> Result[dict]:
        if not (await self._params(tenant_id))["enabled"]: return Result.fail("identity_twin.errors.disabled")
        twin=DigitalTwin.create(tenant_id=tenant_id, twin_ref=self._twins.next_ref(tenant_id), identity_ref=identity_ref, attributes=attributes)
        await self._twins.save(twin)
        await publish_integration_event(TwinCreatedIntegration(tenant_id=TenantId(tenant_id), correlation_id=correlation_id, twin_ref=twin.twin_ref, identity_ref=identity_ref))
        return Result.ok(twin.to_dict())
    async def handle_source_event(self, envelope: dict, *, source_event: str) -> None:
        """ACL entry point for peer integration-event envelopes; never imports peer models."""
        tenant_id = str(envelope.get("tenant_id") or "")
        payload = envelope.get("payload") or {}
        identity_ref = str(payload.get("identity_ref") or payload.get("user_id") or "")
        if not tenant_id or not identity_ref:
            return
        twins = await self._twins.list_by_tenant(tenant_id)
        twin = next((item for item in twins if item.identity_ref == identity_ref), None)
        if twin is None:
            created = await self.create(
                tenant_id,
                identity_ref=identity_ref,
                attributes=payload.get("attributes") or {},
                correlation_id=str(envelope.get("correlation_id") or ""),
            )
            if not created.succeeded:
                return
            twin_ref = created.unwrap()["twin_ref"]
        else:
            twin_ref = twin.twin_ref
        await self.sync(
            tenant_id,
            twin_ref,
            projection=payload.get("projection") or {
                "attributes": payload.get("attributes") or {},
                "role_refs": payload.get("role_refs") or [],
                "session_refs": payload.get("session_refs") or [],
                "federation_link_refs": payload.get("federation_link_refs") or [],
                "lifecycle_state": payload.get("lifecycle_state"),
            },
            source_event=source_event,
            correlation_id=str(envelope.get("correlation_id") or ""),
        )
    async def sync(self, tenant_id: str, twin_ref: str, *, projection: dict, source_event: str, correlation_id: str = "") -> Result[dict]:
        twin=await self._twins.find_by_ref(tenant_id, twin_ref)
        if not twin: return Result.fail("identity_twin.errors.not_found")
        normalized=twin_engine.normalize_projection(projection); twin.synchronize(normalized, source_event); await self._twins.save(twin)
        snapshot=TwinSnapshot(id=UniqueId.generate(), tenant_id=tenant_id, snapshot_ref=self._snapshots.next_ref(tenant_id), twin_ref=twin_ref, projection=twin.to_dict(), source_event=source_event)
        await self._snapshots.save(snapshot)
        await publish_integration_event(TwinSynchronizedIntegration(tenant_id=TenantId(tenant_id), correlation_id=correlation_id, twin_ref=twin_ref, source_event=source_event))
        return Result.ok({"twin": twin.to_dict(), "snapshot": snapshot.to_dict()})
    async def simulate(self, tenant_id: str, twin_ref: str, *, scenario_type: str, proposed_change: dict, correlation_id: str = "") -> Result[dict]:
        params=await self._params(tenant_id)
        if not params["simulation_enabled"]: return Result.fail("identity_twin.errors.simulation_disabled")
        twin=await self._twins.find_by_ref(tenant_id,twin_ref)
        if not twin: return Result.fail("identity_twin.errors.not_found")
        try: outcome=twin_simulation_engine.simulate(twin.to_dict(),scenario_type,proposed_change)
        except ValueError: return Result.fail("identity_twin.errors.unsupported_scenario")
        simulation=TwinSimulation(id=UniqueId.generate(),tenant_id=tenant_id,simulation_ref=self._simulations.next_ref(tenant_id),twin_ref=twin_ref,scenario_type=scenario_type,proposed_change=proposed_change,outcome=outcome)
        await self._simulations.save(simulation)
        await publish_integration_event(TwinSimulationCompletedIntegration(tenant_id=TenantId(tenant_id), correlation_id=correlation_id, simulation_ref=simulation.simulation_ref, twin_ref=twin_ref, scenario_type=scenario_type))
        return Result.ok(simulation.to_dict())
    async def detect_drift(self, tenant_id: str, twin_ref: str, *, observed_projection: dict, source_event: str, correlation_id: str = "") -> Result[dict]:
        twin=await self._twins.find_by_ref(tenant_id,twin_ref)
        if not twin: return Result.fail("identity_twin.errors.not_found")
        result=twin_drift_engine.detect(twin.to_dict(), twin_engine.normalize_projection(observed_projection), int((await self._params(tenant_id))["drift_threshold"]))
        if not result["detected"]: return Result.ok({"detected":False,"drift_fields":[]})
        alert=TwinDriftAlert(id=UniqueId.generate(),tenant_id=tenant_id,alert_ref=self._alerts.next_ref(tenant_id),twin_ref=twin_ref,source_event=source_event,drift_fields=result["drift_fields"],severity=result["severity"])
        await self._alerts.save(alert)
        await publish_integration_event(TwinDriftDetectedIntegration(tenant_id=TenantId(tenant_id),correlation_id=correlation_id,alert_ref=alert.alert_ref,twin_ref=twin_ref,severity=alert.severity))
        return Result.ok(alert.to_dict())
    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        twins=await self._twins.list_by_tenant(tenant_id); alerts=await self._alerts.list_by_tenant(tenant_id)
        return Result.ok(twin_engine.dashboard([x.to_dict() for x in twins],[x.to_dict() for x in alerts]))
    async def get(self, tenant_id: str, twin_ref: str) -> Result[dict]:
        twin=await self._twins.find_by_ref(tenant_id,twin_ref)
        return Result.ok(twin.to_dict()) if twin else Result.fail("identity_twin.errors.not_found")
