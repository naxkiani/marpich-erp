"""P209-E Enterprise Certificate Authority & Trust Chain aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsCaRootProtectionRoot(AggregateRoot):
    """Root CA must not be online without protection."""

    tenant_id: str
    ca_ref: str
    offline: bool
    protected: bool
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
        protected: bool = True,
    ) -> SecretsCaRootProtectionRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ca.tenant_required")
        if not offline or not protected:
            raise ValueError("secrets.ca.root_ca_online_without_protection")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ca_ref=ca_ref.strip(),
            offline=True,
            protected=True,
            status="hardened",
        )
        root.pending_events.append("RootCaHardened")
        root.history.append({"event": "RootCaHardened"})
        return root

    def is_online_unprotected(self) -> bool:
        return not self.offline or not self.protected


@dataclass(eq=False, kw_only=True)
class SecretsCaPrivateKeyHsmRoot(AggregateRoot):
    """CA private keys must be HSM protected."""

    tenant_id: str
    ca_ref: str
    hsm_protected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def protect(
        cls,
        *,
        tenant_id: str,
        ca_ref: str,
        hsm_protected: bool = True,
    ) -> SecretsCaPrivateKeyHsmRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ca.hsm_tenant_required")
        if not hsm_protected:
            raise ValueError("secrets.ca.ca_private_keys_lack_hsm_protection")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ca_ref=ca_ref.strip(),
            hsm_protected=True,
            status="protected",
        )
        root.pending_events.append("RootCACreated")
        root.history.append({"event": "CaPrivateKeyHsmProtected"})
        return root

    def lacks_hsm(self) -> bool:
        return not self.hsm_protected


@dataclass(eq=False, kw_only=True)
class SecretsCaTrustChainRoot(AggregateRoot):
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
    ) -> SecretsCaTrustChainRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ca.chain_tenant_required")
        if not validatable:
            raise ValueError("secrets.ca.trust_chains_cannot_be_validated")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            chain_ref=chain_ref.strip(),
            validatable=True,
            status="validated",
        )
        root.pending_events.append("TrustChainValidated")
        root.pending_events.append("TrustChainChanged")
        root.history.append({"event": "TrustChainValidated"})
        return root

    def is_unvalidatable(self) -> bool:
        return not self.validatable


@dataclass(eq=False, kw_only=True)
class SecretsCaRevocationRoot(AggregateRoot):
    """Certificate revocation must be available."""

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
    ) -> SecretsCaRevocationRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ca.rev_tenant_required")
        if not ocsp or not crl:
            raise ValueError("secrets.ca.certificate_revocation_unavailable")
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
        root.pending_events.append("CertificateRevoked")
        root.history.append({"event": "RevocationEnabled"})
        return root

    def is_unavailable(self) -> bool:
        return not self.ocsp or not self.crl


@dataclass(eq=False, kw_only=True)
class SecretsCaOwnershipRoot(AggregateRoot):
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
    ) -> SecretsCaOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ca.own_tenant_required")
        if not known or not owner_ref.strip():
            raise ValueError("secrets.ca.certificate_ownership_unknown")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            cert_ref=cert_ref.strip(),
            owner_ref=owner_ref.strip(),
            known=True,
            status="bound",
        )
        root.pending_events.append("CertificateIssued")
        root.history.append({"event": "CertificateOwnershipBound"})
        return root

    def is_unknown(self) -> bool:
        return not self.known or not self.owner_ref


@dataclass(eq=False, kw_only=True)
class SecretsCaGovernanceRoot(AggregateRoot):
    """CA governance must be defined."""

    tenant_id: str
    governance_ref: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        governance_ref: str,
        defined: bool = True,
    ) -> SecretsCaGovernanceRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ca.gov_tenant_required")
        if not defined:
            raise ValueError("secrets.ca.ca_governance_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            governance_ref=governance_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("CaGovernanceDefined")
        root.history.append({"event": "CaGovernanceDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class SecretsCaAuditTrailRoot(AggregateRoot):
    """CA audit trail must be complete."""

    tenant_id: str
    audit_ref: str
    action_ref: str
    complete: bool
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
        complete: bool = True,
    ) -> SecretsCaAuditTrailRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ca.audit_tenant_required")
        if not complete:
            raise ValueError("secrets.ca.audit_trail_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            audit_ref=audit_ref.strip(),
            action_ref=action_ref.strip(),
            complete=True,
            status="recorded",
        )
        root.pending_events.append("CaAuditRecorded")
        root.history.append({"event": "CaAuditRecorded"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class SecretsCaKeyCeremonyRoot(AggregateRoot):
    """Root CA key ceremony with dual control."""

    tenant_id: str
    ceremony_ref: str
    dual_control: bool
    multi_person: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def complete(
        cls,
        *,
        tenant_id: str,
        ceremony_ref: str,
        dual_control: bool = True,
        multi_person: bool = True,
    ) -> SecretsCaKeyCeremonyRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.ca.ceremony_tenant_required")
        if not dual_control or not multi_person:
            raise ValueError("secrets.ca.root_ca_online_without_protection")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ceremony_ref=ceremony_ref.strip(),
            dual_control=True,
            multi_person=True,
            status="completed",
        )
        root.pending_events.append("CaKeyCeremonyCompleted")
        root.pending_events.append("TrustAnchorPublished")
        root.history.append({"event": "CaKeyCeremonyCompleted"})
        return root
