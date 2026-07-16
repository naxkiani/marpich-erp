"""PostgreSQL repositories — Pharmacy (CAP-HLT-008)."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.pharmacy.domain.aggregates.dispense_record import DispenseRecord
from contexts.pharmacy.domain.aggregates.prescription import Prescription
from contexts.pharmacy.domain.ports.repositories import IDispenseRepository, IPrescriptionRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import PharmacyDispenseRow, PharmacyPrescriptionRow


class PostgresPrescriptionRepository(IPrescriptionRepository):
    async def save(self, prescription: Prescription) -> None:
        async with session_scope() as session:
            row = await session.get(PharmacyPrescriptionRow, UUID(str(prescription.id)))
            if row is None:
                session.add(
                    PharmacyPrescriptionRow(
                        id=UUID(str(prescription.id)),
                        tenant_id=prescription.tenant_id,
                        rx_number=prescription.rx_number,
                        patient_ref=prescription.patient_ref,
                        drug_code=prescription.drug_code,
                        drug_name=prescription.drug_name,
                        quantity=prescription.quantity,
                        status=prescription.status,
                        source_encounter_ref=prescription.source_encounter_ref,
                        created_at=prescription.created_at,
                    )
                )
            else:
                row.status = prescription.status
                row.quantity = prescription.quantity
                row.drug_name = prescription.drug_name

    async def find_by_id(self, tenant_id: str, prescription_id: UniqueId) -> Prescription | None:
        async with session_scope() as session:
            row = await session.get(PharmacyPrescriptionRow, UUID(str(prescription_id)))
            return _prescription_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_by_rx_number(self, tenant_id: str, rx_number: str) -> Prescription | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(PharmacyPrescriptionRow).where(
                    PharmacyPrescriptionRow.tenant_id == tenant_id,
                    PharmacyPrescriptionRow.rx_number == rx_number.strip().upper(),
                )
            )
            return _prescription_from_row(row) if row else None

    async def list_prescriptions(self, tenant_id: str) -> list[Prescription]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(PharmacyPrescriptionRow)
                    .where(PharmacyPrescriptionRow.tenant_id == tenant_id)
                    .order_by(PharmacyPrescriptionRow.created_at.desc())
                )
            ).all()
        return [_prescription_from_row(r) for r in rows]


class PostgresDispenseRepository(IDispenseRepository):
    async def save(self, dispense: DispenseRecord) -> None:
        async with session_scope() as session:
            row = await session.get(PharmacyDispenseRow, UUID(str(dispense.id)))
            if row is None:
                session.add(
                    PharmacyDispenseRow(
                        id=UUID(str(dispense.id)),
                        tenant_id=dispense.tenant_id,
                        prescription_id=UUID(str(dispense.prescription_id)),
                        patient_ref=dispense.patient_ref,
                        drug_code=dispense.drug_code,
                        quantity_dispensed=dispense.quantity_dispensed,
                        dispensed_by=dispense.dispensed_by,
                        dispensed_at=dispense.dispensed_at,
                    )
                )

    async def list_dispenses(self, tenant_id: str) -> list[DispenseRecord]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(PharmacyDispenseRow)
                    .where(PharmacyDispenseRow.tenant_id == tenant_id)
                    .order_by(PharmacyDispenseRow.dispensed_at.desc())
                )
            ).all()
        return [_dispense_from_row(r) for r in rows]


def _prescription_from_row(row: PharmacyPrescriptionRow) -> Prescription:
    return Prescription(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        rx_number=row.rx_number,
        patient_ref=row.patient_ref,
        drug_code=row.drug_code,
        drug_name=row.drug_name,
        quantity=float(row.quantity),
        status=row.status,
        source_encounter_ref=row.source_encounter_ref,
        created_at=row.created_at,
    )


def _dispense_from_row(row: PharmacyDispenseRow) -> DispenseRecord:
    return DispenseRecord(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        prescription_id=UniqueId.from_string(str(row.prescription_id)),
        patient_ref=row.patient_ref,
        drug_code=row.drug_code,
        quantity_dispensed=float(row.quantity_dispensed),
        dispensed_by=row.dispensed_by,
        dispensed_at=row.dispensed_at,
    )
