"""PostgreSQL repositories — Tax (CAP-ENT-026)."""
from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from contexts.tax.domain.aggregates.tax_liability import TaxLiability, TaxLiabilityStatus
from contexts.tax.domain.aggregates.tax_return import TaxReturn, TaxReturnStatus
from contexts.tax.domain.ports.repositories import ITaxLiabilityRepository, ITaxReturnRepository
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import TaxLiabilityRow, TaxReturnRow


class PostgresTaxLiabilityRepository(ITaxLiabilityRepository):
    async def save(self, liability: TaxLiability) -> None:
        async with session_scope(tenant_id=liability.tenant_id) as session:
            row = await session.get(TaxLiabilityRow, UUID(str(liability.id)))
            if row is None:
                session.add(
                    TaxLiabilityRow(
                        id=UUID(str(liability.id)),
                        tenant_id=liability.tenant_id,
                        payroll_run_id=UUID(str(liability.payroll_run_id)),
                        period_label=liability.period_label,
                        taxable_base=liability.taxable_base,
                        tax_amount=liability.tax_amount,
                        currency=liability.currency,
                        status=liability.status.value,
                        correlation_id=liability.correlation_id,
                        created_at=liability.created_at,
                        updated_at=liability.updated_at,
                    )
                )
            else:
                row.period_label = liability.period_label
                row.taxable_base = liability.taxable_base
                row.tax_amount = liability.tax_amount
                row.currency = liability.currency
                row.status = liability.status.value
                row.correlation_id = liability.correlation_id
                row.updated_at = liability.updated_at

    async def find_by_id(self, tenant_id: str, liability_id: UniqueId) -> TaxLiability | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.get(TaxLiabilityRow, UUID(str(liability_id)))
            return _liability_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_by_payroll_run(
        self, tenant_id: str, payroll_run_id: UniqueId
    ) -> TaxLiability | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.scalar(
                select(TaxLiabilityRow).where(
                    TaxLiabilityRow.tenant_id == tenant_id,
                    TaxLiabilityRow.payroll_run_id == UUID(str(payroll_run_id)),
                )
            )
            return _liability_from_row(row) if row else None

    async def list_open(
        self, tenant_id: str, *, period_label: str | None = None
    ) -> list[TaxLiability]:
        async with session_scope(tenant_id=tenant_id) as session:
            stmt = select(TaxLiabilityRow).where(
                TaxLiabilityRow.tenant_id == tenant_id,
                TaxLiabilityRow.status == TaxLiabilityStatus.OPEN.value,
            )
            if period_label:
                stmt = stmt.where(TaxLiabilityRow.period_label == period_label.strip())
            rows = (await session.scalars(stmt)).all()
        return [_liability_from_row(r) for r in rows]

    async def list_all(self, tenant_id: str) -> list[TaxLiability]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(TaxLiabilityRow).where(TaxLiabilityRow.tenant_id == tenant_id)
                )
            ).all()
        return [_liability_from_row(r) for r in rows]


class PostgresTaxReturnRepository(ITaxReturnRepository):
    async def save(self, tax_return: TaxReturn) -> None:
        async with session_scope(tenant_id=tax_return.tenant_id) as session:
            row = await session.get(TaxReturnRow, UUID(str(tax_return.id)))
            ids = [str(i) for i in tax_return.liability_ids]
            if row is None:
                session.add(
                    TaxReturnRow(
                        id=UUID(str(tax_return.id)),
                        tenant_id=tax_return.tenant_id,
                        period_label=tax_return.period_label,
                        status=tax_return.status.value,
                        liability_ids=ids,
                        total_tax=tax_return.total_tax,
                        currency=tax_return.currency,
                        correlation_id=tax_return.correlation_id,
                        created_at=tax_return.created_at,
                        updated_at=tax_return.updated_at,
                        filed_at=tax_return.filed_at,
                    )
                )
            else:
                row.period_label = tax_return.period_label
                row.status = tax_return.status.value
                row.liability_ids = ids
                row.total_tax = tax_return.total_tax
                row.currency = tax_return.currency
                row.correlation_id = tax_return.correlation_id
                row.updated_at = tax_return.updated_at
                row.filed_at = tax_return.filed_at

    async def find_by_id(self, tenant_id: str, return_id: UniqueId) -> TaxReturn | None:
        async with session_scope(tenant_id=tenant_id) as session:
            row = await session.get(TaxReturnRow, UUID(str(return_id)))
            return _return_from_row(row) if row and row.tenant_id == tenant_id else None

    async def list_returns(self, tenant_id: str) -> list[TaxReturn]:
        async with session_scope(tenant_id=tenant_id) as session:
            rows = (
                await session.scalars(
                    select(TaxReturnRow).where(TaxReturnRow.tenant_id == tenant_id)
                )
            ).all()
        return [_return_from_row(r) for r in rows]


def _liability_from_row(row: TaxLiabilityRow) -> TaxLiability:
    return TaxLiability(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        payroll_run_id=UniqueId.from_string(str(row.payroll_run_id)),
        period_label=row.period_label,
        taxable_base=Decimal(str(row.taxable_base)),
        tax_amount=Decimal(str(row.tax_amount)),
        currency=row.currency,
        status=TaxLiabilityStatus(row.status),
        correlation_id=row.correlation_id or "",
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _return_from_row(row: TaxReturnRow) -> TaxReturn:
    return TaxReturn(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        period_label=row.period_label,
        status=TaxReturnStatus(row.status),
        liability_ids=[UniqueId.from_string(str(i)) for i in (row.liability_ids or [])],
        total_tax=Decimal(str(row.total_tax)),
        currency=row.currency,
        correlation_id=row.correlation_id or "",
        created_at=row.created_at,
        updated_at=row.updated_at,
        filed_at=row.filed_at,
    )
