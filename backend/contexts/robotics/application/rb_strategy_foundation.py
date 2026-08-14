"""Robotics P216-B strategic architecture foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/474-enterprise-robotics-strategic-architecture.md",
    "docs/architecture/ENTERPRISE_ROBOTICS_STRATEGY.md",
    "docs/architecture/robotics/ROBOTICS_STRATEGY_ARCHITECTURE.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_STRATEGY_CAPABILITIES.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_STRATEGY_DDD_CQRS.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_STRATEGY_SECURITY.v1.yaml",
    "docs/architecture/robotics/ROBOTICS_STRATEGY_VALIDATION.v1.yaml",
    "docs/architecture/robotics/P216_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/robotics/domain/services/rb_platform_strategy.py",
    "backend/contexts/robotics/domain/aggregates/rb_strategy_aggregates.py",
    "backend/contexts/robotics/infrastructure/acl/rb_strategy_acl.py",
    "backend/contexts/robotics/application/rb_strategy_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/robotics_strategy_platform",
    "backend/contexts/robotics_capability_platform",
    "backend/contexts/robotics_operating_framework_platform",
)
def validate_rb_strategy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.robotics.domain.aggregates.rb_strategy_aggregates import (
        StrategicArchitectureRoot, CapabilityModelRoot, OperatingFrameworkRoot,
        ServiceModelRoot, OrganizationalModelRoot, GovernanceModelRoot,
        SecurityModelRoot, DataArchitectureRoot, MaturityModelRoot,
    )
    from contexts.robotics.domain.services import rb_platform_strategy as catmod
    cat = catmod.catalog()
    catalog_ok = (
        cat["prompt_id"] == "P216-B" and cat["adr"] == 474 and cat["sor"] == "robotics"
        and cat["capability"] == "CAP-PLT-RB-001"
        and cat["fabric"] == "meos_robotics_strategic_architecture_framework"
        and cat["foundation_gate"] == "P216" and cat["mission_gate"] == "P216-A"
        and cat["supreme_gate"] == "P215-Z" and cat["ai_gate"] == "P214-Z"
        and cat["robotics_strategic_architecture_present_required"] is True
        and cat["capability_model_present_required"] is True
        and cat["operating_framework_present_required"] is True
        and cat["service_model_present_required"] is True
        and cat["organizational_model_present_required"] is True
        and cat["governance_model_present_required"] is True
        and cat["security_model_present_required"] is True
        and cat["data_architecture_present_required"] is True
        and cat["integration_architecture_present_required"] is True
        and cat["scalability_model_present_required"] is True
        and cat["maturity_model_present_required"] is True
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["microservices"]["service_count"] >= 8
        and cat["architecture_layers"]["layer_count"] == 5
        and cat["capability_model"]["domain_count"] == 7
        and cat["operating_framework"]["layer_count"] == 5
        and cat["service_model"]["service_count"] == 10
        and cat["maturity_model"]["level_count"] == 6
        and cat["never_replace_p216_foundation"] is True
        and cat["never_replace_p216_a_mission"] is True
        and cat["ungated_physical_autonomy_strategy_forbidden"] is True
        and cat["opaque_safety_strategy_forbidden"] is True
        and cat["foundation_for_p216_c"] is True
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )
    checks = [
        StrategicArchitectureRoot.enable(tenant_id="t1", architecture_ref="a1").is_missing() is False,
        CapabilityModelRoot.enable(tenant_id="t1", capability_ref="c1").is_missing() is False,
        OperatingFrameworkRoot.enable(tenant_id="t1", framework_ref="f1").is_missing() is False,
        ServiceModelRoot.enable(tenant_id="t1", service_ref="s1").is_missing() is False,
        OrganizationalModelRoot.enable(tenant_id="t1", org_ref="o1").is_missing() is False,
        GovernanceModelRoot.enable(tenant_id="t1", governance_ref="g1").is_missing() is False,
        SecurityModelRoot.enable(tenant_id="t1", security_ref="sec1").is_missing() is False,
        DataArchitectureRoot.enable(tenant_id="t1", data_ref="d1").is_missing() is False,
        MaturityModelRoot.enable(tenant_id="t1", maturity_ref="m1").is_missing() is False,
    ]
    acl_text = (root / "backend/contexts/robotics/infrastructure/acl/rb_strategy_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in (
        "via_p216", "via_p216_a", "via_p215_z", "via_p214_z", "via_p213", "via_policy_engine", "via_workflow",
        "via_audit", "via_identity", "via_core_platform", "never_replace_p216_foundation",
        "never_replace_p216_a_mission", "never_replace_p215_z", "never_replace_ai_platform",
        "never_replace_core_platform", "ungated_physical_autonomy_strategy_forbidden",
        "opaque_safety_strategy_forbidden", "module_local_robotics_strategy_forbidden",
    ))
    router = (root / "backend/contexts/robotics/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in (
        '@robotics_router.get("/strategy")', "/strategy/layers", "/strategy/capabilities",
        "/strategy/operating-model", "/strategy/services", "/strategy/organization",
        "/strategy/governance", "/strategy/data", "/strategy/integration",
        "/strategy/security", "/strategy/scalability", "/strategy/maturity",
        "/strategy/cqrs", "/strategy/events", "/strategy/readiness",
    ))
    law = (root / "docs/architecture/ENTERPRISE_ROBOTICS_STRATEGY.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in (
        "Never Robotics Strategic Architecture is missing",
        "Never Capability Model is missing",
        "Never Operating Framework is missing",
        "Never Service Model is missing",
        "Never Organizational Model is missing",
        "Never Governance Model is missing",
        "Never Security Model is missing",
        "Never Data Architecture is missing",
        "Never Integration Architecture is missing",
        "Never Scalability Model is missing",
        "Never Maturity Model is missing",
        "Never CQRS architecture is missing",
        "Never Event Architecture is missing",
        "Never Microservices Architecture is missing",
        "Never API First Architecture is missing",
        "Never Cloud Native Deployment is missing",
        "Never Sibling Robotics BC",
        "Never Replace P216 Foundation",
        "Never Replace P216-A Mission",
        "Never Replace Core Platform",
        "Never Replace AI Platform",
        "Never Replace Quantum Supreme (P215-Z)",
        "Never Ungated Physical Autonomy Strategy",
        "Never Opaque Safety Strategy",
        "MEOS Robotics Architecture SHALL",
        "P216", "P216-A", "P215-Z", "P214-Z", "P216-C",
    ))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {
        "prompt": "P216-B", "adr": 474, "passed": passed, "missing_artifacts": missing,
        "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks),
        "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "robotics",
        "capability": "CAP-PLT-RB-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
