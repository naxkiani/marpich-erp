"""Application profile unit tests."""
import pytest

from core.presentation.api.app_profiles import contexts_for_profile, filter_specs_by_profile, list_profiles
from core.presentation.api.startup_registry import ROUTER_SPECS, router_specs_for_profile


@pytest.mark.unit
def test_list_profiles_includes_core_financial_banking_full():
    names = {p["profile"] for p in list_profiles()}
    assert {"core", "financial", "banking", "enterprise", "test", "full"} <= names


@pytest.mark.unit
def test_test_profile_is_minimal_subset():
    specs = router_specs_for_profile("test")
    assert len(specs) < 15
    assert len(specs) < len(ROUTER_SPECS)
    contexts = {s[0].split(".")[1] for s in specs}
    assert contexts <= contexts_for_profile("test")


@pytest.mark.unit
def test_full_profile_keeps_all_routers():
    assert len(router_specs_for_profile("full")) == len(ROUTER_SPECS)


@pytest.mark.unit
def test_banking_profile_includes_banking_and_fx():
    specs = router_specs_for_profile("banking")
    contexts = {s[0].split(".")[1] for s in specs}
    assert "banking" in contexts
    assert "currency_exchange" in contexts
    assert "hospital" not in contexts
