"""Identity Provider Management REST surface (P200-B7)."""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from contexts.identity.presentation.dependencies import get_tenant_id, require_permissions
from contexts.identity_federation.application.commands.provider_management_commands import (
    ActivateIdentityProviderCommand,
    ConfigureProviderCommand,
    CreateFederationConnectionCommand,
    CreateMappingRuleCommand,
    InstallProtocolPluginCommand,
    RegisterManagedProviderCommand,
    RotateProviderCertificateCommand,
    SuspendIdentityProviderCommand,
    SynchronizeIdentityCommand,
    ValidateProviderTrustCommand,
    VerifyProviderCommand,
    handle_activate_identity_provider,
    handle_configure_provider,
    handle_create_federation_connection,
    handle_create_mapping_rule,
    handle_install_protocol_plugin,
    handle_register_managed_provider,
    handle_rotate_provider_certificate,
    handle_suspend_identity_provider,
    handle_synchronize_identity,
    handle_validate_provider_trust,
    handle_verify_provider,
)
from contexts.identity_federation.application.queries.provider_management_queries import (
    GetFederationConnectionsQuery,
    GetManagedProviderQuery,
    GetProviderHealthQuery,
    GetProviderTrustScoreQuery,
    GetSyncStatusQuery,
    handle_get_federation_connections,
    handle_get_managed_provider,
    handle_get_mapping_rules_catalog,
    handle_get_protocol_plugins,
    handle_get_provider_health,
    handle_get_provider_surface,
    handle_get_provider_trust_score,
    handle_get_sync_status,
)
from contexts.identity_federation.container import (
    get_identity_provider_repository,
    get_sync_job_repository,
)

providers_router = APIRouter(prefix="/federation/providers", tags=["federation-providers"])


