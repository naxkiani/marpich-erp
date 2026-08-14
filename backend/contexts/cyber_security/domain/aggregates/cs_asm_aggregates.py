"""P210-I ASM/CTEM aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class CsAsmAssetDiscoveryCompleteRoot(AggregateRoot):
    tenant_id: str
    discovery_ref: str
    complete: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def discover(
        cls, *, tenant_id: str, discovery_ref: str, complete: bool = True
    ) -> CsAsmAssetDiscoveryCompleteRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.asm.tenant_required")
        if not complete:
            raise ValueError("cyber_security.asm.asset_discovery_incomplete")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            discovery_ref=discovery_ref.strip(),
            complete=True,
            status="discovered",
        )
        root.pending_events.append("AssetDiscovered")
        root.pending_events.append("IncompleteDiscoveryRejected")
        root.history.append({"event": "AssetDiscoveryComplete"})
        return root

    def is_incomplete(self) -> bool:
        return not self.complete


@dataclass(eq=False, kw_only=True)
class CsAsmExternalSurfaceContinuousRoot(AggregateRoot):
    tenant_id: str
    surface_ref: str
    continuous: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def monitor(
        cls, *, tenant_id: str, surface_ref: str, continuous: bool = True
    ) -> CsAsmExternalSurfaceContinuousRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.asm.easm_tenant_required")
        if not continuous:
            raise ValueError(
                "cyber_security.asm.external_attack_surface_not_continuously_monitored"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            surface_ref=surface_ref.strip(),
            continuous=True,
            status="monitoring",
        )
        root.pending_events.append("NonContinuousEasmRejected")
        root.history.append({"event": "ExternalSurfaceContinuous"})
        return root

    def is_not_continuous(self) -> bool:
        return not self.continuous


@dataclass(eq=False, kw_only=True)
class CsAsmBusinessContextRiskRoot(AggregateRoot):
    tenant_id: str
    risk_ref: str
    business_context: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def calculate(
        cls,
        *,
        tenant_id: str,
        risk_ref: str,
        business_context: bool = True,
    ) -> CsAsmBusinessContextRiskRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.asm.risk_tenant_required")
        if not business_context:
            raise ValueError(
                "cyber_security.asm.risk_prioritization_ignores_business_context"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            risk_ref=risk_ref.strip(),
            business_context=True,
            status="calculated",
        )
        root.pending_events.append("RiskCalculated")
        root.pending_events.append("ContextlessRiskRejected")
        root.history.append({"event": "BusinessContextRiskCalculated"})
        return root

    def ignores_business_context(self) -> bool:
        return not self.business_context


@dataclass(eq=False, kw_only=True)
class CsAsmAttackPathRoot(AggregateRoot):
    tenant_id: str
    path_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def generate(
        cls, *, tenant_id: str, path_ref: str, present: bool = True
    ) -> CsAsmAttackPathRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.asm.path_tenant_required")
        if not present:
            raise ValueError("cyber_security.asm.attack_path_analysis_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            path_ref=path_ref.strip(),
            present=True,
            status="generated",
        )
        root.pending_events.append("AttackPathGenerated")
        root.pending_events.append("AbsentAttackPathRejected")
        root.history.append({"event": "AttackPathGenerated"})
        return root

    def is_absent(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class CsAsmExplainableAiRoot(AggregateRoot):
    tenant_id: str
    advisory_ref: str
    explainable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def advise(
        cls, *, tenant_id: str, advisory_ref: str, explainable: bool = True
    ) -> CsAsmExplainableAiRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.asm.ai_tenant_required")
        if not explainable:
            raise ValueError(
                "cyber_security.asm.ai_recommendations_not_explainable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            advisory_ref=advisory_ref.strip(),
            explainable=True,
            status="advised",
        )
        root.pending_events.append("UnexplainableAiRejected")
        root.history.append({"event": "ExplainableAiAdvisory"})
        return root

    def is_unexplainable(self) -> bool:
        return not self.explainable


@dataclass(eq=False, kw_only=True)
class CsAsmValidatedRemediationRoot(AggregateRoot):
    tenant_id: str
    remediation_ref: str
    validated: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def execute(
        cls,
        *,
        tenant_id: str,
        remediation_ref: str,
        validated: bool = True,
    ) -> CsAsmValidatedRemediationRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.asm.rem_tenant_required")
        if not validated:
            raise ValueError(
                "cyber_security.asm.remediation_cannot_be_validated"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            remediation_ref=remediation_ref.strip(),
            validated=True,
            status="completed",
        )
        root.pending_events.append("RemediationCompleted")
        root.pending_events.append("UnvalidatedRemediationRejected")
        root.history.append({"event": "RemediationValidated"})
        return root

    def cannot_be_validated(self) -> bool:
        return not self.validated


@dataclass(eq=False, kw_only=True)
class CsAsmContinuousCtemRoot(AggregateRoot):
    tenant_id: str
    cycle_ref: str
    continuous: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def run(
        cls, *, tenant_id: str, cycle_ref: str, continuous: bool = True
    ) -> CsAsmContinuousCtemRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.asm.ctem_tenant_required")
        if not continuous:
            raise ValueError(
                "cyber_security.asm.ctem_lifecycle_not_continuous"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            cycle_ref=cycle_ref.strip(),
            continuous=True,
            status="cycling",
        )
        root.pending_events.append("OnePassCtemRejected")
        root.history.append({"event": "ContinuousCtemCycle"})
        return root

    def is_not_continuous(self) -> bool:
        return not self.continuous


@dataclass(eq=False, kw_only=True)
class CsAsmExposureDetectedRoot(AggregateRoot):
    tenant_id: str
    exposure_ref: str
    asset_ref: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def detect(
        cls, *, tenant_id: str, exposure_ref: str, asset_ref: str
    ) -> CsAsmExposureDetectedRoot:
        if not tenant_id.strip():
            raise ValueError("cyber_security.asm.exp_tenant_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            exposure_ref=exposure_ref.strip(),
            asset_ref=asset_ref.strip(),
            status="detected",
        )
        root.pending_events.append("ExposureDetected")
        root.pending_events.append("VulnerabilityImported")
        root.history.append({"event": "ExposureDetected"})
        return root
