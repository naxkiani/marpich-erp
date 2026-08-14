"""Clinic ACL — laboratory.result.available → local lab note."""
from __future__ import annotations

import pytest

from contexts.clinic.container import get_clinic_service, reset_clinic_service
from contexts.clinic.infrastructure.persistence.memory_store import ClinicMemoryStore
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    ClinicMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_clinic_service()
    get_clinic_service()
    yield
    ClinicMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_clinic_service()


@pytest.mark.asyncio
async def test_laboratory_result_available_notes_on_clinic():
    tenant = "clinic-lab-acl"
    await InProcessEventBus.publish(
        {
            "event_name": "laboratory.result.available",
            "event_id": "evt-lab-r1",
            "tenant_id": tenant,
            "correlation_id": "corr-lab-r1",
            "payload": {
                "order_id": "ord-1",
                "patient_ref": "pat-1",
                "test_code": "CBC",
                "result_value": "12.1",
                "result_unit": "g/dL",
            },
        }
    )
    notes = await get_clinic_service().list_lab_result_notes(tenant)
    assert notes.succeeded
    assert notes.unwrap()["total"] == 1
    assert notes.unwrap()["items"][0]["test_code"] == "CBC"

    # idempotent on order_ref
    await InProcessEventBus.publish(
        {
            "event_name": "laboratory.result.available",
            "event_id": "evt-lab-r2",
            "tenant_id": tenant,
            "correlation_id": "corr-lab-r2",
            "payload": {
                "order_id": "ord-1",
                "patient_ref": "pat-1",
                "test_code": "CBC",
                "result_value": "12.1",
                "result_unit": "g/dL",
            },
        }
    )
    assert (await get_clinic_service().list_lab_result_notes(tenant)).unwrap()["total"] == 1
