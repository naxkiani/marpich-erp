"""Civilization P219-B strategic architecture foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/555-enterprise-civilization-operating-system-strategy.md",
    "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_STRATEGY.md",
    "docs/architecture/civilization/CIVILIZATION_STRATEGY_CAPABILITIES.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_STRATEGY_BOUNDED_CONTEXTS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_STRATEGY_DDD_CQRS.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_STRATEGY_SECURITY.v1.yaml",
    "docs/architecture/civilization/CIVILIZATION_STRATEGY_VALIDATION.v1.yaml",
    "docs/architecture/civilization/P219_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/civilization/domain/services/civ_platform_strategy.py",
    "backend/contexts/civilization/domain/aggregates/civ_strategy_aggregates.py",
    "backend/contexts/civilization/infrastructure/acl/civ_strategy_acl.py",
    "backend/contexts/civilization/application/civ_strategy_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/civilization_strategy_architecture_platform",
    "backend/contexts/civilization_operating_model_bc",
    "backend/contexts/civilization_capability_model_bc",
)


def validate_civ_strategy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.civilization.domain.aggregates.civ_strategy_aggregates import (
        CapabilityModelRoot, CivilizationStrategyRoot, DigitalTwinOperatingModelRoot,
        GovernanceFrameworkRoot, IntegrationArchitectureRoot, OperatingFrameworkRoot,
        OperatingModelRoot, ServiceFrameworkRoot, TransformationRoot,
    )
    from contexts.civilization.domain.services import civ_platform_strategy as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P219-B" and cat["adr"] == 555 and cat["sor"] == "civilization"
        and cat["capability"] == "CAP-PLT-CIV-001"
        and cat["fabric"] == "meos_civilization_os_strategic_architecture_framework"
        and cat["foundation_gate"] == "P219" and cat["mission_gate"] == "P219-A"
        and cat["intelligence_nexus_gate"] == "P218-Z" and cat["space_gate"] == "P218"
        and cat["bio_gate"] == "P217-Z" and cat["robotics_gate"] == "P216-Z"
        and cat["quantum_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["civilization_strategic_architecture_present_required"] is True
        and cat["enterprise_capability_model_present_required"] is True
        and cat["civilization_operating_model_present_required"] is True
        and cat["civilization_service_framework_present_required"] is True
        and cat["governance_framework_present_required"] is True
        and cat["operating_framework_present_required"] is True
        and cat["digital_twin_operating_model_present_required"] is True
        and cat["meos_integration_architecture_present_required"] is True
        and cat["evolution_model_present_required"] is True
        and cat["architecture_layers"]["layer_count"] == 5
        and cat["capability_model"]["domain_count"] == 8
        and cat["operating_model"]["layer_count"] == 4
        and cat["service_framework"]["category_count"] == 5
        and cat["operating_framework"]["cycle_step_count"] == 7
        and cat["governance"]["domain_count"] == 6
        and cat["digital_twin"]["representation_count"] == 7
        and cat["bounded_contexts"]["context_count"] == 6
        and cat["microservices"]["service_count"] == 10
        and cat["events"]["core_event_count"] == 8
        and cat["never_replace_p219_foundation"] is True
        and cat["never_replace_p219_a_mission"] is True
        and cat["never_replace_space"] is True
        and cat["never_replace_p218_z_intelligence_nexus"] is True
        and cat["never_merge_p218_t_space_civilization"] is True
        and cat["never_opaque_unexplainable_civilization_architecture_decisions"] is True
        and cat["never_ungated_civilization_decision_architecture"] is True
        and cat["never_skip_human_authority_architecture"] is True
        and cat["foundation_for_p219_c"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        CivilizationStrategyRoot.enable(tenant_id="t1", strategy_ref="s1").is_missing() is False,
        CapabilityModelRoot.enable(tenant_id="t1", capability_ref="c1").is_missing() is False,
        OperatingModelRoot.enable(tenant_id="t1", operating_ref="o1").is_missing() is False,
        ServiceFrameworkRoot.enable(tenant_id="t1", service_ref="sv1").is_missing() is False,
        GovernanceFrameworkRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        OperatingFrameworkRoot.enable(tenant_id="t1", framework_ref="f1").is_missing() is False,
        DigitalTwinOperatingModelRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False,
        TransformationRoot.enable(tenant_id="t1", transformation_ref="tr1").is_missing() is False,
        IntegrationArchitectureRoot.enable(tenant_id="t1", integration_ref="i1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/civilization/infrastructure/acl/civ_strategy_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p219", "via_p219_a", "via_p218_z", "via_p218", "via_p217", "via_p216_z", "via_p215_z", "via_p214_z",
        "via_policy_engine", "via_workflow", "via_audit", "via_identity", "via_core_platform",
        "never_replace_p219_foundation", "never_replace_p219_a_mission",
        "never_replace_p218_z_intelligence_nexus", "never_replace_space",
        "never_merge_p218_t_space_civilization",
        "never_opaque_unexplainable_civilization_architecture_decisions",
        "never_ungated_civilization_decision_architecture",
        "never_skip_human_authority_architecture",
        "never_skip_ethical_civilization_governance_architecture",
        "never_violate_human_sovereignty_architecture",
        "module_local_civilization_strategy_forbidden",
    ))
    router = (root / "backend/contexts/civilization/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@civilization_router.get("/strategy")', "/strategy/layers", "/strategy/capabilities",
        "/strategy/operating-model", "/strategy/services", "/strategy/operating-framework",
        "/strategy/governance", "/strategy/digital-twin", "/strategy/integration",
        "/strategy/security", "/strategy/roadmap", "/strategy/cqrs",
        "/strategy/events", "/strategy/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_CIVILIZATION_OPERATING_SYSTEM_STRATEGY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Civilization Strategic Architecture is missing",
        "Never Enterprise Capability Model is missing",
        "Never Civilization Operating Model is missing",
        "Never Civilization Service Framework is missing",
        "Never Governance Framework is missing",
        "Never Operating Framework is missing",
        "Never Digital Twin Operating Model is missing",
        "Never MEOS Integration Architecture is missing",
        "Never Evolution Model is missing",
        "Never Replace P219 Foundation",
        "Never Replace P219-A Mission",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace P215-Z Quantum",
        "Never Replace P216-Z Robotics",
        "Never Replace P217 Biotechnology",
        "Never Replace P218 Space",
        "Never Replace P218-Z Intelligence Nexus",
        "Never Merge P218-T Space Civilization Phase",
        "Never Opaque Unexplainable Civilization Architecture Decisions",
        "Never Ungated Civilization Decision Architecture",
        "Never Skip Human Authority Architecture",
        "Never Skip Ethical Civilization Governance Architecture",
        "Never Violate Human Sovereignty Architecture",
        "unified enterprise framework where",
        "P219-C",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P219-B", "adr": 555, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "civilization",
        "capability": "CAP-PLT-CIV-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
