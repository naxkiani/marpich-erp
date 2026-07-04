"""PostgreSQL billing repository — Accounting."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from contexts.accounting.domain.aggregates.billing_encounter import BillingEncounter, BillingStatus
from contexts.accounting.domain.ports.repositories import IBillingRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import BillingEncounterRow


class PostgresBillingRepository(IBillingRepository):
    async def save(self, billing: BillingEncounter) -> None:
        async with session_scope() as session:
            row = await session.get(BillingEncounterRow, UUID(str(billing.id)))
            if row is None:
                row = BillingEncounterRow(
                    id=UUID(str(billing.id)),
                    tenant_id=billing.tenant_id,
                    external_encounter_id=billing.external_encounter_id,
                    patient_ref=UUID(str(billing.patient_ref)),
                    procedure_codes=list(billing.procedure_codes),
                    line_items=list(billing.line_items),
                    total_amount=billing.total_amount,
                    currency=billing.currency,
                    status=billing.status.value,
                    correlation_id=billing.correlation_id,
                    created_at=billing.created_at,
                )
                session.add(row)
            else:
                row.status = billing.status.value
                row.line_items = list(billing.line_items)
                row.total_amount = billing.total_amount

    async def find_by_id(self, tenant_id: str, billing_id: UniqueId) -> BillingEncounter | None:
        async with session_scope() as session:
            row = await session.get(BillingEncounterRow, UUID(str(billing_id)))
            if row and row.tenant_id == tenant_id:
                return _billing_from_row(row)
            return None

    async def find_by_external_encounter(
        self, tenant_id: str, external_encounter_id: str
    ) -> BillingEncounter | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(BillingEncounterRow).where(
                    BillingEncounterRow.tenant_id == tenant_id,
                    BillingEncounterRow.external_encounter_id == external_encounter_id,
                )
            )
            return _billing_from_row(row) if row else None

    async def list_billings(self, tenant_id: str) -> list[BillingEncounter]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BillingEncounterRow).where(BillingEncounterRow.tenant_id == tenant_id)
                )
            ).all()
        return [_billing_from_row(r) for r in rows]


def _billing_from_row(row: BillingEncounterRow) -> BillingEncounter:
    return BillingEncounter(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        external_encounter_id=row.external_encounter_id,
        patient_ref=str(row.patient_ref),
        procedure_codes=list(row.procedure_codes or []),
        line_items=list(row.line_items or []),
        total_amount=float(row.total_amount),
        currency=row.currency,
        status=BillingStatus(row.status),
        correlation_id=row.correlation_id,
        created_at=row.created_at,
    )
