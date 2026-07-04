"""OpenTelemetry bootstrap tests."""
import pytest
from httpx import ASGITransport, AsyncClient

from core.presentation.api.main import app
from shared.infrastructure import settings as settings_module
from shared.infrastructure.observability.telemetry import (
    is_telemetry_enabled,
    setup_observability,
    shutdown_observability,
)


@pytest.fixture(autouse=True)
def reset_telemetry():
    shutdown_observability()
    yield
    shutdown_observability()


def test_telemetry_disabled_by_default():
    assert is_telemetry_enabled() is False
    assert setup_observability(app) is False


def test_setup_observability_with_console_export(monkeypatch):
    monkeypatch.setattr(settings_module.settings, "otel_enabled", True)
    monkeypatch.setattr(settings_module.settings, "otel_console_export", True)
    monkeypatch.setattr(settings_module.settings, "otel_exporter_otlp_endpoint", "")

    assert setup_observability(app) is True
    shutdown_observability()


@pytest.mark.asyncio
async def test_health_works_with_otel_enabled(monkeypatch):
    monkeypatch.setattr(settings_module.settings, "otel_enabled", True)
    monkeypatch.setattr(settings_module.settings, "otel_console_export", True)
    setup_observability(app)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.headers.get("X-Request-ID")
    shutdown_observability()
