"""Quantum P215-C domain architecture foundation validator."""
from __future__ import annotations
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[4]
REQUIRED_ARTIFACTS = [
    "docs/adr/449-enterprise-quantum-domain.md",
    "docs/architecture/ENTERPRISE_QUANTUM_DOMAIN.md",
    "docs/architecture/quantum/QUANTUM_DOMAIN_CAPABILITIES.v1.yaml",
    "docs/architecture/quantum/QUANTUM_DOMAIN_DDD_CQRS.v1.yaml",
    "docs/architecture/quantum/QUANTUM_DOMAIN_SECURITY.v1.yaml",
    "docs/architecture/quantum/QUANTUM_DOMAIN_VALIDATION.v1.yaml",
    "docs/architecture/quantum/P215_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/quantum/domain/services/qc_platform_domain.py",
    "backend/contexts/quantum/domain/aggregates/qc_domain_aggregates.py",
    "backend/contexts/quantum/infrastructure/acl/qc_domain_acl.py",
    "backend/contexts/quantum/application/qc_domain_foundation.py",
]
FORBIDDEN_SIBLINGS = (
    "backend/contexts/quantum_domain_platform",
    "backend/contexts/quantum_ddd_platform",
    "backend/contexts/quantum_bounded_context_platform",
)
def validate_qc_domain_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)
    from contexts.quantum.domain.aggregates.qc_domain_aggregates import DomainModelRoot, BoundedContextRoot, AggregateArchitectureRoot, ContextMapRoot, DomainEventArchRoot, KnowledgeGraphRoot, DomainTwinRoot
    from contexts.quantum.domain.services import qc_platform_domain as catmod
    cat = catmod.catalog()
    catalog_ok = cat["prompt_id"] == "P215-C" and cat["adr"] == 449 and cat["sor"] == "quantum" and cat["capability"] == "CAP-PLT-QC-001" and cat["quantum_domain_model_present_required"] is True and cat["bounded_contexts"]["context_count"] >= 8 and cat["aggregates"]["aggregate_count"] >= 8 and cat["builds_on_p215_a"] is True and cat["builds_on_p215_b"] is True and cat["governed_by_p215_k"] is True
    checks = [DomainModelRoot.enable(tenant_id="t1", domain_ref="d1").is_missing() is False, BoundedContextRoot.enable(tenant_id="t1", context_ref="c1").is_missing() is False, AggregateArchitectureRoot.enable(tenant_id="t1", aggregate_ref="a1").is_missing() is False, ContextMapRoot.enable(tenant_id="t1", map_ref="m1").is_missing() is False, DomainEventArchRoot.enable(tenant_id="t1", event_ref="e1").is_missing() is False, KnowledgeGraphRoot.enable(tenant_id="t1", graph_ref="g1").is_missing() is False, DomainTwinRoot.enable(tenant_id="t1", twin_ref="tw1").is_missing() is False]
    acl_text = (root / "backend/contexts/quantum/infrastructure/acl/qc_domain_acl.py").read_text(encoding="utf-8")
    acl_ok = all(x in acl_text for x in ("via_p215_a", "via_p215_b", "via_p215_k", "via_p214_z", "via_p214_v", "via_p214_t", "via_p213", "via_p212", "module_local_quantum_domain_forbidden"))
    router = (root / "backend/contexts/quantum/presentation/router.py").read_text(encoding="utf-8")
    router_ok = all(x in router for x in ('@quantum_router.get("/domain")', "/domain/strategic-map", "/domain/bounded-contexts", "/domain/aggregates", "/domain/context-map", "/domain/knowledge-graph", "/domain/digital-twin", "/domain/readiness"))
    law = (root / "docs/architecture/ENTERPRISE_QUANTUM_DOMAIN.md").read_text(encoding="utf-8")
    doc_ok = all(x in law for x in ("Never Strategic DDD Model is missing", "Never Tactical DDD Model is missing", "Never Quantum Domain Model is missing", "Never Bounded Context Architecture is missing", "Never Aggregate Architecture is missing", "Never Entity Model is missing", "Never Value Object Model is missing", "Never Domain Event Architecture is missing", "Never Context Mapping is missing", "Never Microservice Boundaries are missing", "Never CQRS architecture is missing", "Never Event Sourcing architecture is missing", "Never Knowledge Graph Model is missing", "Never Digital Twin Model is missing", "Never Sibling Quantum BC", "P215-A", "P215-B"))
    passed = not missing and not sibling and catalog_ok and all(checks) and acl_ok and router_ok and doc_ok
    return {"prompt": "P215-C", "adr": 449, "passed": passed, "missing_artifacts": missing, "forbidden_sibling_present": sibling, "catalog": catalog_ok, "aggregates": all(checks), "acl": acl_ok, "router": router_ok, "documentation": doc_ok, "sor": "quantum", "capability": "CAP-PLT-QC-001", "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD"}
