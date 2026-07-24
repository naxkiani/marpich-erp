"""P209-D Enterprise PKI Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsPkiRootCaProtectionRoot(AggregateRoot):
    """Root CA keys must be protected (HSM / offline)."""

    tenant_id: str
    ca_ref: str
    hsm_protected: bool
    offline: bool
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
        hsm_protected: bool = True,
        offline: bool = True,
    ) -> SecretsPkiRootCaProtectionRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.pki.tenant_required")
        if not hsm_protected or not offline:
            raise ValueError("secrets.pki.root_ca_keys_not_protected")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ca_ref=ca_ref.strip(),
            hsm_protected=True,
            offline=True,
            status="hardened",
        )
        root.pending_events.append("RootCaHardened")
        root.history.append({"event": "RootCaHardened"})
        return root

    def is_unprotected(self) -> bool:
        return not self.hsm_protected or not self.offline


@dataclass(eq=False, kw_only=True)
class SecretsPkiCertLifecycleRoot(AggregateRoot):
    """Certificates must be automatically managed with complete lifecycle."""

    tenant_id: str
    cert_ref: str
    automatic: bool
    manual: bool
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
        cert_ref: str,
        automatic: bool = True,
        manual: bool = False,
        complete: bool = True,
    ) -> SecretsPkiCertLifecycleRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.pki.life_tenant_required")
        if manual or not automatic:
            raise ValueError("secrets.pki.certificates_manually_managed")
        if not complete:
            raise ValueError("secrets.pki.certificate_lifecycle_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            cert_ref=cert_ref.strip(),
            automatic=True,
            manual=False,
            complete=True,
            status="managed",
        )
        root.pending_events.append("CertificateIssued")
        root.history.append({"event": "CertLifecycleManaged"})
        return root

    def is_manual_or_incomplete(self) -> bool:
        return self.manual or not self.automatic or not self.complete


@dataclass(eq=False, kw_only=True)
class SecretsPkiRevocationRoot(AggregateRoot):
    """Revocation mechanisms must not be absent."""

    tenant_id: str
    revocation_ref: str
    ocsp: bool
    crl: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        revocation_ref: str,
        ocsp: bool = True,
        crl: bool = True,
    ) -> SecretsPkiRevocationRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.pki.rev_tenant_required")
        if not ocsp or not crl:
            raise ValueError("secrets.pki.revocation_mechanisms_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            revocation_ref=revocation_ref.strip(),
            ocsp=True,
            crl=True,
            status="enabled",
        )
        root.pending_events.append("CrlPublished")
        root.pending_events.append("OcspResponseServed")
        root.history.append({"event": "RevocationEnabled"})
        return root

    def is_absent(self) -> bool:
        return not self.ocsp or not self.crl


@dataclass(eq=False, kw_only=True)
class SecretsPkiTrustChainRoot(AggregateRoot):
    """Trust chains must be validatable."""

    tenant_id: str
    chain_ref: str
    validatable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def validate(
        cls,
        *,
        tenant_id: str,
        chain_ref: str,
        validatable: bool = True,
    ) -> SecretsPkiTrustChainRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.pki.chain_tenant_required")
        if not validatable:
            raise ValueError("secrets.pki.trust_chains_cannot_be_validated")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            chain_ref=chain_ref.strip(),
            validatable=True,
            status="validated",
        )
        root.pending_events.append("TrustChainValidated")
        root.history.append({"event": "TrustChainValidated"})
        return root

    def is_unvalidatable(self) -> bool:
        return not self.validatable


@dataclass(eq=False, kw_only=True)
class SecretsPkiOwnershipRoot(AggregateRoot):
    """Certificate ownership must be known."""

    tenant_id: str
    cert_ref: str
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
        cert_ref: str,
        owner_ref: str,
        known: bool = True,
    ) -> SecretsPkiOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.pki.own_tenant_required")
        if not known or not owner_ref.strip():
            raise ValueError("secrets.pki.certificate_ownership_unknown")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            cert_ref=cert_ref.strip(),
            owner_ref=owner_ref.strip(),
            known=True,
            status="bound",
        )
        root.pending_events.append("CertificateOwnershipBound")
        root.history.append({"event": "CertificateOwnershipBound"})
        return root

    def is_unknown(self) -> bool:
        return not self.known or not self.owner_ref


@dataclass(eq=False, kw_only=True)
class SecretsPkiAuditEvidenceRoot(AggregateRoot):
    """Audit evidence must be available."""

    tenant_id: str
    evidence_ref: str
    action_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        evidence_ref: str,
        action_ref: str,
        available: bool = True,
    ) -> SecretsPkiAuditEvidenceRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.pki.audit_tenant_required")
        if not available:
            raise ValueError("secrets.pki.audit_evidence_unavailable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            evidence_ref=evidence_ref.strip(),
            action_ref=action_ref.strip(),
            available=True,
            status="recorded",
        )
        root.pending_events.append("PkiAuditRecorded")
        root.history.append({"event": "PkiAuditRecorded"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class SecretsPkiIssuingCaRoot(AggregateRoot):
    """Issuing CA under automated PKI."""

    tenant_id: str
    ca_ref: str
    automated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def activate(
        cls,
        *,
        tenant_id: str,
        ca_ref: str,
        automated: bool = True,
    ) -> SecretsPkiIssuingCaRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.pki.issuing_tenant_required")
        if not automated:
            raise ValueError("secrets.pki.certificates_manually_managed")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ca_ref=ca_ref.strip(),
            automated=True,
            status="active",
        )
        root.pending_events.append("CertificateIssued")
        root.history.append({"event": "IssuingCaActivated"})
        return root


@dataclass(eq=False, kw_only=True)
class SecretsPkiRaWorkflowRoot(AggregateRoot):
    """RA approval via Workflow — not local BPM."""

    tenant_id: str
    request_ref: str
    via_workflow: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def submit(
        cls,
        *,
        tenant_id: str,
        request_ref: str,
        via_workflow: bool = True,
    ) -> SecretsPkiRaWorkflowRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.pki.ra_tenant_required")
        if not via_workflow:
            raise ValueError("secrets.pki.certificates_manually_managed")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            request_ref=request_ref.strip(),
            via_workflow=True,
            status="submitted",
        )
        root.pending_events.append("CertificateRequested")
        root.pending_events.append("CertificateApproved")
        root.history.append({"event": "RaWorkflowSubmitted"})
        return root
