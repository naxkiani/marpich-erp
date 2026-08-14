"""Civilization P219-C DDD domain architecture foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/556-enterprise-civilization-operating-system-domain.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_DOMAIN.md",
    "docs/architecture/civilization/CIVILIZATION_DOMAIN_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_DOMAIN_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_DOMAIN_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_DOMAIN_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_DOMAIN_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_domain.py",
    "backend/contexts/civilization/domain/aggregates/civ_domain_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_domain_acl.py",
    "backend/contexts/civilization/application/civ_domain_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_domain_model_platform",
    "backend/contexts/civilization_ddd_bc",
    "backend/contexts/planetary_domain_bc",
)


def validate_civ_domain_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_domain_aggregates import (
        AggregateModelRoot, BoundedContextArchitectureRoot, CivilizationDomainModelRoot,
        CqrsModelRoot, DigitalTwinDomainRoot, DomainEventsModelRoot,
        DomainServicesModelRoot, EnterpriseDddArchitectureRoot, KnowledgeGraphDomainRoot,
    )
    from contexts.civilization.domain.services import civ_platform_domain as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-C" and cat["adr"] == 556 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_domain_architecture_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["strategy_gate"] == "P219-B"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_os_domain_model_present_required"] is True
        and cat["enterprise_ddd_architecture_present_required"] is True
        and cat["bounded_context_architecture_present_required"] is True
        and cat["aggregate_model_present_required"] is True
        and cat["entities_model_present_required"] is True
        and cat["value_objects_model_present_required"] is True
        and cat["domain_services_model_present_required"] is True
        and cat["domain_events_model_present_required"] is True
        and cat["cqrs_model_present_required"] is True
        and cat["knowledge_graph_domain_model_present_required"] is True
        and cat["digital_twin_domain_model_present_required"] is True
        and cat["meos_integration_domain_map_present_required"] is True
        and cat["strategic_domains"]["core_domain_count"] == 5
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["aggregates"]["aggregate_count"] == 8
        and cat["entities"]["entity_count"] >= 20
        and cat["value_objects"]["value_object_count"] >= 15
        and cat["domain_services"]["service_count"] >= 12
        and cat["events"]["core_event_count"] == 15
        and cat["cqrs"]["command_count"] == 6 and cat["cqrs"]["query_count"] == 6
        and cat["knowledge_graph"]["node_count"] == 9
        and cat["knowledge_graph"]["edge_count"] == 7
        and cat["digital_twin"]["entity_count"] == 5
        and cat["microservices"]["service_count"] == 10
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_a_mission"] is True
        and cat["never_replace_p219_b_strategy"] is True
        and cat["never_cross_context_aggregate_imports"] is True
        and cat["never_opaque_unexplainable_civilization_domain_decisions"] is True
        and cat["never_ungated_civilization_decision_domain"] is True
        and cat["foundation_for_p219_d"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationDomainModelRoot.enable(tenant_id="t1", domain_ref="d1").is_missing() is False,
        EnterpriseDddArchitectureRoot.enable(tenant_id="t1", ddd_ref="ddd1").is_missing() is False,
        BoundedContextArchitectureRoot.enable(tenant_id="t1", bc_ref="bc1").is_missing() is False,
        AggregateModelRoot.enable(tenant_id="t1", aggregate_ref="a1").is_missing() is False,
        DomainEventsModelRoot.enable(tenant_id="t1", events_ref="e1").is_missing() is False,
        CqrsModelRoot.enable(tenant_id="t1", cqrs_ref="q1").is_missing() is False,
        KnowledgeGraphDomainRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        DigitalTwinDomainRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        DomainServicesModelRoot.enable(tenant_id="t1", services_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_domain_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p219_b", "via_p218_z", "via_p218", "via_p217",
        "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p219_a_mission", "never_replace_p219_b_strategy",
        "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization", "never_cross_context_aggregate_imports",
        "never_opaque_unexplainable_civilization_domain_decisions",
        "never_ungated_civilization_decision_domain",
        "never_skip_human_authority_domain",
        "never_skip_ethical_civilization_governance_domain",
        "never_violate_human_sovereignty_domain",
        "module_local_civilization_domain_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/domain")', "/domain/strategy", "/domain/bounded-contexts",
        "/domain/aggregates", "/domain/entities", "/domain/value-objects",
        "/domain/services", "/domain/events", "/domain/cqrs",
        "/domain/knowledge-graph", "/domain/digital-twin", "/domain/microservices",
        "/domain/integration", "/domain/relationships", "/domain/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_DOMAIN.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Civilization OS Domain Model is missing",
        "Never Enterprise DDD Architecture is missing",
        "Never Bounded Context Architecture is missing",
        "Never Aggregate Model is missing",
        "Never Entities Model is missing",
        "Never Value Objects Model is missing",
        "Never Domain Services Model is missing",
        "Never Domain Events Model is missing",
        "Never CQRS Model is missing",
        "Never Knowledge Graph Domain Model is missing",
        "Never Digital Twin Domain Model is missing",
        "Never MEOS Integration Domain Map is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-A Mission",
        "Never Replace P219-B Strategy",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace P215-Z Quantum",
        "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology",
        "Never Replace P218 Space",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Merge P218-T Space Civilization Phase",
        "Never Cross-Context Aggregate Imports",
        "Never Opaque Unexplainable Civilization Domain Decisions",
        "Never Ungated Civilization Decision Domain",
        "Never Skip Human Authority Domain",
        "Never Skip Ethical Civilization Governance Domain",
        "Never Violate Human Sovereignty Domain",
        "isolated DDD domain model inside MEOS",
        "P219-D",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-C", "adr": 556, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
