"""Space P218-P Security Intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/542-enterprise-space-intelligence-security.md",
    "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_SECURITY.md",
    "docs/architecture/space/SECURITY_ARCHITECTURE.v1.yaml",
    "docs/architecture/space/SECURITY_LIFECYCLE.v1.yaml",
    "docs/architecture/space/SECURITY_DDD_CQRS.v1.yaml",
    "docs/architecture/space/SECURITY_CONTROLS.v1.yaml",
    "docs/architecture/space/SECURITY_VALIDATION.v1.yaml",
    "docs/architecture/space/P218_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/space/domain/services/sp_platform_security.py",
    "backend/contexts/space/domain/aggregates/sp_security_aggregates.py",
    "backend/contexts/space/infrastructure/acl/sp_security_acl.py",
    "backend/contexts/space/application/sp_security_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/space_security_platform",
    "backend/contexts/space_cybersecurity_bc",
    "backend/contexts/orbital_defense_bc",
)


def validate_sp_security_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.space.domain.aggregates.sp_security_aggregates import (
        AutonomousSecurityRoot, CybersecurityRoot, OrbitalDefenseRoot,
        SatelliteSecurityRoot, SecurityDigitalTwinRoot, SecurityGovernanceRoot,
        SecurityKnowledgeGraphRoot, SecurityPlatformRoot, ThreatIntelligenceRoot,
    )
    from contexts.space.domain.services import sp_platform_security as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P218-P" and cat["adr"] == 542 and cat["sor"] == "space"
        and cat["capability"] == "CAP-PLT-SP-001"
        and cat["fabric"] == "meos_space_security_intelligence_fabric"
        and cat["foundation_gate"] == "P218" and cat["mission_gate"] == "P218-A"
        and cat["strategy_gate"] == "P218-B" and cat["domain_gate"] == "P218-C"
        and cat["infrastructure_gate"] == "P218-D" and cat["space_ai_gate"] == "P218-E"
        and cat["satellite_gate"] == "P218-F" and cat["orbital_gate"] == "P218-G"
        and cat["communications_gate"] == "P218-H" and cat["navigation_gate"] == "P218-I"
        and cat["mission_intel_gate"] == "P218-J" and cat["scientific_gate"] == "P218-K"
        and cat["exploration_gate"] == "P218-L" and cat["manufacturing_gate"] == "P218-M"
        and cat["resources_gate"] == "P218-N" and cat["logistics_gate"] == "P218-O"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["space_security_platform_present_required"] is True
        and cat["space_cybersecurity_present_required"] is True
        and cat["satellite_security_present_required"] is True
        and cat["space_defense_intelligence_present_required"] is True
        and cat["threat_intelligence_present_required"] is True
        and cat["autonomous_security_operations_present_required"] is True
        and cat["security_digital_twin_present_required"] is True
        and cat["knowledge_graph_present_required"] is True
        and cat["governance_present_required"] is True
        and cat["architecture"]["layer_count"] == 5
        and cat["lifecycle"]["stage_count"] == 10
        and cat["cybersecurity"]["domain_count"] == 8
        and cat["cybersecurity"]["capability_count"] == 8
        and cat["satellite_security"]["protected_asset_count"] == 6
        and cat["satellite_security"]["capability_count"] == 7
        and cat["orbital_defense"]["domain_count"] == 5
        and cat["orbital_defense"]["capability_count"] == 6
        and cat["threat_intelligence"]["threat_category_count"] == 7
        and cat["threat_intelligence"]["ai_capability_count"] == 6
        and cat["security_ai"]["capability_count"] == 8
        and cat["security_ai"]["model_count"] == 5
        and cat["autonomy"]["agent_count"] == 7
        and cat["autonomy"]["function_count"] == 6
        and cat["knowledge_graph"]["entity_count"] == 9
        and cat["knowledge_graph"]["relationship_count"] == 5
        and cat["governance"]["domain_count"] == 8
        and cat["governance"]["approval_gate_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 8
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 10
        and cat["never_replace_p218_o_logistics"] is True
        and cat["never_ungated_autonomous_security_response"] is True
        and cat["never_skip_command_authentication"] is True
        and cat["never_skip_satellite_identity_verification"] is True
        and cat["never_opaque_unexplainable_security_decisions"] is True
        and cat["space_ai_via_p214z_acl_only"] is True
        and cat["no_module_local_llm"] is True
        and cat["foundation_for_p218_q"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        SecurityPlatformRoot.enable(tenant_id="t1", platform_ref="p1").is_missing() is False,
        CybersecurityRoot.enable(tenant_id="t1", cyber_ref="c1").is_missing() is False,
        SatelliteSecurityRoot.enable(tenant_id="t1", satellite_sec_ref="s1").is_missing() is False,
        OrbitalDefenseRoot.enable(tenant_id="t1", orbital_defense_ref="o1").is_missing() is False,
        ThreatIntelligenceRoot.enable(tenant_id="t1", threat_ref="t1").is_missing() is False,
        AutonomousSecurityRoot.enable(tenant_id="t1", autonomy_ref="a1").is_missing() is False,
        SecurityDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        SecurityKnowledgeGraphRoot.enable(tenant_id="t1", kg_ref="kg1").is_missing() is False,
        SecurityGovernanceRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/space/infrastructure/acl/sp_security_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "to_space_foundation", "to_space_mission", "to_space_strategy", "to_space_domain",
        "to_space_infrastructure", "to_space_ai", "to_satellite", "to_orbital",
        "to_communications", "to_navigation", "to_mission_intel", "to_scientific",
        "to_exploration", "to_manufacturing", "to_resources", "to_logistics",
        "to_biotechnology", "to_robotics_supreme", "to_quantum_supreme", "to_master_ai",
        "to_integration", "to_policy_engine", "to_workflow", "to_audit", "to_identity",
        "to_core_platform", "to_enterprise_space", "never_replace_p218_o_logistics",
        "never_ungated_autonomous_security_response", "never_skip_command_authentication",
        "never_skip_satellite_identity_verification", "never_opaque_unexplainable_security_decisions",
        "module_local_security_forbidden", "space_ai_via_p214z_acl_only", "no_module_local_llm",
    ))
    router = (root / "backend/contexts/space/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@space_router.get("/security")', "/security/vision",
        "/security/architecture", "/security/lifecycle", "/security/cybersecurity",
        "/security/satellite", "/security/orbital-defense", "/security/threat-intelligence",
        "/security/security-ai", "/security/autonomy", "/security/digital-twin",
        "/security/knowledge-graph", "/security/observability", "/security/governance",
        "/security/controls", "/security/integration", "/security/deployment",
        "/security/testing", "/security/cqrs", "/security/events",
        "/security/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_SPACE_INTELLIGENCE_SECURITY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Space Security Platform is missing",
        "Never Space Cybersecurity is missing",
        "Never Satellite Security is missing",
        "Never Space Defense Intelligence is missing",
        "Never Threat Intelligence is missing",
        "Never Autonomous Security Operations is missing",
        "Never Security Digital Twin is missing", "Never Knowledge Graph is missing",
        "Never Governance is missing", "Never Security Architecture is missing",
        "Never Observability is missing", "Never Deployment Architecture is missing",
        "Never CQRS architecture is missing", "Never Event Architecture is missing",
        "Never Microservices Architecture is missing", "Never Sibling Space BC",
        "Never Replace P218-O Logistics",
        "Never Module-Local LLM", "Never Ungated Autonomous Security Response",
        "Never Skip Command Authentication", "Never Skip Satellite Identity Verification",
        "Never Opaque Unexplainable Security Decisions",
        "intelligent security ecosystem capable of detecting",
        "P218-P", "P218-Q",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P218-P", "adr": 542, "passed": passed,
        "missing_artifacts": missing, "forbidden_sibling_present": sibling,
        "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok,
        "router": router_ok, "documentation": doc_ok, "sor": "space",
        "capability": "CAP-PLT-SP-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
