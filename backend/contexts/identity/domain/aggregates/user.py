"""User aggregate — Identity bounded context."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.identity.domain.events.integration_events import (
    MfaEnabledIntegration,
    UserCreatedIntegration,
    UserLoggedInIntegration,
)


class UserStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"
    PENDING_MFA = "pending_mfa"


@dataclass(eq=False, kw_only=True)
class User(AggregateRoot):
    tenant_id: str
    email: str
    password_hash: str
    display_name: str
    status: UserStatus = UserStatus.ACTIVE
    locale: str = "en-US"
    mfa_enabled: bool = False
    mfa_secret: str | None = None
    backup_codes: list[str] = field(default_factory=list)
    role_ids: list[str] = field(default_factory=list)
    failed_login_attempts: int = 0
    locked_until: datetime | None = None
    last_login_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        email: str,
        password_hash: str,
        display_name: str,
        locale: str = "en-US",
        role_ids: list[str] | None = None,
        correlation_id: str,
    ) -> tuple[User, UserCreatedIntegration]:
        user = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            email=email.strip().lower(),
            password_hash=password_hash,
            display_name=display_name.strip(),
            locale=locale,
            role_ids=role_ids or [],
        )
        event = UserCreatedIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            user_id=user.id,
            email=user.email,
            display_name=user.display_name,
        )
        return user, event

    def is_locked(self) -> bool:
        if self.status == UserStatus.LOCKED and self.locked_until:
            return self.locked_until > datetime.now(UTC)
        return self.status == UserStatus.LOCKED

    def record_failed_login(self) -> None:
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.status = UserStatus.LOCKED
            self.locked_until = datetime.now(UTC) + timedelta(minutes=15)
        self.updated_at = datetime.now(UTC)

    def record_successful_login(
        self,
        *,
        correlation_id: str,
        ip_address: str | None = None,
    ) -> UserLoggedInIntegration:
        self.failed_login_attempts = 0
        self.locked_until = None
        if self.status == UserStatus.LOCKED:
            self.status = UserStatus.ACTIVE
        self.last_login_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
        return UserLoggedInIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            user_id=self.id,
            email=self.email,
            ip_address=ip_address,
        )

    def enable_mfa(
        self,
        *,
        secret: str,
        backup_codes: list[str],
        correlation_id: str,
    ) -> MfaEnabledIntegration:
        self.mfa_secret = secret
        self.backup_codes = backup_codes
        self.mfa_enabled = True
        self.updated_at = datetime.now(UTC)
        return MfaEnabledIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            user_id=self.id,
        )

    def verify_backup_code(self, code: str) -> bool:
        if code in self.backup_codes:
            self.backup_codes.remove(code)
            self.updated_at = datetime.now(UTC)
            return True
        return False

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "email": self.email,
            "display_name": self.display_name,
            "status": self.status.value,
            "locale": self.locale,
            "mfa_enabled": self.mfa_enabled,
            "role_ids": self.role_ids,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
