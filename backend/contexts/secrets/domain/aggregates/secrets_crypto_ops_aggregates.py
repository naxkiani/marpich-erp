"""P209-I Enterprise Cryptography Services & Encryption aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsCryptoNoUnmanagedRoot(AggregateRoot):
    """Applications must not implement unmanaged cryptography."""

    tenant_id: str
    app_ref: str
    managed: bool
    unmanaged: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def bind(
        cls,
        *,
        tenant_id: str,
        app_ref: str,
        managed: bool = True,
        unmanaged: bool = False,
    ) -> SecretsCryptoNoUnmanagedRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.crypto.tenant_required")
        if unmanaged or not managed:
            raise ValueError(
                "secrets.crypto.applications_implement_unmanaged_cryptography"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            app_ref=app_ref.strip(),
            managed=True,
            unmanaged=False,
            status="bound",
        )
        root.pending_events.append("UnmanagedCryptoBlocked")
        root.pending_events.append("EaaSInvoked")
        root.history.append({"event": "ManagedCryptoBound"})
        return root

    def is_unmanaged(self) -> bool:
        return self.unmanaged or not self.managed


@dataclass(eq=False, kw_only=True)
class SecretsCryptoGovernedOpsRoot(AggregateRoot):
    """Encryption operations must not bypass governance."""

    tenant_id: str
    operation_ref: str
    governed: bool
    bypass: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def perform(
        cls,
        *,
        tenant_id: str,
        operation_ref: str,
        governed: bool = True,
        bypass: bool = False,
    ) -> SecretsCryptoGovernedOpsRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.crypto.gov_tenant_required")
        if bypass or not governed:
            raise ValueError(
                "secrets.crypto.encryption_operations_bypass_governance"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            operation_ref=operation_ref.strip(),
            governed=True,
            bypass=False,
            status="performed",
        )
        root.pending_events.append("EncryptionPerformed")
        root.pending_events.append("EncryptionGoverned")
        root.history.append({"event": "GovernedEncryption"})
        return root

    def bypasses_governance(self) -> bool:
        return self.bypass or not self.governed


@dataclass(eq=False, kw_only=True)
class SecretsCryptoNoKeyExposureRoot(AggregateRoot):
    """Keys must not be exposed."""

    tenant_id: str
    key_ref: str
    exposed: bool
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
        exposed: bool = False,
    ) -> SecretsCryptoNoKeyExposureRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.crypto.key_tenant_required")
        if exposed or not key_ref.strip():
            raise ValueError("secrets.crypto.keys_are_exposed")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            key_ref=key_ref.strip(),
            exposed=False,
            status="protected",
        )
        root.pending_events.append("KeyExposureRejected")
        root.history.append({"event": "KeyRefOnly"})
        return root

    def is_exposed(self) -> bool:
        return self.exposed or not self.key_ref


@dataclass(eq=False, kw_only=True)
class SecretsCryptoAlgorithmControlRoot(AggregateRoot):
    """Algorithms must be controlled."""

    tenant_id: str
    algorithm_ref: str
    controlled: bool
    approved: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def approve(
        cls,
        *,
        tenant_id: str,
        algorithm_ref: str,
        controlled: bool = True,
        approved: bool = True,
    ) -> SecretsCryptoAlgorithmControlRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.crypto.alg_tenant_required")
        if not controlled or not approved:
            raise ValueError("secrets.crypto.algorithms_are_uncontrolled")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            algorithm_ref=algorithm_ref.strip(),
            controlled=True,
            approved=True,
            status="approved",
        )
        root.pending_events.append("AlgorithmApproved")
        root.pending_events.append("CryptoPolicyChanged")
        root.history.append({"event": "AlgorithmControlled"})
        return root

    def is_uncontrolled(self) -> bool:
        return not self.controlled or not self.approved


@dataclass(eq=False, kw_only=True)
class SecretsCryptoSignatureVerifyRoot(AggregateRoot):
    """Signatures must be verifiable."""

    tenant_id: str
    signature_ref: str
    verifiable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def verify(
        cls,
        *,
        tenant_id: str,
        signature_ref: str,
        verifiable: bool = True,
    ) -> SecretsCryptoSignatureVerifyRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.crypto.sig_tenant_required")
        if not verifiable:
            raise ValueError("secrets.crypto.signatures_cannot_be_verified")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            signature_ref=signature_ref.strip(),
            verifiable=True,
            status="verified",
        )
        root.pending_events.append("SignatureVerified")
        root.pending_events.append("SignatureCreated")
        root.history.append({"event": "SignatureVerified"})
        return root

    def is_unverifiable(self) -> bool:
        return not self.verifiable


@dataclass(eq=False, kw_only=True)
class SecretsCryptoOpAuditRoot(AggregateRoot):
    """Cryptographic operations must have audit trails."""

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
    ) -> SecretsCryptoOpAuditRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.crypto.audit_tenant_required")
        if not audited:
            raise ValueError(
                "secrets.crypto.cryptographic_operations_lack_audit_trails"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            audit_ref=audit_ref.strip(),
            operation_ref=operation_ref.strip(),
            audited=True,
            status="recorded",
        )
        root.pending_events.append("CryptoOpAudited")
        root.history.append({"event": "CryptoOpAudited"})
        return root

    def lacks_audit(self) -> bool:
        return not self.audited


@dataclass(eq=False, kw_only=True)
class SecretsCryptoEncryptionPolicyRoot(AggregateRoot):
    """Encryption policy via Policy Engine."""

    tenant_id: str
    policy_ref: str
    applied: bool
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
        applied: bool = True,
    ) -> SecretsCryptoEncryptionPolicyRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.crypto.pol_tenant_required")
        if not applied:
            raise ValueError(
                "secrets.crypto.encryption_operations_bypass_governance"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            applied=True,
            status="applied",
        )
        root.pending_events.append("CryptoPolicyChanged")
        root.history.append({"event": "EncryptionPolicyApplied"})
        return root


@dataclass(eq=False, kw_only=True)
class SecretsCryptoEaaSRoot(AggregateRoot):
    """Encryption as a Service invocation."""

    tenant_id: str
    eaas_ref: str
    via_platform: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def invoke(
        cls,
        *,
        tenant_id: str,
        eaas_ref: str,
        via_platform: bool = True,
    ) -> SecretsCryptoEaaSRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.crypto.eaas_tenant_required")
        if not via_platform:
            raise ValueError(
                "secrets.crypto.applications_implement_unmanaged_cryptography"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            eaas_ref=eaas_ref.strip(),
            via_platform=True,
            status="invoked",
        )
        root.pending_events.append("EaaSInvoked")
        root.pending_events.append("EncryptionPerformed")
        root.history.append({"event": "EaaSInvoked"})
        return root
