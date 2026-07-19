"""Federation Engine REST surface — thin CQRS wiring (P200-B5)."""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions
from contexts.identity_federation.application.commands.connect_federation_provider import (
    ConnectFederationProviderCommand,
    DisconnectFederationProviderCommand,
    ProbeProviderHealthCommand,
    handle_connect_federation_provider,
    handle_disconnect_federation_provider,
    handle_probe_provider_health,
)
from contexts.identity_federation.application.commands.federation_engine_commands import (
    ExchangeFederatedTokenCommand,
    MapIdentityCommand,
    ResolveSyncConflictCommand,
    handle_exchange_federated_token,
    handle_map_identity,
    handle_resolve_sync_conflict,
)
from contexts.identity_federation.application.commands.register_identity_provider import (
    RegisterIdentityProviderCommand,
    handle_register_identity_provider,
)
from contexts.identity_federation.application.queries.federation_engine_queries import (
    GetIdentityMappingQuery,
    GetProviderQuery,
    GetSynchronizationStatusQuery,
    GetTrustStatusQuery,
    handle_get_engine_surface,
    handle_get_identity_mapping,
    handle_get_provider,
    handle_get_synchronization_status,
    handle_get_trust_status,
)
from contexts.identity_federation.container import (
    get_federation_health_probe,
    get_identity_link_repository,
    get_identity_provider_repository,
    get_sync_job_repository,
    get_trust_relationship_repository,
)

engine_router = APIRouter(prefix="/federation/engine", tags=["federation-engine"])


@engine_router.get(
    "/surface",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def engine_surface() -> dict:
    return {"data": handle_get_engine_surface()}


@engine_router.post(
    "/providers/register",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def register_provider(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_register_identity_provider(
            RegisterIdentityProviderCommand(
                tenant_id=tenant_id,
                provider_ref=body.get("provider_ref"),
                protocol=str(body.get("protocol") or "oidc"),
                name=str(body.get("name") or ""),
                config=dict(body.get("config") or {}),
                plugin_id=body.get("plugin_id"),
            ),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@engine_router.post(
    "/providers/{provider_ref}/connect",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def connect_provider(
    provider_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_connect_federation_provider(
            ConnectFederationProviderCommand(tenant_id=tenant_id, provider_ref=provider_ref),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@engine_router.post(
    "/providers/{provider_ref}/disconnect",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def disconnect_provider(
    provider_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_disconnect_federation_provider(
            DisconnectFederationProviderCommand(tenant_id=tenant_id, provider_ref=provider_ref),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@engine_router.post(
    "/providers/{provider_ref}/health",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def probe_health(
    provider_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_probe_provider_health(
            ProbeProviderHealthCommand(tenant_id=tenant_id, provider_ref=provider_ref),
            providers=get_identity_provider_repository(),
            health=get_federation_health_probe(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@engine_router.get(
    "/providers/{provider_ref}",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_provider(
    provider_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_get_provider(
            GetProviderQuery(tenant_id=tenant_id, provider_ref=provider_ref),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@engine_router.post(
    "/tokens/exchange",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def exchange_token(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    result = await handle_exchange_federated_token(
        ExchangeFederatedTokenCommand(
            tenant_id=tenant_id,
            source_type=str(body.get("source_type") or "access_token"),
            target_type=str(body.get("target_type") or "access_token"),
            subject=str(body.get("subject") or ""),
            audience=str(body.get("audience") or ""),
            scopes=list(body.get("scopes") or []),
            claims=dict(body.get("claims") or {}),
        )
    )
    if not result.get("exchanged"):
        raise HTTPException(status_code=400, detail=result.get("error") or "exchange_failed")
    return {"data": result}


@engine_router.post(
    "/identities/map",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def map_identity(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    result = await handle_map_identity(
        MapIdentityCommand(
            tenant_id=tenant_id,
            user_id=str(body.get("user_id") or ""),
            provider_id=str(body.get("provider_id") or ""),
            external_subject=str(body.get("external_subject") or ""),
            raw_claims=dict(body.get("raw_claims") or {}),
            mappings=list(body.get("mappings") or []),
        ),
        links=get_identity_link_repository(),
    )
    return {"data": result}


@engine_router.post(
    "/sync/resolve-conflict",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def resolve_conflict(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    result = await handle_resolve_sync_conflict(
        ResolveSyncConflictCommand(
            tenant_id=tenant_id,
            primary=dict(body.get("primary") or {}),
            secondary=dict(body.get("secondary") or {}),
            strategy=str(body.get("strategy") or "prefer_verified"),
            job_ref=body.get("job_ref"),
        ),
        sync_jobs=get_sync_job_repository(),
    )
    return {"data": result}


@engine_router.get(
    "/trust/{trust_ref}/status",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def trust_status(
    trust_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_get_trust_status(
            GetTrustStatusQuery(tenant_id=tenant_id, trust_ref=trust_ref),
            trusts=get_trust_relationship_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@engine_router.get(
    "/identities/{user_id}/mappings",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def identity_mappings(
    user_id: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    result = await handle_get_identity_mapping(
        GetIdentityMappingQuery(tenant_id=tenant_id, user_id=user_id),
        links=get_identity_link_repository(),
    )
    return {"data": result}


@engine_router.get(
    "/sync/status",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def sync_status(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    result = await handle_get_synchronization_status(
        GetSynchronizationStatusQuery(tenant_id=tenant_id),
        sync_jobs=get_sync_job_repository(),
    )
    return {"data": result}
