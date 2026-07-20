"""P209-J Digital Signature, Code Signing & Supply Chain aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsSigningArtifactSignedRoot(AggregateRoot):
    """Software artifacts must not be unsigned."""

    tenant_id: str
    artifact_ref: str
    signed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def sign(
        cls,
        *,
        tenant_id: str,
        artifact_ref: str,
        signed: bool = True,
    ) -> SecretsSigningArtifactSignedRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.signing.tenant_required")
        if not signed:
            raise ValueError("secrets.signing.software_artifacts_are_unsigned")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            artifact_ref=artifact_ref.strip(),
            signed=True,
            status="signed",
        )
        root.pending_events.append("ArtifactSigned")
        root.pending_events.append("UnsignedArtifactBlocked")
        root.history.append({"event": "ArtifactSigned"})
        return root

    def is_unsigned(self) -> bool:
        return not self.signed


@dataclass(eq=False, kw_only=True)
class SecretsSigningKeyManagedRoot(AggregateRoot):
    """Signing keys must not be unmanaged."""

    tenant_id: str
    key_ref: str
    managed: bool
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
        managed: bool = True,
    ) -> SecretsSigningKeyManagedRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.signing.key_tenant_required")
        if not managed or not key_ref.strip():
            raise ValueError("secrets.signing.signing_keys_are_unmanaged")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            key_ref=key_ref.strip(),
            managed=True,
            status="managed",
        )
        root.pending_events.append("SigningKeyManaged")
        root.history.append({"event": "SigningKeyManaged"})
        return root

    def is_unmanaged(self) -> bool:
        return not self.managed or not self.key_ref


@dataclass(eq=False, kw_only=True)
class SecretsSigningProvenanceRoot(AggregateRoot):
    """Supply chain provenance must be available."""

    tenant_id: str
    provenance_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def validate(
        cls,
        *,
        tenant_id: str,
        provenance_ref: str,
        available: bool = True,
    ) -> SecretsSigningProvenanceRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.signing.prov_tenant_required")
        if not available:
            raise ValueError(
                "secrets.signing.supply_chain_provenance_unavailable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            provenance_ref=provenance_ref.strip(),
            available=True,
            status="validated",
        )
        root.pending_events.append("ProvenanceValidated")
        root.history.append({"event": "ProvenanceValidated"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class SecretsSigningSbomVerifyRoot(AggregateRoot):
    """SBOM verification must not be absent."""

    tenant_id: str
    sbom_ref: str
    verified: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def verify(
        cls,
        *,
        tenant_id: str,
        sbom_ref: str,
        verified: bool = True,
    ) -> SecretsSigningSbomVerifyRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.signing.sbom_tenant_required")
        if not verified:
            raise ValueError("secrets.signing.sbom_verification_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            sbom_ref=sbom_ref.strip(),
            verified=True,
            status="verified",
        )
        root.pending_events.append("SbomVerified")
        root.history.append({"event": "SbomVerified"})
        return root

    def is_absent(self) -> bool:
        return not self.verified


@dataclass(eq=False, kw_only=True)
class SecretsSigningDeploymentTrustRoot(AggregateRoot):
    """Deployment trust must be validatable."""

    tenant_id: str
    deployment_ref: str
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
        deployment_ref: str,
        validatable: bool = True,
    ) -> SecretsSigningDeploymentTrustRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.signing.dep_tenant_required")
        if not validatable:
            raise ValueError(
                "secrets.signing.deployment_trust_cannot_be_validated"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            deployment_ref=deployment_ref.strip(),
            validatable=True,
            status="validated",
        )
        root.pending_events.append("DeploymentTrustValidated")
        root.pending_events.append("ReleaseApproved")
        root.history.append({"event": "DeploymentTrustValidated"})
        return root

    def is_unvalidatable(self) -> bool:
        return not self.validatable


@dataclass(eq=False, kw_only=True)
class SecretsSigningOwnershipRoot(AggregateRoot):
    """Artifact ownership must be known."""

    tenant_id: str
    artifact_ref: str
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
        artifact_ref: str,
        owner_ref: str,
        known: bool = True,
    ) -> SecretsSigningOwnershipRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.signing.own_tenant_required")
        if not known or not owner_ref.strip():
            raise ValueError("secrets.signing.artifact_ownership_unknown")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            artifact_ref=artifact_ref.strip(),
            owner_ref=owner_ref.strip(),
            known=True,
            status="bound",
        )
        root.pending_events.append("ArtifactOwnershipBound")
        root.history.append({"event": "ArtifactOwnershipBound"})
        return root

    def is_unknown(self) -> bool:
        return not self.known or not self.owner_ref


@dataclass(eq=False, kw_only=True)
class SecretsSigningOpAuditRoot(AggregateRoot):
    """Signature operations must be audited."""

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
    ) -> SecretsSigningOpAuditRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.signing.audit_tenant_required")
        if not audited:
            raise ValueError("secrets.signing.signature_operations_unaudited")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            audit_ref=audit_ref.strip(),
            operation_ref=operation_ref.strip(),
            audited=True,
            status="recorded",
        )
        root.pending_events.append("SignatureOpAudited")
        root.pending_events.append("SignatureVerified")
        root.history.append({"event": "SignatureOpAudited"})
        return root

    def is_unaudited(self) -> bool:
        return not self.audited


@dataclass(eq=False, kw_only=True)
class SecretsSigningReleaseGateRoot(AggregateRoot):
    """Release approval via Workflow."""

    tenant_id: str
    release_ref: str
    via_workflow: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def approve(
        cls,
        *,
        tenant_id: str,
        release_ref: str,
        via_workflow: bool = True,
    ) -> SecretsSigningReleaseGateRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.signing.rel_tenant_required")
        if not via_workflow:
            raise ValueError(
                "secrets.signing.deployment_trust_cannot_be_validated"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            release_ref=release_ref.strip(),
            via_workflow=True,
            status="approved",
        )
        root.pending_events.append("SigningRequested")
        root.pending_events.append("ReleaseApproved")
        root.history.append({"event": "ReleaseApproved"})
        return root
