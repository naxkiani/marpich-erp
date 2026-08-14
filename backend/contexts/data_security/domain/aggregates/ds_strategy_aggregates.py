"""P211-A Data Security strategy aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class DsDiscoverableAssetRoot(AggregateRoot):
    tenant_id: str
    asset_ref: str
    discoverable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def register(
        cls, *, tenant_id: str, asset_ref: str, discoverable: bool = True
    ) -> DsDiscoverableAssetRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.strategy.tenant_required")
        if not discoverable:
            raise ValueError(
                "data_security.strategy.data_assets_cannot_be_discovered"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            asset_ref=asset_ref.strip(),
            discoverable=True,
            status="registered",
        )
        root.pending_events.append("DataAssetRegistered")
        root.pending_events.append("UndiscoverableAssetRejected")
        root.history.append({"event": "AssetDiscovered"})
        return root

    def is_undiscoverable(self) -> bool:
        return not self.discoverable


@dataclass(eq=False, kw_only=True)
class DsClassifiableDataRoot(AggregateRoot):
    tenant_id: str
    asset_ref: str
    classifiable: bool
    classification: str
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def classify(
        cls,
        *,
        tenant_id: str,
        asset_ref: str,
        classifiable: bool = True,
        classification: str = "confidential",
    ) -> DsClassifiableDataRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.strategy.class_tenant_required")
        if not classifiable:
            raise ValueError(
                "data_security.strategy.sensitive_data_cannot_be_classified"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            asset_ref=asset_ref.strip(),
            classifiable=True,
            classification=classification.strip(),
            status="classified",
        )
        root.pending_events.append("DataClassified")
        root.pending_events.append("UnclassifiableDataRejected")
        root.history.append({"event": "DataClassified"})
        return root

    def is_unclassifiable(self) -> bool:
        return not self.classifiable


@dataclass(eq=False, kw_only=True)
class DsMeasurablePrivacyRiskRoot(AggregateRoot):
    tenant_id: str
    risk_ref: str
    measurable: bool
    score: float
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def assess(
        cls,
        *,
        tenant_id: str,
        risk_ref: str,
        measurable: bool = True,
        score: float = 1.0,
    ) -> DsMeasurablePrivacyRiskRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.strategy.risk_tenant_required")
        if not measurable:
            raise ValueError(
                "data_security.strategy.privacy_risks_cannot_be_measured"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            risk_ref=risk_ref.strip(),
            measurable=True,
            score=float(score),
            status="assessed",
        )
        root.pending_events.append("DataRiskDetected")
        root.pending_events.append("UnmeasurablePrivacyRiskRejected")
        root.history.append({"event": "PrivacyRiskMeasured"})
        return root

    def is_unmeasurable(self) -> bool:
        return not self.measurable


@dataclass(eq=False, kw_only=True)
class DsGovernedAccessRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    governed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def govern(
        cls, *, tenant_id: str, policy_ref: str, governed: bool = True
    ) -> DsGovernedAccessRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.strategy.access_tenant_required")
        if not governed:
            raise ValueError(
                "data_security.strategy.data_access_cannot_be_governed"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            governed=True,
            status="governed",
        )
        root.pending_events.append("AccessReviewed")
        root.pending_events.append("UngovernedAccessRejected")
        root.history.append({"event": "AccessGoverned"})
        return root

    def is_ungoverned(self) -> bool:
        return not self.governed


@dataclass(eq=False, kw_only=True)
class DsProtectedAiDataRoot(AggregateRoot):
    tenant_id: str
    dataset_ref: str
    protected: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def protect(
        cls, *, tenant_id: str, dataset_ref: str, protected: bool = True
    ) -> DsProtectedAiDataRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.strategy.ai_tenant_required")
        if not protected:
            raise ValueError(
                "data_security.strategy.ai_data_cannot_be_protected"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            dataset_ref=dataset_ref.strip(),
            protected=True,
            status="protected",
        )
        root.pending_events.append("DataPolicyApplied")
        root.pending_events.append("UnprotectedAiDataRejected")
        root.history.append({"event": "AiDataProtected"})
        return root

    def is_unprotected(self) -> bool:
        return not self.protected


@dataclass(eq=False, kw_only=True)
class DsAvailableLineageRoot(AggregateRoot):
    tenant_id: str
    lineage_ref: str
    available: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, lineage_ref: str, available: bool = True
    ) -> DsAvailableLineageRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.strategy.lineage_tenant_required")
        if not available:
            raise ValueError(
                "data_security.strategy.data_lineage_is_unavailable"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            lineage_ref=lineage_ref.strip(),
            available=True,
            status="available",
        )
        root.pending_events.append("LineageDeclared")
        root.pending_events.append("UnavailableLineageRejected")
        root.history.append({"event": "LineageAvailable"})
        return root

    def is_unavailable(self) -> bool:
        return not self.available


@dataclass(eq=False, kw_only=True)
class DsComplianceEvidenceRoot(AggregateRoot):
    tenant_id: str
    evidence_ref: str
    generatable: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def generate(
        cls, *, tenant_id: str, evidence_ref: str, generatable: bool = True
    ) -> DsComplianceEvidenceRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.strategy.ev_tenant_required")
        if not generatable:
            raise ValueError(
                "data_security.strategy.compliance_evidence_cannot_be_generated"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            evidence_ref=evidence_ref.strip(),
            generatable=True,
            status="generated",
        )
        root.pending_events.append("ComplianceEvidenceGenerated")
        root.pending_events.append("UngeneratableEvidenceRejected")
        root.history.append({"event": "EvidenceGenerated"})
        return root

    def is_ungeneratable(self) -> bool:
        return not self.generatable


@dataclass(eq=False, kw_only=True)
class DsStrategyProfileRoot(AggregateRoot):
    tenant_id: str
    strategy_ref: str
    published: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, strategy_ref: str, published: bool = True
    ) -> DsStrategyProfileRoot:
        if not tenant_id.strip():
            raise ValueError("data_security.strategy.pub_tenant_required")
        if not published:
            raise ValueError("data_security.strategy.strategy_not_published")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            strategy_ref=strategy_ref.strip(),
            published=True,
            status="published",
        )
        root.pending_events.append("DataSecurityStrategyPublished")
        root.history.append({"event": "StrategyPublished"})
        return root
