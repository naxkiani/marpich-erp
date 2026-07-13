"""Directory application service."""
from __future__ import annotations

import base64
import uuid

from contexts.directory.domain.aggregates.directory_platform import (
    DirectoryProfile,
    DirectorySyncJob,
    LdapConnector,
    SamlProvider,
    ScimProvider,
)
from contexts.directory.domain.events.directory_integration_events import (
    DirectorySyncCompletedIntegration,
    IntegrationDirectorySyncedIntegration,
    LdapConnectorRegisteredIntegration,
    ScimUserProvisionedIntegration,
    SamlProviderRegisteredIntegration,
)
from contexts.directory.domain.ports.directory_repositories import (
    IDirectoryProfileRepository,
    IDirectorySyncJobRepository,
    IIdentityProvisioningPort,
    ILdapConnectorRepository,
    ILdapDirectoryClient,
    ISamlProviderRepository,
    ISamlRelayStateStore,
    IScimProviderRepository,
)
from contexts.directory.domain.services import directory_engine as engine
from contexts.directory.infrastructure.security.ldap_service import StubLdapDirectoryClient
from contexts.directory.infrastructure.security.saml_service import SamlFederationService
from contexts.directory.infrastructure.security.scim_service import ScimProvisioningService
from contexts.directory.infrastructure.workers.directory_sync_worker import DirectorySyncWorker
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event
from shared.infrastructure.settings import settings


