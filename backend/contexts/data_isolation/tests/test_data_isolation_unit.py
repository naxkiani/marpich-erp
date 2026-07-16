"""Data isolation — unit tests."""
import pytest

from contexts.data_isolation.domain.aggregates.data_isolation_platform import IsolationCapability
from contexts.data_isolation.domain.services import data_isolation_engine as engine


@pytest.mark.unit
def test_capability_catalog_has_ten_capabilities():
    caps = {c["capability"] for c in engine.list_capability_catalog()}
    assert IsolationCapability.PRINCIPAL_PARTITIONING.value in caps
    assert IsolationCapability.RLS_CATALOG.value in caps
    assert len(caps) == 10


@pytest.mark.unit
def test_partition_bucket_is_stable():
    assert engine.partition_bucket("acme-bank", 8) == engine.partition_bucket("acme-bank", 8)
    assert 0 <= engine.partition_bucket("tenant-x", 8) < 8


@pytest.mark.unit
def test_rls_policy_catalog_includes_identity_tables():
    tables = {(p["schema"], p["table"]) for p in engine.list_rls_policies()}
    assert ("identity", "users") in tables
    assert ("identity", "principals") in tables
    assert ("authorization", "access_decisions") in tables
