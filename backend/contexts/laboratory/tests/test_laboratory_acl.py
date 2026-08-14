"""ACL — hospital.encounter.* → laboratory REVIEW order (idempotent)."""
from __future__ import annotations

import pytest

from contexts.laboratory.container import get_laboratory_service, reset_laboratory_service
from contexts.laboratory.infrastructure.persistence.memory_store import LaboratoryMemoryStore
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    LaboratoryMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_laboratory_service()
    get_laboratory_service()
    yield
    LaboratoryMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_laboratory_service()


@pytest.mark.asyncio
async def test_hospital_encounter_completed_creates_review_order():
    tenant = "lab-acl-1"
    encounter_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    patient_id = "11111111-2222-3333-4444-555555555555"

    await InProcessEventBus.publish(
        {
            "event_name": "hospital.encounter.completed",
            "event_id": "evt-lab-1",
            "tenant_id": tenant,
            "correlation_id": "corr-lab-1",
            "payload": {
                "encounter_id": encounter_id,
                "patient_id": patient_id,
                "admission_id": "adm-1",
            },
        }
    )

    orders = await get_laboratory_service().list_orders(tenant)
    assert orders.succeeded
    items = orders.unwrap()["items"]
    assert len(items) == 1
    assert items[0]["test_code"] == "REVIEW"
    assert items[0]["source_encounter_ref"] == encounter_id
    assert items[0]["patient_ref"] == patient_id

    # idempotent
    await InProcessEventBus.publish(
        {
            "event_name": "hospital.encounter.completed",
            "event_id": "evt-lab-2",
            "tenant_id": tenant,
            "correlation_id": "corr-lab-2",
            "payload": {
                "encounter_id": encounter_id,
                "patient_id": patient_id,
                "admission_id": "adm-1",
            },
        }
    )
    orders2 = await get_laboratory_service().list_orders(tenant)
    assert orders2.unwrap()["total"] == 1


@pytest.mark.asyncio
async def test_hospital_encounter_started_does_not_create_order():
    tenant = "lab-acl-2"
    await InProcessEventBus.publish(
        {
            "event_name": "hospital.encounter.started",
            "event_id": "evt-lab-start",
            "tenant_id": tenant,
            "correlation_id": "corr-start",
            "payload": {
                "encounter_id": "bbbbbbbb-bbbb-cccc-dddd-eeeeeeeeeeee",
                "patient_id": "11111111-2222-3333-4444-555555555555",
                "admission_id": "adm-2",
            },
        }
    )
    orders = await get_laboratory_service().list_orders(tenant)
    assert orders.unwrap()["total"] == 0


@pytest.mark.asyncio
async def test_clinic_encounter_completed_creates_review_order():
    tenant = "lab-acl-clinic"
    encounter_id = "cccccccc-bbbb-cccc-dddd-eeeeeeeeeeee"
    patient_id = "22222222-2222-3333-4444-555555555555"

    await InProcessEventBus.publish(
        {
            "event_name": "clinic.encounter.completed",
            "event_id": "evt-cln-1",
            "tenant_id": tenant,
            "correlation_id": "corr-cln-1",
            "payload": {
                "encounter_id": encounter_id,
                "patient_id": patient_id,
            },
        }
    )

    orders = await get_laboratory_service().list_orders(tenant)
    assert orders.succeeded
    items = orders.unwrap()["items"]
    assert len(items) == 1
    assert items[0]["order_number"].startswith("CLN-")
    assert items[0]["test_code"] == "REVIEW"
    assert items[0]["source_encounter_ref"] == encounter_id
