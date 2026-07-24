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
from contexts.identity.domain.services.session_policy import remember_me_expiry, session_expiry
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
        remember_me: bool = False,
        remember_me_days: int = 30,
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
            remember_me=remember_me,
            remember_me_days=remember_me_days,
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

    async def change_password(
        self,
        *,
        tenant_id: str,
        user_id: str,
        current_password: str,
        new_password: str,
        revoke_other_sessions: bool = True,
        correlation_id: str,
        ip_address: str | None = None,
    ) -> Result[dict]:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(user_id))
        if not user:
            return Result.fail("identity.errors.user_not_found")
        if not await self._hasher.verify(current_password, user.password_hash):
            return Result.fail("identity.errors.invalid_credentials")
        if current_password == new_password:
            return Result.fail("identity.errors.password_unchanged")
        password_hash = await self._hasher.hash(new_password)
        user.update_password(password_hash=password_hash, must_change=False)
        await self._users.save(user)
        if revoke_other_sessions:
            await self._sessions.revoke_all_for_user(tenant_id, user_id)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="identity.password.updated",
            resource_type="user",
            resource_id=user_id,
            actor_id=user_id,
            ip_address=ip_address,
        )
        return Result.ok(
            {
                "password_changed": True,
                "password_must_change": user.password_must_change,
                "password_changed_at": (
                    user.password_changed_at.isoformat() if user.password_changed_at else None
                ),
                "other_sessions_revoked": bool(revoke_other_sessions),
            }
        )

    async def _issue_tokens(
        self,
        *,
        user: User,
        tenant_id: str,
        correlation_id: str,
        ip_address: str | None,
        user_agent: str | None = None,
        remember_me: bool = False,
        remember_me_days: int = 30,
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
        expiry = remember_me_expiry(remember_me_days) if remember_me else session_expiry()
        await self._sessions.create(
            session_id=session_id,
            tenant_id=tenant_id,
            user_id=str(user.id),
            refresh_hash=self._tokens.hash_refresh_token(refresh),
            expires_at=expiry,
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

    async def get_user_credential(self, tenant_id: str, user_id: str) -> Result[dict]:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(user_id))
        if not user:
            return Result.fail("identity.errors.user_not_found")
        return Result.ok(
            {
                "user_id": str(user.id),
                "email": user.email,
                "password_hash": user.password_hash,
                "password_hash_algorithm": user.password_hash_algorithm,
                "status": user.status.value,
                "failed_login_attempts": user.failed_login_attempts,
                "locked_until": user.locked_until.isoformat() if user.locked_until else None,
                "password_must_change": user.password_must_change,
                "password_changed_at": (
                    user.password_changed_at.isoformat() if user.password_changed_at else None
                ),
                "mfa_enabled": user.mfa_enabled,
            }
        )

    async def update_password_hash(
        self,
        *,
        tenant_id: str,
        user_id: str,
        password_hash: str,
        hash_algorithm: str,
        must_change_password: bool = False,
        correlation_id: str,
        ip_address: str | None = None,
    ) -> Result[dict]:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(user_id))
        if not user:
            return Result.fail("identity.errors.user_not_found")
        user.update_password(
            password_hash=password_hash,
            hash_algorithm=hash_algorithm,
            must_change=must_change_password,
        )
        await self._users.save(user)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="identity.password.updated",
            resource_type="user",
            resource_id=user_id,
            actor_id=user_id,
            ip_address=ip_address,
        )
        return Result.ok({"user_id": user_id, "password_must_change": user.password_must_change})

    async def record_failed_login_policy(
        self,
        *,
        tenant_id: str,
        user_id: str,
        max_attempts: int,
        lock_minutes: int,
    ) -> Result[dict]:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(user_id))
        if not user:
            return Result.fail("identity.errors.user_not_found")
        user.record_failed_login(max_attempts=max_attempts, lock_minutes=lock_minutes)
        await self._users.save(user)
        return Result.ok(
            {
                "failed_login_attempts": user.failed_login_attempts,
                "status": user.status.value,
                "locked_until": user.locked_until.isoformat() if user.locked_until else None,
            }
        )

    async def unlock_user(
        self,
        *,
        tenant_id: str,
        user_id: str,
        correlation_id: str,
        ip_address: str | None = None,
    ) -> Result[dict]:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(user_id))
        if not user:
            return Result.fail("identity.errors.user_not_found")
        user.unlock_account()
        await self._users.save(user)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="identity.account.unlocked",
            resource_type="user",
            resource_id=user_id,
            ip_address=ip_address,
        )
        return Result.ok({"user_id": user_id, "status": user.status.value})

    async def list_sessions(self, tenant_id: str, user_id: str) -> Result[list[dict]]:
        sessions = await self._sessions.list_for_user(tenant_id, user_id)
        return Result.ok(sessions)

    async def revoke_session(self, tenant_id: str, user_id: str, session_id: str) -> Result[dict]:
        sessions = await self._sessions.list_for_user(tenant_id, user_id)
        if not any(s["id"] == session_id for s in sessions):
            return Result.fail("identity.errors.session_not_found")
        await self._sessions.revoke(session_id)
        return Result.ok({"revoked": True, "session_id": session_id})

    async def begin_mfa_login(self, tenant_id: str, user_id: str) -> Result[str]:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(user_id))
        if not user or not user.mfa_enabled:
            return Result.fail("identity.errors.invalid_mfa")
        challenge = str(uuid.uuid4())
        self._mfa_challenges[challenge] = str(user.id)
        return Result.ok(challenge)

    async def verify_mfa_login(
        self,
        *,
        tenant_id: str,
        user_id: str,
        mfa_code: str | None,
        mfa_token: str | None,
        correlation_id: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
        remember_me: bool = False,
        remember_me_days: int = 30,
    ) -> Result[AuthTokens]:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(user_id))
        if not user:
            return Result.fail("identity.errors.user_not_found")
        if mfa_token:
            uid = self._mfa_challenges.pop(mfa_token, None)
            if uid != str(user.id):
                return Result.fail("identity.errors.invalid_mfa")
        if mfa_code and user.mfa_secret:
            valid = self._mfa.verify(user.mfa_secret, mfa_code)
            if not valid and not user.verify_backup_code(mfa_code):
                return Result.fail("identity.errors.invalid_mfa")
        elif not mfa_code:
            return Result.fail("identity.errors.invalid_mfa")
        return await self._issue_tokens(
            user=user,
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            ip_address=ip_address,
            user_agent=user_agent,
            remember_me=remember_me,
            remember_me_days=remember_me_days,
        )

    async def seed_education_personas(self, tenant_id: str) -> Result[dict]:
        """Ensure staff/student system roles exist for education industry tenants."""
        created: list[str] = []
        staff = await self._roles.find_by_code(tenant_id, "staff")
        if not staff:
            staff = Role.create_education_staff(tenant_id)
            await self._roles.save(staff)
            created.append("staff")
        student = await self._roles.find_by_code(tenant_id, "student")
        if not student:
            student = Role.create_education_student(tenant_id)
            await self._roles.save(student)
            created.append("student")
        return Result.ok(
            {
                "staff_role_id": str(staff.id),
                "student_role_id": str(student.id),
                "created": created,
            }
        )

    async def seed_clinic_personas(self, tenant_id: str) -> Result[dict]:
        """Ensure clinic_staff system role for outpatient industry tenants."""
        created: list[str] = []
        staff = await self._roles.find_by_code(tenant_id, "clinic_staff")
        if not staff:
            staff = Role.create_clinic_staff(tenant_id)
            await self._roles.save(staff)
            created.append("clinic_staff")
        return Result.ok(
            {
                "clinic_staff_role_id": str(staff.id),
                "created": created,
            }
        )

    async def seed_hospital_personas(self, tenant_id: str) -> Result[dict]:
        """Ensure hospital_staff system role for acute industry tenants."""
        created: list[str] = []
        staff = await self._roles.find_by_code(tenant_id, "hospital_staff")
        if not staff:
            staff = Role.create_hospital_staff(tenant_id)
            await self._roles.save(staff)
            created.append("hospital_staff")
        return Result.ok(
            {
                "hospital_staff_role_id": str(staff.id),
                "created": created,
            }
        )

    async def seed_pharmacy_personas(self, tenant_id: str) -> Result[dict]:
        """Ensure pharmacy_staff system role for dispensing tenants."""
        created: list[str] = []
        staff = await self._roles.find_by_code(tenant_id, "pharmacy_staff")
        if not staff:
            staff = Role.create_pharmacy_staff(tenant_id)
            await self._roles.save(staff)
            created.append("pharmacy_staff")
        return Result.ok(
            {
                "pharmacy_staff_role_id": str(staff.id),
                "created": created,
            }
        )

    async def seed_laboratory_personas(self, tenant_id: str) -> Result[dict]:
        """Ensure laboratory_staff system role for LIMS tenants."""
        created: list[str] = []
        staff = await self._roles.find_by_code(tenant_id, "laboratory_staff")
        if not staff:
            staff = Role.create_laboratory_staff(tenant_id)
            await self._roles.save(staff)
            created.append("laboratory_staff")
        return Result.ok(
            {
                "laboratory_staff_role_id": str(staff.id),
                "created": created,
            }
        )

    async def assign_user_roles(
        self,
        *,
        tenant_id: str,
        user_id: str,
        role_codes: list[str],
        correlation_id: str,
        actor_id: str | None = None,
    ) -> Result[dict]:
        user = await self._users.find_by_id(tenant_id, UniqueId.from_string(user_id))
        if not user:
            return Result.fail("identity.errors.user_not_found")

        role_ids: list[str] = []
        for code in role_codes:
            role = await self._roles.find_by_code(tenant_id, code.strip().lower())
            if not role:
                return Result.fail(f"identity.errors.role_not_found:{code}")
            role_ids.append(str(role.id))

        user.assign_roles(role_ids)
        await self._users.save(user)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="identity.user.roles_assigned",
            resource_type="user",
            resource_id=user_id,
            actor_id=actor_id,
            payload={"role_codes": [c.strip().lower() for c in role_codes]},
        )
        return Result.ok(user.to_dict())

    async def list_roles(self, tenant_id: str) -> Result[list[dict]]:
        roles = await self._roles.list_roles(tenant_id)
        return Result.ok([r.to_dict() for r in roles])
