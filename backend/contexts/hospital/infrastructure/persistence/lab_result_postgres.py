"""PostgreSQL lab result projections — hospital schema."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.hospital.domain.entities.lab_result_projection import LabResultProjection
from contexts.hospital.domain.ports.repositories import ILabResultProjectionRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import HospitalLabResultProjectionRow


class PostgresLabResultProjectionRepository(ILabResultProjectionRepository):
    async def save(self, projection: LabResultProjection) -> None:
        async with session_scope() as session:
            existing = await session.scalar(
                select(HospitalLabResultProjectionRow).where(
                    HospitalLabResultProjectionRow.tenant_id == projection.tenant_id,
                    HospitalLabResultProjectionRow.source_event_id == projection.source_event_id,
                )
            )
            if existing is not None:
                return
            session.add(
                HospitalLabResultProjectionRow(
                    id=UUID(str(projection.id)),
                    tenant_id=projection.tenant_id,
                    order_id=projection.order_id,
                    patient_ref=projection.patient_ref,
                    test_code=projection.test_code,
                    result_value=projection.result_value,
                    result_unit=projection.result_unit,
                    source_event_id=projection.source_event_id,
                    projected_at=projection.projected_at,
                )
            )

    async def find_by_event_id(
        self, tenant_id: str, source_event_id: str
    ) -> LabResultProjection | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(HospitalLabResultProjectionRow).where(
                    HospitalLabResultProjectionRow.tenant_id == tenant_id,
                    HospitalLabResultProjectionRow.source_event_id == source_event_id,
                )
            )
            return _from_row(row) if row else None

    async def list_projections(self, tenant_id: str) -> list[LabResultProjection]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(HospitalLabResultProjectionRow)
                    .where(HospitalLabResultProjectionRow.tenant_id == tenant_id)
                    .order_by(HospitalLabResultProjectionRow.projected_at.desc())
                )
            ).all()
        return [_from_row(r) for r in rows]


def _from_row(row: HospitalLabResultProjectionRow) -> LabResultProjection:
    return LabResultProjection(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        order_id=row.order_id,
        patient_ref=row.patient_ref,
        test_code=row.test_code,
        result_value=row.result_value,
        result_unit=row.result_unit,
        source_event_id=row.source_event_id,
        projected_at=row.projected_at,
    )
