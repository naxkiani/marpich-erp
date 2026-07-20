"""P209-H Workload Identity, SPIFFE/SPIRE & mTLS aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsWorkloadCryptoIdentityRoot(AggregateRoot):
    """Workloads must have cryptographic identity."""

    tenant_id: str
    workload_ref: str
    spiffe_id: str
    cryptographic: bool
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
        cryptographic: bool = True,
    ) -> SecretsWorkloadCryptoIdentityRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.workload.tenant_required")
        if not cryptographic or not spiffe_id.strip():
            raise ValueError(
                "secrets.workload.workloads_lack_cryptographic_identity"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            workload_ref=workload_ref.strip(),
            spiffe_id=spiffe_id.strip(),
            cryptographic=True,
            status="issued",
        )
        root.pending_events.append("IdentityIssued")
        root.pending_events.append("SpiffeIdIssued")
        root.pending_events.append("WorkloadRegistered")
        root.history.append({"event": "CryptoIdentityIssued"})
        return root

    def lacks_crypto(self) -> bool:
        return not self.cryptographic or not self.spiffe_id


@dataclass(eq=False, kw_only=True)
class SecretsWorkloadSecretlessRoot(AggregateRoot):
    """Static credentials must not be required."""

    tenant_id: str
    workload_ref: str
    secretless: bool
    static_required: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        workload_ref: str,
        secretless: bool = True,
        static_required: bool = False,
    ) -> SecretsWorkloadSecretlessRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.workload.sec_tenant_required")
        if static_required or not secretless:
            raise ValueError("secrets.workload.static_credentials_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            workload_ref=workload_ref.strip(),
            secretless=True,
            static_required=False,
            status="enabled",
        )
        root.pending_events.append("StaticCredentialBlocked")
        root.history.append({"event": "SecretlessEnabled"})
        return root

    def requires_static(self) -> bool:
        return self.static_required or not self.secretless


@dataclass(eq=False, kw_only=True)
class SecretsWorkloadMtlsEnforcementRoot(AggregateRoot):
    """mTLS must be enforceable."""

    tenant_id: str
    mesh_ref: str
    enforceable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls,
        *,
        tenant_id: str,
        mesh_ref: str,
        enforceable: bool = True,
    ) -> SecretsWorkloadMtlsEnforcementRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.workload.mtls_tenant_required")
        if not enforceable:
            raise ValueError("secrets.workload.mtls_cannot_be_enforced")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            mesh_ref=mesh_ref.strip(),
            enforceable=True,
            status="enforced",
        )
        root.pending_events.append("MtlsEnforced")
        root.history.append({"event": "MtlsEnforced"})
        return root

    def is_unenforceable(self) -> bool:
        return not self.enforceable


@dataclass(eq=False, kw_only=True)
class SecretsWorkloadAutoRotationRoot(AggregateRoot):
    """Certificate rotation must not be manual."""

    tenant_id: str
    identity_ref: str
    automatic: bool
    manual: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        identity_ref: str,
        automatic: bool = True,
        manual: bool = False,
    ) -> SecretsWorkloadAutoRotationRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.workload.rot_tenant_required")
        if manual or not automatic:
            raise ValueError("secrets.workload.certificate_rotation_manual")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            identity_ref=identity_ref.strip(),
            automatic=True,
            manual=False,
            status="enabled",
        )
        root.pending_events.append("IdentityRotated")
        root.pending_events.append("SvidRotated")
        root.history.append({"event": "AutoRotationEnabled"})
        return root

    def is_manual(self) -> bool:
        return self.manual or not self.automatic


@dataclass(eq=False, kw_only=True)
class SecretsWorkloadTrustDomainRoot(AggregateRoot):
    """Trust domains must be defined."""

    tenant_id: str
    trust_domain: str
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
        trust_domain: str,
        defined: bool = True,
    ) -> SecretsWorkloadTrustDomainRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.workload.td_tenant_required")
        if not defined or not trust_domain.strip():
            raise ValueError("secrets.workload.trust_domains_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            trust_domain=trust_domain.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("TrustDomainDefined")
        root.pending_events.append("TrustDomainFederated")
        root.history.append({"event": "TrustDomainDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined or not self.trust_domain


@dataclass(eq=False, kw_only=True)
class SecretsWorkloadOwnershipRoot(AggregateRoot):
    """Workload identity ownership must be known."""

    tenant_id: str
    workload_ref: str
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
        workload_ref: str,
        owner_ref: str,
        known: bool = True,
    ) -> SecretsWorkloadOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.workload.own_tenant_required")
        if not known or not owner_ref.strip():
            raise ValueError(
                "secrets.workload.workload_identity_ownership_unknown"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            workload_ref=workload_ref.strip(),
            owner_ref=owner_ref.strip(),
            known=True,
            status="bound",
        )
        root.pending_events.append("WorkloadOwnershipBound")
        root.history.append({"event": "WorkloadOwnershipBound"})
        return root

    def is_unknown(self) -> bool:
        return not self.known or not self.owner_ref


@dataclass(eq=False, kw_only=True)
class SecretsWorkloadCommAuditRoot(AggregateRoot):
    """Service communication must be audited."""

    tenant_id: str
    audit_ref: str
    connection_ref: str
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
        connection_ref: str,
        audited: bool = True,
    ) -> SecretsWorkloadCommAuditRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.workload.audit_tenant_required")
        if not audited:
            raise ValueError(
                "secrets.workload.service_communication_unaudited"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            audit_ref=audit_ref.strip(),
            connection_ref=connection_ref.strip(),
            audited=True,
            status="recorded",
        )
        root.pending_events.append("ServiceCommAudited")
        root.history.append({"event": "ServiceCommAudited"})
        return root

    def is_unaudited(self) -> bool:
        return not self.audited


@dataclass(eq=False, kw_only=True)
class SecretsWorkloadAttestationRoot(AggregateRoot):
    """Workload attestation via SPIRE."""

    tenant_id: str
    workload_ref: str
    attested: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def attest(
        cls,
        *,
        tenant_id: str,
        workload_ref: str,
        attested: bool = True,
    ) -> SecretsWorkloadAttestationRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.workload.att_tenant_required")
        if not attested:
            raise ValueError(
                "secrets.workload.workloads_lack_cryptographic_identity"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            workload_ref=workload_ref.strip(),
            attested=True,
            status="attested",
        )
        root.pending_events.append("WorkloadAttested")
        root.history.append({"event": "WorkloadAttested"})
        return root
