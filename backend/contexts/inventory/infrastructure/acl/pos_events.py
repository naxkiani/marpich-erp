"""Inventory ACL — POS sale completed → stock decrement (no peer domain imports)."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def handle_pos_sale_completed(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "pos.sale.completed":
        return
    tenant_id = str(envelope.get("tenant_id") or "")
    payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
    sale_id = str(payload.get("sale_id") or "")
    items = list(payload.get("items") or [])
    if not tenant_id or not sale_id:
        logger.warning("inventory pos acl skipped — missing tenant/sale_id")
        return
    if not items:
        logger.info("inventory pos acl — sale %s has no line items; skip", sale_id)
        return

    from contexts.inventory.container import get_inventory_service

    result = await get_inventory_service().apply_pos_sale_decrement(
        tenant_id=tenant_id,
        sale_id=sale_id,
        items=items,
        correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
    )
    if not result.succeeded:
        logger.error("inventory pos acl failed: %s", result.error)
        raise RuntimeError(result.error)
