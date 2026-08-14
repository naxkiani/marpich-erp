"""Biotechnology P217-C DDD domain architecture foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/502-enterprise-biotechnology-domain-architecture.md",
    "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_DOMAIN.md",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_DOMAIN_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_DOMAIN_AGGREGATES.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_DOMAIN_DDD_CQRS.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_DOMAIN_SECURITY.v1.yaml",
    "docs/architecture/biotechnology/BIOTECHNOLOGY_DOMAIN_VALIDATION.v1.yaml",
    "docs/architecture/biotechnology/P217_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/biotechnology/domain/services/bio_platform_domain.py",
    "backend/contexts/biotechnology/domain/aggregates/bio_domain_aggregates.py",
    "backend/contexts/biotechnology/infrastructure/acl/bio_domain_acl.py",
    "backend/contexts/biotechnology/application/bio_domain_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/biotechnology_domain_platform",
    "backend/contexts/bio_ddd_platform",
    "backend/contexts/bio_intelligence_domain_platform",
)
def validate_bio_domain_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.biotechnology.domain.aggregates.bio_domain_aggregates import (
        CoreDomainRoot, BoundedContextMapRoot, BioIntelligenceDomainRoot,
        SyntheticBiologyDomainRoot, ComputationalBiologyDomainRoot, DigitalHealthDomainRoot,
        BioDigitalTwinDomainRoot, ResearchIntelligenceDomainRoot, BioGovernanceDomainRoot,
    )
    from contexts.biotechnology.domain.services import bio_platform_domain as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P217-C" and cat["adr"] == 502 and cat["sor"] == "biotechnology"
        and cat["capability"] == "CAP-PLT-BIO-001"
        and cat["fabric"] == "meos_biotechnology_domain_architecture_framework"
        and cat["foundation_gate"] == "P217" and cat["mission_gate"] == "P217-A"
        and cat["strategy_gate"] == "P217-B"
        and cat["robotics_gate"] == "P216-Z" and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["biotechnology_core_domain_present_required"] is True
        and cat["supporting_domains_present_required"] is True
        and cat["generic_domains_present_required"] is True
        and cat["bounded_context_map_present_required"] is True
        and cat["aggregates_present_required"] is True
        and cat["entities_present_required"] is True
        and cat["value_objects_present_required"] is True
        and cat["domain_services_present_required"] is True
        and cat["repository_boundaries_present_required"] is True
        and cat["domain_events_present_required"] is True
        and cat["bounded_contexts"]["context_count"] == 7
        and cat["aggregates"]["aggregate_count"] == 7
        and cat["domain_services"]["service_count"] == 14
        and cat["repositories"]["repository_count"] == 7
        and cat["microservices"]["service_count"] == 7
        and cat["events"]["core_event_count"] == 9
        and cat["never_replace_p217_foundation"] is True
        and cat["never_replace_p217_a_mission"] is True
        and cat["never_replace_p217_b_strategy"] is True
        and cat["never_cross_context_aggregate_mutation"] is True
        and cat["never_peer_domain_imports"] is True
        and cat["never_replace_hospital_emr"] is True
        and cat["opaque_bio_safety_strategy_forbidden"] is True
        and cat["foundation_for_p217_d"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CoreDomainRoot.enable(tenant_id="t1", domain_ref="d1").is_missing() is False,
        BoundedContextMapRoot.enable(tenant_id="t1", map_ref="m1").is_missing() is False,
        BioIntelligenceDomainRoot.enable(tenant_id="t1", intelligence_ref="i1").is_missing() is False,
        SyntheticBiologyDomainRoot.enable(tenant_id="t1", synthetic_ref="s1").is_missing() is False,
        ComputationalBiologyDomainRoot.enable(tenant_id="t1", computational_ref="c1").is_missing() is False,
        DigitalHealthDomainRoot.enable(tenant_id="t1", health_ref="h1").is_missing() is False,
        BioDigitalTwinDomainRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        ResearchIntelligenceDomainRoot.enable(tenant_id="t1", research_ref="r1").is_missing() is False,
        BioGovernanceDomainRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/biotechnology/infrastructure/acl/bio_domain_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p217", "via_p217_a", "via_p217_b", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p217_foundation", "never_replace_p217_a_mission", "never_replace_p217_b_strategy",
        "never_replace_p215_z", "never_replace_p216_z", "never_replace_ai_platform",
        "never_replace_core_platform", "opaque_bio_safety_strategy_forbidden",
        "module_local_biotechnology_domain_forbidden", "never_cross_context_aggregate_mutation",
        "never_peer_domain_imports",
    ))
    router = (root / "backend/contexts/biotechnology/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@biotechnology_router.get("/domain")', "/domain/strategy", "/domain/bounded-contexts",
        "/domain/aggregates", "/domain/entities", "/domain/value-objects",
        "/domain/services", "/domain/repositories", "/domain/events",
        "/domain/cqrs", "/domain/microservices", "/domain/integration",
        "/domain/relationships", "/domain/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_BIOTECHNOLOGY_DOMAIN.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Biotechnology Core Domain is missing",
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
        "Never Sibling Biotechnology BC",
        "Never Replace P217 Foundation",
        "Never Replace P217-A Mission",
        "Never Replace P217-B Strategy",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Replace Robotics Supreme (P216-Z)",
        "Never Replace Hospital EMR SoR",
        "Never Replace Laboratory LIMS SoR",
        "Never Replace Pharmacy SoR",
        "Never Skip Genomic Privacy Strategy",
        "Never Skip Ethical Bioengineering Strategy",
        "Never Skip Scientific Integrity Strategy",
        "Never Opaque Bio Safety Strategy",
        "Never Cross-Context Aggregate Mutation",
        "Never Peer Domain Imports",
        "Enterprise Bio Intelligence Domain",
        "P217", "P217-A", "P217-B", "P216-Z", "P215-Z", "P214-Z", "P217-D",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P217-C", "adr": 502, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "biotechnology",
        "capability": "CAP-PLT-BIO-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
