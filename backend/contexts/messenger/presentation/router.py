"""Messenger FastAPI router."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_tenant_id,
    require_permissions,
)
from contexts.messenger.container import get_messenger_service
from contexts.messenger.presentation.schemas import OpenConversationRequest, SendMessageRequest

router = APIRouter(prefix="/messenger", tags=["Messenger"])


@router.post("/conversations", status_code=status.HTTP_201_CREATED)
async def open_conversation(
    body: OpenConversationRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("messenger.conversations.write"))],
):
    members = list(body.member_ids)
    if user.get("sub") and user["sub"] not in members:
        members.append(user["sub"])
    result = await get_messenger_service().open_conversation(
        tenant_id=tenant_id,
        title=body.title,
        member_ids=members,
        correlation_id=correlation_id,
        e2ee_enabled=body.e2ee_enabled,
        issue_livekit_token=body.issue_livekit_token,
        requester_id=user.get("sub"),
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/conversations/{conversation_id}/livekit-token", status_code=status.HTTP_200_OK)
async def issue_livekit_token(
    conversation_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("messenger.conversations.write"))],
):
    result = await get_messenger_service().issue_livekit_token(
        tenant_id=tenant_id,
        conversation_id=conversation_id,
        requester_id=user["sub"],
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        code = (
            status.HTTP_404_NOT_FOUND
            if "not_found" in (result.error or "")
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(code, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.post("/conversations/{conversation_id}/messages", status_code=status.HTTP_201_CREATED)
async def send_message(
    conversation_id: str,
    body: SendMessageRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("messenger.messages.write"))],
):
    result = await get_messenger_service().send_message(
        tenant_id=tenant_id,
        conversation_id=conversation_id,
        sender_id=user["sub"],
        body=body.body,
        ciphertext=body.ciphertext,
        ciphertext_type=body.ciphertext_type,
        correlation_id=correlation_id,
    )
    if not result.succeeded:
        code = (
            status.HTTP_404_NOT_FOUND
            if "not_found" in (result.error or "")
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(code, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}


@router.get("/conversations/{conversation_id}/messages")
async def list_messages(
    conversation_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    _user: Annotated[dict, Depends(require_permissions("messenger.messages.read"))],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
):
    result = await get_messenger_service().list_messages(
        tenant_id, conversation_id, limit=limit
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_404_NOT_FOUND, result.error)
    return {"data": result.unwrap()}
