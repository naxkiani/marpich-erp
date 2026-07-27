"""Data Governance P212-J Knowledge Graph foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/402-enterprise-data-governance-knowledge-graph.md",
    "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_KNOWLEDGE_GRAPH.md",
    "docs/architecture/data_governance/DATA_GOVERNANCE_GRAPH_CAPABILITIES.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_GRAPH_DDD_CQRS.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_GRAPH_SECURITY.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_GRAPH_VALIDATION.v1.yaml",
    "backend/contexts/data_governance/domain/services/dg_platform_graph.py",
    "backend/contexts/data_governance/domain/aggregates/dg_graph_aggregates.py",
    "backend/contexts/data_governance/infrastructure/acl/dg_graph_acl.py",
    "backend/contexts/data_governance/application/dg_graph_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/knowledge_graph",
    "backend/contexts/ontology_platform",
    "backend/contexts/semantic_fabric_platform",
    "backend/contexts/data_mesh",
    "backend/contexts/data_marketplace",
    "backend/contexts/metadata_governance_platform",
)


def validate_dg_graph_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_governance.domain.aggregates.dg_graph_aggregates import (
        DgGraphArchitectureRoot,
        DgGraphDddModelRoot,
        DgGraphOntologyRoot,
        DgGraphSemanticFabricRoot,
        DgGraphIntelligenceRoot,
        DgGraphAiReasoningRoot,
        DgGraphMeshIntegrationRoot,
        DgGraphMetadataIntegrationRoot,
        DgGraphMarketplaceIntegrationRoot,
        DgGraphPolicyIntegrationRoot,
        DgGraphDigitalTwinRoot,
        DgGraphCqrsRoot,
        DgGraphEventSourcingRoot,
        DgGraphMicroservicesRoot,
        DgGraphZeroTrustRoot,
        DgGraphScalabilityRoot,
    )
    from contexts.data_governance.domain.services import (
        dg_platform_graph as graph,
    )

    cat = graph.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P212-J"
        and cat.get("adr") == 402
        and cat.get("sor") == "data_governance"
        and cat.get("capability") == "CAP-PLT-DG-001"
        and cat["knowledge_graph_architecture_complete_required"] is True
        and cat["ddd_domain_model_present_required"] is True
        and cat["ontology_architecture_present_required"] is True
        and cat["semantic_data_fabric_present_required"] is True
        and cat["graph_intelligence_engine_present_required"] is True
        and cat["ai_reasoning_layer_present_required"] is True
        and cat["data_mesh_integration_present_required"] is True
        and cat["metadata_integration_present_required"] is True
        and cat["data_marketplace_integration_present_required"] is True
        and cat["policy_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_sourcing_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["enterprise_scalability_present_required"] is True
        and cat["graph_architecture"]["not_incomplete"] is True
        and cat["ddd_model"]["not_missing"] is True
        and cat["ontology"]["not_missing"] is True
        and cat["semantic_fabric"]["not_missing"] is True
        and cat["graph_intelligence"]["not_missing"] is True
        and cat["ai_reasoning"]["not_missing"] is True
        and cat["mesh_alignment"]["not_missing"] is True
        and cat["metadata_integration"]["not_missing"] is True
        and cat["marketplace_integration"]["not_missing"] is True
        and cat["policy_integration"]["not_missing"] is True
        and cat["digital_twin"]["not_missing"] is True
        and cat["cqrs"]["not_missing"] is True
        and cat["event_sourcing"]["not_missing"] is True
        and cat["microservices"]["not_missing"] is True
        and cat["zero_trust"]["not_missing"] is True
        and cat["scalability"]["not_missing"] is True
        and cat["graph_architecture"]["bc_count"] >= 5
        and cat["ontology"]["capability_count"] >= 6
        and cat["semantic_fabric"]["layer_count"] >= 5
        and cat["graph_intelligence"]["capability_count"] >= 6
        and cat["node_model"]["category_count"] >= 5
        and cat["microservices"]["service_count"] >= 6
        and cat["cqrs"]["event_count"] >= 6
        and cat["cursor_outputs"]["count"] >= 18
        and (
            "enterprise_knowledge_graph_architecture_is_incomplete"
            in cat["quality_gates"]["reject_if"]
        )
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
            DgGraphArchitectureRoot.publish,
            tenant_id="t1",
            architecture_ref="r0",
            complete=False,
        )
        and DgGraphArchitectureRoot.publish(
            tenant_id="t1", architecture_ref="ok0"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DgGraphDddModelRoot.define,
            tenant_id="t1",
            model_ref="r1",
            present=False,
        )
        and DgGraphDddModelRoot.define(
            tenant_id="t1", model_ref="ok1"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphOntologyRoot.define,
            tenant_id="t1",
            ontology_ref="r2",
            present=False,
        )
        and DgGraphOntologyRoot.define(
            tenant_id="t1", ontology_ref="ok2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphSemanticFabricRoot.enable,
            tenant_id="t1",
            fabric_ref="r3",
            present=False,
        )
        and DgGraphSemanticFabricRoot.enable(
            tenant_id="t1", fabric_ref="ok3"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphIntelligenceRoot.enable,
            tenant_id="t1",
            intel_ref="r4",
            present=False,
        )
        and DgGraphIntelligenceRoot.enable(
            tenant_id="t1", intel_ref="ok4"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphAiReasoningRoot.enable,
            tenant_id="t1",
            ai_ref="r5",
            present=False,
        )
        and DgGraphAiReasoningRoot.enable(
            tenant_id="t1", ai_ref="ok5"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphMeshIntegrationRoot.align,
            tenant_id="t1",
            mesh_ref="r6",
            present=False,
        )
        and DgGraphMeshIntegrationRoot.align(
            tenant_id="t1", mesh_ref="ok6"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphMetadataIntegrationRoot.integrate,
            tenant_id="t1",
            metadata_ref="r7",
            present=False,
        )
        and DgGraphMetadataIntegrationRoot.integrate(
            tenant_id="t1", metadata_ref="ok7"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphMarketplaceIntegrationRoot.integrate,
            tenant_id="t1",
            marketplace_ref="r8",
            present=False,
        )
        and DgGraphMarketplaceIntegrationRoot.integrate(
            tenant_id="t1", marketplace_ref="ok8"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphPolicyIntegrationRoot.integrate,
            tenant_id="t1",
            policy_ref="r9",
            present=False,
        )
        and DgGraphPolicyIntegrationRoot.integrate(
            tenant_id="t1", policy_ref="ok9"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphDigitalTwinRoot.integrate,
            tenant_id="t1",
            twin_ref="r10",
            present=False,
        )
        and DgGraphDigitalTwinRoot.integrate(
            tenant_id="t1", twin_ref="ok10"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphCqrsRoot.align,
            tenant_id="t1",
            cqrs_ref="r11",
            present=False,
        )
        and DgGraphCqrsRoot.align(
            tenant_id="t1", cqrs_ref="ok11"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphEventSourcingRoot.enable,
            tenant_id="t1",
            es_ref="r12",
            present=False,
        )
        and DgGraphEventSourcingRoot.enable(
            tenant_id="t1", es_ref="ok12"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphMicroservicesRoot.declare,
            tenant_id="t1",
            ms_ref="r13",
            present=False,
        )
        and DgGraphMicroservicesRoot.declare(
            tenant_id="t1", ms_ref="ok13"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphZeroTrustRoot.confirm,
            tenant_id="t1",
            zt_ref="r14",
            present=False,
        )
        and DgGraphZeroTrustRoot.confirm(
            tenant_id="t1", zt_ref="ok14"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgGraphScalabilityRoot.confirm,
            tenant_id="t1",
            scale_ref="r15",
            present=False,
        )
        and DgGraphScalabilityRoot.confirm(
            tenant_id="t1", scale_ref="ok15"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_governance/infrastructure/acl/dg_graph_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p212_d" in acl_text
        and "via_p212_e" in acl_text
        and "via_p212_f" in acl_text
        and "via_p212_g" in acl_text
        and "via_p212_h" in acl_text
        and "via_enterprise_ai" in acl_text
        and "via_enterprise_search" in acl_text
        and "ai_reasoning_layer_present_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_governance/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_governance_router.get("/graph")' in router
        and "/graph/ontology" in router
        and "/graph/intelligence" in router
        and "/graph/semantic-fabric" in router
        and "/graph/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_KNOWLEDGE_GRAPH.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise knowledge graph architecture is incomplete" in law
        and "Never DDD domain model is missing" in law
        and "Never Ontology architecture is missing" in law
        and "Never Semantic data fabric is missing" in law
        and "Never Graph intelligence engine is missing" in law
        and "Never AI reasoning layer is missing" in law
        and "Never Data mesh integration is missing" in law
        and "Never Metadata integration is missing" in law
        and "Never Data marketplace integration is missing" in law
        and "Never Policy integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Enterprise scalability is missing" in law
        and "Never Sibling knowledge graph BC" in law
        and (
            "Enterprise intelligence requires connected knowledge,"
            in law
        )
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
        "prompt": "P212-J",
        "adr": 402,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "data_governance",
        "capability": "CAP-PLT-DG-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
