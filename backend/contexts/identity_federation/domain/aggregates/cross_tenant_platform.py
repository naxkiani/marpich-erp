"""Cross-tenant delegation, partner access, external identity aggregates (P200-B8)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

DELEGATION_TYPES = frozenset({"user", "organization", "service", "ai_agent"})
PARTNER_KINDS = frozenset({"supplier", "vendor", "contractor", "customer", "partner"})
EXTERNAL_KINDS = frozenset({"guest", "customer", "partner", "temporary"})


def _require_future(expires_at: datetime | None) -> datetime:
    when = expires_at or (datetime.now(UTC) + timedelta(days=30))
    if when.tzinfo is None:
        when = when.replace(tzinfo=UTC)
    if when <= datetime.now(UTC):
        raise ValueError("cross_tenant.expiration_required_future")
    return when


@dataclass(eq=False, kw_only=True)
class DelegationAgreement(AggregateRoot):
    tenant_id: str
    delegation_ref: str
    delegation_type: str
    owner_id: str
    delegate_id: str
    scope: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    conditions: dict = field(default_factory=dict)
    status: str = "pending"  # pending|approved|active|expired|revoked
    expires_at: datetime = field(default_factory=lambda: datetime.now(UTC) + timedelta(days=30))
    audit: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        delegation_ref: str,
        delegation_type: str,
        owner_id: str,
        delegate_id: str,
        scope: list[str] | None = None,
        permissions: list[str] | None = None,
        conditions: dict | None = None,
        expires_at: datetime | None = None,
    ) -> DelegationAgreement:
        dtype = (delegation_type or "").strip().lower()
        if dtype not in DELEGATION_TYPES:
            raise ValueError("delegation.invalid_type")
        if not owner_id or not delegate_id:
            raise ValueError("delegation.requires_parties")
        perms = list(permissions or [])
        if "*" in perms or "admin.*" in perms:
            raise ValueError("delegation.unlimited_privileges_forbidden")
        if not scope and not perms:
            raise ValueError("delegation.requires_scope_or_permissions")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            delegation_ref=delegation_ref,
            delegation_type=dtype,
            owner_id=owner_id,
            delegate_id=delegate_id,
            scope=list(scope or []),
            permissions=perms,
            conditions=conditions or {},
            expires_at=_require_future(expires_at),
            status="pending",
            audit=[{"action": "created", "at": datetime.now(UTC).isoformat()}],
        )

    def approve(self, *, actor_id: str | None = None) -> None:
        if self.status not in ("pending", "approved"):
            raise ValueError("delegation.approve_illegal_state")
        if self.expires_at <= datetime.now(UTC):
            self.status = "expired"
            raise ValueError("delegation.expired")
        self.status = "approved"
        self.audit.append(
            {"action": "approved", "actor_id": actor_id, "at": datetime.now(UTC).isoformat()}
        )

    def activate(self) -> None:
        if self.status != "approved":
            raise ValueError("delegation.activate_requires_approval")
        if self.expires_at <= datetime.now(UTC):
            self.status = "expired"
            raise ValueError("delegation.expired")
        self.status = "active"
        self.audit.append({"action": "activated", "at": datetime.now(UTC).isoformat()})

    def revoke(self, *, reason: str = "") -> None:
        self.status = "revoked"
        self.audit.append(
            {"action": "revoked", "reason": reason, "at": datetime.now(UTC).isoformat()}
        )

    def ensure_not_expired(self) -> None:
        if self.status in ("revoked", "expired"):
            return
        if self.expires_at <= datetime.now(UTC):
            self.status = "expired"
            self.audit.append({"action": "expired", "at": datetime.now(UTC).isoformat()})

    def to_dict(self) -> dict:
        return {
            "delegation_ref": self.delegation_ref,
            "delegation_type": self.delegation_type,
            "owner_id": self.owner_id,
            "delegate_id": self.delegate_id,
            "scope": self.scope,
            "permissions": self.permissions,
            "conditions": self.conditions,
            "status": self.status,
            "expires_at": self.expires_at.isoformat(),
            "audit_count": len(self.audit),
        }


@dataclass(eq=False, kw_only=True)
class PartnerAccess(AggregateRoot):
    tenant_id: str
    partner_ref: str
    partner_kind: str
    partner_tenant_id: str | None = None
    organization_name: str = ""
    access_scopes: list[str] = field(default_factory=list)
    status: str = "registered"  # registered|access_assigned|suspended|revoked
    expires_at: datetime = field(default_factory=lambda: datetime.now(UTC) + timedelta(days=90))
    policy_ref: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        partner_ref: str,
        partner_kind: str,
        organization_name: str = "",
        partner_tenant_id: str | None = None,
        expires_at: datetime | None = None,
    ) -> PartnerAccess:
        kind = (partner_kind or "").strip().lower()
        if kind not in PARTNER_KINDS:
            raise ValueError("partner.invalid_kind")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            partner_ref=partner_ref,
            partner_kind=kind,
            organization_name=organization_name or partner_ref,
            partner_tenant_id=partner_tenant_id,
            expires_at=_require_future(expires_at),
            status="registered",
        )

    def assign_access(self, *, scopes: list[str], policy_ref: str | None = None) -> None:
        if self.status == "revoked":
            raise ValueError("partner.revoked")
        if not scopes:
            raise ValueError("partner.requires_scopes")
        if "*" in scopes:
            raise ValueError("partner.unlimited_scopes_forbidden")
        if self.expires_at <= datetime.now(UTC):
            raise ValueError("partner.expired")
        self.access_scopes = list(scopes)
        self.policy_ref = policy_ref
        self.status = "access_assigned"

    def revoke(self, *, reason: str = "") -> None:
        self.status = "revoked"
        self.access_scopes = []

    def to_dict(self) -> dict:
        return {
            "partner_ref": self.partner_ref,
            "partner_kind": self.partner_kind,
            "partner_tenant_id": self.partner_tenant_id,
            "organization_name": self.organization_name,
            "access_scopes": self.access_scopes,
            "status": self.status,
            "policy_ref": self.policy_ref,
            "expires_at": self.expires_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class ExternalIdentity(AggregateRoot):
    tenant_id: str
    external_ref: str
    identity_kind: str
    email: str
    status: str = "invited"  # invited|verified|active|expired|removed
    expires_at: datetime = field(default_factory=lambda: datetime.now(UTC) + timedelta(days=14))
    sponsor_id: str | None = None
    access_scopes: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def invite(
        cls,
        *,
        tenant_id: str,
        external_ref: str,
        identity_kind: str,
        email: str,
        sponsor_id: str | None = None,
        access_scopes: list[str] | None = None,
        expires_at: datetime | None = None,
    ) -> ExternalIdentity:
        kind = (identity_kind or "").strip().lower()
        if kind not in EXTERNAL_KINDS:
            raise ValueError("external.invalid_kind")
        if not email or "@" not in email:
            raise ValueError("external.invalid_email")
        scopes = list(access_scopes or [])
        if "*" in scopes:
            raise ValueError("external.unlimited_scopes_forbidden")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            external_ref=external_ref,
            identity_kind=kind,
            email=email.strip().lower(),
            sponsor_id=sponsor_id,
            access_scopes=scopes,
            expires_at=_require_future(expires_at),
            status="invited",
        )

    def activate(self) -> None:
        if self.status not in ("invited", "verified", "active"):
            raise ValueError("external.activate_illegal_state")
        if self.expires_at <= datetime.now(UTC):
            self.status = "expired"
            raise ValueError("external.expired")
        self.status = "active"

    def remove(self, *, reason: str = "") -> None:
        self.status = "removed"
        self.access_scopes = []

    def to_dict(self) -> dict:
        return {
            "external_ref": self.external_ref,
            "identity_kind": self.identity_kind,
            "email": self.email,
            "status": self.status,
            "sponsor_id": self.sponsor_id,
            "access_scopes": self.access_scopes,
            "expires_at": self.expires_at.isoformat(),
        }
