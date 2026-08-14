"""Payroll ACL — HR employee hired → local projection (no peer domain imports)."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def handle_employee_hired(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "human_resources.employee.hired":
        return
    tenant_id = str(envelope.get("tenant_id") or "")
    payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
    hr_employee_id = str(payload.get("employee_id") or "")
    email = str(payload.get("email") or "")
    full_name = str(payload.get("full_name") or "")
    if not tenant_id or not hr_employee_id or not email or not full_name:
        logger.warning("payroll hr acl skipped — missing tenant/employee fields")
        return

    from contexts.payroll.container import get_payroll_service

    result = await get_payroll_service().project_hired_employee(
        tenant_id=tenant_id,
        hr_employee_id=hr_employee_id,
        email=email,
        full_name=full_name,
        job_title=str(payload.get("job_title") or ""),
        department=str(payload.get("department") or ""),
        employee_number=str(payload.get("employee_number") or ""),
        correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
    )
    if not result.succeeded:
        logger.error("payroll hr acl failed: %s", result.error)
        raise RuntimeError(result.error)
