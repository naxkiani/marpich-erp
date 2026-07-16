"""Enterprise Connector Framework — integration smoke tests."""
import pytest

from contexts.enterprise_connector_framework.domain.aggregates.enterprise_connector_framework_platform import (
    ConnectorFrameworkCapability,
)
from tests.support.platform import auth_headers


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_catalog_smoke(integration_client):
    headers = await auth_headers(
        integration_client,
        tenant="ecf-smoke",
        email="ecf-smoke@enterprise.dev",
        display_name="ECF Smoke",
    )
    resp = await integration_client.get("/api/v1/enterprise-connector-framework/catalog", headers=headers)
    assert resp.status_code == 200
    caps = {c["capability"] for c in resp.json()["data"]["capabilities"]}
    assert ConnectorFrameworkCapability.CONNECTOR_SDK.value in caps
    assert len(caps) == 24
