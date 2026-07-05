"""Treasury → General Ledger posting bridge (Financial Kernel side).

Treasury publishes integration events; this bridge calls execute_posting().
Treasury never duplicates financial logic.
"""
from __future__ import annotations

import logging

from contexts.financial_kernel.application.service import FinancialKernelApplicationService

logger = logging.getLogger(__name__)

_KEY_CHAIN: dict[str, list[str]] = {
    "bank": ["bank", "cash", "treasury_cash"],
    "cash": ["cash", "treasury_cash", "pos_cash"],
    "petty_cash": ["petty_cash", "cash", "treasury_cash"],
    "vault": ["cash", "treasury_cash"],
    "safe": ["cash", "treasury_cash"],
    "investments": ["investments", "fixed_assets", "cash"],
    "loan_payable": ["loan_payable", "accounts_payable"],
    "interest_expense": ["interest_expense", "clinical_staff"],
}


class TreasuryPostingBridge:
    def __init__(self, kernel: FinancialKernelApplicationService) -> None:
        self._kernel = kernel

    async def _resolve_gl_code(self, tenant_id: str, account_type: str) -> str | None:
        for key in _KEY_CHAIN.get(account_type, ["cash"]):
            result = await self._kernel.resolve_account_code(tenant_id, key)
            if result.succeeded:
                return result.unwrap()
        return None

    async def handle_transfer_executed(self, envelope: dict) -> None:
        tenant_id = str(envelope.get("tenant_id", ""))
        payload = envelope.get("payload", envelope)
        transfer_id = payload.get("transfer_id", "")
        amount = float(payload.get("amount", 0))
        currency = payload.get("currency", "USD")
        correlation_id = envelope.get("correlation_id", f"treasury-transfer-{transfer_id}")

        to_gl = await self._resolve_gl_code(tenant_id, payload.get("to_account_type", "cash"))
        from_gl = await self._resolve_gl_code(tenant_id, payload.get("from_account_type", "cash"))
        if not to_gl or not from_gl:
            logger.warning(
                "Treasury GL post skipped for transfer %s — no COA mapping for tenant %s",
                transfer_id,
                tenant_id,
            )
            return

        result = await self._kernel.execute_posting(
            tenant_id=tenant_id,
            rule_id="treasury_transfer",
            source_context="treasury",
            source_document_id=transfer_id,
            amount=amount,
            currency=currency,
            correlation_id=correlation_id,
            idempotency_key=f"posting:treasury_transfer:{transfer_id}",
            description=f"Treasury transfer {transfer_id}",
            account_mappings={"debit": to_gl, "credit": from_gl},
            use_default_accounts=False,
            require_approval=False,
        )
        if not result.succeeded:
            logger.error("Treasury GL post failed for transfer %s: %s", transfer_id, result.error)

    async def handle_transaction_executed(self, envelope: dict) -> None:
        tenant_id = str(envelope.get("tenant_id", ""))
        payload = envelope.get("payload", envelope)
        transaction_id = payload.get("transaction_id", "")
        rule_id = payload.get("posting_rule_id", "treasury_internal_transfer")
        amount = float(payload.get("amount", 0))
        currency = payload.get("currency", "USD")
        correlation_id = envelope.get("correlation_id", f"treasury-txn-{transaction_id}")

        to_type = payload.get("to_account_type")
        from_type = payload.get("from_account_type")
        to_gl = await self._resolve_gl_code(tenant_id, to_type) if to_type else None
        from_gl = await self._resolve_gl_code(tenant_id, from_type) if from_type else None

        account_mappings: dict[str, str] = {}
        if to_gl and from_gl:
            account_mappings = {"debit": to_gl, "credit": from_gl}
        elif to_gl:
            account_mappings = {"debit": to_gl}
        elif from_gl:
            account_mappings = {"credit": from_gl}

        if not account_mappings:
            logger.warning(
                "Treasury GL post skipped for transaction %s — no COA mapping for tenant %s",
                transaction_id,
                tenant_id,
            )
            return

        result = await self._kernel.execute_posting(
            tenant_id=tenant_id,
            rule_id=rule_id,
            source_context="treasury",
            source_document_id=transaction_id,
            amount=amount,
            currency=currency,
            correlation_id=correlation_id,
            idempotency_key=f"posting:{rule_id}:{transaction_id}",
            description=f"Treasury transaction {transaction_id} ({payload.get('transaction_type', '')})",
            account_mappings=account_mappings,
            use_default_accounts=len(account_mappings) < 2,
            require_approval=False,
        )
        if not result.succeeded:
            logger.error(
                "Treasury GL post failed for transaction %s: %s", transaction_id, result.error
            )

