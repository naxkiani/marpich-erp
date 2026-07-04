"""Contract tests — OpenAPI and REST response envelopes."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from core.presentation.api.main import app

# Stable platform surface — breaking changes require ADR + version bump
REQUIRED_OPENAPI_PATHS = (
    "/api/v1/health",
    "/api/v1/auth/register",
    "/api/v1/auth/login",
    "/api/v1/users/me",
    "/api/v1/platform/industry-packs",
    "/api/v1/platform/tenants",
    "/api/v1/organizations",
    "/api/v1/audit/entries",
    "/api/v1/documents/folders/root",
    "/api/v1/workflow/definitions",
    "/api/v1/integrations/connectors",
    "/api/v1/media/assets",
    "/api/v1/analytics/metrics",
    "/api/v1/search/query",
    "/api/v1/search/indices",
    "/api/v1/notifications/inbox",
    "/api/v1/settings/config",
    "/api/v1/hospital/patients",
    "/api/v1/accounting/billings",
    "/api/v1/finance/accounts",
)

DATA_ENVELOPE_PATHS = ("/api/v1/platform/industry-packs",)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


def test_openapi_metadata():
    schema = app.openapi()
    assert schema["openapi"].startswith("3.")
    assert schema["info"]["title"] == "Marpich ERP"
    assert schema["info"]["version"]


@pytest.mark.parametrize("path", REQUIRED_OPENAPI_PATHS)
def test_openapi_includes_required_paths(path: str):
    schema = app.openapi()
    assert path in schema["paths"], f"Missing contract path: {path}"


def test_openapi_platform_tags_present():
    schema = app.openapi()
    all_tags: set[str] = set()
    for path_item in schema["paths"].values():
        for operation in path_item.values():
            if isinstance(operation, dict):
                all_tags.update(operation.get("tags", []))
    expected = {
        "Auth",
        "Core Platform",
        "Organization",
        "Audit",
        "Documents",
        "Workflow",
        "Integration",
        "Media",
        "Analytics",
        "Search",
    }
    missing = expected - all_tags
    assert not missing, f"Missing OpenAPI tags: {missing}"


@pytest.mark.asyncio
async def test_health_contract(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "marpich-backend"


@pytest.mark.asyncio
@pytest.mark.parametrize("path", DATA_ENVELOPE_PATHS)
async def test_public_endpoints_use_data_envelope(client, path: str):
    response = await client.get(path)
    assert response.status_code == 200
    body = response.json()
    assert "data" in body, f"{path} must return {{data: ...}} contract"


@pytest.mark.asyncio
async def test_tenant_scoped_endpoint_requires_tenant_header(client):
    response = await client.get("/api/v1/organizations")
    assert response.status_code in {400, 401, 403, 422}
