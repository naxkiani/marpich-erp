"""Identity Intelligence P207-K Knowledge Graph foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/326-enterprise-identity-intelligence-knowledge-graph-reasoning.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_KNOWLEDGE_GRAPH_REASONING.md",
    "docs/architecture/identity/intelligence/II_GRAPH_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_GRAPH_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_GRAPH_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_GRAPH_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_graph.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_graph_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_graph_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_graph_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/knowledge_graph_platform",
    "backend/contexts/identity_graph_intelligence_bc",
    "backend/contexts/graph_reasoning_bc",
)


def validate_ii_graph_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_graph_aggregates import (
        AttackPathAnalysisRoot,
        GraphReasoningSessionRoot,
        GraphRelationshipRoot,
        GraphSecurityContextRoot,
        KnowledgeGraphEntityRoot,
        OntologyGovernancePolicyRoot,
        SemanticQueryCaseRoot,
    )
    from contexts.identity_intelligence.domain.services import ii_platform_graph as graph
    from contexts.identity_intelligence.infrastructure.acl import ii_graph_acl as acls

    cat = graph.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-K"
        and cat.get("adr") == 326
        and cat.get("sor") == "identity_intelligence"
        and cat.get("graph_storage_peer") == "directory"
        and cat["not_data_only"] is True
        and cat["reasoning_required"] is True
        and cat["capabilities"]["not_data_only_graph"] is True
        and cat["capabilities"]["not_relationships_undefined"] is True
        and cat["capabilities"]["not_ai_unexplainable"] is True
        and cat["capabilities"]["not_security_missing"] is True
        and cat["capabilities"]["not_ontology_ungoverned"] is True
        and cat["capabilities"]["not_weak_ii_integration"] is True
        and cat["capabilities"]["does_not_own_graph_sor"] is True
        and cat["relationship_model"]["defined"] is True
        and cat["reasoning"]["explainable"] is True
        and cat["ontology"]["governed"] is True
        and cat["ddd"]["aggregate_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["integrations"]["graph_integration_complete"] is True
        and "graph_only_data_without_reasoning" in cat["quality_gates"]["reject_if"]
        and "duplicates_directory_graph_sor" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        KnowledgeGraphEntityRoot.create(
            tenant_id="t1",
            entity_ref="e1",
            peer_projection_ref="dir:g1",
            data_only=True,
        )
        data_only = True
    except ValueError:
        data_only = False

    try:
        KnowledgeGraphEntityRoot.create(
            tenant_id="t1",
            entity_ref="e2",
            peer_projection_ref="dir:g2",
            owns_graph_sor=True,
        )
        dup_sor = True
    except ValueError:
        dup_sor = False

    entity = KnowledgeGraphEntityRoot.create(
        tenant_id="t1",
        entity_ref="e3",
        peer_projection_ref="dir:g3",
    )
    entity_ok = (
        not data_only
        and not dup_sor
        and entity.is_data_only() is False
        and "EntityCreated" in entity.pending_events
    )

    try:
        GraphRelationshipRoot.link(
            tenant_id="t1",
            relationship_ref="r1",
            source_ref="u1",
            target_ref="role1",
            edge_type="UNKNOWN_EDGE",
        )
        undef = True
    except ValueError:
        undef = False

    rel = GraphRelationshipRoot.link(
        tenant_id="t1",
        relationship_ref="r2",
        source_ref="u1",
        target_ref="role1",
        edge_type="HAS_ROLE",
    )
    rel_ok = not undef and rel.is_undefined() is False

    try:
        GraphReasoningSessionRoot.run(
            tenant_id="t1",
            session_ref="s1",
            conclusion="High risk path",
            explanation="",
        )
        no_exp = True
    except ValueError:
        no_exp = False

    try:
        GraphReasoningSessionRoot.run(
            tenant_id="t1",
            session_ref="s2",
            conclusion="High risk path",
            explanation="Privilege chain to finance",
            security_context=False,
        )
        no_sec = True
    except ValueError:
        no_sec = False

    try:
        GraphReasoningSessionRoot.run(
            tenant_id="t1",
            session_ref="s3",
            conclusion="High risk path",
            explanation="Privilege chain to finance",
            via_ai_platform=False,
            reasoning_type="ai_reasoning",
        )
        embed_llm = True
    except ValueError:
        embed_llm = False

    try:
        GraphReasoningSessionRoot.run(
            tenant_id="t1",
            session_ref="s4",
            conclusion="High risk path",
            explanation="Privilege chain to finance",
            ii_integration_strong=False,
        )
        weak_ii = True
    except ValueError:
        weak_ii = False

    reason = GraphReasoningSessionRoot.run(
        tenant_id="t1",
        session_ref="s5",
        conclusion="Generate security review",
        explanation="Identity has privilege and risk is high",
    )
    reason_ok = (
        not no_exp
        and not no_sec
        and not embed_llm
        and not weak_ii
        and reason.is_unexplainable() is False
        and "ReasoningCompleted" in reason.pending_events
    )

    try:
        AttackPathAnalysisRoot.discover(
            tenant_id="t1",
            analysis_ref="a1",
            subject_ref="u1",
            path_summary="",
        )
        no_path = True
    except ValueError:
        no_path = False

    try:
        AttackPathAnalysisRoot.discover(
            tenant_id="t1",
            analysis_ref="a2",
            subject_ref="u1",
            path_summary="identity→role→critical system",
            security_context=False,
        )
        attack_no_sec = True
    except ValueError:
        attack_no_sec = False

    attack = AttackPathAnalysisRoot.discover(
        tenant_id="t1",
        analysis_ref="a3",
        subject_ref="u1",
        path_summary="compromised identity→privilege escalation→critical resource",
    )
    attack_ok = (
        not no_path
        and not attack_no_sec
        and "AttackPathIdentified" in attack.pending_events
    )

    try:
        SemanticQueryCaseRoot.search(
            tenant_id="t1",
            query_ref="q1",
            query_text="users with excessive privilege",
            explanation="",
        )
        query_no_exp = True
    except ValueError:
        query_no_exp = False

    query = SemanticQueryCaseRoot.search(
        tenant_id="t1",
        query_ref="q2",
        query_text="Which identities can access financial systems?",
        explanation="Path via HAS_ROLE and USES_APPLICATION to finance app",
    )
    query_ok = not query_no_exp and query.via_search is True

    try:
        OntologyGovernancePolicyRoot.define(
            tenant_id="t1",
            policy_ref="p1",
            ontology_governed=False,
        )
        ungov = True
    except ValueError:
        ungov = False

    ontology = OntologyGovernancePolicyRoot.define(
        tenant_id="t1", policy_ref="p2"
    )
    ontology_ok = not ungov and ontology.is_ungoverned() is False

    try:
        GraphSecurityContextRoot.establish(
            tenant_id="t1",
            context_ref="c1",
            security_context_present=False,
        )
        sec_missing = True
    except ValueError:
        sec_missing = False

    sec = GraphSecurityContextRoot.establish(
        tenant_id="t1", context_ref="c2"
    )
    sec_ok = not sec_missing and sec.is_missing() is False

    aggregates_ok = (
        entity_ok
        and rel_ok
        and reason_ok
        and attack_ok
        and query_ok
        and ontology_ok
        and sec_ok
    )

    acl_ok = (
        acls.to_directory_graph(tenant_id="t1", projection_ref="g1")[
            "duplicates_directory_graph_sor_forbidden"
        ]
        is True
        and acls.to_ai_infer(tenant_id="t1", surface="graph", context={})[
            "explainable_required"
        ]
        is True
        and acls.to_search(tenant_id="t1", query="excessive privilege")[
            "via_search_platform"
        ]
        is True
        and acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")["via_p207f"]
        is True
        and acls.to_risk_calculate(
            tenant_id="t1", subject_ref="u1", graph_context={}
        )["ii_integration_strong"]
        is True
        and acls.to_authz_check(
            tenant_id="t1", subject_id="u1", action="identity_intelligence.write"
        )["bypasses_authorization_pdp_forbidden"]
        is True
        and acls.to_audit(
            tenant_id="t1", action="ii.graph.reason", resource_ref="s5"
        )["decision_tracking"]
        is True
        and acls.to_agent_task(
            tenant_id="t1",
            agent_kind="graph_analyst_agent",
            graph_ref="g1",
        )["via_p207e"]
        is True
    )

    router = (
        root
        / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/graph"' in router
        and "/graph/reasoning" in router
        and "/graph/attack-path" in router
        and "/graph/search" in router
        and "/graph/security" in router
        and "/graph/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_KNOWLEDGE_GRAPH_REASONING.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never graph data-only without reasoning" in law
        and "Never undefined relationships" in law
        and "Never unexplained AI conclusions" in law
        and "Never missing security context" in law
        and "Never absent ontology governance" in law
        and "Never weak II integration" in law
        and "Never duplicate directory graph SoR" in law
    )

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and doc_ok
    )
    return {
        "prompt": "P207-K",
        "adr": 326,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "identity_intelligence",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
