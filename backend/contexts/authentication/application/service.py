"""Authentication application service."""
from __future__ import annotations

import base64
import json
import uuid

from contexts.authentication.domain.aggregates.authentication_platform import (
    AuthenticationProfile,
    OidcProvider,
    WebAuthnCredential,
)
from contexts.authentication.domain.events.authentication_integration_events import (
    AuthenticationLoginSuccessIntegration,
    OidcProviderRegisteredIntegration,
    PasskeyRegisteredIntegration,
    PasskeyRevokedIntegration,
)
from contexts.authentication.domain.ports.authentication_repositories import (
    IAuthenticationProfileRepository,
    IIdentityTokenPort,
    IOidcProviderRepository,
    IOidcStateStore,
    IWebAuthnChallengeStore,
    IWebAuthnCredentialRepository,
)
from contexts.authentication.domain.services import authentication_engine as engine
from contexts.authentication.infrastructure.security.oidc_service import OidcFederationService
from contexts.authentication.infrastructure.security.webauthn_service import WebAuthnService
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event
from shared.infrastructure.settings import settings


class AuthenticationApplicationService:
    def __init__(
        self,
        profiles: IAuthenticationProfileRepository,
        credentials: IWebAuthnCredentialRepository,
        providers: IOidcProviderRepository,
        challenges: IWebAuthnChallengeStore,
        oidc_states: IOidcStateStore,
        identity: IIdentityTokenPort,
        policy_evaluator: IPolicyEvaluator,
        webauthn: WebAuthnService | None = None,
        oidc: OidcFederationService | None = None,
    ) -> None:
        self._profiles = profiles
        self._credentials = credentials
        self._providers = providers
        self._challenges = challenges
        self._oidc_states = oidc_states
        self._identity = identity
        self._policy = policy_evaluator
        self._webauthn = webauthn or WebAuthnService()
        self._oidc = oidc or OidcFederationService()

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "webauthn_enabled": profile.webauthn_enabled if profile else True,
            "passkeys_required": profile.passkeys_required if profile else False,
            "oidc_enabled": profile.oidc_enabled if profile else True,
            "password_enabled": profile.password_enabled if profile else True,
        }
        pmap = {
            "authentication.webauthn.enabled": ("webauthn_enabled", "enabled"),
            "authentication.passkeys.required": ("passkeys_required", "required"),
            "authentication.oidc.enabled": ("oidc_enabled", "enabled"),
            "authentication.password.enabled": ("password_enabled", "enabled"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> AuthenticationProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = AuthenticationProfile.create(
            tenant_id=tenant_id,
            profile_ref=self._profiles.next_profile_ref(tenant_id),
        )
        await self._profiles.save(profile)
        return profile

    async def handle_tenant_provisioned(self, event: dict) -> None:
        tenant_id = event.get("tenant_id") or event.get("payload", {}).get("tenant_id")
        if tenant_id:
            await self.seed(tenant_id)

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": engine.list_capability_catalog(),
            "policy_keys": engine.list_policy_keys(),
            "auth_methods": engine.list_auth_methods(),
            "dependency_map": engine.dependency_map(),
        })

    async def seed(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        return Result.ok({"seeded": True, "profile_ref": profile.profile_ref})

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        all_providers = await self._providers.list_by_tenant(tenant_id)
        all_credentials = await self._credentials.list_by_tenant(tenant_id)
        policy = await self._policy_params(tenant_id)
        return Result.ok({
            "summary": {
                "capabilities": len(engine.list_capability_catalog()),
                "passkeys": len(all_credentials),
                "oidc_providers": len(all_providers),
                "auth_methods": len(engine.list_auth_methods()),
            },
            "profile": profile.to_dict(),
            "policy": policy,
            "passkeys_by_user": len({c.user_id for c in all_credentials}),
            "enabled_oidc_providers": len([p for p in all_providers if p.enabled]),
        })

    async def list_passkeys(self, tenant_id: str, user_id: str) -> Result[list[dict]]:
        creds = await self._credentials.list_by_user(tenant_id, user_id)
        return Result.ok([c.to_dict() for c in creds])

    async def begin_passkey_registration(
        self,
        tenant_id: str,
        user_id: str,
        *,
        email: str,
        display_name: str,
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["webauthn_enabled"]:
            return Result.fail("authentication.errors.webauthn_disabled")
        existing = await self._credentials.list_by_user(tenant_id, user_id)
        challenge_id, options = self._webauthn.create_registration_options(
            user_id=user_id,
            user_email=email,
            user_display_name=display_name,
            existing_credentials=[c.to_dict() for c in existing],
        )
        challenge_b64 = self._webauthn.challenge_from_options(options)
        await self._challenges.put_registration(
            challenge_id,
            {
                "tenant_id": tenant_id,
                "user_id": user_id,
                "challenge": challenge_b64,
                "email": email,
            },
            settings.webauthn_challenge_ttl_seconds,
        )
        return Result.ok({"challenge_id": challenge_id, "options": options})

    async def complete_passkey_registration(
        self,
        tenant_id: str,
        user_id: str,
        *,
        challenge_id: str,
        credential: dict,
        nickname: str = "Passkey",
    ) -> Result[dict]:
        stored = await self._challenges.pop_registration(challenge_id)
        if not stored or stored["tenant_id"] != tenant_id or stored["user_id"] != user_id:
            return Result.fail("authentication.errors.invalid_challenge")
        verified = self._webauthn.verify_registration(
            challenge_b64=stored["challenge"],
            credential=credential,
            expected_user_id=user_id,
        )
        cred = WebAuthnCredential.register(
            tenant_id=tenant_id,
            user_id=user_id,
            credential_ref=self._credentials.next_credential_ref(tenant_id),
            credential_id=verified["credential_id"],
            public_key=verified["public_key"],
            sign_count=verified["sign_count"],
            nickname=nickname,
            aaguid=verified.get("aaguid"),
        )
        await self._credentials.save(cred)
        await publish_integration_event(
            PasskeyRegisteredIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                user_id=user_id,
                credential_ref=cred.credential_ref,
            )
        )
        return Result.ok(cred.to_dict())

    async def begin_passkey_login(self, tenant_id: str, email: str) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["webauthn_enabled"]:
            return Result.fail("authentication.errors.webauthn_disabled")
        user_id = await self._identity.find_user_id_by_email(tenant_id, email)
        if not user_id:
            return Result.fail("authentication.errors.user_not_found")
        creds = await self._credentials.list_by_user(tenant_id, user_id)
        if not creds:
            return Result.fail("authentication.errors.no_passkeys")
        challenge_id, options = self._webauthn.create_authentication_options(
            credentials=[c.to_dict() for c in creds],
        )
        challenge_b64 = self._webauthn.challenge_from_options(options)
        await self._challenges.put_authentication(
            challenge_id,
            {
                "tenant_id": tenant_id,
                "user_id": user_id,
                "challenge": challenge_b64,
                "email": email,
            },
            settings.webauthn_challenge_ttl_seconds,
        )
        return Result.ok({"challenge_id": challenge_id, "options": options})

    async def complete_passkey_login(
        self,
        tenant_id: str,
        *,
        challenge_id: str,
        credential: dict,
        correlation_id: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> Result[dict]:
        stored = await self._challenges.pop_authentication(challenge_id)
        if not stored or stored["tenant_id"] != tenant_id:
            return Result.fail("authentication.errors.invalid_challenge")
        credential_id = credential.get("id") or credential.get("rawId")
        if isinstance(credential_id, dict):
            credential_id = credential_id.get("id")
        if not credential_id:
            return Result.fail("authentication.errors.invalid_webauthn_credential")
        if isinstance(credential_id, bytes):
            credential_id = base64.urlsafe_b64encode(credential_id).decode("ascii").rstrip("=")
        stored_cred = await self._credentials.find_by_credential_id(tenant_id, str(credential_id))
        if not stored_cred:
            return Result.fail("authentication.errors.credential_not_found")
        verified = self._webauthn.verify_authentication(
            challenge_b64=stored["challenge"],
            credential=credential,
            stored_credential={
                "credential_id": stored_cred.credential_id,
                "public_key": stored_cred.public_key,
                "sign_count": stored_cred.sign_count,
                "user_id": stored_cred.user_id,
            },
        )
        stored_cred.mark_used(verified["sign_count"])
        await self._credentials.save(stored_cred)
        tokens = await self._identity.issue_tokens_for_user(
            tenant_id=tenant_id,
            user_id=stored_cred.user_id,
            correlation_id=correlation_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        await publish_integration_event(
            AuthenticationLoginSuccessIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                user_id=stored_cred.user_id,
                auth_method="webauthn",
            )
        )
        return Result.ok(tokens)

    async def revoke_passkey(self, tenant_id: str, user_id: str, credential_ref: str) -> Result[dict]:
        cred = await self._credentials.find_by_ref(tenant_id, credential_ref)
        if not cred or cred.user_id != user_id:
            return Result.fail("authentication.errors.credential_not_found")
        await self._credentials.delete(tenant_id, credential_ref)
        await publish_integration_event(
            PasskeyRevokedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                user_id=user_id,
                credential_ref=credential_ref,
            )
        )
        return Result.ok({"revoked": True, "credential_ref": credential_ref})

    async def register_oidc_provider(
        self,
        tenant_id: str,
        *,
        name: str,
        issuer_url: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: str | None = None,
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["oidc_enabled"]:
            return Result.fail("authentication.errors.oidc_disabled")
        provider = OidcProvider.register(
            tenant_id=tenant_id,
            provider_ref=self._providers.next_provider_ref(tenant_id),
            name=name,
            issuer_url=issuer_url,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scopes=scopes or settings.oidc_default_scopes,
        )
        await self._providers.save(provider)
        await publish_integration_event(
            OidcProviderRegisteredIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                provider_ref=provider.provider_ref,
                name=provider.name,
            )
        )
        return Result.ok(provider.to_dict())

    async def list_oidc_providers(self, tenant_id: str) -> Result[list[dict]]:
        providers = await self._providers.list_by_tenant(tenant_id)
        return Result.ok([p.to_dict() for p in providers])

    async def begin_oidc_authorize(self, tenant_id: str, provider_ref: str) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["oidc_enabled"]:
            return Result.fail("authentication.errors.oidc_disabled")
        provider = await self._providers.find_by_ref(tenant_id, provider_ref)
        if not provider or not provider.enabled:
            return Result.fail("authentication.errors.provider_not_found")
        state = engine.new_oidc_state()
        nonce = engine.new_oidc_nonce()
        await self._oidc_states.put(
            state,
            {
                "tenant_id": tenant_id,
                "provider_ref": provider_ref,
                "nonce": nonce,
            },
            settings.webauthn_challenge_ttl_seconds,
        )
        authorization_url = self._oidc.build_authorize_url(
            issuer_url=provider.issuer_url,
            client_id=provider.client_id,
            redirect_uri=provider.redirect_uri,
            scopes=provider.scopes,
            state=state,
            nonce=nonce,
        )
        return Result.ok({
            "provider_ref": provider_ref,
            "state": state,
            "authorization_url": authorization_url,
        })

    async def complete_oidc_callback(
        self,
        tenant_id: str,
        *,
        code: str,
        state: str,
        correlation_id: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> Result[dict]:
        stored = await self._oidc_states.pop(state)
        if not stored or stored["tenant_id"] != tenant_id:
            return Result.fail("authentication.errors.invalid_oidc_state")
        provider = await self._providers.find_by_ref(tenant_id, stored["provider_ref"])
        if not provider:
            return Result.fail("authentication.errors.provider_not_found")
        try:
            token_response = await self._oidc.exchange_code(
                issuer_url=provider.issuer_url,
                client_id=provider.client_id,
                client_secret=provider.client_secret,
                redirect_uri=provider.redirect_uri,
                code=code,
            )
        except Exception as exc:
            return Result.fail(f"authentication.errors.oidc_exchange_failed:{exc}")
        id_token = token_response.get("id_token")
        email = None
        if isinstance(id_token, str):
            payload_segment = id_token.split(".")[1]
            padding = "=" * (-len(payload_segment) % 4)
            payload = json.loads(base64.urlsafe_b64decode(payload_segment + padding))
            email = self._oidc.extract_email_from_id_token(payload)
        if not email:
            return Result.fail("authentication.errors.oidc_email_missing")
        user_id = await self._identity.find_user_id_by_email(tenant_id, email)
        if not user_id:
            return Result.fail("authentication.errors.user_not_found")
        tokens = await self._identity.issue_tokens_for_user(
            tenant_id=tenant_id,
            user_id=user_id,
            correlation_id=correlation_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        await publish_integration_event(
            AuthenticationLoginSuccessIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                user_id=user_id,
                auth_method="oidc",
            )
        )
        return Result.ok(tokens)
