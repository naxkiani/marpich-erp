"""Federation Open Host Service REST surface (P200-B10)."""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions
from contexts.identity_federation.application.commands.ohs_commands import (
    AdvanceFederationSagaCommand,
    DispatchCommandBusCommand,
    DispatchQueryBusCommand,
    IngestInboxCommand,
    PublishOhsEventCommand,
    StartFederationSagaCommand,
    handle_advance_federation_saga,
    handle_dispatch_command,
    handle_dispatch_query,
    handle_ingest_inbox,
    handle_publish_ohs_event,
    handle_start_federation_saga,
)
from contexts.identity_federation.application.queries.ohs_queries import (
    GetInboxQuery,
    GetOutboxQuery,
    GetSagaQuery,
    handle_get_inbox,
    handle_get_ohs_apis,
    handle_get_ohs_cqrs,
    handle_get_ohs_events,
    handle_get_ohs_surface,
    handle_get_outbox,
    handle_get_saga,
)

ohs_router = APIRouter(prefix="/federation/ohs", tags=["federation-ohs"])


@ohs_router.get(
    "/surface",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def surface() -> dict:
    return {"data": handle_get_ohs_surface()}


@ohs_router.get(
    "/apis",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def apis() -> dict:
    return {"data": handle_get_ohs_apis()}


@ohs_router.get(
    "/events",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def events() -> dict:
    return {"data": handle_get_ohs_events()}


@ohs_router.get(
    "/cqrs",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def cqrs() -> dict:
    return {"data": handle_get_ohs_cqrs()}


@ohs_router.post(
    "/commands/dispatch",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def dispatch_command(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_dispatch_command(
            DispatchCommandBusCommand(
                tenant_id=tenant_id,
                name=str(body.get("name") or ""),
                payload=dict(body.get("payload") or {}),
                correlation_id=str(body.get("correlation_id") or ""),
                idempotency_key=str(body.get("idempotency_key") or ""),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@ohs_router.post(
    "/queries/dispatch",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def dispatch_query(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_dispatch_query(
            DispatchQueryBusCommand(
                tenant_id=tenant_id,
                name=str(body.get("name") or ""),
                payload=dict(body.get("payload") or {}),
                correlation_id=str(body.get("correlation_id") or ""),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@ohs_router.post(
    "/events/publish",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def publish_event(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_publish_ohs_event(
            PublishOhsEventCommand(
                tenant_id=tenant_id,
                event_name=str(body.get("event_name") or ""),
                payload=dict(body.get("payload") or {}),
                event_version=int(body.get("event_version") or 1),
                correlation_id=str(body.get("correlation_id") or ""),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@ohs_router.post(
    "/sagas/start",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def start_saga(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_start_federation_saga(
            StartFederationSagaCommand(
                tenant_id=tenant_id,
                saga_type=str(body.get("saga_type") or ""),
                context=dict(body.get("context") or {}),
                timeout_minutes=int(body.get("timeout_minutes") or 60),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@ohs_router.post(
    "/sagas/{saga_ref}/advance",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def advance_saga(
    saga_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_advance_federation_saga(
            AdvanceFederationSagaCommand(
                tenant_id=tenant_id,
                saga_ref=saga_ref,
                step_ok=bool(body.get("step_ok", True)),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@ohs_router.get(
    "/sagas/{saga_ref}",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_saga(
    saga_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = handle_get_saga(GetSagaQuery(tenant_id=tenant_id, saga_ref=saga_ref))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@ohs_router.get(
    "/outbox",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def outbox(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    limit: int = 50,
) -> dict:
    return {"data": handle_get_outbox(GetOutboxQuery(tenant_id=tenant_id, limit=limit))}


@ohs_router.get(
    "/inbox",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def inbox(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    limit: int = 50,
) -> dict:
    return {"data": handle_get_inbox(GetInboxQuery(tenant_id=tenant_id, limit=limit))}


@ohs_router.post(
    "/inbox/ingest",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def ingest_inbox(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    result = await handle_ingest_inbox(
        IngestInboxCommand(
            tenant_id=tenant_id,
            event_id=str(body.get("event_id") or ""),
            event_name=str(body.get("event_name") or ""),
            consumer_id=str(body.get("consumer_id") or "default"),
            payload=dict(body.get("payload") or {}),
        )
    )
    return {"data": result}
