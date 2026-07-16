"""Pharmacy repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.pharmacy.domain.aggregates.dispense_record import DispenseRecord
from contexts.pharmacy.domain.aggregates.prescription import Prescription
from shared.domain.value_objects.unique_id import UniqueId


class IPrescriptionRepository(Protocol):
    async def save(self, prescription: Prescription) -> None: ...
    async def find_by_id(self, tenant_id: str, prescription_id: UniqueId) -> Prescription | None: ...
    async def find_by_rx_number(self, tenant_id: str, rx_number: str) -> Prescription | None: ...
    async def list_prescriptions(self, tenant_id: str) -> list[Prescription]: ...


class IDispenseRepository(Protocol):
    async def save(self, dispense: DispenseRecord) -> None: ...
    async def list_dispenses(self, tenant_id: str) -> list[DispenseRecord]: ...
