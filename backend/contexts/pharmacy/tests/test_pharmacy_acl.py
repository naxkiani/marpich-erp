"""ACL — hospital.encounter.completed + inventory.stock.adjusted → pharmacy."""
from __future__ import annotations

import pytest

from contexts.pharmacy.container import get_pharmacy_service, reset_pharmacy_service
from contexts.pharmacy.infrastructure.persistence.memory_store import PharmacyMemoryStore
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.messaging.event_fabric import EventFabric


@pytest.fixture(autouse=True)
def reset_all():
    PharmacyMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_pharmacy_service()
    get_pharmacy_service()
    yield
    PharmacyMemoryStore.reset()
    InProcessEventBus.reset()
    EventFabric.reset_dev_state()
    reset_pharmacy_service()


@pytest.mark.asyncio
async def test_hospital_encounter_completed_creates_review_rx():
    tenant = "rx-acl-1"
    encounter_id = "cccccccc-bbbb-cccc-dddd-eeeeeeeeeeee"
    patient_id = "aaaaaaaa-2222-3333-4444-555555555555"

    await InProcessEventBus.publish(
        {
            "event_name": "hospital.encounter.completed",
            "event_id": "evt-rx-1",
            "tenant_id": tenant,
            "correlation_id": "corr-rx-1",
            "payload": {
                "encounter_id": encounter_id,
                "patient_id": patient_id,
                "admission_id": "adm-1",
            },
        }
    )

    listed = await get_pharmacy_service().list_prescriptions(tenant)
    assert listed.succeeded
    items = listed.unwrap()["items"]
    assert len(items) == 1
    assert items[0]["drug_code"] == "REVIEW"
    assert items[0]["source_encounter_ref"] == encounter_id


@pytest.mark.asyncio
async def test_inventory_stock_adjusted_noted():
    tenant = "rx-acl-2"
    await InProcessEventBus.publish(
        {
            "event_name": "inventory.stock.adjusted",
            "event_id": "evt-stock-1",
            "tenant_id": tenant,
            "correlation_id": "corr-stock",
            "payload": {
                "sku": "AMOX-500",
                "quantity_on_hand": 42,
                "reason": "receive",
            },
        }
    )
    # no crash; prescriptions unchanged
    listed = await get_pharmacy_service().list_prescriptions(tenant)
    assert listed.unwrap()["total"] == 0


@pytest.mark.asyncio
async def test_clinic_encounter_completed_creates_review_rx():
    tenant = "rx-acl-clinic"
    encounter_id = "dddddddd-bbbb-cccc-dddd-eeeeeeeeeeee"
    patient_id = "bbbbbbbb-2222-3333-4444-555555555555"

    await InProcessEventBus.publish(
        {
            "event_name": "clinic.encounter.completed",
            "event_id": "evt-rx-cln",
            "tenant_id": tenant,
            "correlation_id": "corr-rx-cln",
            "payload": {
                "encounter_id": encounter_id,
                "patient_id": patient_id,
            },
        }
    )

    listed = await get_pharmacy_service().list_prescriptions(tenant)
    items = listed.unwrap()["items"]
    assert len(items) == 1
    assert items[0]["rx_number"].startswith("CLN-")
    assert items[0]["drug_code"] == "REVIEW"
