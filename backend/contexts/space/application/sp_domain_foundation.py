"""Space P218-C DDD domain architecture foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/529-enterprise-space-intelligence-domain-architecture.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_DOMAIN.md",
    "docs/architecture/space/SPACE_DOMAIN_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/space/SPACE_DOMAIN_AGGREGATES.v1.yaml",
    "docs/architecture/space/SPACE_DOMAIN_DDD_CQRS.v1.yaml",
    "docs/architecture/space/SPACE_DOMAIN_SECURITY.v1.yaml",
    "docs/architecture/space/SPACE_DOMAIN_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_domain.py",
    "backend/contexts/space/domain/aggregates/sp_domain_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_domain_acl.py",
    "backend/contexts/space/application/sp_domain_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_domain_platform",
    "backend/contexts/space_ddd_platform",
    "backend/contexts/space_intelligence_domain_platform",
)
def validate_sp_domain_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_domain_aggregates import (
        CoreDomainRoot, BoundedContextMapRoot, MissionManagementDomainRoot,
        OrbitalOperationsDomainRoot, SatelliteFleetDomainRoot, SpaceAIDomainRoot,
        ScientificResearchDomainRoot, SpaceEconomyDomainRoot, SpaceSecurityDomainRoot,
        SpaceDigitalTwinDomainRoot,
    )
    from contexts.space.domain.services import sp_platform_domain as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-C" and cat["adr"] == 529 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_intelligence_domain_architecture_framework"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_core_domain_present_required"] is True
        and cat["supporting_domains_present_required"] is True
        and cat["generic_domains_present_required"] is True
        and cat["bounded_context_map_present_required"] is True
        and cat["aggregates_present_required"] is True
        and cat["entities_present_required"] is True
        and cat["value_objects_present_required"] is True
        and cat["domain_services_present_required"] is True
        and cat["repository_boundaries_present_required"] is True
        and cat["domain_events_present_required"] is True
        and cat["knowledge_graph_mapping_present_required"] is True
        and cat["digital_twin_mapping_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["aggregates"]["aggregate_count"] == 8
        and cat["domain_services"]["service_count"] == 12
        and cat["repositories"]["repository_count"] == 9
        and cat["microservices"]["service_count"] == 8
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_foundation"] is True
        and cat["never_replace_p218_a_mission"] is True
        and cat["never_replace_p218_b_strategy"] is True
        and cat["never_cross_context_aggregate_mutation"] is True
        and cat["never_peer_domain_imports"] is True
        and cat["never_replace_biotechnology"] is True
        and cat["never_opaque_mission_critical_strategy"] is True
        and cat["never_ungated_autonomous_mission_strategy"] is True
        and cat["module_local_llm_forbidden"] is True
        and cat["foundation_for_p218_d"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CoreDomainRoot.enable(tenant_id="t1", domain_ref="d1").is_missing() is False,
        BoundedContextMapRoot.enable(tenant_id="t1", map_ref="m1").is_missing() is False,
        MissionManagementDomainRoot.enable(tenant_id="t1", mission_ref="m1").is_missing() is False,
        OrbitalOperationsDomainRoot.enable(tenant_id="t1", orbit_ref="o1").is_missing() is False,
        SatelliteFleetDomainRoot.enable(tenant_id="t1", satellite_ref="s1").is_missing() is False,
        SpaceAIDomainRoot.enable(tenant_id="t1", ai_ref="a1").is_missing() is False,
        ScientificResearchDomainRoot.enable(tenant_id="t1", research_ref="r1").is_missing() is False,
        SpaceEconomyDomainRoot.enable(tenant_id="t1", economy_ref="e1").is_missing() is False,
        SpaceSecurityDomainRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        SpaceDigitalTwinDomainRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_domain_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p218", "via_p218_a", "via_p218_b", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p218_foundation", "never_replace_p218_a_mission", "never_replace_p218_b_strategy",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "never_replace_biotechnology",
        "module_local_space_domain_forbidden", "never_cross_context_aggregate_mutation",
        "never_peer_domain_imports", "module_local_llm_forbidden",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/domain")', "/domain/strategy", "/domain/bounded-contexts",
        "/domain/aggregates", "/domain/entities", "/domain/value-objects",
        "/domain/services", "/domain/repositories", "/domain/events",
        "/domain/cqrs", "/domain/microservices", "/domain/integration",
        "/domain/relationships", "/domain/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_DOMAIN.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Core Domain is missing",
        "Never Supporting Domains are missing",
        "Never Generic Domains are missing",
        "Never Bounded Context Map is missing",
        "Never Aggregates are missing",
        "Never Entities are missing",
        "Never Value Objects are missing",
        "Never Domain Services are missing",
        "Never Repository Boundaries are missing",
        "Never Domain Events are missing",
        "Never Knowledge Graph Mapping is missing",
        "Never Digital Twin Mapping is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Space BC",
        "Never Replace P218 Foundation",
        "Never Replace P218-A Mission",
        "Never Replace P218-B Strategy",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Biotechnology (P217)",
        "Never Skip Human Mission Oversight Strategy",
        "Never Skip Space Cybersecurity Strategy",
        "Never Skip Space Sustainability Strategy",
        "Never Opaque Mission-Critical Strategy",
        "Never Ungated Autonomous Mission Strategy",
        "Never Cross-Context Aggregate Mutation",
        "Never Peer Domain Imports",
        "Enterprise Space Intelligence Domain",
        "P218", "P218-A", "P218-B", "P217-Z", "P216-Z", "P215-Z", "P214-Z", "P218-D",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-C", "adr": 529, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
