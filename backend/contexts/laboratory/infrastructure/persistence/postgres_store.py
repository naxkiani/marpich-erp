"""PostgreSQL repositories — Laboratory (CAP-HLT-007)."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.laboratory.domain.aggregates.sample import Sample
from contexts.laboratory.domain.aggregates.test_order import TestOrder
from contexts.laboratory.domain.ports.repositories import ISampleRepository, ITestOrderRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import LaboratorySampleRow, LaboratoryTestOrderRow


class PostgresTestOrderRepository(ITestOrderRepository):
    async def save(self, order: TestOrder) -> None:
        async with session_scope() as session:
            row = await session.get(LaboratoryTestOrderRow, UUID(str(order.id)))
            if row is None:
                session.add(
                    LaboratoryTestOrderRow(
                        id=UUID(str(order.id)),
                        tenant_id=order.tenant_id,
                        order_number=order.order_number,
                        patient_ref=order.patient_ref,
                        test_code=order.test_code,
                        status=order.status,
                        result_value=order.result_value,
                        result_unit=order.result_unit,
                        source_encounter_ref=order.source_encounter_ref,
                        created_at=order.created_at,
                        finalized_at=order.finalized_at,
                    )
                )
            else:
                row.status = order.status
                row.result_value = order.result_value
                row.result_unit = order.result_unit
                row.finalized_at = order.finalized_at

    async def find_by_id(self, tenant_id: str, order_id: UniqueId) -> TestOrder | None:
        async with session_scope() as session:
            row = await session.get(LaboratoryTestOrderRow, UUID(str(order_id)))
            return _order_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_by_number(self, tenant_id: str, order_number: str) -> TestOrder | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(LaboratoryTestOrderRow).where(
                    LaboratoryTestOrderRow.tenant_id == tenant_id,
                    LaboratoryTestOrderRow.order_number == order_number.strip().upper(),
                )
            )
            return _order_from_row(row) if row else None

    async def list_orders(self, tenant_id: str) -> list[TestOrder]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(LaboratoryTestOrderRow)
                    .where(LaboratoryTestOrderRow.tenant_id == tenant_id)
                    .order_by(LaboratoryTestOrderRow.created_at.desc())
                )
            ).all()
        return [_order_from_row(r) for r in rows]


class PostgresSampleRepository(ISampleRepository):
    async def save(self, sample: Sample) -> None:
        async with session_scope() as session:
            row = await session.get(LaboratorySampleRow, UUID(str(sample.id)))
            if row is None:
                session.add(
                    LaboratorySampleRow(
                        id=UUID(str(sample.id)),
                        tenant_id=sample.tenant_id,
                        order_id=UUID(str(sample.order_id)),
                        accession_number=sample.accession_number,
                        specimen_type=sample.specimen_type,
                        patient_ref=sample.patient_ref,
                        received_at=sample.received_at,
                    )
                )

    async def list_samples(self, tenant_id: str) -> list[Sample]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(LaboratorySampleRow)
                    .where(LaboratorySampleRow.tenant_id == tenant_id)
                    .order_by(LaboratorySampleRow.received_at.desc())
                )
            ).all()
        return [_sample_from_row(r) for r in rows]


def _order_from_row(row: LaboratoryTestOrderRow) -> TestOrder:
    return TestOrder(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        order_number=row.order_number,
        patient_ref=row.patient_ref,
        test_code=row.test_code,
        status=row.status,
        result_value=row.result_value,
        result_unit=row.result_unit,
        source_encounter_ref=row.source_encounter_ref,
        created_at=row.created_at,
        finalized_at=row.finalized_at,
    )


def _sample_from_row(row: LaboratorySampleRow) -> Sample:
    return Sample(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        order_id=UniqueId.from_string(str(row.order_id)),
        accession_number=row.accession_number,
        specimen_type=row.specimen_type,
        patient_ref=row.patient_ref,
        received_at=row.received_at,
    )
