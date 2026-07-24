"""P209-A Secrets strategy aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsGovernedStoreRoot(AggregateRoot):
    """Secrets must not be stored outside governed secret stores."""

    tenant_id: str
    store_ref: str
    governed: bool
    outside: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls,
        *,
        tenant_id: str,
        store_ref: str,
        governed: bool = True,
        outside: bool = False,
    ) -> SecretsGovernedStoreRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.strategy.tenant_required")
        if outside or not governed:
            raise ValueError(
                "secrets.strategy.secrets_stored_outside_governed_stores"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            store_ref=store_ref.strip(),
            governed=True,
            outside=False,
            status="registered",
        )
        root.pending_events.append("GovernedStoreRegistered")
        root.history.append({"event": "GovernedStoreRegistered"})
        return root

    def is_outside(self) -> bool:
        return self.outside or not self.governed


@dataclass(eq=False, kw_only=True)
class SecretsKeyExportPolicyRoot(AggregateRoot):
    """Keys must not be exportable without policy."""

    tenant_id: str
    policy_ref: str
    key_ref: str
    export_allowed: bool
    policy_present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        policy_ref: str,
        key_ref: str,
        export_allowed: bool = False,
        policy_present: bool = True,
    ) -> SecretsKeyExportPolicyRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.strategy.key_tenant_required")
        if export_allowed and not policy_present:
            raise ValueError(
                "secrets.strategy.keys_exportable_without_policy"
            )
        if not policy_present:
            raise ValueError(
                "secrets.strategy.keys_exportable_without_policy"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            key_ref=key_ref.strip(),
            export_allowed=export_allowed,
            policy_present=True,
            status="defined",
        )
        root.pending_events.append("KeyExportPolicyDefined")
        if export_allowed is False:
            root.pending_events.append("KeyExportDenied")
        root.history.append({"event": "KeyExportPolicyDefined"})
        return root

    def is_exportable_without_policy(self) -> bool:
        return self.export_allowed and not self.policy_present


@dataclass(eq=False, kw_only=True)
class SecretsCertLifecycleStrategyRoot(AggregateRoot):
    """Certificates must not be manually managed."""

    tenant_id: str
    strategy_ref: str
    automatic: bool
    manual: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def set(
        cls,
        *,
        tenant_id: str,
        strategy_ref: str,
        automatic: bool = True,
        manual: bool = False,
    ) -> SecretsCertLifecycleStrategyRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.strategy.cert_tenant_required")
        if manual or not automatic:
            raise ValueError(
                "secrets.strategy.certificates_manually_managed"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            strategy_ref=strategy_ref.strip(),
            automatic=True,
            manual=False,
            status="set",
        )
        root.pending_events.append("CertLifecycleStrategySet")
        root.history.append({"event": "CertLifecycleStrategySet"})
        return root

    def is_manual(self) -> bool:
        return self.manual or not self.automatic


@dataclass(eq=False, kw_only=True)
class SecretsRootCaSecurityRoot(AggregateRoot):
    """Root CA security must be adequate."""

    tenant_id: str
    ca_ref: str
    offline: bool
    adequate: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def harden(
        cls,
        *,
        tenant_id: str,
        ca_ref: str,
        offline: bool = True,
        adequate: bool = True,
    ) -> SecretsRootCaSecurityRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.strategy.ca_tenant_required")
        if not adequate or not offline:
            raise ValueError(
                "secrets.strategy.root_ca_security_inadequate"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ca_ref=ca_ref.strip(),
            offline=True,
            adequate=True,
            status="hardened",
        )
        root.pending_events.append("RootCaHardened")
        root.pending_events.append("RootOfTrustApproved")
        root.history.append({"event": "RootCaHardened"})
        return root

    def is_inadequate(self) -> bool:
        return not self.adequate or not self.offline


@dataclass(eq=False, kw_only=True)
class SecretsHsmStrategyRoot(AggregateRoot):
    """HSM integration must not be absent."""

    tenant_id: str
    binding_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls,
        *,
        tenant_id: str,
        binding_ref: str,
        present: bool = True,
    ) -> SecretsHsmStrategyRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.strategy.hsm_tenant_required")
        if not present:
            raise ValueError("secrets.strategy.hsm_integration_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            binding_ref=binding_ref.strip(),
            present=True,
            status="bound",
        )
        root.pending_events.append("HsmStrategyBound")
        root.history.append({"event": "HsmStrategyBound"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SecretsCryptoLifecycleRoot(AggregateRoot):
    """Cryptographic lifecycle must be complete."""

    tenant_id: str
    lifecycle_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def complete_review(
        cls,
        *,
        tenant_id: str,
        lifecycle_ref: str,
        complete: bool = True,
    ) -> SecretsCryptoLifecycleRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.strategy.lifecycle_tenant_required")
        if not complete:
            raise ValueError(
                "secrets.strategy.cryptographic_lifecycle_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            lifecycle_ref=lifecycle_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("CryptoLifecycleCompleted")
        root.history.append({"event": "CryptoLifecycleCompleted"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class SecretsCryptoAuditStrategyRoot(AggregateRoot):
    """Cryptographic operations must be audited."""

    tenant_id: str
    audit_ref: str
    operation_ref: str
    audited: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        audit_ref: str,
        operation_ref: str,
        audited: bool = True,
    ) -> SecretsCryptoAuditStrategyRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.strategy.audit_tenant_required")
        if not audited:
            raise ValueError(
                "secrets.strategy.cryptographic_operations_unaudited"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            audit_ref=audit_ref.strip(),
            operation_ref=operation_ref.strip(),
            audited=True,
            status="recorded",
        )
        root.pending_events.append("CryptoOperationAudited")
        root.history.append({"event": "CryptoOperationAudited"})
        return root

    def is_unaudited(self) -> bool:
        return not self.audited


@dataclass(eq=False, kw_only=True)
class SecretsStrategyProfileRoot(AggregateRoot):
    """Strategy profile for Cryptographic Trust Fabric."""

    tenant_id: str
    profile_ref: str
    published: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls,
        *,
        tenant_id: str,
        profile_ref: str,
        published: bool = True,
    ) -> SecretsStrategyProfileRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.strategy.profile_tenant_required")
        if not published:
            raise ValueError("secrets.strategy.strategy_not_published")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            profile_ref=profile_ref.strip(),
            published=True,
            status="published",
        )
        root.pending_events.append("StrategyPublished")
        root.history.append({"event": "StrategyPublished"})
        return root
