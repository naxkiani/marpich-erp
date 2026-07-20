"""P209-K AI Cryptography, HSM, Confidential Computing & PQC aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SecretsHsmCryptoAgilityRoot(AggregateRoot):
    """Cryptographic algorithms must be able to evolve."""

    tenant_id: str
    algorithm_ref: str
    can_evolve: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls,
        *,
        tenant_id: str,
        algorithm_ref: str,
        can_evolve: bool = True,
    ) -> SecretsHsmCryptoAgilityRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.hsm.tenant_required")
        if not can_evolve:
            raise ValueError(
                "secrets.hsm.cryptographic_algorithms_cannot_evolve"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            algorithm_ref=algorithm_ref.strip(),
            can_evolve=True,
            status="enabled",
        )
        root.pending_events.append("CryptoAgilityVerified")
        root.pending_events.append("AlgorithmDeprecated")
        root.history.append({"event": "CryptoAgilityEnabled"})
        return root

    def cannot_evolve(self) -> bool:
        return not self.can_evolve


@dataclass(eq=False, kw_only=True)
class SecretsHsmProtectionRoot(AggregateRoot):
    """HSM protection must not be absent."""

    tenant_id: str
    hsm_ref: str
    protected: bool
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
        protected: bool = True,
    ) -> SecretsHsmProtectionRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.hsm.prot_tenant_required")
        if not protected:
            raise ValueError("secrets.hsm.hsm_protection_is_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            hsm_ref=hsm_ref.strip(),
            protected=True,
            status="verified",
        )
        root.pending_events.append("HsmProtectionVerified")
        root.history.append({"event": "HsmProtectionVerified"})
        return root

    def is_absent(self) -> bool:
        return not self.protected


@dataclass(eq=False, kw_only=True)
class SecretsHsmAiDecisionAuditRoot(AggregateRoot):
    """AI cryptographic decisions must be auditable."""

    tenant_id: str
    decision_ref: str
    auditable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        decision_ref: str,
        auditable: bool = True,
    ) -> SecretsHsmAiDecisionAuditRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.hsm.ai_tenant_required")
        if not auditable:
            raise ValueError(
                "secrets.hsm.ai_cryptographic_decisions_unauditable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            decision_ref=decision_ref.strip(),
            auditable=True,
            status="recorded",
        )
        root.pending_events.append("AiCryptoDecisionAudited")
        root.history.append({"event": "AiCryptoDecisionAudited"})
        return root

    def is_unauditable(self) -> bool:
        return not self.auditable


@dataclass(eq=False, kw_only=True)
class SecretsHsmConfidentialAttestRoot(AggregateRoot):
    """Confidential workloads must have attestation."""

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
    ) -> SecretsHsmConfidentialAttestRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.hsm.cc_tenant_required")
        if not attested:
            raise ValueError(
                "secrets.hsm.confidential_workloads_lack_attestation"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            workload_ref=workload_ref.strip(),
            attested=True,
            status="attested",
        )
        root.pending_events.append("ConfidentialWorkloadAttested")
        root.pending_events.append("AttestationValidated")
        root.history.append({"event": "ConfidentialWorkloadAttested"})
        return root

    def lacks_attestation(self) -> bool:
        return not self.attested


@dataclass(eq=False, kw_only=True)
class SecretsHsmPqcMigrationRoot(AggregateRoot):
    """PQC migration strategy must be defined."""

    tenant_id: str
    strategy_ref: str
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
        strategy_ref: str,
        defined: bool = True,
    ) -> SecretsHsmPqcMigrationRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.hsm.pqc_tenant_required")
        if not defined:
            raise ValueError("secrets.hsm.pqc_migration_strategy_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            strategy_ref=strategy_ref.strip(),
            defined=True,
            status="defined",
        )
        root.pending_events.append("PqcStrategyDefined")
        root.pending_events.append("PQCTransitionStarted")
        root.history.append({"event": "PqcStrategyDefined"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined


@dataclass(eq=False, kw_only=True)
class SecretsHsmHardwareTrustRoot(AggregateRoot):
    """Hardware trust must be validated."""

    tenant_id: str
    hardware_ref: str
    validated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def validate(
        cls,
        *,
        tenant_id: str,
        hardware_ref: str,
        validated: bool = True,
    ) -> SecretsHsmHardwareTrustRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.hsm.hw_tenant_required")
        if not validated:
            raise ValueError("secrets.hsm.hardware_trust_not_validated")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            hardware_ref=hardware_ref.strip(),
            validated=True,
            status="validated",
        )
        root.pending_events.append("HardwareTrustValidated")
        root.history.append({"event": "HardwareTrustValidated"})
        return root

    def is_unvalidated(self) -> bool:
        return not self.validated


@dataclass(eq=False, kw_only=True)
class SecretsHsmRiskMeasurableRoot(AggregateRoot):
    """Cryptographic risks must be measurable."""

    tenant_id: str
    risk_ref: str
    measurable: bool
    score: float
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def measure(
        cls,
        *,
        tenant_id: str,
        risk_ref: str,
        measurable: bool = True,
        score: float = 0.0,
    ) -> SecretsHsmRiskMeasurableRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.hsm.risk_tenant_required")
        if not measurable:
            raise ValueError("secrets.hsm.cryptographic_risks_not_measurable")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            risk_ref=risk_ref.strip(),
            measurable=True,
            score=score,
            status="measured",
        )
        root.pending_events.append("CryptoRiskMeasured")
        root.pending_events.append("CryptoRiskDetected")
        root.history.append({"event": "CryptoRiskMeasured"})
        return root

    def is_unmeasurable(self) -> bool:
        return not self.measurable


@dataclass(eq=False, kw_only=True)
class SecretsHsmDualControlRoot(AggregateRoot):
    """HSM dual control / multi-person authorization."""

    tenant_id: str
    ceremony_ref: str
    dual_control: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enforce(
        cls,
        *,
        tenant_id: str,
        ceremony_ref: str,
        dual_control: bool = True,
    ) -> SecretsHsmDualControlRoot:
        if not tenant_id.strip():
            raise ValueError("secrets.hsm.dual_tenant_required")
        if not dual_control:
            raise ValueError("secrets.hsm.hsm_protection_is_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            ceremony_ref=ceremony_ref.strip(),
            dual_control=True,
            status="enforced",
        )
        root.pending_events.append("DualControlEnforced")
        root.pending_events.append("CryptoPolicyUpdated")
        root.history.append({"event": "DualControlEnforced"})
        return root
