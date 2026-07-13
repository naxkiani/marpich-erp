"""Identity application services."""
from __future__ import annotations

import secrets
import uuid
from dataclasses import dataclass

from contexts.identity.domain.aggregates.role import Role
from contexts.identity.domain.aggregates.user import User, UserStatus
from contexts.identity.domain.ports.messaging import IAuditLogger, IOutboxPublisher
from contexts.identity.domain.ports.repositories import (
    IPermissionCatalog,
    IRoleRepository,
    ISessionRepository,
    IUserRepository,
)
from contexts.identity.domain.ports.security import IMfaService, IPasswordHasher, ITokenService
from contexts.identity.domain.services.session_policy import session_expiry
from shared.application.result import Result
from shared.domain.permissions import PermissionEvaluator
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.settings import settings


@dataclass
class AuthTokens:
    access_token: str
    refresh_token: str
    expires_in: int
    mfa_required: bool = False
    mfa_token: str | None = None


class IdentityApplicationService:
    def __init__(
        self,
        users: IUserRepository,
        roles: IRoleRepository,
        sessions: ISessionRepository,
        permissions: IPermissionCatalog,
        hasher: IPasswordHasher,
        tokens: ITokenService,
        mfa: IMfaService,
        audit: IAuditLogger,
        outbox: IOutboxPublisher,
    ) -> None:
        self._users = users
        self._roles = roles
        self._sessions = sessions
        self._permissions = permissions
        self._hasher = hasher
        self._tokens = tokens
        self._mfa = mfa
        self._audit = audit
        self._outbox = outbox
        self._evaluator = PermissionEvaluator()
        self._mfa_challenges: dict[str, str] = {}

    async def register(
        self,
        *,
        tenant_id: str,
        email: str,
        password: str,
        display_name: str,
        locale: str = "en-US",
        correlation_id: str,
        ip_address: str | None = None,
    ) -> Result[dict]:
        if await self._users.exists_by_email(tenant_id, email):
            return Result.fail("identity.errors.email_exists")

        admin_role = await self._roles.find_by_code(tenant_id, "admin")
        if not admin_role:
            admin_role = Role.create_system_admin(tenant_id)
            await self._roles.save(admin_role)

        is_first_user = len(await self._users.list_users(tenant_id, limit=1)) == 0
        role_ids = [str(admin_role.id)] if is_first_user else []

        password_hash = await self._hasher.hash(password)
        user, event = User.register(
            tenant_id=tenant_id,
            email=email,
            password_hash=password_hash,
            display_name=display_name,
            locale=locale,
            role_ids=role_ids,
            correlation_id=correlation_id,
        )
        await self._users.save(user)
        await self._outbox.publish(event)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="identity.user.registered",
            resource_type="user",
            resource_id=str(user.id),
            payload={"email": user.email},
            ip_address=ip_address,
        )
        return Result.ok(user.to_dict())

    async def login(
        self,
        *,
        tenant_id: str,
        email: str,
        password: str,
        correlation_id: str,
        mfa_code: str | None = None,
        mfa_token: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> Result[AuthTokens]:
        user = await self._users.find_by_email(tenant_id, email)
        if not user:
            return Result.fail("identity.errors.invalid_credentials")

        if user.is_locked():
            return Result.fail("identity.errors.account_locked")

        if not await self._hasher.verify(password, user.password_hash):
            user.record_failed_login()
            await self._users.save(user)
            return Result.fail("identity.errors.invalid_credentials")

        if user.mfa_enabled:
            if not mfa_code and not mfa_token:
                challenge = str(uuid.uuid4())
                self._mfa_challenges[challenge] = str(user.id)
                return Result.ok(
                    AuthTokens(
                        access_token="",
                        refresh_token="",
                        expires_in=0,
                        mfa_required=True,
                        mfa_token=challenge,
                    )
                )
            if mfa_token:
                uid = self._mfa_challenges.pop(mfa_token, None)
                if uid != str(user.id):
                    return Result.fail("identity.errors.invalid_mfa")
            if mfa_code and user.mfa_secret:
                valid = self._mfa.verify(user.mfa_secret, mfa_code)
                if not valid and not user.verify_backup_code(mfa_code):
                    return Result.fail("identity.errors.invalid_mfa")

        return await self._issue_tokens(
            user=user,
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    async def issue_tokens_for_user(
        self,
        *,
        tenant_id: str,
        user_id: str,
        correlation_id: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> Result[AuthTokens]:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(user_id))
        if not user:
            return Result.fail("identity.errors.user_not_found")
        if user.status != UserStatus.ACTIVE:
            return Result.fail("identity.errors.user_inactive")
        if user.is_locked():
            return Result.fail("identity.errors.account_locked")
        return await self._issue_tokens(
            user=user,
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    async def find_user_id_by_email(self, tenant_id: str, email: str) -> str | None:
        user = await self._users.find_by_email(tenant_id, email)
        return str(user.id) if user else None

    async def provision_directory_user(
        self,
        *,
        tenant_id: str,
        email: str,
        display_name: str,
        external_id: str,
        correlation_id: str,
    ) -> Result[dict]:
        existing = await self._users.find_by_email(tenant_id, email)
        if existing:
            return Result.ok(existing.to_dict())

        password_hash = await self._hasher.hash(secrets.token_urlsafe(48))
        user, event = User.register(
            tenant_id=tenant_id,
            email=email,
            password_hash=password_hash,
            display_name=display_name,
            correlation_id=correlation_id,
        )
        await self._users.save(user)
        await self._outbox.publish(event)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="identity.user.provisioned",
            resource_type="user",
            resource_id=str(user.id),
            payload={"email": user.email, "external_id": external_id, "source": "directory"},
        )
        return Result.ok(user.to_dict())

    async def refresh(
        self,
        *,
        tenant_id: str,
        refresh_token: str,
        correlation_id: str,
        ip_address: str | None = None,
    ) -> Result[AuthTokens]:
        try:
            payload = self._tokens.verify_refresh(refresh_token)
        except ValueError:
            return Result.fail("identity.errors.invalid_refresh_token")

        if payload.get("tenant_id") != tenant_id:
            return Result.fail("identity.errors.invalid_refresh_token")

        refresh_hash = self._tokens.hash_refresh_token(refresh_token)
        session = await self._sessions.find_by_refresh_hash(refresh_hash)
        if not session:
            return Result.fail("identity.errors.session_expired")

        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(payload["sub"]))
        if not user or user.status != UserStatus.ACTIVE:
            return Result.fail("identity.errors.user_inactive")

        await self._sessions.revoke(session["id"])
        return await self._issue_tokens(
            user=user,
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            ip_address=ip_address,
            user_agent=None,
        )

    async def logout(
        self,
        *,
        tenant_id: str,
        user_id: str,
        refresh_token: str | None,
        revoke_all: bool,
        correlation_id: str,
        ip_address: str | None = None,
    ) -> Result[dict]:
        if revoke_all:
            await self._sessions.revoke_all_for_user(tenant_id, user_id)
        elif refresh_token:
            refresh_hash = self._tokens.hash_refresh_token(refresh_token)
            session = await self._sessions.find_by_refresh_hash(refresh_hash)
            if session:
                await self._sessions.revoke(session["id"])

        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="identity.logout",
            resource_type="session",
            resource_id=user_id,
            actor_id=user_id,
            ip_address=ip_address,
        )
        return Result.ok({"revoked": True})

    async def get_me(self, tenant_id: str, user_id: str) -> Result[dict]:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(user_id))
        if not user:
            return Result.fail("identity.errors.user_not_found")
        perms = await self._permissions.resolve_permissions(tenant_id, user.role_ids)
        roles = await self._roles.list_roles(tenant_id)
        role_codes = [r.code for r in roles if str(r.id) in user.role_ids]
        data = user.to_dict()
        data["permissions"] = perms
        data["roles"] = role_codes
        return Result.ok(data)

    async def list_users(self, tenant_id: str, *, limit: int = 1000) -> Result[list[dict]]:
        users = await self._users.list_users(tenant_id, limit=limit)
        return Result.ok([user.to_dict() for user in users])

    async def setup_mfa(
        self,
        *,
        tenant_id: str,
        user_id: str,
        correlation_id: str,
    ) -> Result[dict]:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(user_id))
        if not user:
            return Result.fail("identity.errors.user_not_found")
        secret = self._mfa.generate_secret()
        self._mfa_challenges[f"setup:{user_id}"] = secret
        return Result.ok({
            "secret": secret,
            "provisioning_uri": self._mfa.provisioning_uri(user.email, secret),
        })

    async def verify_mfa_setup(
        self,
        *,
        tenant_id: str,
        user_id: str,
        code: str,
        correlation_id: str,
    ) -> Result[dict]:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(user_id))
        if not user:
            return Result.fail("identity.errors.user_not_found")
        secret = self._mfa_challenges.pop(f"setup:{user_id}", None)
        if not secret or not self._mfa.verify(secret, code):
            return Result.fail("identity.errors.invalid_mfa")
        backup_codes = self._mfa.generate_backup_codes()
        event = user.enable_mfa(secret=secret, backup_codes=backup_codes, correlation_id=correlation_id)
        await self._users.save(user)
        await self._outbox.publish(event)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="identity.mfa.enabled",
            resource_type="user",
            resource_id=user_id,
            actor_id=user_id,
        )
        return Result.ok({"mfa_enabled": True, "backup_codes": backup_codes})

    async def _issue_tokens(
        self,
        *,
        user: User,
        tenant_id: str,
        correlation_id: str,
        ip_address: str | None,
        user_agent: str | None = None,
    ) -> Result[AuthTokens]:
        perms = await self._permissions.resolve_permissions(tenant_id, user.role_ids)
        roles = await self._roles.list_roles(tenant_id)
        role_codes = [r.code for r in roles if str(r.id) in user.role_ids]

        token_payload = {
            "sub": str(user.id),
            "tenant_id": tenant_id,
            "email": user.email,
            "roles": role_codes,
            "permissions": perms,
            "locale": user.locale,
        }
        access = self._tokens.sign_access(token_payload)
        refresh = self._tokens.sign_refresh(token_payload)

        session_id = str(uuid.uuid4())
        await self._sessions.create(
            session_id=session_id,
            tenant_id=tenant_id,
            user_id=str(user.id),
            refresh_hash=self._tokens.hash_refresh_token(refresh),
            expires_at=session_expiry(),
            ip_address=ip_address,
            user_agent=user_agent,
        )

        login_event = user.record_successful_login(correlation_id=correlation_id, ip_address=ip_address)
        await self._users.save(user)
        await self._outbox.publish(login_event)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="identity.login.success",
            resource_type="user",
            resource_id=str(user.id),
            actor_id=str(user.id),
            ip_address=ip_address,
        )

        return Result.ok(
            AuthTokens(
                access_token=access,
                refresh_token=refresh,
                expires_in=settings.jwt_access_ttl,
                mfa_required=False,
            )
        )

    def check_permission(self, user_permissions: list[str], required: str) -> bool:
        return self._evaluator.has_permission(user_permissions, required)

    def verify_access_token(self, token: str) -> dict:
        return self._tokens.verify_access(token)
