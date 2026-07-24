"""P207-K Knowledge Graph Intelligence aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId

GRAPH_EDGES = frozenset(
    {
        "WORKS_FOR",
        "REPORTS_TO",
        "MEMBER_OF",
        "HAS_ROLE",
        "HAS_PERMISSION",
        "USES_APPLICATION",
        "OWNS_RESOURCE",
        "HAS_RISK",
        "TRUSTS",
        "VIOLATES_POLICY",
        "CONNECTED_TO_THREAT",
        "DEPENDS_ON",
        "SUPPORTS",
        "IMPACTS",
    }
)

REASONING_TYPES = frozenset(
    {
        "rule_based_reasoning",
        "semantic_reasoning",
        "ai_reasoning",
        "graph_neural_reasoning",
    }
)


@dataclass(eq=False, kw_only=True)
class KnowledgeGraphEntityRoot(AggregateRoot):
    tenant_id: str
    entity_ref: str
    entity_kind: str
    peer_projection_ref: str
    data_only: bool
    reasoning_enabled: bool
    owns_graph_sor: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        entity_ref: str,
        entity_kind: str = "identity",
        peer_projection_ref: str,
        data_only: bool = False,
        reasoning_enabled: bool = True,
        owns_graph_sor: bool = False,
    ) -> KnowledgeGraphEntityRoot:
        if not tenant_id.strip():
            raise ValueError("ii.graph.tenant_required")
        if data_only or not reasoning_enabled:
            raise ValueError("ii.graph.graph_only_data_without_reasoning")
        if owns_graph_sor:
            raise ValueError("ii.graph.duplicates_directory_graph_sor")
        if not peer_projection_ref.strip():
            raise ValueError("ii.graph.peer_projection_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            entity_ref=entity_ref.strip(),
            entity_kind=entity_kind.strip(),
            peer_projection_ref=peer_projection_ref.strip(),
            data_only=False,
            reasoning_enabled=True,
            owns_graph_sor=False,
            status="created",
        )
        root.pending_events.append("EntityCreated")
        root.history.append({"event": "EntityCreated"})
        return root

    def is_data_only(self) -> bool:
        return self.data_only or not self.reasoning_enabled


@dataclass(eq=False, kw_only=True)
class GraphRelationshipRoot(AggregateRoot):
    tenant_id: str
    relationship_ref: str
    source_ref: str
    target_ref: str
    edge_type: str
    defined: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def link(
        cls,
        *,
        tenant_id: str,
        relationship_ref: str,
        source_ref: str,
        target_ref: str,
        edge_type: str,
        defined: bool = True,
    ) -> GraphRelationshipRoot:
        if not tenant_id.strip():
            raise ValueError("ii.graph.rel_tenant_required")
        edge = edge_type.strip().upper()
        if not defined or edge not in GRAPH_EDGES:
            raise ValueError("ii.graph.relationships_undefined")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            relationship_ref=relationship_ref.strip(),
            source_ref=source_ref.strip(),
            target_ref=target_ref.strip(),
            edge_type=edge,
            defined=True,
            status="linked",
        )
        root.pending_events.append("RelationshipDiscovered")
        root.history.append({"event": "RelationshipDiscovered"})
        return root

    def is_undefined(self) -> bool:
        return not self.defined or self.edge_type not in GRAPH_EDGES


@dataclass(eq=False, kw_only=True)
class GraphReasoningSessionRoot(AggregateRoot):
    tenant_id: str
    session_ref: str
    reasoning_type: str
    conclusion: str
    explanation: str
    security_context: bool
    via_ai_platform: bool
    ii_integration_strong: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def run(
        cls,
        *,
        tenant_id: str,
        session_ref: str,
        reasoning_type: str = "ai_reasoning",
        conclusion: str = "",
        explanation: str = "",
        security_context: bool = True,
        via_ai_platform: bool = True,
        ii_integration_strong: bool = True,
    ) -> GraphReasoningSessionRoot:
        if not tenant_id.strip():
            raise ValueError("ii.graph.reason_tenant_required")
        rt = reasoning_type.strip().lower()
        if rt not in REASONING_TYPES:
            raise ValueError("ii.graph.reasoning_type_invalid")
        if not conclusion.strip() or not explanation.strip():
            raise ValueError("ii.graph.ai_cannot_explain_conclusions")
        if not security_context:
            raise ValueError("ii.graph.security_context_missing")
        if not via_ai_platform and rt == "ai_reasoning":
            raise ValueError("ii.graph.embeds_llm_sdk")
        if not ii_integration_strong:
            raise ValueError("ii.graph.identity_intelligence_integration_weak")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            session_ref=session_ref.strip(),
            reasoning_type=rt,
            conclusion=conclusion.strip(),
            explanation=explanation.strip(),
            security_context=True,
            via_ai_platform=True,
            ii_integration_strong=True,
            status="completed",
        )
        root.pending_events.append("ReasoningCompleted")
        root.pending_events.append("KnowledgeUpdated")
        root.history.append({"event": "ReasoningCompleted"})
        return root

    def is_unexplainable(self) -> bool:
        return not self.explanation.strip()


@dataclass(eq=False, kw_only=True)
class AttackPathAnalysisRoot(AggregateRoot):
    tenant_id: str
    analysis_ref: str
    subject_ref: str
    path_summary: str
    security_context: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def discover(
        cls,
        *,
        tenant_id: str,
        analysis_ref: str,
        subject_ref: str,
        path_summary: str,
        security_context: bool = True,
    ) -> AttackPathAnalysisRoot:
        if not tenant_id.strip() or not path_summary.strip():
            raise ValueError("ii.graph.attack_required")
        if not security_context:
            raise ValueError("ii.graph.security_context_missing")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            analysis_ref=analysis_ref.strip(),
            subject_ref=subject_ref.strip(),
            path_summary=path_summary.strip(),
            security_context=True,
            status="discovered",
        )
        root.pending_events.append("AttackPathIdentified")
        root.pending_events.append("RiskPathDetected")
        root.history.append({"event": "AttackPathIdentified"})
        return root


@dataclass(eq=False, kw_only=True)
class SemanticQueryCaseRoot(AggregateRoot):
    tenant_id: str
    query_ref: str
    query_text: str
    explanation: str
    via_search: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def search(
        cls,
        *,
        tenant_id: str,
        query_ref: str,
        query_text: str,
        explanation: str = "",
        via_search: bool = True,
    ) -> SemanticQueryCaseRoot:
        if not tenant_id.strip() or not query_text.strip():
            raise ValueError("ii.graph.query_required")
        if not explanation.strip():
            raise ValueError("ii.graph.ai_cannot_explain_conclusions")
        if not via_search:
            raise ValueError("ii.graph.search_platform_required")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            query_ref=query_ref.strip(),
            query_text=query_text.strip(),
            explanation=explanation.strip(),
            via_search=True,
            status="answered",
        )
        root.history.append({"event": "SemanticQueryAnswered"})
        return root


@dataclass(eq=False, kw_only=True)
class OntologyGovernancePolicyRoot(AggregateRoot):
    tenant_id: str
    policy_ref: str
    ontology_governed: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        policy_ref: str,
        ontology_governed: bool = True,
    ) -> OntologyGovernancePolicyRoot:
        if not tenant_id.strip():
            raise ValueError("ii.graph.ontology_tenant_required")
        if not ontology_governed:
            raise ValueError("ii.graph.ontology_governance_absent")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            policy_ref=policy_ref.strip(),
            ontology_governed=True,
            status="active",
        )
        root.history.append({"event": "OntologyGovernanceDefined"})
        return root

    def is_ungoverned(self) -> bool:
        return not self.ontology_governed


@dataclass(eq=False, kw_only=True)
class GraphSecurityContextRoot(AggregateRoot):
    tenant_id: str
    context_ref: str
    security_context_present: bool
    audited: bool
    status: str
    pending_events: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def establish(
        cls,
        *,
        tenant_id: str,
        context_ref: str,
        security_context_present: bool = True,
        audited: bool = True,
    ) -> GraphSecurityContextRoot:
        if not tenant_id.strip():
            raise ValueError("ii.graph.sec_tenant_required")
        if not security_context_present:
            raise ValueError("ii.graph.security_context_missing")
        if not audited:
            raise ValueError("ii.graph.decision_not_audited")
        root = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id.strip(),
            context_ref=context_ref.strip(),
            security_context_present=True,
            audited=True,
            status="active",
        )
        root.history.append({"event": "GraphSecurityContextEstablished"})
        return root

    def is_missing(self) -> bool:
        return not self.security_context_present
