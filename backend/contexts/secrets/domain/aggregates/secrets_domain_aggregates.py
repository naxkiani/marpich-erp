"""P209-C Cryptographic Trust Domain Architecture aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsDomainBlueprintRoot(AggregateRoot):
    """Domain boundaries must be clear."""

    tenant_id: str
    blueprint_ref: str
    boundaries_clear: bool
    logical_context_count: int
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls,
        *,
        tenant_id: str,
        blueprint_ref: str,
        boundaries_clear: bool = True,
        logical_context_count: int = 7,
    ) -> SecretsDomainBlueprintRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.domain.tenant_required")
        if not boundaries_clear or logical_context_count < 7:
            raise ValueError("secrets.domain.domain_boundaries_unclear")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            blueprint_ref=blueprint_ref.strip(),
            boundaries_clear=True,
            logical_context_count=logical_context_count,
            status="published",
        )
        root.pending_events.append("DomainBlueprintPublished")
        root.history.append({"event": "DomainBlueprintPublished"})
        return root

    def is_unclear(self) -> bool:
        return not self.boundaries_clear or self.logical_context_count < 7


@dataclass(eq=False, kw_only=True)
class SecretsPkiKmsSeparationRoot(AggregateRoot):
    """PKI and KMS responsibilities must not be mixed."""

    tenant_id: str
    separation_ref: str
    separated: bool
    mixed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls,
        *,
        tenant_id: str,
        separation_ref: str,
        separated: bool = True,
        mixed: bool = False,
    ) -> SecretsPkiKmsSeparationRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.domain.sep_tenant_required")
        if mixed or not separated:
            raise ValueError(
                "secrets.domain.pki_and_kms_responsibilities_mixed"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            separation_ref=separation_ref.strip(),
            separated=True,
            mixed=False,
            status="enforced",
        )
        root.history.append({"event": "PkiKmsSeparated"})
        return root

    def is_mixed(self) -> bool:
        return self.mixed or not self.separated


@dataclass(eq=False, kw_only=True)
class SecretsManagedSecretsRoot(AggregateRoot):
    """Secrets must be managed — never unmanaged."""

    tenant_id: str
    managed_ref: str
    managed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        managed_ref: str,
        managed: bool = True,
    ) -> SecretsManagedSecretsRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.domain.managed_tenant_required")
        if not managed:
            raise ValueError("secrets.domain.secrets_unmanaged")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            managed_ref=managed_ref.strip(),
            managed=True,
            status="managed",
        )
        root.pending_events.append("SecretCreated")
        root.history.append({"event": "SecretsManagedRegistered"})
        return root

    def is_unmanaged(self) -> bool:
        return not self.managed


@dataclass(eq=False, kw_only=True)
class SecretsTrustRelationshipModelRoot(AggregateRoot):
    """Trust relationships must be modeled."""

    tenant_id: str
    trust_ref: str
    modeled: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def model(
        cls,
        *,
        tenant_id: str,
        trust_ref: str,
        modeled: bool = True,
    ) -> SecretsTrustRelationshipModelRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.domain.trust_tenant_required")
        if not modeled:
            raise ValueError(
                "secrets.domain.trust_relationships_not_modeled"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            trust_ref=trust_ref.strip(),
            modeled=True,
            status="modeled",
        )
        root.pending_events.append("TrustCreated")
        root.history.append({"event": "TrustRelationshipModeled"})
        return root

    def is_unmodeled(self) -> bool:
        return not self.modeled


@dataclass(eq=False, kw_only=True)
class SecretsDomainEventsCatalogRoot(AggregateRoot):
    """Domain events must not be absent."""

    tenant_id: str
    catalog_ref: str
    event_count: int
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls,
        *,
        tenant_id: str,
        catalog_ref: str,
        event_count: int = 21,
        present: bool = True,
    ) -> SecretsDomainEventsCatalogRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.domain.events_tenant_required")
        if not present or event_count < 12:
            raise ValueError("secrets.domain.domain_events_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            catalog_ref=catalog_ref.strip(),
            event_count=event_count,
            present=True,
            status="published",
        )
        root.history.append({"event": "DomainEventsCatalogPublished"})
        return root

    def is_absent(self) -> bool:
        return not self.present or self.event_count < 12


@dataclass(eq=False, kw_only=True)
class SecretsAggregateOwnershipRoot(AggregateRoot):
    """Aggregates must not violate ownership rules."""

    tenant_id: str
    ownership_ref: str
    valid: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def validate(
        cls,
        *,
        tenant_id: str,
        ownership_ref: str,
        valid: bool = True,
    ) -> SecretsAggregateOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.domain.own_tenant_required")
        if not valid:
            raise ValueError(
                "secrets.domain.aggregates_violate_ownership_rules"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ownership_ref=ownership_ref.strip(),
            valid=True,
            status="validated",
        )
        root.history.append({"event": "AggregateOwnershipValidated"})
        return root

    def is_violating(self) -> bool:
        return not self.valid


@dataclass(eq=False, kw_only=True)
class SecretsCryptoLifecycleDomainRoot(AggregateRoot):
    """Cryptographic lifecycle must be complete."""

    tenant_id: str
    lifecycle_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def complete_model(
        cls,
        *,
        tenant_id: str,
        lifecycle_ref: str,
        complete: bool = True,
    ) -> SecretsCryptoLifecycleDomainRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.domain.life_tenant_required")
        if not complete:
            raise ValueError(
                "secrets.domain.cryptographic_lifecycle_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            lifecycle_ref=lifecycle_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("KeyRotated")
        root.pending_events.append("CertificateRenewed")
        root.pending_events.append("SecretRotated")
        root.history.append({"event": "CryptoLifecycleDomainComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class SecretsBoundedContextMapRoot(AggregateRoot):
    """Bounded context map for logical crypto domains."""

    tenant_id: str
    map_ref: str
    context_count: int
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls,
        *,
        tenant_id: str,
        map_ref: str,
        context_count: int = 7,
    ) -> SecretsBoundedContextMapRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.domain.map_tenant_required")
        if context_count < 7:
            raise ValueError("secrets.domain.domain_boundaries_unclear")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            map_ref=map_ref.strip(),
            context_count=context_count,
            status="published",
        )
        root.history.append({"event": "BoundedContextMapPublished"})
        return root
