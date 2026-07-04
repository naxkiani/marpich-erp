"""Notifications FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)
from contexts.notifications.container import get_notification_service
from contexts.notifications.presentation.schemas import SendNotificationRequest

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/inbox")
async def list_inbox(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(get_current_user)],
    unread_only: Annotated[bool, Query()] = False,
):
    result = await get_notification_service().list_inbox(
        tenant_id, user["sub"], unread_only=unread_only
    )
    return {"data": result.unwrap()}


@router.patch("/inbox/{message_id}/read")
async def mark_inbox_read(
    message_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[dict, Depends(get_current_user)],
):
    result = await get_notification_service().mark_read(tenant_id, user["sub"], message_id)
    if not result.succeeded:
        code = status.HTTP_404_NOT_FOUND if "not_found" in (result.error or "") else status.HTTP_403_FORBIDDEN
        raise HTTPException(code, result.error)
    return {"data": result.unwrap()}


@router.post("/send", status_code=status.HTTP_202_ACCEPTED)
async def send_notification(
    body: SendNotificationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    _user: Annotated[dict, Depends(require_permissions("notifications.send"))],
):
    result = await get_notification_service().send(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        user_id=body.user_id,
        channel=body.channel,
        title=body.title,
        body=body.body,
        category=body.category,
        recipient_email=body.recipient_email,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/templates")
async def list_templates(
    _user: Annotated[dict, Depends(require_permissions("notifications.templates.read"))],
):
    result = await get_notification_service().list_templates()
    return {"data": result.unwrap()}


@router.get("/deliveries")
async def list_deliveries(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("notifications.deliveries.read"))],
):
    result = await get_notification_service().list_deliveries(tenant_id)
    return {"data": result.unwrap()}
