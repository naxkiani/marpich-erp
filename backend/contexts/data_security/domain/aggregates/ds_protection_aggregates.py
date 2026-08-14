"""P211-J Protection aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsProtectedSensitiveRoot(AggregateRoot):
    tenant_id: str
    asset_ref: str
    protected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def protect(
        cls, *, tenant_id: str, asset_ref: str, protected: bool = True
    ) -> DsProtectedSensitiveRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.protection.tenant_required")
        if not protected:
            raise ValueError(
                "data_security.protection.sensitive_data_can_exist_unprotected"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            asset_ref=asset_ref.strip(),
            protected=True,
            status="protected",
        )
        root.pending_events.append("DataProtectionApplied")
        root.pending_events.append("UnprotectedSensitiveRejected")
        root.history.append({"event": "SensitiveProtected"})
        return root

    def is_unprotected(self) -> bool:
        return not self.protected


@dataclass(eq=False, kw_only=True)
class DsDefinedEncryptionPolicyRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls, *, tenant_id: str, policy_ref: str, defined: bool = True
    ) -> DsDefinedEncryptionPolicyRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.protection.pol_tenant_required")
        if not defined:
            raise ValueError(
                "data_security.protection.encryption_policies_are_undefined"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("ProtectionPolicyChanged")
        root.pending_events.append("UndefinedEncryptionPolicyRejected")
        root.history.append({"event": "EncryptionPolicyDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class DsTokenLifecycleRoot(AggregateRoot):
    tenant_id: str
    token_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def manage(
        cls, *, tenant_id: str, token_ref: str, present: bool = True
    ) -> DsTokenLifecycleRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.protection.tok_tenant_required")
        if not present:
            raise ValueError(
                "data_security.protection.token_lifecycle_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            token_ref=token_ref.strip(),
            present=True,
            status="active",
        )
        root.pending_events.append("TokenCreated")
        root.pending_events.append("TokenLifecycleUpdated")
        root.pending_events.append("MissingTokenLifecycleRejected")
        root.history.append({"event": "TokenLifecyclePresent"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DsKeyIntegrationRoot(AggregateRoot):
    tenant_id: str
    key_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls, *, tenant_id: str, key_ref: str, available: bool = True
    ) -> DsKeyIntegrationRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.protection.key_tenant_required")
        if not available or not key_ref.strip():
            raise ValueError(
                "data_security.protection.key_integration_is_unavailable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            key_ref=key_ref.strip(),
            available=True,
            status="bound",
        )
        root.pending_events.append("KeyReferenceBound")
        root.pending_events.append("UnavailableKeyIntegrationRejected")
        root.history.append({"event": "KeyIntegrationAvailable"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class DsAuditableProtectionDecisionRoot(AggregateRoot):
    tenant_id: str
    decision_ref: str
    auditable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def decide(
        cls, *, tenant_id: str, decision_ref: str, auditable: bool = True
    ) -> DsAuditableProtectionDecisionRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.protection.dec_tenant_required")
        if not auditable:
            raise ValueError(
                "data_security.protection.protection_decisions_are_not_auditable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            auditable=True,
            status="audited",
        )
        root.pending_events.append("DataProtectionApplied")
        root.pending_events.append("UnauditableProtectionDecisionRejected")
        root.history.append({"event": "DecisionAuditable"})
        return root

    def is_unauditable(self) -> bool:
        return not self.auditable


@dataclass(eq=False, kw_only=True)
class DsCompletePrivacyControlsRoot(AggregateRoot):
    tenant_id: str
    control_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def ensure(
        cls, *, tenant_id: str, control_ref: str, complete: bool = True
    ) -> DsCompletePrivacyControlsRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.protection.priv_tenant_required")
        if not complete:
            raise ValueError(
                "data_security.protection.privacy_controls_are_incomplete"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            control_ref=control_ref.strip(),
            complete=True,
            status="complete",
        )
        root.pending_events.append("MaskingApplied")
        root.pending_events.append("IncompletePrivacyControlsRejected")
        root.history.append({"event": "PrivacyControlsComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class DsEncryptionCompletedRoot(AggregateRoot):
    tenant_id: str
    asset_ref: str
    completed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def encrypt(
        cls, *, tenant_id: str, asset_ref: str, completed: bool = True
    ) -> DsEncryptionCompletedRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.protection.enc_tenant_required")
        if not completed:
            raise ValueError("data_security.protection.encryption_not_completed")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            asset_ref=asset_ref.strip(),
            completed=True,
            status="encrypted",
        )
        root.pending_events.append("EncryptionCompleted")
        root.history.append({"event": "EncryptionCompleted"})
        return root


@dataclass(eq=False, kw_only=True)
class DsProtectionViolationRoot(AggregateRoot):
    tenant_id: str
    violation_ref: str
    detected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, violation_ref: str, detected: bool = True
    ) -> DsProtectionViolationRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.protection.vio_tenant_required")
        if not detected:
            raise ValueError("data_security.protection.violation_not_detected")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            violation_ref=violation_ref.strip(),
            detected=True,
            status="detected",
        )
        root.pending_events.append("ProtectionViolationDetected")
        root.history.append({"event": "ViolationDetected"})
        return root
