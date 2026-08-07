"""Space P218-N Resource Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/540-enterprise-space-intelligence-resources.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_RESOURCES.md",
    "docs/architecture/space/RESOURCES_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/RESOURCES_LIFECYCLE.v1.yaml",
    "docs/architecture/space/RESOURCES_DDD_CQRS.v1.yaml",
    "docs/architecture/space/RESOURCES_SECURITY.v1.yaml",
    "docs/architecture/space/RESOURCES_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_resources.py",
    "backend/contexts/space/domain/aggregates/sp_resources_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_resources_acl.py",
    "backend/contexts/space/application/sp_resources_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_resource_platform",
    "backend/contexts/isru_platform_bc",
    "backend/contexts/asteroid_mining_bc",
)


def validate_sp_resources_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_resources_aggregates import (
        AsteroidMiningRoot, AutonomousExtractionRoot, IsruPlatformRoot,
        PlanetaryResourceRoot, ResourceAiRoot, ResourceDigitalTwinRoot,
        ResourceGovernanceRoot, ResourceIntelPlatformRoot, ResourceSecurityRoot,
    )
    from contexts.space.domain.services import sp_platform_resources as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-N" and cat["adr"] == 540 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_resource_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["satellite_gate"] == "P218-F" and cat["orbital_gate"] == "P218-G"
        and cat["communications_gate"] == "P218-H" and cat["navigation_gate"] == "P218-I"
        and cat["mission_intel_gate"] == "P218-J" and cat["scientific_gate"] == "P218-K"
        and cat["exploration_gate"] == "P218-L" and cat["manufacturing_gate"] == "P218-M"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["resource_intelligence_present_required"] is True
        and cat["isru_platform_present_required"] is True
        and cat["asteroid_mining_intelligence_present_required"] is True
        and cat["planetary_resource_management_present_required"] is True
        and cat["autonomous_extraction_present_required"] is True
        and cat["resource_ai_present_required"] is True
        and cat["digital_twin_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["stage_count"] == 10
        and cat["isru"]["capability_count"] == 7
        and cat["isru"]["operation_count"] == 7
        and cat["asteroid"]["target_count"] == 4
        and cat["asteroid"]["capability_count"] == 7
        and cat["planetary"]["domain_count"] == 7
        and cat["planetary"]["capability_count"] == 6
        and cat["autonomy"]["agent_count"] == 7
        and cat["autonomy"]["function_count"] == 6
        and cat["resource_ai"]["capability_count"] == 7
        and cat["resource_ai"]["model_count"] == 5
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_m_manufacturing"] is True
        and cat["never_ungated_resource_extraction_authorization"] is True
        and cat["never_skip_resource_environmental_assessment"] is True
        and cat["never_skip_planetary_protection_for_extraction"] is True
        and cat["never_violate_circular_resource_economy_principles"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p218_o"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        ResourceIntelPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        IsruPlatformRoot.enable(tenant_id="t1", isru_ref="i1").is_missing() is False,
        AsteroidMiningRoot.enable(tenant_id="t1", asteroid_ref="a1").is_missing() is False,
        PlanetaryResourceRoot.enable(tenant_id="t1", planetary_ref="pl1").is_missing() is False,
        AutonomousExtractionRoot.enable(tenant_id="t1", autonomy_ref="au1").is_missing() is False,
        ResourceAiRoot.enable(tenant_id="t1", ai_ref="ai1").is_missing() is False,
        ResourceDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        ResourceGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        ResourceSecurityRoot.enable(tenant_id="t1", security_ref="s1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_resources_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_mission_intel", "to_scientific",
        "to_exploration", "to_manufacturing", "to_biotechnology", "to_robotics_supreme",
        "to_quantum_supreme", "to_master_ai", "to_integration", "to_policy_engine",
        "to_workflow", "to_audit", "to_identity", "to_core_platform", "to_enterprise_space",
        "never_replace_p218_m_manufacturing", "never_ungated_resource_extraction_authorization",
        "never_skip_resource_environmental_assessment", "never_skip_planetary_protection_for_extraction",
        "never_violate_circular_resource_economy_principles", "module_local_resources_forbidden",
        "space_ai_via_p214z_acl_only", "no_module_local_llm",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/resources")', "/resources/vision",
        "/resources/architecture", "/resources/lifecycle", "/resources/isru",
        "/resources/asteroid", "/resources/planetary", "/resources/autonomy",
        "/resources/resource-ai", "/resources/digital-twin", "/resources/economy",
        "/resources/observability", "/resources/governance", "/resources/security",
        "/resources/integration", "/resources/deployment", "/resources/testing",
        "/resources/cqrs", "/resources/events", "/resources/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_RESOURCES.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Resource Intelligence is missing",
        "Never ISRU Platform is missing",
        "Never Asteroid Mining Intelligence is missing",
        "Never Planetary Resource Management is missing",
        "Never Autonomous Extraction is missing",
        "Never Resource AI is missing",
        "Never Digital Twin is missing", "Never DDD Model is missing",
        "Never Governance is missing", "Never Security Architecture is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-M Manufacturing",
        "Never Module-Local LLM", "Never Ungated Resource Extraction Authorization",
        "Never Skip Resource Environmental Assessment",
        "Never Skip Planetary Protection for Extraction",
        "Never Violate Circular Resource Economy Principles",
        "intelligent planetary-scale resource platform",
        "P218-N", "P218-O",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-N", "adr": 540, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
