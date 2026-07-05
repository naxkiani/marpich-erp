"""Treasury Transaction Engine application service."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.treasury_transaction import (
    TransactionWorkflowStatus,
    TreasuryTransaction,
)
from contexts.treasury.domain.events.integration_events import (
    TreasuryLiquidityUpdatedIntegration,
    TreasuryTransactionApprovalRequestedIntegration,
    TreasuryTransactionExecutedIntegration,
)
from contexts.treasury.domain.ports.repositories import ITreasuryAccountRepository
from contexts.treasury.domain.ports.treasury_transaction_repositories import (
    ITreasuryTransactionRepository,
)
from contexts.treasury.domain.services.treasury_engine import compute_liquidity
from contexts.treasury.domain.services.treasury_transaction_engine import (
    assert_transaction_type,
    build_transaction_dashboard,
    can_auto_execute,
    list_posting_rules,
    list_transaction_catalog,
    list_workflow_states,
    requires_approval,
    resolve_approval_levels,
    resolve_posting_rule,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class TreasuryTransactionApplicationService:
    def __init__(
        self,
        transactions: ITreasuryTransactionRepository,
        accounts: ITreasuryAccountRepository,
    ) -> None:
        self._transactions = transactions
        self._accounts = accounts

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_transaction_catalog())

    async def list_workflow(self) -> Result[list[dict]]:
        return Result.ok(list_workflow_states())

    async def list_posting_rule_map(self) -> Result[list[dict]]:
        return Result.ok(list_posting_rules())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        txns = await self._transactions.list_by_tenant(tenant_id)
        sorted_txns = sorted(txns, key=lambda t: t.created_at, reverse=True)
        return Result.ok(build_transaction_dashboard(transactions=[t.to_dict() for t in sorted_txns]))

    async def create_transaction(
        self,
        *,
        tenant_id: str,
        transaction_type: str,
        amount: float,
        currency: str,
        reference: str,
        description: str | None = None,
        from_account_id: str | None = None,
        to_account_id: str | None = None,
        metadata: dict | None = None,
        auto_submit: bool = False,
    ) -> Result[dict]:
        try:
            assert_transaction_type(transaction_type)
        except ValueError:
            return Result.fail("treasury.errors.invalid_transaction_type")

        if amount <= 0:
            return Result.fail("treasury.errors.invalid_amount")

        from_acc = None
        to_acc = None
        if from_account_id:
            from_acc = await self._accounts.find_by_id(from_account_id)
            if not from_acc or from_acc.tenant_id != tenant_id:
                return Result.fail("treasury.errors.account_not_found")
            if from_acc.currency != currency:
                return Result.fail("treasury.errors.currency_mismatch")
        if to_account_id:
            to_acc = await self._accounts.find_by_id(to_account_id)
            if not to_acc or to_acc.tenant_id != tenant_id:
                return Result.fail("treasury.errors.account_not_found")
            if to_acc.currency != currency:
                return Result.fail("treasury.errors.currency_mismatch")

        approval_levels = resolve_approval_levels(transaction_type, amount)
        posting_rule_id = resolve_posting_rule(transaction_type)

        txn = TreasuryTransaction.create_draft(
            tenant_id=tenant_id,
            transaction_type=transaction_type,
            amount=amount,
            currency=currency,
            reference=reference,
            description=description,
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            posting_rule_id=posting_rule_id,
            required_approval_levels=approval_levels,
            metadata=metadata,
        )
        await self._transactions.save(txn)

        if auto_submit:
            return await self.submit_transaction(str(txn.id), f"auto-submit-{txn.id}")
        return Result.ok(txn.to_dict())

    async def submit_transaction(self, transaction_id: str, correlation_id: str) -> Result[dict]:
        txn = await self._transactions.find_by_id(transaction_id)
        if not txn:
            return Result.fail("treasury.errors.transaction_not_found")
        txn.submit()
        await self._transactions.save(txn)

        if requires_approval(txn.transaction_type, txn.amount):
            txn.enter_approval()
            await self._transactions.save(txn)
            await publish_integration_event(
                TreasuryTransactionApprovalRequestedIntegration(
                    tenant_id=TenantId.create(txn.tenant_id),
                    correlation_id=correlation_id,
                    transaction_id=str(txn.id),
                    transaction_type=txn.transaction_type,
                    amount=txn.amount,
                    currency=txn.currency,
                    required_approval_levels=txn.required_approval_levels,
                )
            )
            return Result.ok(txn.to_dict())

        txn.mark_approved()
        await self._transactions.save(txn)
        return await self._execute_transaction(txn, correlation_id)

    async def approve_transaction(
        self,
        transaction_id: str,
        *,
        approver_id: str,
        correlation_id: str,
        comment: str | None = None,
    ) -> Result[dict]:
        txn = await self._transactions.find_by_id(transaction_id)
        if not txn:
            return Result.fail("treasury.errors.transaction_not_found")
        try:
            txn.approve(
                approver_id=approver_id,
                level=txn.current_approval_level + 1,
                comment=comment,
            )
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")
        await self._transactions.save(txn)
        if txn.status == TransactionWorkflowStatus.APPROVED.value:
            return await self._execute_transaction(txn, correlation_id)
        return Result.ok(txn.to_dict())

    async def reject_transaction(
        self,
        transaction_id: str,
        *,
        approver_id: str,
        comment: str | None = None,
    ) -> Result[dict]:
        txn = await self._transactions.find_by_id(transaction_id)
        if not txn:
            return Result.fail("treasury.errors.transaction_not_found")
        try:
            txn.reject(approver_id=approver_id, comment=comment)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")
        await self._transactions.save(txn)
        return Result.ok(txn.to_dict())

    async def cancel_transaction(self, transaction_id: str) -> Result[dict]:
        txn = await self._transactions.find_by_id(transaction_id)
        if not txn:
            return Result.fail("treasury.errors.transaction_not_found")
        try:
            txn.cancel()
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")
        await self._transactions.save(txn)
        return Result.ok(txn.to_dict())

    async def list_transactions(self, tenant_id: str) -> Result[list[dict]]:
        txns = await self._transactions.list_by_tenant(tenant_id)
        return Result.ok(
            [t.to_dict() for t in sorted(txns, key=lambda x: x.created_at, reverse=True)]
        )

    async def get_transaction(self, transaction_id: str) -> Result[dict]:
        txn = await self._transactions.find_by_id(transaction_id)
        if not txn:
            return Result.fail("treasury.errors.transaction_not_found")
        return Result.ok(txn.to_dict())

    async def _execute_transaction(
        self, txn: TreasuryTransaction, correlation_id: str
    ) -> Result[dict]:
        from_acc = None
        to_acc = None
        if txn.from_account_id:
            from_acc = await self._accounts.find_by_id(txn.from_account_id)
            if not from_acc:
                return Result.fail("treasury.errors.account_not_found")
        if txn.to_account_id:
            to_acc = await self._accounts.find_by_id(txn.to_account_id)
            if not to_acc:
                return Result.fail("treasury.errors.account_not_found")

        try:
            if from_acc and to_acc:
                from_acc.debit(txn.amount)
                to_acc.credit(txn.amount)
            elif from_acc:
                from_acc.debit(txn.amount)
            elif to_acc:
                to_acc.credit(txn.amount)
        except ValueError:
            return Result.fail("treasury.errors.insufficient_balance")

        txn.mark_executed()
        if from_acc:
            await self._accounts.save(from_acc)
        if to_acc:
            await self._accounts.save(to_acc)
        await self._transactions.save(txn)

        await publish_integration_event(
            TreasuryTransactionExecutedIntegration(
                tenant_id=TenantId.create(txn.tenant_id),
                correlation_id=correlation_id,
                transaction_id=str(txn.id),
                transaction_type=txn.transaction_type,
                posting_rule_id=txn.posting_rule_id,
                from_account_id=txn.from_account_id,
                to_account_id=txn.to_account_id,
                from_account_type=from_acc.account_type if from_acc else None,
                to_account_type=to_acc.account_type if to_acc else None,
                amount=txn.amount,
                currency=txn.currency,
            )
        )
        await self._emit_liquidity(txn.tenant_id, correlation_id)
        return Result.ok(txn.to_dict())

    async def _emit_liquidity(self, tenant_id: str, correlation_id: str) -> None:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        liquidity = compute_liquidity(accounts)
        await publish_integration_event(
            TreasuryLiquidityUpdatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                total_balance=liquidity["total_balance"],
                liquid_balance=liquidity["liquid_balance"],
                liquidity_ratio=liquidity["liquidity_ratio"],
            )
        )
