"""Municipality application service."""
from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal

from contexts.municipality.domain.aggregates.permit import Permit
from contexts.municipality.domain.aggregates.service_request import ServiceRequest
from contexts.municipality.domain.aggregates.utility_account import UtilityAccount, UtilityType
from contexts.municipality.domain.ports.repositories import (
    IPermitRepository,
    IServiceRequestRepository,
    IUtilityAccountRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class ConsoleMunicipalityAudit:
    async def log(self, **kwargs: object) -> None:
        entry = {"type": "audit", "context": "municipality", **kwargs, "occurred_at": datetime.now(UTC).isoformat()}
        print(json.dumps(entry, default=str))


class MunicipalityApplicationService:
    def __init__(
        self,
        permits: IPermitRepository,
        service_requests: IServiceRequestRepository,
        utility_accounts: IUtilityAccountRepository,
        audit: ConsoleMunicipalityAudit | None = None,
    ) -> None:
        self._permits = permits
        self._service_requests = service_requests
        self._utility_accounts = utility_accounts
        self._audit = audit or ConsoleMunicipalityAudit()

    async def apply_permit(
        self,
        *,
        tenant_id: str,
        applicant_name: str,
        permit_type: str,
        description: str,
        correlation_id: str,
    ) -> Result[dict]:
        permit = Permit.apply(
            tenant_id=tenant_id,
            applicant_name=applicant_name,
            permit_type=permit_type,
            description=description,
        )
        await self._permits.save(permit)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="municipality.permit.submitted",
            resource_type="permit",
            resource_id=str(permit.id),
        )
        return Result.ok(permit.to_dict())

    async def issue_permit(self, *, tenant_id: str, permit_id: str, correlation_id: str) -> Result[dict]:
        permit = await self._permits.find_by_id(tenant_id, UniqueId.from_string(permit_id))
        if not permit:
            return Result.fail("municipality.errors.permit_not_found")
        try:
            event = permit.issue(correlation_id=correlation_id)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._permits.save(permit)
        await publish_integration_event(event)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="municipality.permit.issued",
            resource_type="permit",
            resource_id=str(permit.id),
        )
        return Result.ok(permit.to_dict())

    async def list_permits(self, tenant_id: str) -> Result[list[dict]]:
        permits = await self._permits.list_permits(tenant_id)
        return Result.ok([p.to_dict() for p in permits])

    async def open_service_request(
        self,
        *,
        tenant_id: str,
        citizen_name: str,
        category: str,
        description: str,
        correlation_id: str,
    ) -> Result[dict]:
        request = ServiceRequest.open(
            tenant_id=tenant_id,
            citizen_name=citizen_name,
            category=category,
            description=description,
        )
        await self._service_requests.save(request)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="municipality.service_request.opened",
            resource_type="service_request",
            resource_id=str(request.id),
        )
        return Result.ok(request.to_dict())

    async def close_service_request(
        self, *, tenant_id: str, request_id: str, resolution: str, correlation_id: str
    ) -> Result[dict]:
        request = await self._service_requests.find_by_id(tenant_id, UniqueId.from_string(request_id))
        if not request:
            return Result.fail("municipality.errors.request_not_found")
        try:
            event = request.close(correlation_id=correlation_id, resolution=resolution)
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._service_requests.save(request)
        await publish_integration_event(event)
        return Result.ok(request.to_dict())

    async def register_utility_account(
        self,
        *,
        tenant_id: str,
        account_number: str,
        holder_name: str,
        utility_type: str,
        correlation_id: str,
    ) -> Result[dict]:
        if await self._utility_accounts.find_by_number(tenant_id, account_number):
            return Result.fail("municipality.errors.account_exists")
        account = UtilityAccount.register(
            tenant_id=tenant_id,
            account_number=account_number,
            holder_name=holder_name,
            utility_type=UtilityType(utility_type),
        )
        await self._utility_accounts.save(account)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="municipality.utility.registered",
            resource_type="utility_account",
            resource_id=str(account.id),
        )
        return Result.ok(account.to_dict())

    async def issue_utility_bill(
        self,
        *,
        tenant_id: str,
        account_id: str,
        amount: Decimal,
        period: str,
        correlation_id: str,
    ) -> Result[dict]:
        account = await self._utility_accounts.find_by_id(tenant_id, UniqueId.from_string(account_id))
        if not account:
            return Result.fail("municipality.errors.account_not_found")
        try:
            event = account.issue_bill(correlation_id=correlation_id, amount=amount, period=period)
        except ValueError as exc:
            return Result.fail(str(exc))
        await publish_integration_event(event)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="municipality.utility.bill.issued",
            resource_type="utility_account",
            resource_id=str(account.id),
            payload={"amount": str(amount), "period": period},
        )
        return Result.ok({"account": account.to_dict(), "bill": event.to_payload()})
