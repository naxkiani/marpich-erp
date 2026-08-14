"""Tax ACL — payroll.run.completed → tax liability (no peer domain imports)."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def handle_payroll_run_completed(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "payroll.run.completed":
        return
    tenant_id = str(envelope.get("tenant_id") or "")
    payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
    run_id = str(payload.get("run_id") or "")
    period_label = str(payload.get("period_label") or "")
    total_gross = str(payload.get("total_gross") or "")
    currency = str(payload.get("currency") or "USD")
    if not tenant_id or not run_id or not period_label or not total_gross:
        logger.warning("tax payroll acl skipped — missing fields")
        return

    from contexts.tax.container import get_tax_service

    result = await get_tax_service().calculate_from_payroll_run(
        tenant_id=tenant_id,
        payroll_run_id=run_id,
        period_label=period_label,
        total_gross=total_gross,
        currency=currency,
        correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
    )
    if not result.succeeded:
        logger.error("tax payroll acl failed: %s", result.error)
        raise RuntimeError(result.error)
