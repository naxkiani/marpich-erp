"""Permission Registry — unit tests."""
import pytest

from contexts.permission_registry.domain.aggregates.permission_registry_platform import RegistryCapability
from contexts.permission_registry.domain.services import permission_registry_engine as engine


@pytest.mark.unit
def test_capability_catalog_has_ten_capabilities():
    caps = {c["capability"] for c in engine.list_capability_catalog()}
    assert RegistryCapability.PERMISSION_CATALOG.value in caps
    assert RegistryCapability.REGISTRY_API.value in caps
    assert len(caps) == 10


@pytest.mark.unit
def test_parse_permission_code_valid():
    parsed = engine.parse_permission_code("banking.accounts.read")
    assert parsed == ("banking", "accounts", "read")


@pytest.mark.unit
def test_validate_permission_codes_rejects_invalid():
    valid, invalid = engine.validate_permission_codes(["banking.accounts.read", "INVALID"])
    assert "banking.accounts.read" in valid
    assert "INVALID" in invalid


@pytest.mark.unit
def test_validate_role_permissions_detects_missing():
    ok, missing = engine.validate_role_permissions(
        ["banking.accounts.read", "missing.perm.read"],
        {"banking.accounts.read"},
    )
    assert ok is False
    assert "missing.perm.read" in missing


@pytest.mark.unit
def test_build_dashboard_structure():
    dash = engine.build_dashboard(
        profile=None,
        permissions=[{"module": "banking"}],
        roles=[{"code": "treasury_operator"}],
        bindings=[],
        sets=[],
    )
    assert dash["summary"]["capabilities"] == 10
    assert dash["summary"]["permissions"] == 1
