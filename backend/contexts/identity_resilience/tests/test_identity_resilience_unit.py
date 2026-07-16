"""Identity resilience — unit tests."""
from datetime import UTC, datetime, timedelta

import pytest

from contexts.identity_resilience.domain.aggregates.identity_resilience_platform import ResilienceCapability
from contexts.identity_resilience.domain.services import identity_resilience_engine as engine


@pytest.mark.unit
def test_capability_catalog_has_ten_capabilities():
    caps = {c["capability"] for c in engine.list_capability_catalog()}
    assert ResilienceCapability.DIRECTORY_SYNC_WORKER_HA.value in caps
    assert ResilienceCapability.FAILOVER_ORCHESTRATION.value in caps
    assert len(caps) == 10


@pytest.mark.unit
def test_is_heartbeat_stale():
    recent = datetime.now(UTC) - timedelta(seconds=10)
    stale = datetime.now(UTC) - timedelta(seconds=120)
    assert engine.is_heartbeat_stale(recent, timeout_seconds=60) is False
    assert engine.is_heartbeat_stale(stale, timeout_seconds=60) is True
    assert engine.is_heartbeat_stale(None, timeout_seconds=60) is True


@pytest.mark.unit
def test_select_failover_target_prefers_standby():
    workers = [
        {"worker_ref": "w1", "worker_type": "directory_sync", "region_id": "eu-west-1", "role": "leader", "status": "offline"},
        {"worker_ref": "w2", "worker_type": "directory_sync", "region_id": "us-east-1", "role": "standby", "status": "healthy"},
    ]
    target = engine.select_failover_target(workers, worker_type="directory_sync", exclude_region_id="eu-west-1")
    assert target is not None
    assert target["worker_ref"] == "w2"
