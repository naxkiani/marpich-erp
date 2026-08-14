"""Robotics P216-C DDD domain architecture foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/475-enterprise-robotics-domain-architecture.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_DOMAIN.md",
    "docs/architecture/robotics/ROBOTICS_DOMAIN_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_DOMAIN_AGGREGATES.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_DOMAIN_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_DOMAIN_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_DOMAIN_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_domain.py",
    "backend/contexts/robotics/domain/aggregates/rb_domain_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_domain_acl.py",
    "backend/contexts/robotics/application/rb_domain_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/robotics_domain_platform",
    "backend/contexts/robotics_ddd_platform",
    "backend/contexts/cyber_physical_domain_platform",
)
def validate_rb_domain_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_domain_aggregates import (
        CoreDomainRoot, BoundedContextMapRoot, RobotLifecycleDomainRoot,
        AutonomousMachineDomainRoot, PhysicalAIDomainRoot, MissionDomainRoot,
        FleetDomainRoot, DigitalTwinDomainRoot, SafetyDomainRoot,
    )
    from contexts.robotics.domain.services import rb_platform_domain as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-C" and cat["adr"] == 475 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_robotics_domain_architecture_framework"
        and cat["foundation_gate"] == "P216" and cat["mission_gate"] == "P216-A"
        and cat["strategy_gate"] == "P216-B"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["robotics_core_domain_present_required"] is True
        and cat["supporting_domains_present_required"] is True
        and cat["generic_domains_present_required"] is True
        and cat["bounded_context_map_present_required"] is True
        and cat["aggregates_present_required"] is True
        and cat["entities_present_required"] is True
        and cat["value_objects_present_required"] is True
        and cat["domain_services_present_required"] is True
        and cat["repository_boundaries_present_required"] is True
        and cat["domain_events_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 9
        and cat["aggregates"]["aggregate_count"] == 9
        and cat["domain_services"]["service_count"] == 7
        and cat["repositories"]["repository_count"] == 6
        and cat["microservices"]["service_count"] == 9
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_a_mission"] is True
        and cat["never_replace_p216_b_strategy"] is True
        and cat["never_cross_context_aggregate_mutation"] is True
        and cat["never_peer_domain_imports"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_d"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CoreDomainRoot.enable(tenant_id="t1", domain_ref="d1").is_missing() is False,
        BoundedContextMapRoot.enable(tenant_id="t1", map_ref="m1").is_missing() is False,
        RobotLifecycleDomainRoot.enable(tenant_id="t1", lifecycle_ref="l1").is_missing() is False,
        AutonomousMachineDomainRoot.enable(tenant_id="t1", autonomy_ref="a1").is_missing() is False,
        PhysicalAIDomainRoot.enable(tenant_id="t1", physical_ai_ref="p1").is_missing() is False,
        MissionDomainRoot.enable(tenant_id="t1", mission_ref="mi1").is_missing() is False,
        FleetDomainRoot.enable(tenant_id="t1", fleet_ref="f1").is_missing() is False,
        DigitalTwinDomainRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        SafetyDomainRoot.enable(tenant_id="t1", safety_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_domain_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p216_b", "via_p215_z", "via_p214_z", "via_p213",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p216_foundation", "never_replace_p216_a_mission", "never_replace_p216_b_strategy",
        "never_replace_p215_z", "never_replace_ai_platform", "never_replace_core_platform",
        "ungated_physical_autonomy_strategy_forbidden", "opaque_safety_strategy_forbidden",
        "module_local_robotics_domain_forbidden", "never_cross_context_aggregate_mutation",
        "never_peer_domain_imports",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/domain")', "/domain/strategy", "/domain/bounded-contexts",
        "/domain/aggregates", "/domain/entities", "/domain/value-objects",
        "/domain/services", "/domain/repositories", "/domain/events",
        "/domain/cqrs", "/domain/microservices", "/domain/integration",
        "/domain/relationships", "/domain/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_DOMAIN.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Robotics Core Domain is missing",
        "Never Supporting Domains are missing",
        "Never Generic Domains are missing",
        "Never Bounded Context Map is missing",
        "Never Aggregates are missing",
        "Never Entities are missing",
        "Never Value Objects are missing",
        "Never Domain Services are missing",
        "Never Repository Boundaries are missing",
        "Never Domain Events are missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-A Mission",
        "Never Replace P216-B Strategy",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "Never Cross-Context Aggregate Mutation",
        "Never Peer Domain Imports",
        "Enterprise Cyber-Physical Intelligence Domain",
        "P216", "P216-A", "P216-B", "P215-Z", "P214-Z", "P216-D",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-C", "adr": 475, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
