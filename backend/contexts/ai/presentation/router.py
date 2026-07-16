"""AI FastAPI router — Core Platform assist."""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from contexts.ai.container import get_ai_service
from contexts.identity.presentation.dependencies import (
    get_correlation_id,
    get_current_user,
    get_tenant_id,
    require_permissions,
)

router = APIRouter(prefix="/ai", tags=["AI Platform"])


class AssistRequest(BaseModel):
    module_id: str = Field(default="platform", max_length=64)
    surface: str = Field(default="assistant", max_length=64)
    prompt: str = Field(min_length=1, max_length=8000)
    context: dict[str, Any] | None = None


@router.post("/assist", status_code=status.HTTP_200_OK)
async def assist(
    body: AssistRequest,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    correlation_id: Annotated[str, Depends(get_correlation_id)],
    user: Annotated[dict, Depends(require_permissions("ai.assist.infer"))],
):
    result = await get_ai_service().assist(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        module_id=body.module_id,
        surface=body.surface,
        prompt=body.prompt,
        actor_user_id=user.get("sub"),
        context=body.context,
    )
    if not result.succeeded:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result.error)
    return {"data": result.unwrap(), "meta": {"correlation_id": correlation_id}}
