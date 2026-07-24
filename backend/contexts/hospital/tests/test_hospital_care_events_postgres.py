"""Postgres care-event projections — wiring + row mapper (no live DB required)."""
from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest

from contexts.hospital.container import get_hospital_service, reset_hospital_service
from contexts.hospital.domain.aggregates.care_event_projection import CareEventKind
from contexts.hospital.infrastructure.persistence.memory_store import (
    InMemoryCareEventProjectionRepository,
)
from contexts.hospital.infrastructure.persistence.postgres_store import (
    PostgresCareEventProjectionRepository,
    _care_event_from_row,
)


@pytest.fixture(autouse=True)
def _reset():
    reset_hospital_service()
    yield
    reset_hospital_service()


@pytest.mark.unit
def test_hospital_container_defaults_to_memory_care_events():
    svc = get_hospital_service()
    assert isinstance(svc._care_events, InMemoryCareEventProjectionRepository)


@pytest.mark.unit
def test_hospital_container_wires_postgres_care_events(monkeypatch):
    monkeypatch.setattr(
        "contexts.hospital.container.use_postgres",
        lambda: True,
    )
    reset_hospital_service()
    svc = get_hospital_service()
    assert isinstance(svc._care_events, PostgresCareEventProjectionRepository)


@pytest.mark.unit
def test_care_event_projection_row_mapper():
    eid = uuid4()
    pid = uuid4()
    aid = uuid4()
    enc = uuid4()
    occurred = datetime.now(UTC)
    row = SimpleNamespace(
        id=eid,
        tenant_id="t1",
        source_event_id="evt-1",
        source_context="laboratory",
        event_kind="lab_result",
        peer_id=str(uuid4()),
        patient_id=pid,
        admission_id=aid,
        encounter_id=enc,
        summary={"test_code": "CBC", "result_value": "12.4"},
        correlation_id="corr-1",
        occurred_at=occurred,
    )
    event = _care_event_from_row(row)
    assert event.tenant_id == "t1"
    assert event.source_event_id == "evt-1"
    assert event.event_kind == CareEventKind.LAB_RESULT
    assert event.patient_id == str(pid)
    assert event.admission_id == str(aid)
    assert event.encounter_id == str(enc)
    assert event.summary["test_code"] == "CBC"


@pytest.mark.unit
def test_care_event_projection_row_mapper_optional_ids():
    row = SimpleNamespace(
        id=uuid4(),
        tenant_id="t1",
        source_event_id="evt-2",
        source_context="pharmacy",
        event_kind="pharmacy_dispense",
        peer_id=str(uuid4()),
        patient_id=uuid4(),
        admission_id=None,
        encounter_id=None,
        summary={"drug_code": "AMOX500"},
        correlation_id="",
        occurred_at=datetime.now(UTC),
    )
    event = _care_event_from_row(row)
    assert event.admission_id == ""
    assert event.encounter_id == ""
    assert event.event_kind == CareEventKind.PHARMACY_DISPENSE
