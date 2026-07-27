"""P212-O QA aggregates — quality-gate invariants."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


def _tid(tenant_id: str, code: str) -> str:
    if not tenant_id.strip():
        raise ValueError(code)
    return tenant_id.strip()


@dataclass(eq=False, kw_only=True)
class DgQaTestingRoot(AggregateRoot):
    tenant_id: str
    testing_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def publish(
        cls, *, tenant_id: str, testing_ref: str, present: bool = True
    ) -> "DgQaTestingRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_0_required")
        if not present:
            raise ValueError(
                "data_governance.qa.complete_enterprise_testing_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            testing_ref=testing_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("ValidationStartedEvent")
        root.history.append({"event": "DgQaTestingRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQaGovernanceRoot(AggregateRoot):
    tenant_id: str
    gov_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, gov_ref: str, present: bool = True
    ) -> "DgQaGovernanceRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_1_required")
        if not present:
            raise ValueError(
                "data_governance.qa.governance_validation_platform_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            gov_ref=gov_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("GovernanceApprovedEvent")
        root.history.append({"event": "DgQaGovernanceRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQaComplianceRoot(AggregateRoot):
    tenant_id: str
    compliance_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, compliance_ref: str, present: bool = True
    ) -> "DgQaComplianceRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_2_required")
        if not present:
            raise ValueError(
                "data_governance.qa.compliance_automation_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            compliance_ref=compliance_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("CompliancePassedEvent")
        root.history.append({"event": "DgQaComplianceRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQaSecurityRoot(AggregateRoot):
    tenant_id: str
    security_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, security_ref: str, present: bool = True
    ) -> "DgQaSecurityRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_3_required")
        if not present:
            raise ValueError(
                "data_governance.qa.security_assurance_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            security_ref=security_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("TestExecutedEvent")
        root.history.append({"event": "DgQaSecurityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQaDodRoot(AggregateRoot):
    tenant_id: str
    dod_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, dod_ref: str, present: bool = True
    ) -> "DgQaDodRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_4_required")
        if not present:
            raise ValueError(
                "data_governance.qa.definition_of_done_engine_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            dod_ref=dod_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("CertificationIssuedEvent")
        root.history.append({"event": "DgQaDodRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQaAiQualityRoot(AggregateRoot):
    tenant_id: str
    ai_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, ai_ref: str, present: bool = True
    ) -> "DgQaAiQualityRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_5_required")
        if not present:
            raise ValueError(
                "data_governance.qa.ai_quality_intelligence_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ai_ref=ai_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("EvidenceGeneratedEvent")
        root.history.append({"event": "DgQaAiQualityRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQaGraphRoot(AggregateRoot):
    tenant_id: str
    graph_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, graph_ref: str, present: bool = True
    ) -> "DgQaGraphRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_6_required")
        if not present:
            raise ValueError(
                "data_governance.qa.knowledge_graph_integration_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            graph_ref=graph_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("EvidenceGeneratedEvent")
        root.history.append({"event": "DgQaGraphRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQaTwinRoot(AggregateRoot):
    tenant_id: str
    twin_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def integrate(
        cls, *, tenant_id: str, twin_ref: str, present: bool = True
    ) -> "DgQaTwinRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_7_required")
        if not present:
            raise ValueError(
                "data_governance.qa.digital_twin_integration_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            twin_ref=twin_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("ValidationStartedEvent")
        root.history.append({"event": "DgQaTwinRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQaCqrsRoot(AggregateRoot):
    tenant_id: str
    cqrs_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, cqrs_ref: str, present: bool = True
    ) -> "DgQaCqrsRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_8_required")
        if not present:
            raise ValueError(
                "data_governance.qa.cqrs_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            cqrs_ref=cqrs_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("ValidationStartedEvent")
        root.history.append({"event": "DgQaCqrsRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQaEventSourcingRoot(AggregateRoot):
    tenant_id: str
    es_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, es_ref: str, present: bool = True
    ) -> "DgQaEventSourcingRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_9_required")
        if not present:
            raise ValueError(
                "data_governance.qa.event_sourcing_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            es_ref=es_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("TestExecutedEvent")
        root.history.append({"event": "DgQaEventSourcingRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQaMicroservicesRoot(AggregateRoot):
    tenant_id: str
    ms_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def declare(
        cls, *, tenant_id: str, ms_ref: str, present: bool = True
    ) -> "DgQaMicroservicesRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_10_required")
        if not present:
            raise ValueError(
                "data_governance.qa.microservices_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            ms_ref=ms_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("ValidationStartedEvent")
        root.history.append({"event": "DgQaMicroservicesRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQaApiFirstRoot(AggregateRoot):
    tenant_id: str
    api_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def confirm(
        cls, *, tenant_id: str, api_ref: str, present: bool = True
    ) -> "DgQaApiFirstRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_11_required")
        if not present:
            raise ValueError(
                "data_governance.qa.api_first_architecture_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            api_ref=api_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("EvidenceGeneratedEvent")
        root.history.append({"event": "DgQaApiFirstRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present


@dataclass(eq=False, kw_only=True)
class DgQaContinuousRoot(AggregateRoot):
    tenant_id: str
    continuous_ref: str
    present: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def enable(
        cls, *, tenant_id: str, continuous_ref: str, present: bool = True
    ) -> "DgQaContinuousRoot":
        tid = _tid(tenant_id, "data_governance.qa.tenant_12_required")
        if not present:
            raise ValueError(
                "data_governance.qa.continuous_governance_is_missing"
            )
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tid,
            continuous_ref=continuous_ref.strip(),
            present=True,
            status="ok",
        )
        root.pending_events.append("CertificationIssuedEvent")
        root.history.append({"event": "DgQaContinuousRoot"})
        return root

    def is_missing(self) -> bool:
        return not self.present
