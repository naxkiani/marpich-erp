"""Pharmacy in-memory repositories."""
from __future__ import annotations

from contexts.pharmacy.domain.aggregates.dispense_record import DispenseRecord
from contexts.pharmacy.domain.aggregates.prescription import Prescription
from contexts.pharmacy.domain.ports.repositories import IDispenseRepository, IPrescriptionRepository
from shared.domain.value_objects.unique_id import UniqueId


class PharmacyMemoryStore:
    prescriptions: dict[str, Prescription] = {}
    dispenses: dict[str, DispenseRecord] = {}

    @classmethod
    def reset(cls) -> None:
        cls.prescriptions.clear()
        cls.dispenses.clear()


class InMemoryPrescriptionRepository(IPrescriptionRepository):
    async def save(self, prescription: Prescription) -> None:
        PharmacyMemoryStore.prescriptions[str(prescription.id)] = prescription

    async def find_by_id(self, tenant_id: str, prescription_id: UniqueId) -> Prescription | None:
        row = PharmacyMemoryStore.prescriptions.get(str(prescription_id))
        return row if row and row.tenant_id == tenant_id else None

    async def find_by_rx_number(self, tenant_id: str, rx_number: str) -> Prescription | None:
        key = rx_number.strip().upper()
        for row in PharmacyMemoryStore.prescriptions.values():
            if row.tenant_id == tenant_id and row.rx_number == key:
                return row
        return None

    async def list_prescriptions(self, tenant_id: str) -> list[Prescription]:
        rows = [r for r in PharmacyMemoryStore.prescriptions.values() if r.tenant_id == tenant_id]
        return sorted(rows, key=lambda r: r.created_at, reverse=True)


class InMemoryDispenseRepository(IDispenseRepository):
    async def save(self, dispense: DispenseRecord) -> None:
        PharmacyMemoryStore.dispenses[str(dispense.id)] = dispense

    async def list_dispenses(self, tenant_id: str) -> list[DispenseRecord]:
        rows = [r for r in PharmacyMemoryStore.dispenses.values() if r.tenant_id == tenant_id]
        return sorted(rows, key=lambda r: r.dispensed_at, reverse=True)
