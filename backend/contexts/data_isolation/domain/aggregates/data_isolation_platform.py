"""Data isolation aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class IsolationCapability(StrEnum):
    RLS_CATALOG = "rls_catalog"
    RLS_POLICY_REGISTRY = "rls_policy_registry"
    PRINCIPAL_REGISTRY = "principal_registry"
    PRINCIPAL_PARTITIONING = "principal_partitioning"
    TENANT_CONTEXT_BINDING = "tenant_context_binding"
    ISOLATION_VERIFICATION = "isolation_verification"
    POLICY_DRIVEN_ISOLATION = "policy_driven_isolation"
    DATA_ISOLATION_DASHBOARD = "data_isolation_dashboard"
    PRINCIPAL_SYNC = "principal_sync"
    DATA_ISOLATION_API = "data_isolation_api"


class PrincipalType(StrEnum):
    USER = "user"
    SERVICE = "service"


@dataclass(eq=False, kw_only=True)
class IsolationProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    rls_enabled: bool = True
    principal_partition_modulus: int = 8
    enforce_tenant_context: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str, partition_modulus: int = 8) -> IsolationProfile:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            profile_ref=profile_ref,
            principal_partition_modulus=partition_modulus,
        )

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "rls_enabled": self.rls_enabled,
            "principal_partition_modulus": self.principal_partition_modulus,
            "enforce_tenant_context": self.enforce_tenant_context,
        }


@dataclass(eq=False, kw_only=True)
class Principal(AggregateRoot):
    tenant_id: str
    principal_ref: str
    principal_type: str
    email: str | None
    display_name: str
    status: str = "active"
    partition_bucket: int = 0
    source_user_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register_user(
        cls,
        *,
        tenant_id: str,
        principal_ref: str,
        user_id: str,
        email: str,
        display_name: str,
        partition_bucket: int,
    ) -> Principal:
        return cls(
            id=UniqueId.from_string(user_id),
            tenant_id=tenant_id,
            principal_ref=principal_ref,
            principal_type=PrincipalType.USER.value,
            email=email,
            display_name=display_name,
            source_user_id=user_id,
            partition_bucket=partition_bucket,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "principal_ref": self.principal_ref,
            "principal_type": self.principal_type,
            "email": self.email,
            "display_name": self.display_name,
            "status": self.status,
            "partition_bucket": self.partition_bucket,
            "source_user_id": self.source_user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(frozen=True)
class RlsPolicyDescriptor:
    schema_name: str
    table_name: str
    policy_name: str
    enabled: bool = True

    def to_dict(self) -> dict:
        return {
            "schema": self.schema_name,
            "table": self.table_name,
            "policy": self.policy_name,
            "enabled": self.enabled,
        }
