"""P209-F Enterprise Key Management Service aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsKmsKeyProtectionRoot(AggregateRoot):
    """Keys must not be stored without protection."""

    tenant_id: str
    key_ref: str
    protected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def protect(
        cls,
        *,
        tenant_id: str,
        key_ref: str,
        protected: bool = True,
    ) -> SecretsKmsKeyProtectionRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.kms.tenant_required")
        if not protected:
            raise ValueError("secrets.kms.keys_stored_without_protection")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            key_ref=key_ref.strip(),
            protected=True,
            status="protected",
        )
        root.pending_events.append("KeyProtected")
        root.pending_events.append("KeyCreated")
        root.history.append({"event": "KeyProtected"})
        return root

    def is_unprotected(self) -> bool:
        return not self.protected


@dataclass(eq=False, kw_only=True)
class SecretsKmsHsmCapabilityRoot(AggregateRoot):
    """HSM capability must be available."""

    tenant_id: str
    hsm_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def verify(
        cls,
        *,
        tenant_id: str,
        hsm_ref: str,
        available: bool = True,
    ) -> SecretsKmsHsmCapabilityRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.kms.hsm_tenant_required")
        if not available:
            raise ValueError("secrets.kms.hsm_capability_unavailable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            hsm_ref=hsm_ref.strip(),
            available=True,
            status="verified",
        )
        root.pending_events.append("HsmCapabilityVerified")
        root.history.append({"event": "HsmCapabilityVerified"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class SecretsKmsKeyLifecycleRoot(AggregateRoot):
    """Key lifecycle must be complete."""

    tenant_id: str
    key_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def manage(
        cls,
        *,
        tenant_id: str,
        key_ref: str,
        complete: bool = True,
    ) -> SecretsKmsKeyLifecycleRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.kms.life_tenant_required")
        if not complete:
            raise ValueError("secrets.kms.key_lifecycle_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            key_ref=key_ref.strip(),
            complete=True,
            status="managed",
        )
        root.pending_events.append("KeyGenerated")
        root.pending_events.append("KeyActivated")
        root.history.append({"event": "KeyLifecycleManaged"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class SecretsKmsKeyOwnershipRoot(AggregateRoot):
    """Key ownership must be known."""

    tenant_id: str
    key_ref: str
    owner_ref: str
    known: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls,
        *,
        tenant_id: str,
        key_ref: str,
        owner_ref: str,
        known: bool = True,
    ) -> SecretsKmsKeyOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.kms.own_tenant_required")
        if not known or not owner_ref.strip():
            raise ValueError("secrets.kms.key_ownership_unknown")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            key_ref=key_ref.strip(),
            owner_ref=owner_ref.strip(),
            known=True,
            status="bound",
        )
        root.pending_events.append("KeyOwnershipBound")
        root.history.append({"event": "KeyOwnershipBound"})
        return root

    def is_unknown(self) -> bool:
        return not self.known or not self.owner_ref


@dataclass(eq=False, kw_only=True)
class SecretsKmsAutoRotationRoot(AggregateRoot):
    """Rotation must not be manual only."""

    tenant_id: str
    key_ref: str
    automatic: bool
    manual_only: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        key_ref: str,
        automatic: bool = True,
        manual_only: bool = False,
    ) -> SecretsKmsAutoRotationRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.kms.rot_tenant_required")
        if manual_only or not automatic:
            raise ValueError("secrets.kms.rotation_manual_only")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            key_ref=key_ref.strip(),
            automatic=True,
            manual_only=False,
            status="enabled",
        )
        root.pending_events.append("KeyRotated")
        root.history.append({"event": "AutoRotationEnabled"})
        return root

    def is_manual_only(self) -> bool:
        return self.manual_only or not self.automatic


@dataclass(eq=False, kw_only=True)
class SecretsKmsKeyAuditRoot(AggregateRoot):
    """Key operations must be audited."""

    tenant_id: str
    audit_ref: str
    action_ref: str
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
        action_ref: str,
        audited: bool = True,
    ) -> SecretsKmsKeyAuditRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.kms.audit_tenant_required")
        if not audited:
            raise ValueError("secrets.kms.key_operations_unaudited")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            audit_ref=audit_ref.strip(),
            action_ref=action_ref.strip(),
            audited=True,
            status="recorded",
        )
        root.pending_events.append("KeyAuditRecorded")
        root.history.append({"event": "KeyAuditRecorded"})
        return root

    def is_unaudited(self) -> bool:
        return not self.audited


@dataclass(eq=False, kw_only=True)
class SecretsKmsCryptoPolicyRoot(AggregateRoot):
    """Cryptographic policies must be present."""

    tenant_id: str
    policy_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def apply(
        cls,
        *,
        tenant_id: str,
        policy_ref: str,
        present: bool = True,
    ) -> SecretsKmsCryptoPolicyRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.kms.pol_tenant_required")
        if not present:
            raise ValueError("secrets.kms.cryptographic_policies_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            present=True,
            status="applied",
        )
        root.pending_events.append("CryptoPolicyApplied")
        root.history.append({"event": "CryptoPolicyApplied"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class SecretsKmsEnvelopeEncryptionRoot(AggregateRoot):
    """Envelope encryption DEK/KEK/Master model."""

    tenant_id: str
    envelope_ref: str
    enabled: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        envelope_ref: str,
        enabled: bool = True,
    ) -> SecretsKmsEnvelopeEncryptionRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.kms.env_tenant_required")
        if not enabled:
            raise ValueError("secrets.kms.keys_stored_without_protection")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            envelope_ref=envelope_ref.strip(),
            enabled=True,
            status="enabled",
        )
        root.pending_events.append("EnvelopeEncryptionEnabled")
        root.history.append({"event": "EnvelopeEncryptionEnabled"})
        return root
