"""EIFTP Quality / Governance / DoD (P200-B12) foundation + series validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/226-enterprise-identity-federation-quality-governance-dod.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_QUALITY_GOVERNANCE_DOD.md",
    "docs/architecture/identity/eiftp/QA_ARCHITECTURE.v1.yaml",
    "docs/architecture/identity/eiftp/QA_QUALITY_GATES.v1.yaml",
    "docs/architecture/identity/eiftp/QA_DOD_CHECKLIST.v1.yaml",
    "docs/architecture/identity/eiftp/QA_TRACEABILITY.v1.yaml",
    "docs/architecture/identity/eiftp/QA_TESTING_CATALOG.v1.yaml",
    "docs/architecture/identity/eiftp/QA_SURFACE.v1.yaml",
    "docs/architecture/identity/eiftp/QA_GOVERNANCE.v1.yaml",
    "docs/architecture/identity/eiftp/SERIES_PRODUCTION_READINESS.v1.yaml",
    "backend/contexts/identity_federation/domain/services/federation_quality_platform.py",
    "backend/contexts/identity_federation/infrastructure/observability/federation_quality_metrics.py",
    "backend/contexts/identity_federation/application/commands/qa_commands.py",
    "backend/contexts/identity_federation/application/queries/qa_queries.py",
    "backend/contexts/identity_federation/presentation/qa_router.py",
    "backend/contexts/identity_federation/tests/test_eiftp_quality_governance.py",
]

FORBIDDEN_SIBLING = "backend/contexts/eiftp"

SERIES_VALIDATORS = [
    (
        "P200-B2",
        "contexts.identity_federation.domain.services.eiftp_architecture",
        "validate_architecture_foundation",
    ),
    (
        "P200-B3",
        "contexts.identity_federation.domain.services.eiftp_ddd_strategic",
        "validate_ddd_strategic_foundation",
    ),
    (
        "P200-B4",
        "contexts.identity_federation.domain.services.eiftp_domain_model",
        "validate_domain_model_foundation",
    ),
    (
        "P200-B5",
        "contexts.identity_federation.domain.services.eiftp_federation_engine",
        "validate_federation_engine_foundation",
    ),
    (
        "P200-B6",
        "contexts.identity_federation.domain.services.eiftp_trust_fabric",
        "validate_trust_fabric_foundation",
    ),
    (
        "P200-B7",
        "contexts.identity_federation.domain.services.eiftp_identity_providers",
        "validate_identity_providers_foundation",
    ),
    (
        "P200-B8",
        "contexts.identity_federation.domain.services.eiftp_cross_tenant",
        "validate_cross_tenant_foundation",
    ),
    (
        "P200-B9",
        "contexts.identity_federation.domain.services.eiftp_security_zero_trust",
        "validate_security_zero_trust_foundation",
    ),
    (
        "P200-B10",
        "contexts.identity_federation.domain.services.eiftp_ohs_apis_events_cqrs",
        "validate_ohs_apis_events_cqrs_foundation",
    ),
    (
        "P200-B11",
        "contexts.identity_federation.domain.services.eiftp_ops_deployment",
        "validate_ops_deployment_foundation",
    ),
]


def _import_validator(module_path: str, attr: str):
    import importlib

    mod = importlib.import_module(module_path)
    return getattr(mod, attr)


def validate_quality_governance_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()

    from contexts.identity_federation.domain.services.federation_quality_platform import (
        FederationQualityPlatform,
    )

    platform = FederationQualityPlatform()
    gates = platform.quality_gates().get("gates") or []
    dod = platform.dod_checklist().get("module_dod") or []
    gate_ids = {g.get("id") for g in gates}
    required_gates = {
        "gate.architecture_validation",
        "gate.unit_tests",
        "gate.security_scan",
        "gate.production_deployment",
    }
    gates_ok = required_gates.issubset(gate_ids) and len(gates) >= 10
    dod_ok = len(dod) >= 15
    qa_router = (
        root / "backend/contexts/identity_federation/presentation/qa_router.py"
    ).read_text(encoding="utf-8")
    router_ok = 'prefix="/federation/qa"' in qa_router

    phase_results: dict[str, bool] = {}
    for phase_id, mod_path, fn_name in SERIES_VALIDATORS:
        fn = _import_validator(mod_path, fn_name)
        result = fn(repo_root=root)
        phase_results[phase_id] = bool(result.get("passed"))

    series_ok = all(phase_results.values())
    b12_local = not missing and not sibling and gates_ok and dod_ok and router_ok
    passed = b12_local and series_ok

    return {
        "prompt": "P200-B12",
        "adr": 226,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "quality_gates": gates_ok,
        "dod_checklist": dod_ok,
        "qa_router": router_ok,
        "series_phases": phase_results,
        "series_core_passed": series_ok,
        "foundation_backlog": [
            "P200-B1.1-D2",
            "P200-B1.Scope",
            "P200-B1.Stakeholders",
            "P200-B1.Principles",
        ],
        "full_foundation_complete": False,
        "foundation_for": "EIFTP_SERIES_COMPLETE",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
