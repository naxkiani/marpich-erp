"""Enterprise Connector Framework application service."""
from __future__ import annotations

import uuid

from contexts.enterprise_connector_framework.domain.aggregates.enterprise_connector_framework_platform import (
    ConnectorFrameworkProfile,
    ConnectorHealthRecord,
    ConnectorInstance,
    ConnectorInstanceStatus,
    ExecutionStatus,
    OperationExecution,
    PluginConnectorBinding,
)
from contexts.enterprise_connector_framework.domain.events.enterprise_connector_framework_integration_events import (
    ConnectorDashboardGeneratedIntegration,
    ConnectorHealthCheckedIntegration,
    ConnectorInstanceRegisteredIntegration,
    ConnectorOperationExecutedIntegration,
)
from contexts.enterprise_connector_framework.domain.events.lms_sync_events import (
    LmsBatchSyncedIntegration,
)
from contexts.enterprise_connector_framework.domain.ports.enterprise_connector_framework_repositories import (
    IConnectorFrameworkProfileRepository,
    IConnectorHealthRepository,
    IConnectorInstanceRepository,
    IOperationExecutionRepository,
    IPluginConnectorBindingRepository,
)
from contexts.enterprise_connector_framework.domain.services import enterprise_connector_framework_engine as engine
from contexts.enterprise_connector_framework.infrastructure.adapters.connector_sdk_bridge import ConnectorSdkBridge
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class EnterpriseConnectorFrameworkApplicationService:
    def __init__(
        self,
        profiles: IConnectorFrameworkProfileRepository,
        instances: IConnectorInstanceRepository,
        health: IConnectorHealthRepository,
        executions: IOperationExecutionRepository,
        plugin_bindings: IPluginConnectorBindingRepository,
        policy_evaluator: IPolicyEvaluator,
        sdk_bridge: ConnectorSdkBridge | None = None,
    ) -> None:
        self._profiles = profiles
        self._instances = instances
        self._health = health
        self._executions = executions
        self._plugin_bindings = plugin_bindings
        self._policy = policy_evaluator
        self._sdk = sdk_bridge or ConnectorSdkBridge()

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "health_check_enabled": profile.health_check_enabled if profile else True,
            "retry_enabled": profile.retry_enabled if profile else True,
            "plugin_connectors_enabled": profile.plugin_connectors_enabled if profile else True,
            "sdk_extensions_enabled": profile.sdk_extensions_enabled if profile else True,
        }
        pmap = {
            "enterprise_connector_framework.health_check.enabled": ("health_check_enabled", "enabled"),
            "enterprise_connector_framework.retry.enabled": ("retry_enabled", "enabled"),
            "enterprise_connector_framework.plugin_connectors.enabled": ("plugin_connectors_enabled", "enabled"),
            "enterprise_connector_framework.sdk_extensions.enabled": ("sdk_extensions_enabled", "enabled"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> ConnectorFrameworkProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = ConnectorFrameworkProfile.create(
            tenant_id=tenant_id,
            profile_ref=self._profiles.next_profile_ref(tenant_id),
        )
        await self._profiles.save(profile)
        return profile

    async def list_catalog(self) -> Result[dict]:
        catalog = engine.load_connector_catalog()
        return Result.ok({
            "capabilities": engine.list_capability_catalog(),
            "policy_keys": engine.list_policy_keys(),
            "connector_types": sorted(catalog.keys()),
            "sdk_types": self._sdk.list_sdk_types(),
            "plugin_extensible": True,
            "connector_sdk": "shared.connectors",
        })

    async def get_dependency_map(self) -> Result[dict]:
        return Result.ok(engine.dependency_map())

    async def get_connector_catalog(self) -> Result[dict]:
        catalog = engine.load_connector_catalog()
        entries = []
        for connector_type, entry in sorted(catalog.items()):
            entries.append({
                "connector_type": connector_type,
                "display_name": entry.get("display_name", connector_type),
                "category": entry.get("category", "custom"),
                "direction": entry.get("direction", "bidirectional"),
                "operations": entry.get("operations", []),
                "auth": entry.get("auth", []),
                "sdk_registered": connector_type in self._sdk.list_sdk_types(),
            })
        return Result.ok({"total": len(entries), "entries": entries})

    async def get_sdk_info(self) -> Result[dict]:
        types = self._sdk.list_sdk_types()
        return Result.ok({
            "package": "shared.connectors",
            "registered_types": types,
            "total": len(types),
            "plugin_architecture": True,
            "extension_point": "connector.execute",
        })

    async def seed(self, tenant_id: str) -> Result[dict]:
        await self._ensure_profile(tenant_id)
        seed_data = engine.generate_seed_data()
        created = 0
        first_ref = ""
        for data in seed_data["connector_instances"]:
            instance = ConnectorInstance.create(
                tenant_id=tenant_id,
                instance_ref=self._instances.next_instance_ref(tenant_id),
                connector_type=data["connector_type"],
                display_name=data["display_name"],
                category=data["category"],
                direction=data["direction"],
                config=data.get("config", {}),
            )
            instance.status = ConnectorInstanceStatus.ACTIVE.value
            await self._instances.save(instance)
            created += 1
            if not first_ref:
                first_ref = instance.instance_ref

        for pdata in seed_data["plugin_bindings"]:
            if first_ref:
                binding = PluginConnectorBinding.create(
                    tenant_id=tenant_id,
                    binding_ref=self._plugin_bindings.next_binding_ref(tenant_id),
                    plugin_id=pdata["plugin_id"],
                    instance_ref=first_ref,
                    extension_point=pdata.get("extension_point", "connector.execute"),
                )
                await self._plugin_bindings.save(binding)

        return Result.ok({
            "seeded": True,
            "connector_instances": created,
            "plugin_bindings": len(seed_data["plugin_bindings"]),
        })

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        instances = await self._instances.list_by_tenant(tenant_id)
        health_records = await self._health.list_by_tenant(tenant_id)
        executions = await self._executions.list_by_tenant(tenant_id)
        bindings = await self._plugin_bindings.list_by_tenant(tenant_id)
        dashboard = engine.build_monitoring_dashboard(
            profile=profile.to_dict() if profile else None,
            instances=[i.to_dict() for i in instances],
            health_records=[h.to_dict() for h in health_records],
            executions=[e.to_dict() for e in executions],
            plugin_bindings=[b.to_dict() for b in bindings],
            sdk_connectors=self._sdk.list_sdk_types(),
        )
        await publish_integration_event(
            ConnectorDashboardGeneratedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=str(uuid.uuid4()),
                instances_total=dashboard["summary"]["connector_instances"],
                success_rate_pct=dashboard["summary"]["success_rate_pct"],
            )
        )
        return Result.ok(dashboard)

    async def list_connectors(self, tenant_id: str) -> Result[list[dict]]:
        return Result.ok([i.to_dict() for i in await self._instances.list_by_tenant(tenant_id)])

    async def register_connector(
        self,
        tenant_id: str,
        *,
        connector_type: str,
        display_name: str,
        config: dict | None = None,
        plugin_id: str = "",
    ) -> Result[dict]:
        await self._ensure_profile(tenant_id)
        entry = engine.catalog_entry_for_type(connector_type)
        if not entry:
            return Result.fail(f"Unknown connector type: {connector_type}")
        instance = ConnectorInstance.create(
            tenant_id=tenant_id,
            instance_ref=self._instances.next_instance_ref(tenant_id),
            connector_type=connector_type,
            display_name=display_name,
            category=entry.get("category", "custom"),
            direction=entry.get("direction", "bidirectional"),
            config=config or {},
            plugin_id=plugin_id,
        )
        await self._instances.save(instance)
        await publish_integration_event(
            ConnectorInstanceRegisteredIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=str(uuid.uuid4()),
                instance_ref=instance.instance_ref,
                connector_type=connector_type,
            )
        )
        return Result.ok(instance.to_dict())

    async def test_connection(self, tenant_id: str, instance_ref: str) -> Result[dict]:
        instance = await self._instances.find_by_ref(tenant_id, instance_ref)
        if not instance:
            return Result.fail(f"Connector not found: {instance_ref}")
        policy = await self._policy_params(tenant_id)
        if not policy.get("health_check_enabled", True):
            return Result.fail("Health checks disabled by policy")
        result = await self._sdk.test_connection(
            connector_type=instance.connector_type,
            config=instance.config,
            secret=instance.secret_ref,
        )
        record = ConnectorHealthRecord.create(
            tenant_id=tenant_id,
            health_ref=self._health.next_health_ref(tenant_id),
            instance_ref=instance_ref,
            healthy=result.succeeded,
            latency_ms=result.unwrap().get("latency_ms", 0) if result.succeeded else 0,
            message=result.error or "ok",
        )
        await self._health.save(record)
        if result.succeeded:
            instance.status = ConnectorInstanceStatus.ACTIVE.value
        else:
            instance.status = ConnectorInstanceStatus.DEGRADED.value
        await self._instances.save(instance)
        await publish_integration_event(
            ConnectorHealthCheckedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=str(uuid.uuid4()),
                instance_ref=instance_ref,
                healthy=result.succeeded,
            )
        )
        return result

    async def execute_operation(
        self,
        tenant_id: str,
        *,
        instance_ref: str,
        operation: str,
        payload: dict,
        correlation_id: str = "",
        idempotency_key: str = "",
    ) -> Result[dict]:
        instance = await self._instances.find_by_ref(tenant_id, instance_ref)
        if not instance:
            return Result.fail(f"Connector not found: {instance_ref}")
        if instance.status == ConnectorInstanceStatus.DISABLED.value:
            return Result.fail("Connector is disabled")

        execution = OperationExecution.create(
            tenant_id=tenant_id,
            execution_ref=self._executions.next_execution_ref(tenant_id),
            instance_ref=instance_ref,
            connector_type=instance.connector_type,
            operation=operation,
            idempotency_key=idempotency_key,
            correlation_id=correlation_id or str(uuid.uuid4()),
        )
        result = await self._sdk.execute(
            connector_type=instance.connector_type,
            operation=operation,
            payload=payload,
            config=instance.config,
            secret=instance.secret_ref,
            idempotency_key=idempotency_key,
        )
        execution.status = ExecutionStatus.SUCCEEDED.value if result.succeeded else ExecutionStatus.FAILED.value
        await self._executions.save(execution)
        await publish_integration_event(
            ConnectorOperationExecutedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=execution.correlation_id,
                execution_ref=execution.execution_ref,
                connector_type=instance.connector_type,
                operation=operation,
                status=execution.status,
            )
        )
        if not result.succeeded:
            return result
        body = result.unwrap()
        body["execution_ref"] = execution.execution_ref
        if instance.connector_type in {"moodle", "google_classroom"}:
            await self._publish_lms_batch(
                tenant_id=tenant_id,
                correlation_id=execution.correlation_id,
                provider=instance.connector_type,
                operation=operation,
                instance_ref=instance_ref,
                execution_ref=execution.execution_ref,
                body=body,
            )
        return Result.ok(body)

    async def _publish_lms_batch(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        provider: str,
        operation: str,
        instance_ref: str,
        execution_ref: str,
        body: dict,
    ) -> None:
        result_block = body.get("result") if isinstance(body.get("result"), dict) else {}
        await publish_integration_event(
            LmsBatchSyncedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                provider=provider,
                operation=operation,
                instance_ref=instance_ref,
                execution_ref=execution_ref,
                courses=list(result_block.get("courses") or []),
                enrollments=list(result_block.get("enrollments") or []),
                grades=list(result_block.get("grades") or []),
            )
        )

    async def list_executions(self, tenant_id: str) -> Result[list[dict]]:
        return Result.ok([e.to_dict() for e in await self._executions.list_by_tenant(tenant_id)])

    async def list_health_records(self, tenant_id: str) -> Result[list[dict]]:
        return Result.ok([h.to_dict() for h in await self._health.list_by_tenant(tenant_id)])

    async def list_plugin_bindings(self, tenant_id: str) -> Result[list[dict]]:
        return Result.ok([b.to_dict() for b in await self._plugin_bindings.list_by_tenant(tenant_id)])

    async def register_plugin_binding(
        self,
        tenant_id: str,
        *,
        plugin_id: str,
        instance_ref: str,
        extension_point: str = "connector.execute",
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy.get("plugin_connectors_enabled", True):
            return Result.fail("Plugin connectors disabled by policy")
        instance = await self._instances.find_by_ref(tenant_id, instance_ref)
        if not instance:
            return Result.fail(f"Connector not found: {instance_ref}")
        binding = PluginConnectorBinding.create(
            tenant_id=tenant_id,
            binding_ref=self._plugin_bindings.next_binding_ref(tenant_id),
            plugin_id=plugin_id,
            instance_ref=instance_ref,
            extension_point=extension_point,
        )
        instance.plugin_id = plugin_id
        await self._plugin_bindings.save(binding)
        await self._instances.save(instance)
        return Result.ok(binding.to_dict())

    async def handle_tenant_provisioned(self, event: dict) -> None:
        tenant_id = event.get("tenant_id") or event.get("payload", {}).get("tenant_id")
        if tenant_id:
            await self._ensure_profile(str(tenant_id))
