"""University ACL — LMS sync events → local commands (no peer domain imports)."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

_LMS_EVENT_NAMES = (
    "integration.moodle.batch.synced",
    "integration.google_classroom.batch.synced",
)


async def handle_lms_batch_synced(envelope: dict) -> None:
    event_name = str(envelope.get("event_name") or "")
    if event_name not in _LMS_EVENT_NAMES:
        return
    tenant_id = str(envelope.get("tenant_id") or "")
    payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
    provider = str(payload.get("provider") or "")
    if not tenant_id or not provider:
        logger.warning("lms acl skipped — missing tenant/provider")
        return
    from contexts.university.container import get_university_service

    result = await get_university_service().apply_lms_batch(
        tenant_id=tenant_id,
        provider=provider,
        correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
        courses=list(payload.get("courses") or []),
        enrollments=list(payload.get("enrollments") or []),
        grades=list(payload.get("grades") or []),
    )
    if not result.succeeded:
        logger.error("lms acl failed: %s", result.error)
        raise RuntimeError(result.error)
