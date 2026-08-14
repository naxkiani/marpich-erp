"""AI P214-T Operating System / Control Plane foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/440-enterprise-ai-aios.md",
    "docs/architecture/ENTERPRISE_AI_AIOS.md",
    "docs/architecture/enterprise_ai/AI_AIOS_CAPABILITIES.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIOS_DDD_CQRS.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIOS_SECURITY.v1.yaml",
    "docs/architecture/enterprise_ai/AI_AIOS_VALIDATION.v1.yaml",
    "backend/contexts/ai/domain/services/ai_platform_aios.py",
    "backend/contexts/ai/domain/aggregates/ai_aios_aggregates.py",
    "backend/contexts/ai/infrastructure/acl/ai_aios_acl.py",
    "backend/contexts/ai/application/ai_aios_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/ai_operating_system",
    "backend/contexts/ai_control_plane",
    "backend/contexts/autonomous_intelligence_governance",
    "backend/contexts/ai_orchestration_platform",
    "backend/contexts/ai_capability_management_platform",
    "backend/contexts/ai_command_center_platform",
    "backend/contexts/ai_decision_control_platform",
)


def validate_ai_aios_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.ai.domain.aggregates.ai_aios_aggregates import (
        CapabilityManagementRoot,
        CommandCenterRoot,
        ControlPlaneRoot,
        DecisionControlRoot,
        LifecycleRoot,
        OperatingSystemRoot,
        OrchestrationRoot,
        OSDigitalTwinRoot,
        PolicyControlRoot,
    )
    from contexts.ai.domain.services import ai_platform_aios as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P214-T"
        and cat.get("adr") == 440
        and cat.get("sor") == "ai"
        and cat.get("capability") == "CAP-PLT-AI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "manages, coordinates, governs and evolves all AI capabilities across MEOS" in cat["principle"]
        and cat["domain_model"]["core_domain"] == catmod.CORE_DOMAIN
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 7
        and cat["enterprise_ai_operating_system_present_required"] is True
        and cat["ai_control_plane_present_required"] is True
        and cat["autonomous_orchestration_present_required"] is True
        and cat["ai_command_center_present_required"] is True
        and cat["ai_capability_management_present_required"] is True
        and cat["ai_policy_control_present_required"] is True
        and cat["ai_decision_governance_present_required"] is True
        and cat["ai_lifecycle_management_present_required"] is True
        and cat["ai_knowledge_graph_present_required"] is True
        and cat["ai_digital_twin_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_architecture_present_required"] is True
        and cat["microservices_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_ai_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["sibling_ai_bc_forbidden"] is True
        and cat["deepens_p214_s_control_plane"] is True
        and cat["governed_by_p214_p"] is True
        and cat["orchestration"]["via_p214_q"] is True
        and cat["policy_control"]["via_p214_p"] is True
        and cat["knowledge_graph"]["via_p214_g"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 9
        and cat["cursor_outputs"]["count"] >= 20
        and "enterprise_ai_operating_system_is_missing" in cat["quality_gates"]["reject_if"]
        and "P214-S" in cat["builds_on"]
        and "P214-P" in cat["builds_on"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = [
        not _bad(OperatingSystemRoot.enable, tenant_id="t1", os_ref="os1", present=False) and OperatingSystemRoot.enable(tenant_id="t1", os_ref="os2").is_missing() is False,
        not _bad(ControlPlaneRoot.enable, tenant_id="t1", control_ref="c1", present=False) and ControlPlaneRoot.enable(tenant_id="t1", control_ref="c2").is_missing() is False,
        not _bad(OrchestrationRoot.enable, tenant_id="t1", orchestration_ref="o1", present=False) and OrchestrationRoot.enable(tenant_id="t1", orchestration_ref="o2").is_missing() is False,
        not _bad(CommandCenterRoot.enable, tenant_id="t1", command_ref="cc1", present=False) and CommandCenterRoot.enable(tenant_id="t1", command_ref="cc2").is_missing() is False,
        not _bad(CapabilityManagementRoot.enable, tenant_id="t1", capability_ref="cp1", present=False) and CapabilityManagementRoot.enable(tenant_id="t1", capability_ref="cp2").is_missing() is False,
        not _bad(PolicyControlRoot.enable, tenant_id="t1", policy_ref="p1", present=False) and PolicyControlRoot.enable(tenant_id="t1", policy_ref="p2").is_missing() is False,
        not _bad(DecisionControlRoot.enable, tenant_id="t1", decision_ref="d1", present=False) and DecisionControlRoot.enable(tenant_id="t1", decision_ref="d2").is_missing() is False,
        not _bad(LifecycleRoot.enable, tenant_id="t1", lifecycle_ref="l1", present=False) and LifecycleRoot.enable(tenant_id="t1", lifecycle_ref="l2").is_missing() is False,
        not _bad(OSDigitalTwinRoot.enable, tenant_id="t1", twin_ref="tw1", present=False) and OSDigitalTwinRoot.enable(tenant_id="t1", twin_ref="tw2").is_missing() is False,
    ]
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/ai/infrastructure/acl/ai_aios_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p214_f" in acl_text
        and "via_p214_g" in acl_text
        and "via_p214_j" in acl_text
        and "via_p214_l" in acl_text
        and "via_p214_m" in acl_text
        and "via_p214_n" in acl_text
        and "via_p214_o" in acl_text
        and "via_p214_p" in acl_text
        and "via_p214_q" in acl_text
        and "via_p214_r" in acl_text
        and "via_p214_s" in acl_text
        and "via_audit_platform" in acl_text
        and "via_policy_engine" in acl_text
        and "module_local_aios_forbidden" in acl_text
    )

    router = (root / "backend/contexts/ai/presentation/router.py").read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/aios")' in router
        and "/aios/readiness" in router
        and "/aios/control-plane" in router
        and "/aios/orchestration" in router
        and "/aios/capabilities" in router
        and "/aios/command-center" in router
        and "/aios/policies" in router
        and "/aios/digital-twin" in router
    )

    law = (root / "docs/architecture/ENTERPRISE_AI_AIOS.md").read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise AI Operating System is missing" in law
        and "Never AI Control Plane is missing" in law
        and "Never Autonomous Orchestration is missing" in law
        and "Never AI Command Center is missing" in law
        and "Never AI Capability Management is missing" in law
        and "Never AI Policy Control is missing" in law
        and "Never AI Decision Governance is missing" in law
        and "Never AI Lifecycle Management is missing" in law
        and "Never AI Knowledge Graph is missing" in law
        and "Never AI Digital Twin is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event architecture is missing" in law
        and "Never Microservices architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust AI security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Sibling AI BC" in law
        and "MEOS AI Operating System Layer" in law
        and "manages, coordinates, governs and evolves all AI capabilities across MEOS" in law
        and "P214-P" in law
        and "P214-S" in law
    )

    passed = not missing and not sibling and catalog_ok and aggregates_ok and acl_ok and router_ok and doc_ok
    return {"prompt": "P214-T", "adr": 440, "passed": passed, "missing_artifacts": missing, "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": aggregates_ok, "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "ai", "capability": "CAP-PLT-AI-001", "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD"}