@providers_router.get(
    "/surface",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def provider_surface() -> dict:
    return {"data": handle_get_provider_surface()}


@providers_router.get(
    "/plugins",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def list_plugins(protocol: str | None = None) -> dict:
    return {"data": handle_get_protocol_plugins(protocol=protocol)}


@providers_router.post(
    "/plugins/install",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def install_plugin(body: dict[str, Any]) -> dict:
    try:
        result = await handle_install_protocol_plugin(
            InstallProtocolPluginCommand(
                plugin_id=str(body.get("plugin_id") or ""),
                protocol=str(body.get("protocol") or ""),
                name=str(body.get("name") or body.get("plugin_id") or ""),
                version=str(body.get("version") or "1.0.0"),
                capabilities=list(body.get("capabilities") or []),
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@providers_router.post(
    "/register",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def register_provider(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_register_managed_provider(
            RegisterManagedProviderCommand(
                tenant_id=tenant_id,
                provider_ref=body.get("provider_ref"),
                protocol=str(body.get("protocol") or "oidc"),
                name=str(body.get("name") or ""),
                provider_type=str(body.get("provider_type") or "external_enterprise"),
                config=dict(body.get("config") or {}),
                plugin_id=body.get("plugin_id"),
                correlation_id=str(body.get("correlation_id") or ""),
            ),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@providers_router.post(
    "/mappings",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def create_mapping(
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    result = await handle_create_mapping_rule(
        CreateMappingRuleCommand(
            tenant_id=tenant_id,
            source_claims=dict(body.get("source_claims") or {}),
            rules=list(body.get("rules") or []),
        )
    )
    return {"data": result}


@providers_router.get(
    "/mappings",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def mapping_catalog() -> dict:
    return {"data": handle_get_mapping_rules_catalog()}


@providers_router.get(
    "/sync/status",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def sync_status(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    provider_ref: str | None = None,
    limit: int = 20,
) -> dict:
    result = await handle_get_sync_status(
        GetSyncStatusQuery(tenant_id=tenant_id, provider_ref=provider_ref, limit=limit),
        sync_jobs=get_sync_job_repository(),
    )
    return {"data": result}


@providers_router.post(
    "/{provider_ref}/configure",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def configure_provider(
    provider_ref: str,
    body: dict[str, Any],
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_configure_provider(
            ConfigureProviderCommand(
                tenant_id=tenant_id,
                provider_ref=provider_ref,
                config=dict(body.get("config") or {}),
                security_profile=dict(body.get("security_profile") or {}),
            ),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@providers_router.post(
    "/{provider_ref}/verify",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def verify_provider(
    provider_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_verify_provider(
            VerifyProviderCommand(tenant_id=tenant_id, provider_ref=provider_ref),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@providers_router.post(
    "/{provider_ref}/activate",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def activate_provider(
    provider_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_activate_identity_provider(
            ActivateIdentityProviderCommand(
                tenant_id=tenant_id,
                provider_ref=provider_ref,
                correlation_id=str(body.get("correlation_id") or ""),
                min_trust_level=int(body.get("min_trust_level", 1)),
            ),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@providers_router.post(
    "/{provider_ref}/suspend",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def suspend_provider(
    provider_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_suspend_identity_provider(
            SuspendIdentityProviderCommand(
                tenant_id=tenant_id,
                provider_ref=provider_ref,
                reason=str(body.get("reason") or "suspended"),
                correlation_id=str(body.get("correlation_id") or ""),
            ),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@providers_router.post(
    "/{provider_ref}/connections",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def create_connection(
    provider_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_create_federation_connection(
            CreateFederationConnectionCommand(
                tenant_id=tenant_id,
                provider_ref=provider_ref,
                connection_ref=body.get("connection_ref"),
                protocol=body.get("protocol"),
                endpoints=dict(body.get("endpoints") or {}),
            ),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@providers_router.post(
    "/{provider_ref}/trust/evaluate",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def evaluate_trust(
    provider_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_validate_provider_trust(
            ValidateProviderTrustCommand(
                tenant_id=tenant_id,
                provider_ref=provider_ref,
                inputs=dict(body.get("inputs") or {}),
                zero_trust_ctx=dict(body.get("zero_trust_ctx") or {}),
            ),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@providers_router.post(
    "/{provider_ref}/certificates/rotate",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def rotate_certificate(
    provider_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_rotate_provider_certificate(
            RotateProviderCertificateCommand(
                tenant_id=tenant_id,
                provider_ref=provider_ref,
                cert_ref=body.get("cert_ref"),
                pem=str(body.get("pem") or "-----BEGIN CERTIFICATE-----\nMEOS\n-----END CERTIFICATE-----"),
            ),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@providers_router.post(
    "/{provider_ref}/synchronize",
    dependencies=[Depends(require_permissions("federation.write"))],
)
async def synchronize(
    provider_ref: str,
    body: dict[str, Any] | None = None,
    tenant_id: Annotated[str, Depends(get_tenant_id)] = "",
) -> dict:
    body = body or {}
    try:
        result = await handle_synchronize_identity(
            SynchronizeIdentityCommand(
                tenant_id=tenant_id,
                provider_ref=provider_ref,
                mode=str(body.get("mode") or "batch"),
                correlation_id=str(body.get("correlation_id") or ""),
            ),
            providers=get_identity_provider_repository(),
            sync_jobs=get_sync_job_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": result}


@providers_router.get(
    "/{provider_ref}",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_provider(
    provider_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_get_managed_provider(
            GetManagedProviderQuery(tenant_id=tenant_id, provider_ref=provider_ref),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@providers_router.get(
    "/{provider_ref}/health",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_health(
    provider_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_get_provider_health(
            GetProviderHealthQuery(tenant_id=tenant_id, provider_ref=provider_ref),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@providers_router.get(
    "/{provider_ref}/connections",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_connections(
    provider_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_get_federation_connections(
            GetFederationConnectionsQuery(tenant_id=tenant_id, provider_ref=provider_ref),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}


@providers_router.get(
    "/{provider_ref}/trust",
    dependencies=[Depends(require_permissions("federation.read"))],
)
async def get_trust(
    provider_ref: str,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
) -> dict:
    try:
        result = await handle_get_provider_trust_score(
            GetProviderTrustScoreQuery(tenant_id=tenant_id, provider_ref=provider_ref),
            providers=get_identity_provider_repository(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"data": result}
