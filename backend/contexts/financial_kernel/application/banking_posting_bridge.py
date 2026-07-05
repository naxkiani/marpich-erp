"""Banking → General Ledger posting bridge (Financial Kernel side).

Banking publishes integration events; this bridge validates kernel linkage.
Account opening does not auto-post (see BANKING_GL_BRIDGE.md).
Deposit/withdrawal events post via execute_posting().
"""
from __future__ import annotations

import logging

from contexts.financial_kernel.application.service import FinancialKernelApplicationService

logger = logging.getLogger(__name__)

_KEY_CHAIN: dict[str, list[str]] = {
    "customer_deposits": ["customer_deposits", "bank"],
    "loans_receivable": ["loans_receivable", "bank"],
    "interest_income": ["interest_income", "revenue"],
    "interest_expense": ["interest_expense", "expense"],
    "cash_reserves": ["cash_reserves", "cash", "bank"],
}


class BankingPostingBridge:
    def __init__(self, kernel: FinancialKernelApplicationService) -> None:
        self._kernel = kernel

    async def _resolve_gl_code(self, tenant_id: str, account_key: str) -> str | None:
        for key in _KEY_CHAIN.get(account_key, [account_key]):
            result = await self._kernel.resolve_account_code(tenant_id, key)
            if result.succeeded:
                return result.unwrap()
        return None

    async def handle_account_opened(self, envelope: dict) -> None:
        tenant_id = str(envelope.get("tenant_id", ""))
        payload = envelope.get("payload", envelope)
        if not payload.get("kernel_linked"):
            logger.warning(
                "Banking account %s opened without kernel link for tenant %s",
                payload.get("account_id"),
                tenant_id,
            )
            return
        gl_code = payload.get("gl_account_code")
        if not gl_code:
            account_type = payload.get("account_type", "savings")
            key = "loans_receivable" if account_type == "loan" else "customer_deposits"
            gl_code = await self._resolve_gl_code(tenant_id, key)
        if gl_code:
            logger.info(
                "Banking account %s linked to GL %s (tenant %s)",
                payload.get("account_number"),
                gl_code,
                tenant_id,
            )

    async def handle_deposit_posted(self, envelope: dict) -> None:
        tenant_id = str(envelope.get("tenant_id", ""))
        payload = envelope.get("payload", envelope)
        account_id = payload.get("account_id", "")
        amount = float(payload.get("amount", 0))
        currency = payload.get("currency", "USD")
        gl_code = payload.get("gl_account_code")
        if not gl_code:
            gl_code = await self._resolve_gl_code(tenant_id, "customer_deposits")
        debit_code = await self._resolve_gl_code(tenant_id, "cash_reserves")
        if not gl_code or not debit_code:
            logger.warning("Banking deposit post skipped — no COA mapping for tenant %s", tenant_id)
            return

        result = await self._kernel.execute_posting(
            tenant_id=tenant_id,
            rule_id="bank_deposit",
            source_context="banking",
            source_document_id=account_id,
            amount=amount,
            currency=currency,
            correlation_id=envelope.get("correlation_id", f"banking-deposit-{account_id}"),
            idempotency_key=f"posting:bank_deposit:{account_id}:{payload.get('transaction_ref', '')}",
            description=f"Customer deposit — account {payload.get('account_number', account_id)}",
            account_mappings={"debit": debit_code, "credit": gl_code},
            require_approval=False,
        )
        if not result.succeeded:
            logger.error("Banking deposit GL post failed for %s: %s", account_id, result.error)

    async def handle_withdrawal_posted(self, envelope: dict) -> None:
        tenant_id = str(envelope.get("tenant_id", ""))
        payload = envelope.get("payload", envelope)
        transaction_id = payload.get("transaction_id", "")
        amount = float(payload.get("amount", 0))
        currency = payload.get("currency", "USD")
        gl_code = payload.get("gl_account_code") or await self._resolve_gl_code(tenant_id, "customer_deposits")
        debit_code = await self._resolve_gl_code(tenant_id, "cash_reserves")
        if not gl_code or not debit_code:
            logger.warning("Banking withdrawal post skipped — no COA mapping for tenant %s", tenant_id)
            return

        result = await self._kernel.execute_posting(
            tenant_id=tenant_id,
            rule_id="bank_withdrawal",
            source_context="banking",
            source_document_id=transaction_id,
            amount=amount,
            currency=currency,
            correlation_id=envelope.get("correlation_id", f"banking-withdrawal-{transaction_id}"),
            idempotency_key=f"posting:bank_withdrawal:{payload.get('transaction_ref', transaction_id)}",
            description=f"Customer withdrawal — ref {payload.get('transaction_ref', transaction_id)}",
            account_mappings={"debit": debit_code, "credit": gl_code},
            require_approval=False,
        )
        if not result.succeeded:
            logger.error("Banking withdrawal GL post failed for %s: %s", transaction_id, result.error)

    async def handle_interest_accrued(self, envelope: dict) -> None:
        tenant_id = str(envelope.get("tenant_id", ""))
        payload = envelope.get("payload", envelope)
        accrual_id = payload.get("accrual_id", "")
        amount = float(payload.get("accrued_amount", 0))
        currency = payload.get("currency", "USD")
        if amount <= 0:
            return

        debit_code = await self._resolve_gl_code(tenant_id, "interest_expense")
        credit_code = await self._resolve_gl_code(tenant_id, "interest_income")
        if not debit_code or not credit_code:
            logger.warning(
                "Banking interest accrual post skipped — missing COA slots for tenant %s",
                tenant_id,
            )
            return

        result = await self._kernel.execute_posting(
            tenant_id=tenant_id,
            rule_id="interest_accrual",
            source_context="banking",
            source_document_id=accrual_id,
            amount=amount,
            currency=currency,
            correlation_id=envelope.get("correlation_id", f"banking-interest-{accrual_id}"),
            idempotency_key=f"posting:interest_accrual:{payload.get('accrual_ref', accrual_id)}",
            description=f"Deposit interest accrual {payload.get('accrual_ref', accrual_id)}",
            account_mappings={"debit": debit_code, "credit": credit_code},
            require_approval=False,
        )
        if not result.succeeded:
            logger.error("Banking interest accrual GL post failed for %s: %s", accrual_id, result.error)

    async def handle_loan_disbursed(self, envelope: dict) -> None:
        tenant_id = str(envelope.get("tenant_id", ""))
        payload = envelope.get("payload", envelope)
        transaction_id = payload.get("transaction_id", "")
        amount = float(payload.get("amount", 0))
        currency = payload.get("currency", "USD")
        gl_code = payload.get("gl_account_code") or await self._resolve_gl_code(tenant_id, "loans_receivable")
        credit_code = await self._resolve_gl_code(tenant_id, "cash_reserves")
        if not gl_code or not credit_code:
            logger.warning("Banking loan disburse post skipped — no COA mapping for tenant %s", tenant_id)
            return

        result = await self._kernel.execute_posting(
            tenant_id=tenant_id,
            rule_id="loan_disbursement",
            source_context="banking",
            source_document_id=transaction_id,
            amount=amount,
            currency=currency,
            correlation_id=envelope.get("correlation_id", f"banking-loan-disburse-{transaction_id}"),
            idempotency_key=f"posting:loan_disbursement:{payload.get('transaction_ref', transaction_id)}",
            description=f"Loan disbursement — ref {payload.get('transaction_ref', transaction_id)}",
            account_mappings={"debit": gl_code, "credit": credit_code},
            require_approval=False,
        )
        if not result.succeeded:
            logger.error("Banking loan disburse GL post failed for %s: %s", transaction_id, result.error)

    async def handle_loan_repayment_posted(self, envelope: dict) -> None:
        tenant_id = str(envelope.get("tenant_id", ""))
        payload = envelope.get("payload", envelope)
        transaction_id = payload.get("transaction_id", "")
        amount = float(payload.get("amount", 0))
        currency = payload.get("currency", "USD")
        gl_code = payload.get("gl_account_code") or await self._resolve_gl_code(tenant_id, "loans_receivable")
        debit_code = await self._resolve_gl_code(tenant_id, "cash_reserves")
        if not gl_code or not debit_code:
            logger.warning("Banking loan repayment post skipped — no COA mapping for tenant %s", tenant_id)
            return

        result = await self._kernel.execute_posting(
            tenant_id=tenant_id,
            rule_id="loan_repayment",
            source_context="banking",
            source_document_id=transaction_id,
            amount=amount,
            currency=currency,
            correlation_id=envelope.get("correlation_id", f"banking-loan-repay-{transaction_id}"),
            idempotency_key=f"posting:loan_repayment:{payload.get('transaction_ref', transaction_id)}",
            description=f"Loan repayment — ref {payload.get('transaction_ref', transaction_id)}",
            account_mappings={"debit": debit_code, "credit": gl_code},
            require_approval=False,
        )
        if not result.succeeded:
            logger.error("Banking loan repayment GL post failed for %s: %s", transaction_id, result.error)

    async def handle_transfer_posted(self, envelope: dict) -> None:
        tenant_id = str(envelope.get("tenant_id", ""))
        payload = envelope.get("payload", envelope)
        transfer_id = payload.get("transfer_id", "")
        amount = float(payload.get("amount", 0))
        currency = payload.get("currency", "USD")
        source_gl = payload.get("source_gl_code") or await self._resolve_gl_code(tenant_id, "customer_deposits")
        dest_gl = payload.get("destination_gl_code") or source_gl
        if not source_gl or not dest_gl:
            logger.warning("Banking transfer post skipped — no COA mapping for tenant %s", tenant_id)
            return

        result = await self._kernel.execute_posting(
            tenant_id=tenant_id,
            rule_id="bank_transfer",
            source_context="banking",
            source_document_id=transfer_id,
            amount=amount,
            currency=currency,
            correlation_id=envelope.get("correlation_id", f"banking-transfer-{transfer_id}"),
            idempotency_key=f"posting:bank_transfer:{payload.get('transfer_ref', transfer_id)}",
            description=f"Bank transfer — ref {payload.get('transfer_ref', transfer_id)}",
            account_mappings={"debit": source_gl, "credit": dest_gl},
            require_approval=False,
        )
        if not result.succeeded:
            logger.error("Banking transfer GL post failed for %s: %s", transfer_id, result.error)
