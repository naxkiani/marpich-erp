"""POS → General Ledger posting bridge (Financial Kernel side)."""
from __future__ import annotations

import logging

from contexts.financial_kernel.application.service import FinancialKernelApplicationService

logger = logging.getLogger(__name__)

_DEBIT_KEYS = ("pos_cash", "cash", "cash_positions", "cash_reserves")
_CREDIT_KEYS = ("sales_revenue", "revenue", "patient_service_revenue")


class PosPostingBridge:
    def __init__(self, kernel: FinancialKernelApplicationService) -> None:
        self._kernel = kernel

    async def _resolve_first(self, tenant_id: str, keys: tuple[str, ...]) -> str | None:
        for key in keys:
            result = await self._kernel.resolve_account_code(tenant_id, key)
            if result.succeeded:
                return result.unwrap()
        return None

    async def handle_sale_completed(self, envelope: dict) -> None:
        if str(envelope.get("event_name") or "") != "pos.sale.completed":
            return
        tenant_id = str(envelope.get("tenant_id") or "")
        payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
        sale_id = str(payload.get("sale_id") or "")
        if not tenant_id or not sale_id:
            logger.warning("POS GL post skipped — missing tenant/sale_id")
            return

        try:
            total = float(payload.get("total") or 0)
        except (TypeError, ValueError):
            logger.warning("POS GL post skipped — invalid amounts for sale %s", sale_id)
            return
        if total <= 0:
            return

        currency = str(payload.get("currency") or "USD")
        correlation_id = str(envelope.get("correlation_id") or f"pos-sale-{sale_id}")
        payment_method = str(payload.get("payment_method") or "cash")

        debit_gl = await self._resolve_first(tenant_id, _DEBIT_KEYS)
        credit_gl = await self._resolve_first(tenant_id, _CREDIT_KEYS)
        if not debit_gl or not credit_gl:
            logger.warning(
                "POS GL post skipped for sale %s — no COA mapping for tenant %s",
                sale_id,
                tenant_id,
            )
            return

        mappings = {"debit": debit_gl, "credit": credit_gl}

        result = await self._kernel.execute_posting(
            tenant_id=tenant_id,
            rule_id="retail_pos_sale",
            source_context="pos",
            source_document_id=sale_id,
            amount=total,
            currency=currency,
            correlation_id=correlation_id,
            idempotency_key=f"posting:retail_pos_sale:{sale_id}",
            description=f"POS sale {sale_id} ({payment_method})",
            account_mappings=mappings,
            require_approval=False,
        )
        if not result.succeeded:
            logger.error("POS GL post failed for %s: %s", sale_id, result.error)
            raise RuntimeError(result.error)
