"""Protocol bridge — wires federation gateway to authentication/directory protocol services."""
from __future__ import annotations


class ProtocolBridgeAdapter:
    """ACL adapter delegating to existing authentication and directory contexts."""

    async def begin_oidc_login(self, *, tenant_id: str, provider_ref: str) -> dict:
        from contexts.authentication.container import get_authentication_service

        result = await get_authentication_service().begin_oidc_authorize(tenant_id, provider_ref)
        return result.unwrap() if result.succeeded else {"error": result.error}

    async def complete_oidc_callback(
        self, *, tenant_id: str, code: str, state: str, correlation_id: str = ""
    ) -> dict:
        from contexts.authentication.container import get_authentication_service

        result = await get_authentication_service().complete_oidc_callback(
            tenant_id, code=code, state=state, correlation_id=correlation_id or "federation-gateway"
        )
        return result.unwrap() if result.succeeded else {"error": result.error}

    async def begin_saml_login(self, *, tenant_id: str, provider_ref: str) -> dict:
        from contexts.directory.container import get_directory_service

        result = await get_directory_service().begin_saml_login(tenant_id, provider_ref)
        return result.unwrap() if result.succeeded else {"error": result.error}

    async def complete_saml_acs(
        self, *, saml_response: str, relay_state: str, correlation_id: str = ""
    ) -> dict:
        from contexts.directory.container import get_directory_service

        result = await get_directory_service().complete_saml_acs(
            saml_response=saml_response,
            relay_state=relay_state,
            correlation_id=correlation_id or "federation-gateway",
        )
        return result.unwrap() if result.succeeded else {"error": result.error}

    async def ldap_sync(self, *, tenant_id: str, connector_ref: str) -> dict:
        from contexts.directory.container import get_directory_service

        svc = get_directory_service()
        result = await svc.sync_ldap(tenant_id, connector_ref=connector_ref)
        return result.unwrap() if result.succeeded else {"error": result.error}
