"""Inventory ACL — procurement goods received → stock restock."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def handle_procurement_goods_received(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "procurement.goods.received":
        return
    tenant_id = str(envelope.get("tenant_id") or "")
    payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
    requisition_id = str(payload.get("requisition_id") or payload.get("purchase_order_id") or "")
    lines = list(payload.get("lines") or [])
    if not lines and payload.get("sku"):
        lines = [{"sku": payload.get("sku"), "quantity": payload.get("quantity")}]
    if not tenant_id or not requisition_id:
        logger.warning("inventory goods-receipt acl skipped — missing tenant/requisition_id")
        return
    if not lines:
        logger.info("inventory goods-receipt acl — receipt %s has no lines; skip", requisition_id)
        return

    from contexts.inventory.container import get_inventory_service

    result = await get_inventory_service().apply_goods_receipt_restock(
        tenant_id=tenant_id,
        requisition_id=requisition_id,
        lines=lines,
        correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
    )
    if not result.succeeded:
        logger.error("inventory goods-receipt acl failed: %s", result.error)
        raise RuntimeError(result.error)
