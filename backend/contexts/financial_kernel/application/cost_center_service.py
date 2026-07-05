"""Enterprise Cost Centers application service."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.cost_center import (
    AllocationType,
    CenterAllocation,
    CenterType,
    EnterpriseCostCenter,
    EnterpriseProfitCenter,
)
from contexts.financial_kernel.domain.events.integration_events import (
    CenterAllocationCreatedIntegration,
    CostCenterCreatedIntegration,
    ProfitCenterCreatedIntegration,
)
from contexts.financial_kernel.domain.ports.cost_center_repositories import (
    ICenterAllocationRepository,
    IEnterpriseCostCenterRepository,
    IEnterpriseProfitCenterRepository,
)
from contexts.financial_kernel.domain.ports.repositories import IChartOfAccountRepository, IJournalRepository
from contexts.financial_kernel.domain.services.cost_center_engine import (
    compute_profitability,
    rollup_profitability,
    split_allocation,
    validate_allocation_amount,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class CostCenterApplicationService:
    def __init__(
        self,
        cost_centers: IEnterpriseCostCenterRepository,
        profit_centers: IEnterpriseProfitCenterRepository,
        allocations: ICenterAllocationRepository,
        journals: IJournalRepository,
        accounts: IChartOfAccountRepository,
    ) -> None:
        self._cost_centers = cost_centers
        self._profit_centers = profit_centers
        self._allocations = allocations
        self._journals = journals
        self._accounts = accounts

    async def create_cost_center(
        self,
        *,
        tenant_id: str,
        code: str,
        name: str,
        center_type: str,
        parent_id: str | None = None,
        profit_center_id: str | None = None,
        manager_id: str | None = None,
        metadata: dict | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        try:
            CenterType(center_type)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_center_type")

        existing = await self._cost_centers.find_by_code(tenant_id, code)
        if existing:
            return Result.fail("financial_kernel.errors.cost_center_exists")

        if parent_id:
            parent = await self._cost_centers.find_by_id(parent_id)
            if not parent or parent.tenant_id != tenant_id:
                return Result.fail("financial_kernel.errors.parent_not_found")

        if profit_center_id:
            pc = await self._profit_centers.find_by_id(profit_center_id)
            if not pc or pc.tenant_id != tenant_id:
                return Result.fail("financial_kernel.errors.profit_center_not_found")

        center = EnterpriseCostCenter.create(
            tenant_id=tenant_id,
            code=code,
            name=name,
            center_type=center_type,
            parent_id=parent_id,
            profit_center_id=profit_center_id,
            manager_id=manager_id,
            metadata=metadata,
        )
        await self._cost_centers.save(center)

        await publish_integration_event(
            CostCenterCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                cost_center_id=str(center.id),
                code=center.code,
                center_type=center_type,
                name=center.name,
            )
        )
        return Result.ok(center.to_dict())

    async def create_profit_center(
        self,
        *,
        tenant_id: str,
        code: str,
        name: str,
        business_unit_id: str | None = None,
        metadata: dict | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        existing = await self._profit_centers.find_by_code(tenant_id, code)
        if existing:
            return Result.fail("financial_kernel.errors.profit_center_exists")

        if business_unit_id:
            bu = await self._cost_centers.find_by_id(business_unit_id)
            if not bu or bu.tenant_id != tenant_id or bu.center_type != CenterType.BUSINESS_UNIT.value:
                return Result.fail("financial_kernel.errors.business_unit_not_found")

        center = EnterpriseProfitCenter.create(
            tenant_id=tenant_id,
            code=code,
            name=name,
            business_unit_id=business_unit_id,
            metadata=metadata,
        )
        await self._profit_centers.save(center)

        await publish_integration_event(
            ProfitCenterCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                profit_center_id=str(center.id),
                code=center.code,
                name=center.name,
            )
        )
        return Result.ok(center.to_dict())

    async def list_cost_centers(
        self,
        tenant_id: str,
        center_type: str | None = None,
    ) -> Result[list[dict]]:
        if center_type:
            try:
                CenterType(center_type)
            except ValueError:
                return Result.fail("financial_kernel.errors.invalid_center_type")
            centers = await self._cost_centers.list_by_type(tenant_id, center_type)
        else:
            centers = await self._cost_centers.list_by_tenant(tenant_id)
        return Result.ok([c.to_dict() for c in centers])

    async def list_profit_centers(self, tenant_id: str) -> Result[list[dict]]:
        centers = await self._profit_centers.list_by_tenant(tenant_id)
        return Result.ok([c.to_dict() for c in centers])

    async def get_cost_center(self, tenant_id: str, center_id: str) -> Result[dict]:
        center = await self._cost_centers.find_by_id(center_id)
        if not center or center.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.cost_center_not_found")
        return Result.ok(center.to_dict())

    async def create_allocation(
        self,
        *,
        tenant_id: str,
        allocation_type: str,
        source_context: str,
        source_document_id: str,
        idempotency_key: str,
        cost_center_code: str,
        account_code: str,
        amount: float,
        currency: str = "USD",
        profit_center_code: str | None = None,
        period_id: str | None = None,
        description: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        existing = await self._allocations.find_by_idempotency(tenant_id, idempotency_key)
        if existing:
            return Result.ok(existing.to_dict())

        try:
            AllocationType(allocation_type)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_allocation_type")

        cc = await self._cost_centers.find_by_code(tenant_id, cost_center_code)
        if not cc:
            return Result.fail("financial_kernel.errors.cost_center_not_found")

        if profit_center_code:
            pc = await self._profit_centers.find_by_code(tenant_id, profit_center_code)
            if not pc:
                return Result.fail("financial_kernel.errors.profit_center_not_found")

        try:
            validate_allocation_amount(amount)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_allocation_amount")

        allocation = CenterAllocation.create(
            tenant_id=tenant_id,
            allocation_type=allocation_type,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            cost_center_code=cost_center_code,
            account_code=account_code,
            amount=amount,
            currency=currency,
            profit_center_code=profit_center_code,
            period_id=period_id,
            description=description,
        )
        await self._allocations.save(allocation)

        await publish_integration_event(
            CenterAllocationCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                allocation_id=str(allocation.id),
                allocation_type=allocation_type,
                cost_center_code=allocation.cost_center_code,
                amount=amount,
            )
        )
        return Result.ok(allocation.to_dict())

    async def split_allocation(
        self,
        *,
        tenant_id: str,
        allocation_type: str,
        source_context: str,
        source_document_id: str,
        account_code: str,
        total_amount: float,
        cost_center_codes: list[str],
        weights: list[float] | None = None,
        currency: str = "USD",
        period_id: str | None = None,
        correlation_id: str = "",
    ) -> Result[list[dict]]:
        if not cost_center_codes:
            return Result.fail("financial_kernel.errors.cost_centers_required")

        for code in cost_center_codes:
            cc = await self._cost_centers.find_by_code(tenant_id, code)
            if not cc:
                return Result.fail("financial_kernel.errors.cost_center_not_found")

        w = weights or [1.0] * len(cost_center_codes)
        if len(w) != len(cost_center_codes):
            return Result.fail("financial_kernel.errors.weight_count_mismatch")

        try:
            parts = split_allocation(total_amount, w)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_allocation_weights")

        results = []
        for code, part in zip(cost_center_codes, parts, strict=True):
            key = f"{source_context}:{source_document_id}:{code}:{allocation_type}"
            result = await self.create_allocation(
                tenant_id=tenant_id,
                allocation_type=allocation_type,
                source_context=source_context,
                source_document_id=source_document_id,
                idempotency_key=key,
                cost_center_code=code,
                account_code=account_code,
                amount=part,
                currency=currency,
                period_id=period_id,
                correlation_id=correlation_id,
            )
            if not result.succeeded:
                return result
            results.append(result.unwrap())
        return Result.ok(results)

    async def list_allocations(
        self,
        tenant_id: str,
        allocation_type: str | None = None,
        cost_center_code: str | None = None,
    ) -> Result[list[dict]]:
        if cost_center_code:
            items = await self._allocations.list_by_cost_center(tenant_id, cost_center_code)
        elif allocation_type:
            items = await self._allocations.list_by_type(tenant_id, allocation_type)
        else:
            items = await self._allocations.list_by_tenant(tenant_id)
        return Result.ok([a.to_dict() for a in items])

    async def profitability_analysis(
        self,
        tenant_id: str,
        *,
        cost_center_code: str | None = None,
        profit_center_code: str | None = None,
    ) -> Result[dict]:
        journals = await self._journals.list_by_tenant(tenant_id)
        journal_dicts = [j.to_dict() for j in journals]
        accounts = await self._accounts.list_by_tenant(tenant_id)
        account_types = {
            a.code: a.account_category.value
            for a in accounts
        }

        if cost_center_code or profit_center_code:
            analysis = compute_profitability(
                journals=journal_dicts,
                account_types=account_types,
                cost_center_code=cost_center_code,
                profit_center_code=profit_center_code,
            )
            allocations = (
                await self._allocations.list_by_cost_center(tenant_id, cost_center_code)
                if cost_center_code
                else await self._allocations.list_by_tenant(tenant_id)
            )
            analysis["budget_allocated"] = round(
                sum(a.amount for a in allocations if a.allocation_type == AllocationType.BUDGET.value), 2
            )
            analysis["expense_allocated"] = round(
                sum(a.amount for a in allocations if a.allocation_type == AllocationType.EXPENSE.value), 2
            )
            analysis["revenue_allocated"] = round(
                sum(a.amount for a in allocations if a.allocation_type == AllocationType.REVENUE.value), 2
            )
            return Result.ok(analysis)

        centers = await self._cost_centers.list_by_tenant(tenant_id)
        center_results = []
        for center in centers:
            result = compute_profitability(
                journals=journal_dicts,
                account_types=account_types,
                cost_center_code=center.code,
            )
            allocs = await self._allocations.list_by_cost_center(tenant_id, center.code)
            result["center_name"] = center.name
            result["center_type"] = center.center_type
            result["budget_allocated"] = round(
                sum(a.amount for a in allocs if a.allocation_type == AllocationType.BUDGET.value), 2
            )
            center_results.append(result)

        return Result.ok(
            {
                "summary": rollup_profitability(center_results),
                "centers": center_results,
            }
        )
