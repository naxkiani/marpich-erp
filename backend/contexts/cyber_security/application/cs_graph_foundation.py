"""Cyber Security P210-K Knowledge Graph foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/371-enterprise-cyber-security-knowledge-graph.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_KNOWLEDGE_GRAPH.md",
    "docs/architecture/cyber_security/CYBER_GRAPH_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_GRAPH_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_GRAPH_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_GRAPH_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_graph.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_graph_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_graph_acl.py",
    "backend/contexts/cyber_security/application/cs_graph_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/cyber_graph",
    "backend/contexts/security_digital_twin",
    "backend/contexts/attack_graph",
    "backend/contexts/ai_ops",
    "backend/contexts/asm",
)


def validate_cs_graph_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_graph_aggregates import (
        CsGraphAccurateResolutionRoot,
        CsGraphAiReasoningRoot,
        CsGraphAttackPathCalculableRoot,
        CsGraphGovernanceRoot,
        CsGraphInsightGeneratedRoot,
        CsGraphLivingTwinRoot,
        CsGraphSemanticRelationshipsRoot,
        CsGraphSimulationRoot,
    )
    from contexts.cyber_security.domain.services import cs_platform_graph as graph

    cat = graph.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-K"
        and cat.get("adr") == 371
        and cat.get("sor") == "cyber_security"
        and cat["semantic_relationships_required"] is True
        and cat["attack_paths_calculable_required"] is True
        and cat["digital_twins_living_required"] is True
        and cat["ai_reasoning_available_required"] is True
        and cat["graph_governance_required"] is True
        and cat["entity_resolution_accurate_required"] is True
        and cat["simulation_capability_required"] is True
        and cat["ontology"]["not_lacking_relationships"] is True
        and cat["attack_graph"]["not_incalculable"] is True
        and cat["digital_twin"]["not_static"] is True
        and cat["reasoning"]["not_unavailable"] is True
        and cat["graph_governance"]["not_missing"] is True
        and cat["entity_resolution"]["not_inaccurate"] is True
        and cat["simulation"]["not_absent"] is True
        and cat["architecture"]["layer_count"] >= 8
        and cat["cqrs"]["event_count"] >= 8
        and cat["cursor_outputs"]["count"] >= 20
        and "security_entities_lack_semantic_relationships"
        in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = []
    checks.append(
        not _bad(
            CsGraphSemanticRelationshipsRoot.link,
            tenant_id="t1",
            entity_ref="e1",
            has_semantic_relationships=False,
        )
        and CsGraphSemanticRelationshipsRoot.link(
            tenant_id="t1", entity_ref="e2"
        ).lacks_relationships()
        is False
    )
    checks.append(
        not _bad(
            CsGraphAttackPathCalculableRoot.analyze,
            tenant_id="t1",
            path_ref="p1",
            calculable=False,
        )
        and CsGraphAttackPathCalculableRoot.analyze(
            tenant_id="t1", path_ref="p2"
        ).is_incalculable()
        is False
    )
    checks.append(
        not _bad(
            CsGraphLivingTwinRoot.sync,
            tenant_id="t1",
            twin_ref="tw1",
            living=False,
        )
        and CsGraphLivingTwinRoot.sync(
            tenant_id="t1", twin_ref="tw2"
        ).is_static()
        is False
    )
    checks.append(
        not _bad(
            CsGraphAiReasoningRoot.execute,
            tenant_id="t1",
            reasoning_ref="r1",
            available=False,
        )
        and CsGraphAiReasoningRoot.execute(
            tenant_id="t1", reasoning_ref="r2"
        ).is_unavailable()
        is False
    )
    checks.append(
        not _bad(
            CsGraphGovernanceRoot.assert_present,
            tenant_id="t1",
            governance_ref="g1",
            present=False,
        )
        and CsGraphGovernanceRoot.assert_present(
            tenant_id="t1", governance_ref="g2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            CsGraphAccurateResolutionRoot.resolve,
            tenant_id="t1",
            resolution_ref="res1",
            accurate=False,
        )
        and CsGraphAccurateResolutionRoot.resolve(
            tenant_id="t1", resolution_ref="res2"
        ).is_inaccurate()
        is False
    )
    checks.append(
        not _bad(
            CsGraphSimulationRoot.generate,
            tenant_id="t1",
            simulation_ref="s1",
            present=False,
        )
        and CsGraphSimulationRoot.generate(
            tenant_id="t1", simulation_ref="s2"
        ).is_absent()
        is False
    )
    insight = CsGraphInsightGeneratedRoot.generate(
        tenant_id="t1", insight_ref="ins1"
    )
    checks.append("InsightGenerated" in insight.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/cyber_security/infrastructure/acl/cs_graph_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_enterprise_ai_platform" in acl_text
        and "ai_reasoning_available_required" in acl_text
        and "graph_governance_required" in acl_text
        and "via_p210_j_ai_ops" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/graph"' in router
        and "/graph/ontology" in router
        and "/graph/attack-paths" in router
        and "/graph/digital-twin" in router
        and "/graph/simulation" in router
        and "/graph/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_KNOWLEDGE_GRAPH.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never security entities lack semantic relationships" in law
        and "Never attack paths cannot be calculated" in law
        and "Never digital twins are static" in law
        and "Never AI reasoning is unavailable" in law
        and "Never graph governance is missing" in law
        and "Never entity resolution is inaccurate" in law
        and "Never simulation capability is absent" in law
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
        "prompt": "P210-K",
        "adr": 371,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "cyber_security",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
