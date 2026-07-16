"""Shared pytest fixtures — unit vs integration test tiers."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "unit: fast tests without full FastAPI app")
    config.addinivalue_line("markers", "integration: API smoke tests with configured app")
    config.addinivalue_line("markers", "contract: JSON schema and OpenAPI contract tests")
    config.addinivalue_line("markers", "profile(name): optional profile scope for startup smoke tests")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--app-profile",
        action="store",
        default="test",
        help="App profile for integration tests: test|core|enterprise|financial|banking|industry|full",
    )


@pytest.fixture(scope="session")
def configured_app(request):
    """Minimal-profile app for integration smoke tests."""
    from core.presentation.api.app_factory import create_app
    from core.presentation.api.startup_registry import configure_application

    profile = request.config.getoption("--app-profile")
    application = create_app(profile=profile, startup_mode="lazy")
    configure_application(application, profile=profile, startup_mode="lazy")
    return application


@pytest.fixture
async def integration_client(configured_app):
    """HTTP client against the profile-scoped test application."""
    transport = ASGITransport(app=configured_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
