"""P209 Cryptographic Trust Fabric aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsMaterialRoot(AggregateRoot):
    """Secrets must never be stored in plaintext."""

    tenant_id: str
    secret_ref: str
    encrypted: bool
    plaintext: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        secret_ref: str,
        encrypted: bool = True,
        plaintext: bool = False,
    ) -> SecretsMaterialRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.tenant_required")
        if plaintext or not encrypted:
            raise ValueError("secrets.secrets_stored_in_plaintext")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            secret_ref=secret_ref.strip(),
            encrypted=True,
            plaintext=False,
            status="created",
        )
        root.pending_events.append("SecretCreated")
        root.history.append({"event": "SecretMaterialCreated"})
        return root

    def is_plaintext(self) -> bool:
        return self.plaintext or not self.encrypted


@dataclass(eq=False, kw_only=True)
class SecretsKeyLifecycleRoot(AggregateRoot):
    """Keys must follow governed lifecycle."""

    tenant_id: str
    key_ref: str
    governed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        key_ref: str,
        governed: bool = True,
    ) -> SecretsKeyLifecycleRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.key_tenant_required")
        if not governed:
            raise ValueError("secrets.keys_outside_governed_lifecycle")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            key_ref=key_ref.strip(),
            governed=True,
            status="active",
        )
        root.pending_events.append("KeyCreated")
        root.history.append({"event": "KeyLifecycleCreated"})
        return root

    def rotate(self) -> None:
        if not self.governed:
            raise ValueError("secrets.keys_outside_governed_lifecycle")
        self.status = "rotated"
        self.pending_events.append("KeyRotated")
        self.history.append({"event": "KeyRotated"})

    def is_ungoverned(self) -> bool:
        return not self.governed


@dataclass(eq=False, kw_only=True)
class SecretsCertificateRoot(AggregateRoot):
    """Certificates must be automatically managed — never manual-only."""

    tenant_id: str
    certificate_ref: str
    automatic: bool
    manual: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def issue(
        cls,
        *,
        tenant_id: str,
        certificate_ref: str,
        automatic: bool = True,
        manual: bool = False,
    ) -> SecretsCertificateRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.cert_tenant_required")
        if manual or not automatic:
            raise ValueError("secrets.certificates_manually_managed")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            certificate_ref=certificate_ref.strip(),
            automatic=True,
            manual=False,
            status="issued",
        )
        root.pending_events.append("CertificateIssued")
        root.history.append({"event": "CertificateIssued"})
        return root

    def is_manual(self) -> bool:
        return self.manual or not self.automatic


@dataclass(eq=False, kw_only=True)
class SecretsHsmBindingRoot(AggregateRoot):
    """HSM integration must not be absent."""

    tenant_id: str
    binding_ref: str
    hsm_bound: bool
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
        hsm_bound: bool = True,
    ) -> SecretsHsmBindingRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.hsm_tenant_required")
        if not hsm_bound:
            raise ValueError("secrets.hsm_integration_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            binding_ref=binding_ref.strip(),
            hsm_bound=True,
            status="bound",
        )
        root.pending_events.append("HsmOperationCompleted")
        root.history.append({"event": "HsmBound"})
        return root

    def is_absent(self) -> bool:
        return not self.hsm_bound


@dataclass(eq=False, kw_only=True)
class SecretsCryptoAgilityRoot(AggregateRoot):
    """Cryptographic agility must be supported."""

    tenant_id: str
    agility_ref: str
    supported: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        agility_ref: str,
        supported: bool = True,
    ) -> SecretsCryptoAgilityRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.agility_tenant_required")
        if not supported:
            raise ValueError("secrets.cryptographic_agility_unsupported")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            agility_ref=agility_ref.strip(),
            supported=True,
            status="enabled",
        )
        root.pending_events.append("CryptoAgilityMigrated")
        root.history.append({"event": "CryptoAgilityEnabled"})
        return root

    def is_unsupported(self) -> bool:
        return not self.supported


@dataclass(eq=False, kw_only=True)
class SecretsWorkloadIdentityRoot(AggregateRoot):
    """Workload identities must be verifiable (SPIFFE/SPIRE)."""

    tenant_id: str
    workload_ref: str
    verifiable: bool
    spiffe_id: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def issue(
        cls,
        *,
        tenant_id: str,
        workload_ref: str,
        spiffe_id: str,
        verifiable: bool = True,
    ) -> SecretsWorkloadIdentityRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.workload_tenant_required")
        if not verifiable or not spiffe_id.strip():
            raise ValueError("secrets.workload_identities_unverifiable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            workload_ref=workload_ref.strip(),
            verifiable=True,
            spiffe_id=spiffe_id.strip(),
            status="issued",
        )
        root.pending_events.append("WorkloadIdentityIssued")
        root.history.append({"event": "WorkloadIdentityIssued"})
        return root

    def is_unverifiable(self) -> bool:
        return not self.verifiable or not self.spiffe_id


@dataclass(eq=False, kw_only=True)
class SecretsTrustAuditRoot(AggregateRoot):
    """Trust relationships must be auditable."""

    tenant_id: str
    trust_ref: str
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
        trust_ref: str,
        audited: bool = True,
    ) -> SecretsTrustAuditRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.trust_tenant_required")
        if not audited:
            raise ValueError("secrets.trust_relationships_unauditable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            trust_ref=trust_ref.strip(),
            audited=True,
            status="recorded",
        )
        root.pending_events.append("TrustRelationshipAudited")
        root.history.append({"event": "TrustAudited"})
        return root

    def is_unauditable(self) -> bool:
        return not self.audited


@dataclass(eq=False, kw_only=True)
class SecretsEnvelopeRoot(AggregateRoot):
    """Envelope encryption (DEK wrapped by KEK)."""

    tenant_id: str
    envelope_ref: str
    dek_ref: str
    kek_ref: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def wrap(
        cls,
        *,
        tenant_id: str,
        envelope_ref: str,
        dek_ref: str,
        kek_ref: str,
    ) -> SecretsEnvelopeRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.envelope_tenant_required")
        if not dek_ref.strip() or not kek_ref.strip():
            raise ValueError("secrets.keys_outside_governed_lifecycle")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            envelope_ref=envelope_ref.strip(),
            dek_ref=dek_ref.strip(),
            kek_ref=kek_ref.strip(),
            status="wrapped",
        )
        root.history.append({"event": "EnvelopeWrapped"})
        return root
