"""Quantum P215-B mission foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/448-enterprise-quantum-mission.md",
    "docs/architecture/ENTERPRISE_QUANTUM_MISSION.md",
    "docs/architecture/quantum/QUANTUM_MISSION_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_MISSION_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_MISSION_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_MISSION_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_mission.py",
    "backend/contexts/quantum/domain/aggregates/qc_mission_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_mission_acl.py",
    "backend/contexts/quantum/application/qc_mission_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_mission_platform",
    "backend/contexts/quantum_strategy_platform",
    "backend/contexts/quantum_vision_platform",
)
def validate_qc_mission_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_mission_aggregates import MissionRoot, VisionRoot, StrategicScopeRoot, MaturityRoot, RoadmapRoot, BusinessValueRoot, StrategicTwinRoot
    from contexts.quantum.domain.services import qc_platform_mission as catmod
    cat = catmod.catalog()
    catalog_ok = cat["prompt_id"] == "P215-B" and cat["adr"] == 448 and cat["sor"] == "quantum" and cat["capability"] == "CAP-PLT-QC-001" and cat["quantum_mission_framework_present_required"] is True and cat["governance_strategy"]["via_p215_k"] is True and cat["governance_strategy"]["via_p214_y"] is True and cat["builds_on_p215_a"] is True and cat["microservices"]["service_count"] >= 8
    checks = [MissionRoot.enable(tenant_id="t1", mission_ref="m1").is_missing() is False, VisionRoot.enable(tenant_id="t1", vision_ref="v1").is_missing() is False, StrategicScopeRoot.enable(tenant_id="t1", scope_ref="s1").is_missing() is False, MaturityRoot.enable(tenant_id="t1", maturity_ref="mat1").is_missing() is False, RoadmapRoot.enable(tenant_id="t1", roadmap_ref="r1").is_missing() is False, BusinessValueRoot.enable(tenant_id="t1", value_ref="bv1").is_missing() is False, StrategicTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_mission_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in ("via_p215_a", "via_p215_k", "via_p214_y", "via_p214_z", "via_p214_v", "via_p214_t", "via_p212", "via_p213", "module_local_quantum_mission_forbidden"))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in ('@quantum_router.get("/mission")', "/mission/vision", "/mission/scope", "/mission/value", "/mission/maturity", "/mission/roadmap", "/mission/twin", "/mission/readiness"))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_MISSION.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in ("Never Quantum Mission Framework is missing", "Never Quantum Vision Framework is missing", "Never Strategic Intelligence Scope is missing", "Never Quantum Maturity Model is missing", "Never Quantum Roadmap is missing", "Never Business Value Architecture is missing", "Never Quantum Governance Strategy is missing", "Never Quantum Knowledge Strategy is missing", "Never Quantum Workforce Strategy is missing", "Never CQRS architecture is missing", "Never Event architecture is missing", "Never Microservices architecture is missing", "Never API first architecture is missing", "Never Cloud native deployment is missing", "Never Sibling Quantum BC", "P215-A", "P214-Y"))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {"prompt": "P215-B", "adr": 448, "passed": passed, "missing_artifacts": missing, "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum", "capability": "CAP-PLT-QC-001", "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD"}