class DirectoryApplicationService:
    def __init__(
        self,
        profiles: IDirectoryProfileRepository,
        saml_providers: ISamlProviderRepository,
        ldap_connectors: ILdapConnectorRepository,
        scim_providers: IScimProviderRepository,
        sync_jobs: IDirectorySyncJobRepository,
        relay_states: ISamlRelayStateStore,
        identity: IIdentityProvisioningPort,
        policy_evaluator: IPolicyEvaluator,
        ldap_client: ILdapDirectoryClient | None = None,
        saml: SamlFederationService | None = None,
        scim: ScimProvisioningService | None = None,
        worker: DirectorySyncWorker | None = None,
    ) -> None:
        self._profiles = profiles
        self._saml_providers = saml_providers
        self._ldap_connectors = ldap_connectors
        self._scim_providers = scim_providers
        self._sync_jobs = sync_jobs
        self._relay_states = relay_states
        self._identity = identity
        self._policy = policy_evaluator
        self._ldap = ldap_client or StubLdapDirectoryClient()
        self._saml = saml or SamlFederationService()
        self._scim = scim or ScimProvisioningService()
        self._worker = worker or DirectorySyncWorker()

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "saml_enabled": profile.saml_enabled if profile else True,
            "ldap_enabled": profile.ldap_enabled if profile else True,
            "scim_enabled": profile.scim_enabled if profile else True,
            "auto_provision": profile.auto_provision if profile else True,
        }
        pmap = {
            "directory.saml.enabled": ("saml_enabled", "enabled"),
            "directory.ldap.enabled": ("ldap_enabled", "enabled"),
            "directory.scim.enabled": ("scim_enabled", "enabled"),
            "directory.sync.auto_provision": ("auto_provision", "enabled"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> DirectoryProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = DirectoryProfile.create(
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
            "directory_sources": engine.list_directory_sources(),
            "dependency_map": engine.dependency_map(),
            "runtime": {
                "saml_sp_entity_id": settings.saml_sp_entity_id,
                "saml_acs_url": settings.saml_acs_url,
            },
        })

    async def seed(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        return Result.ok({"seeded": True, "profile_ref": profile.profile_ref})

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        saml = await self._saml_providers.list_by_tenant(tenant_id)
        ldap = await self._ldap_connectors.list_by_tenant(tenant_id)
        scim = await self._scim_providers.list_by_tenant(tenant_id)
        jobs = await self._sync_jobs.list_by_tenant(tenant_id)
        policy = await self._policy_params(tenant_id)
        return Result.ok({
            "summary": {
                "capabilities": len(engine.list_capability_catalog()),
                "saml_providers": len(saml),
                "ldap_connectors": len(ldap),
                "scim_providers": len(scim),
                "sync_jobs": len(jobs),
                "pending_jobs": len([j for j in jobs if j.status == "pending"]),
            },
            "profile": profile.to_dict(),
            "policy": policy,
        })

    async def register_saml_provider(
        self,
        tenant_id: str,
        *,
        name: str,
        entity_id: str,
        sso_url: str,
        x509_cert: str,
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["saml_enabled"]:
            return Result.fail("directory.errors.saml_disabled")
        provider = SamlProvider.register(
            tenant_id=tenant_id,
            provider_ref=self._saml_providers.next_provider_ref(tenant_id),
            name=name,
            entity_id=entity_id,
            sso_url=sso_url,
            x509_cert=x509_cert,
        )
        await self._saml_providers.save(provider)
        await publish_integration_event(
            SamlProviderRegisteredIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                provider_ref=provider.provider_ref,
                name=provider.name,
            )
        )
        return Result.ok(provider.to_dict())

    async def list_saml_providers(self, tenant_id: str) -> Result[list[dict]]:
        providers = await self._saml_providers.list_by_tenant(tenant_id)
        return Result.ok([p.to_dict() for p in providers])

    async def begin_saml_login(self, tenant_id: str, provider_ref: str) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["saml_enabled"]:
            return Result.fail("directory.errors.saml_disabled")
        provider = await self._saml_providers.find_by_ref(tenant_id, provider_ref)
        if not provider or not provider.enabled:
            return Result.fail("directory.errors.saml_provider_not_found")
        url, relay_state = self._saml.build_login_redirect(
            sp_entity_id=settings.saml_sp_entity_id,
            acs_url=settings.saml_acs_url,
            idp_sso_url=provider.sso_url,
        )
        await self._relay_states.put(
            relay_state,
            {"tenant_id": tenant_id, "provider_ref": provider_ref},
            settings.saml_relay_state_ttl_seconds,
        )
        return Result.ok({"authorization_url": url, "relay_state": relay_state})

    async def complete_saml_acs(
        self,
        *,
        saml_response: str,
        relay_state: str,
        correlation_id: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> Result[dict]:
        state = await self._relay_states.pop(relay_state)
        if not state:
            return Result.fail("directory.errors.saml_relay_state_expired")
        tenant_id = str(state["tenant_id"])
        email = self._saml.extract_email(saml_response)
        if not email:
            return Result.fail("directory.errors.saml_email_not_found")
        user_id = await self._identity.find_user_id_by_email(tenant_id, email)
        policy = await self._policy_params(tenant_id)
        if not user_id:
            if not policy["auto_provision"]:
                return Result.fail("directory.errors.user_not_provisioned")
            user = await self._identity.provision_user(
                tenant_id=tenant_id,
                email=email,
                display_name=email.split("@")[0],
                external_id=f"saml:{email}",
                correlation_id=correlation_id,
            )
            user_id = str(user["id"])
        tokens = await self._identity.issue_tokens_for_user(
            tenant_id=tenant_id,
            user_id=user_id,
            correlation_id=correlation_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return Result.ok({**tokens, "auth_method": "saml", "email": email})

    async def register_ldap_connector(
        self,
        tenant_id: str,
        *,
        name: str,
        host: str,
        port: int,
        bind_dn: str,
        bind_password: str,
        base_dn: str,
        user_filter: str = "(objectClass=person)",
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["ldap_enabled"]:
            return Result.fail("directory.errors.ldap_disabled")
        connector = LdapConnector.register(
            tenant_id=tenant_id,
            connector_ref=self._ldap_connectors.next_connector_ref(tenant_id),
            name=name,
            host=host,
            port=port,
            bind_dn=bind_dn,
            bind_password=bind_password,
            base_dn=base_dn,
            user_filter=user_filter,
        )
        await self._ldap_connectors.save(connector)
        await publish_integration_event(
            LdapConnectorRegisteredIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                connector_ref=connector.connector_ref,
                name=connector.name,
            )
        )
        return Result.ok(connector.to_dict())

    async def list_ldap_connectors(self, tenant_id: str) -> Result[list[dict]]:
        connectors = await self._ldap_connectors.list_by_tenant(tenant_id)
        return Result.ok([c.to_dict() for c in connectors])

    async def _sync_ldap_connector(self, tenant_id: str, connector_ref: str, correlation_id: str) -> dict:
        connector = await self._ldap_connectors.find_by_ref(tenant_id, connector_ref)
        if not connector or not connector.enabled:
            raise ValueError("directory.errors.ldap_connector_not_found")
        policy = await self._policy_params(tenant_id)
        entries = await self._ldap.search_users(connector)
        synced = 0
        created = 0
        for entry in entries:
            synced += 1
            email = str(entry.get("email", "")).lower()
            if not email:
                continue
            existing = await self._identity.find_user_id_by_email(tenant_id, email)
            if existing:
                continue
            if not policy["auto_provision"]:
                continue
            await self._identity.provision_user(
                tenant_id=tenant_id,
                email=email,
                display_name=str(entry.get("display_name", email)),
                external_id=str(entry.get("external_id", email)),
                correlation_id=correlation_id,
            )
            created += 1
        await publish_integration_event(
            DirectorySyncCompletedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                source_type="ldap",
                source_ref=connector_ref,
                users_synced=synced,
                users_created=created,
            )
        )
        await publish_integration_event(
            IntegrationDirectorySyncedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                source_type="ldap",
                users_synced=synced,
                users_created=created,
            )
        )
        return {"synced": synced, "created": created}

    async def sync_ldap(self, tenant_id: str, connector_ref: str) -> Result[dict]:
        correlation_id = str(uuid.uuid4())
        try:
            result = await self._sync_ldap_connector(tenant_id, connector_ref, correlation_id)
        except ValueError as exc:
            return Result.fail(str(exc))
        return Result.ok(result)

    async def enqueue_ldap_sync(self, tenant_id: str, connector_ref: str) -> Result[dict]:
        connector = await self._ldap_connectors.find_by_ref(tenant_id, connector_ref)
        if not connector:
            return Result.fail("directory.errors.ldap_connector_not_found")
        job = DirectorySyncJob.enqueue(
            tenant_id=tenant_id,
            job_ref=self._sync_jobs.next_job_ref(tenant_id),
            source_type="ldap",
            source_ref=connector_ref,
        )
        await self._sync_jobs.save(job)
        return Result.ok(job.to_dict())

    async def run_sync_worker(self, tenant_id: str) -> Result[dict]:
        pending = await self._sync_jobs.list_pending(tenant_id)
        processed = 0
        completed = 0
        failed = 0
        correlation_id = str(uuid.uuid4())

        async def sync_fn(source_ref: str) -> dict:
            return await self._sync_ldap_connector(tenant_id, source_ref, correlation_id)

        for job in pending:
            processed += 1
            updated = await self._worker.process_job(job, sync_fn=sync_fn)
            await self._sync_jobs.save(updated)
            if updated.status == "completed":
                completed += 1
            elif updated.status == "failed":
                failed += 1
        return Result.ok({"processed": processed, "completed": completed, "failed": failed})

    async def list_sync_jobs(self, tenant_id: str) -> Result[list[dict]]:
        jobs = await self._sync_jobs.list_by_tenant(tenant_id)
        return Result.ok([job.to_dict() for job in jobs])

    async def register_scim_provider(
        self,
        tenant_id: str,
        *,
        name: str,
        bearer_token: str | None = None,
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["scim_enabled"]:
            return Result.fail("directory.errors.scim_disabled")
        token = bearer_token or str(uuid.uuid4())
        provider = ScimProvider.register(
            tenant_id=tenant_id,
            provider_ref=self._scim_providers.next_provider_ref(tenant_id),
            name=name,
            bearer_token=token,
        )
        await self._scim_providers.save(provider)
        return Result.ok(provider.to_dict(include_secret=True))

    async def list_scim_providers(self, tenant_id: str) -> Result[list[dict]]:
        providers = await self._scim_providers.list_by_tenant(tenant_id)
        return Result.ok([p.to_dict() for p in providers])

    async def provision_scim_user(
        self,
        tenant_id: str,
        bearer_token: str,
        payload: dict,
        *,
        correlation_id: str,
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["scim_enabled"]:
            return Result.fail("directory.errors.scim_disabled")
        provider = await self._scim_providers.find_by_token(tenant_id, bearer_token)
        if not provider:
            return Result.fail("directory.errors.scim_unauthorized")
        try:
            email, display_name, external_id = self._scim.parse_create_user(payload)
        except ValueError as exc:
            return Result.fail(str(exc))
        user_id = await self._identity.find_user_id_by_email(tenant_id, email)
        if not user_id:
            if not policy["auto_provision"]:
                return Result.fail("directory.errors.user_not_provisioned")
            user = await self._identity.provision_user(
                tenant_id=tenant_id,
                email=email,
                display_name=display_name,
                external_id=external_id,
                correlation_id=correlation_id,
            )
            user_id = str(user["id"])
        await publish_integration_event(
            ScimUserProvisionedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                user_id=user_id,
                email=email,
                provider_ref=provider.provider_ref,
            )
        )
        return Result.ok(
            self._scim.build_user_response(
                user_id=user_id,
                email=email,
                display_name=display_name,
                external_id=external_id,
            )
        )

    @staticmethod
    def build_test_saml_response(email: str) -> str:
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<samlp:Response xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">'
            '<saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">'
            f"<saml:Subject><saml:NameID>{email}</saml:NameID></saml:Subject>"
            "</saml:Assertion></samlp:Response>"
        )
        return base64.b64encode(xml.encode("utf-8")).decode("ascii")
