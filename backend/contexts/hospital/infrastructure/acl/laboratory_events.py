"""Hospital ACL — laboratory.result.available → local lab result projection."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from contexts.hospital.application.service import HospitalApplicationService

logger = logging.getLogger(__name__)


def make_laboratory_result_handler(
    get_service: Callable[[], "HospitalApplicationService"],
):
    async def handle_laboratory_result_available(envelope: dict) -> None:
        if str(envelope.get("event_name") or "") != "laboratory.result.available":
            return
        tenant_id = str(envelope.get("tenant_id") or "")
        event_id = str(envelope.get("event_id") or "")
        payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
        order_id = str(payload.get("order_id") or "")
        patient_ref = str(payload.get("patient_ref") or "")
        test_code = str(payload.get("test_code") or "")
        result_value = str(payload.get("result_value") or "")
        result_unit = payload.get("result_unit")
        if result_unit is not None:
            result_unit = str(result_unit)
        if not tenant_id or not event_id:
            logger.warning("hospital lab acl skipped — missing tenant/event_id")
            return

        result = await get_service().project_laboratory_result(
            tenant_id=tenant_id,
            order_id=order_id,
            patient_ref=patient_ref,
            test_code=test_code,
            result_value=result_value,
            result_unit=result_unit,
            source_event_id=event_id,
        )
        if not result.succeeded:
            logger.error("hospital lab acl failed: %s", result.error)
            raise RuntimeError(result.error)

    return handle_laboratory_result_available
