"""PostgreSQL repositories — Municipality bounded context."""
from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from contexts.municipality.domain.aggregates.permit import Permit, PermitStatus
from contexts.municipality.domain.aggregates.service_request import ServiceRequest, ServiceRequestStatus
from contexts.municipality.domain.aggregates.utility_account import UtilityAccount, UtilityType
from contexts.municipality.domain.ports.repositories import (
    IPermitRepository,
    IServiceRequestRepository,
    IUtilityAccountRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import MunicipalityPermitRow, MunicipalityServiceRequestRow, MunicipalityUtilityAccountRow


class PostgresPermitRepository(IPermitRepository):
    async def save(self, permit: Permit) -> None:
        async with session_scope() as session:
            row = await session.get(MunicipalityPermitRow, UUID(str(permit.id)))
            if row is None:
                session.add(
                    MunicipalityPermitRow(
                        id=UUID(str(permit.id)),
                        tenant_id=permit.tenant_id,
                        applicant_name=permit.applicant_name,
                        permit_type=permit.permit_type,
                        description=permit.description,
                        status=permit.status.value,
                        issued_at=permit.issued_at,
                    )
                )
            else:
                row.status = permit.status.value
                row.issued_at = permit.issued_at

    async def find_by_id(self, tenant_id: str, permit_id: UniqueId) -> Permit | None:
        async with session_scope() as session:
            row = await session.get(MunicipalityPermitRow, UUID(str(permit_id)))
            return _permit_from_row(row) if row and row.tenant_id == tenant_id else None

    async def list_permits(self, tenant_id: str) -> list[Permit]:
        async with session_scope() as session:
            rows = (await session.scalars(select(MunicipalityPermitRow).where(MunicipalityPermitRow.tenant_id == tenant_id))).all()
        return [_permit_from_row(r) for r in rows]


class PostgresServiceRequestRepository(IServiceRequestRepository):
    async def save(self, request: ServiceRequest) -> None:
        async with session_scope() as session:
            row = await session.get(MunicipalityServiceRequestRow, UUID(str(request.id)))
            if row is None:
                session.add(
                    MunicipalityServiceRequestRow(
                        id=UUID(str(request.id)),
                        tenant_id=request.tenant_id,
                        citizen_name=request.citizen_name,
                        category=request.category,
                        description=request.description,
                        status=request.status.value,
                        closed_at=request.closed_at,
                    )
                )
            else:
                row.status = request.status.value
                row.closed_at = request.closed_at

    async def find_by_id(self, tenant_id: str, request_id: UniqueId) -> ServiceRequest | None:
        async with session_scope() as session:
            row = await session.get(MunicipalityServiceRequestRow, UUID(str(request_id)))
            return _request_from_row(row) if row and row.tenant_id == tenant_id else None

    async def list_open(self, tenant_id: str) -> list[ServiceRequest]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(MunicipalityServiceRequestRow).where(
                        MunicipalityServiceRequestRow.tenant_id == tenant_id,
                        MunicipalityServiceRequestRow.status != ServiceRequestStatus.CLOSED.value,
                    )
                )
            ).all()
        return [_request_from_row(r) for r in rows]


class PostgresUtilityAccountRepository(IUtilityAccountRepository):
    async def save(self, account: UtilityAccount) -> None:
        async with session_scope() as session:
            row = await session.get(MunicipalityUtilityAccountRow, UUID(str(account.id)))
            if row is None:
                session.add(
                    MunicipalityUtilityAccountRow(
                        id=UUID(str(account.id)),
                        tenant_id=account.tenant_id,
                        account_number=account.account_number,
                        holder_name=account.holder_name,
                        utility_type=account.utility_type.value,
                    )
                )

    async def find_by_id(self, tenant_id: str, account_id: UniqueId) -> UtilityAccount | None:
        async with session_scope() as session:
            row = await session.get(MunicipalityUtilityAccountRow, UUID(str(account_id)))
            return _account_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_by_number(self, tenant_id: str, account_number: str) -> UtilityAccount | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(MunicipalityUtilityAccountRow).where(
                    MunicipalityUtilityAccountRow.tenant_id == tenant_id,
                    MunicipalityUtilityAccountRow.account_number == account_number.upper(),
                )
            )
            return _account_from_row(row) if row else None


def _permit_from_row(row: MunicipalityPermitRow) -> Permit:
    return Permit(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        applicant_name=row.applicant_name,
        permit_type=row.permit_type,
        description=row.description,
        status=PermitStatus(row.status),
        created_at=row.created_at,
        issued_at=row.issued_at,
    )


def _request_from_row(row: MunicipalityServiceRequestRow) -> ServiceRequest:
    return ServiceRequest(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        citizen_name=row.citizen_name,
        category=row.category,
        description=row.description,
        status=ServiceRequestStatus(row.status),
        created_at=row.created_at,
        closed_at=row.closed_at,
    )


def _account_from_row(row: MunicipalityUtilityAccountRow) -> UtilityAccount:
    return UtilityAccount(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        account_number=row.account_number,
        holder_name=row.holder_name,
        utility_type=UtilityType(row.utility_type),
        created_at=row.created_at,
    )
