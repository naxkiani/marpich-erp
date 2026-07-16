"""Enterprise Connector Framework — unit tests."""
import pytest

from contexts.enterprise_connector_framework.application.service import EnterpriseConnectorFrameworkApplicationService
from contexts.enterprise_connector_framework.container import reset_enterprise_connector_framework_service
from contexts.enterprise_connector_framework.domain.aggregates.enterprise_connector_framework_platform import (
    ConnectorFrameworkCapability,
    ExecutionStatus,
)
from contexts.enterprise_connector_framework.domain.services import enterprise_connector_framework_engine as engine
from contexts.enterprise_connector_framework.infrastructure.adapters.connector_sdk_bridge import ConnectorSdkBridge
from contexts.enterprise_connector_framework.infrastructure.persistence.enterprise_connector_framework_memory_store import (
    InMemoryConnectorFrameworkProfileRepository,
    InMemoryConnectorHealthRepository,
    InMemoryConnectorInstanceRepository,
    InMemoryOperationExecutionRepository,
    InMemoryPluginConnectorBindingRepository,
)
from contexts.policy.container import get_policy_evaluator
from tests.support.platform import reset_policy_stack


@pytest.fixture(autouse=True)
def reset_all():
    reset_policy_stack()
    reset_enterprise_connector_framework_service()
    ConnectorSdkBridge.reset()
    InMemoryConnectorFrameworkProfileRepository.reset()
    InMemoryConnectorInstanceRepository.reset()
    InMemoryConnectorHealthRepository.reset()
    InMemoryOperationExecutionRepository.reset()
    InMemoryPluginConnectorBindingRepository.reset()
    yield


@pytest.fixture
def service() -> EnterpriseConnectorFrameworkApplicationService:
    return EnterpriseConnectorFrameworkApplicationService(
        profiles=InMemoryConnectorFrameworkProfileRepository(),
        instances=InMemoryConnectorInstanceRepository(),
        health=InMemoryConnectorHealthRepository(),
        executions=InMemoryOperationExecutionRepository(),
        plugin_bindings=InMemoryPluginConnectorBindingRepository(),
        policy_evaluator=get_policy_evaluator(),
        sdk_bridge=ConnectorSdkBridge(),
    )


@pytest.mark.unit
def test_engine_capability_catalog_has_24_entries():
    caps = {c["capability"] for c in engine.list_capability_catalog()}
    assert len(caps) == 24
    assert ConnectorFrameworkCapability.CORE_BANKING_SYSTEMS.value in caps
    assert ConnectorFrameworkCapability.CONNECTOR_SDK.value in caps
    assert ConnectorFrameworkCapability.PLUGIN_ARCHITECTURE.value in caps


@pytest.mark.unit
def test_engine_maps_capabilities_to_connector_types():
    assert engine.CAPABILITY_TO_CONNECTOR_TYPE[ConnectorFrameworkCapability.AZURE_AD.value] == "azure_ad"
    assert engine.CAPABILITY_TO_CONNECTOR_TYPE[ConnectorFrameworkCapability.PAYMENT_GATEWAYS.value] == "payment_gateway"


@pytest.mark.unit
def test_engine_loads_catalog_with_embedded_types():
    catalog = engine.load_connector_catalog()
    assert "bank_api" in catalog
    assert "azure_ad" in catalog
    assert "document_management" in catalog


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_seed_and_dashboard(service):
    tenant = "ecf-unit"
    seed = await service.seed(tenant)
    assert seed.succeeded
    body = seed.unwrap()
    assert body["seeded"] is True
    assert body["connector_instances"] == 20

    dash = await service.get_dashboard(tenant)
    assert dash.succeeded
    summary = dash.unwrap()["summary"]
    assert summary["capabilities"] == 24
    assert summary["connector_instances"] == 20


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_test_connection_and_execute(service):
    tenant = "ecf-flow"
    await service.seed(tenant)
    connectors = (await service.list_connectors(tenant)).unwrap()
    bank = next(c for c in connectors if c["connector_type"] == "bank_api")

    tested = await service.test_connection(tenant, bank["instance_ref"])
    assert tested.succeeded
    assert tested.unwrap()["connected"] is True

    executed = await service.execute_operation(
        tenant,
        instance_ref=bank["instance_ref"],
        operation="balance_inquiry",
        payload={"account_ref": "ACC-1"},
    )
    assert executed.succeeded
    assert executed.unwrap()["status"] == "completed"

    executions = (await service.list_executions(tenant)).unwrap()
    assert any(e["status"] == ExecutionStatus.SUCCEEDED.value for e in executions)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_sdk_info_and_plugin_binding(service):
    tenant = "ecf-sdk"
    await service.seed(tenant)
    sdk = (await service.get_sdk_info()).unwrap()
    assert sdk["total"] >= 20
    assert "bank_api" in sdk["registered_types"]

    connectors = (await service.list_connectors(tenant)).unwrap()
    binding = await service.register_plugin_binding(
        tenant,
        plugin_id="com.marpich.custom.connector",
        instance_ref=connectors[0]["instance_ref"],
    )
    assert binding.succeeded
    bindings = (await service.list_plugin_bindings(tenant)).unwrap()
    assert len(bindings) >= 2
