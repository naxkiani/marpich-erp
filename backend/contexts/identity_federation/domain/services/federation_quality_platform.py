"""Federation Quality / Governance / DoD facade (P200-B12) — not a QA Platform BC."""
from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml

REPO_ROOT = Path(__file__).resolve().parents[5]


class FederationQualityPlatform:
    """Quality gates · DoD · traceability · readiness · release certification."""

    def __init__(self) -> None:
        self._assessments: list[dict[str, Any]] = []
        self._gate_results: list[dict[str, Any]] = []
        self._certificates: list[dict[str, Any]] = []

    def reset(self) -> None:
        self._assessments.clear()
        self._gate_results.clear()
        self._certificates.clear()

    def _load_yaml(self, relative: str) -> dict:
        path = REPO_ROOT / relative
        if not path.exists():
            return {}
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return data if isinstance(data, dict) else {}

    def architecture(self) -> dict:
        return self._load_yaml(
            "docs/architecture/identity/eiftp/QA_ARCHITECTURE.v1.yaml"
        )

    def quality_gates(self) -> dict:
        data = self._load_yaml(
            "docs/architecture/identity/eiftp/QA_QUALITY_GATES.v1.yaml"
        )
        return {
            "gates": data.get("gates") or [],
            "reject_if": data.get("reject_if") or [],
            "results": list(self._gate_results[-50:]),
        }

    def dod_checklist(self) -> dict:
        data = self._load_yaml(
            "docs/architecture/identity/eiftp/QA_DOD_CHECKLIST.v1.yaml"
        )
        return {
            "module_dod": data.get("module_dod") or [],
            "series_dod": data.get("series_dod") or [],
            "foundation_backlog": data.get("foundation_backlog") or [],
            "assessments": list(self._assessments[-50:]),
        }

    def traceability(self) -> dict:
        return self._load_yaml(
            "docs/architecture/identity/eiftp/QA_TRACEABILITY.v1.yaml"
        )

    def testing_catalog(self) -> dict:
        return self._load_yaml(
            "docs/architecture/identity/eiftp/QA_TESTING_CATALOG.v1.yaml"
        )

    def governance(self) -> dict:
        return self._load_yaml(
            "docs/architecture/identity/eiftp/QA_GOVERNANCE.v1.yaml"
        )

    def compliance_validation(self) -> dict:
        gov = self.governance()
        frameworks = list(gov.get("compliance_frameworks") or [])
        return {
            "frameworks": [
                {
                    "id": f,
                    "status": "evidence_hooks_ready",
                    "owner": "compliance_platform",
                    "federation_role": "publish_control_evidence_events",
                }
                for f in frameworks
            ],
            "ai_quality": gov.get("ai_quality") or {},
            "authz_permit_deny": None,
        }

    def series_phase_validators(self, *, repo_root: Path | None = None) -> dict:
        root = repo_root or REPO_ROOT
        from contexts.identity_federation.domain.services.eiftp_architecture import (
            validate_architecture_foundation,
        )
        from contexts.identity_federation.domain.services.eiftp_cross_tenant import (
            validate_cross_tenant_foundation,
        )
        from contexts.identity_federation.domain.services.eiftp_ddd_strategic import (
            validate_ddd_strategic_foundation,
        )
        from contexts.identity_federation.domain.services.eiftp_domain_model import (
            validate_domain_model_foundation,
        )
        from contexts.identity_federation.domain.services.eiftp_federation_engine import (
            validate_federation_engine_foundation,
        )
        from contexts.identity_federation.domain.services.eiftp_identity_providers import (
            validate_identity_providers_foundation,
        )
        from contexts.identity_federation.domain.services.eiftp_ohs_apis_events_cqrs import (
            validate_ohs_apis_events_cqrs_foundation,
        )
        from contexts.identity_federation.domain.services.eiftp_ops_deployment import (
            validate_ops_deployment_foundation,
        )
        from contexts.identity_federation.domain.services.eiftp_security_zero_trust import (
            validate_security_zero_trust_foundation,
        )
        from contexts.identity_federation.domain.services.eiftp_trust_fabric import (
            validate_trust_fabric_foundation,
        )

        phases = {
            "P200-B2": validate_architecture_foundation(repo_root=root),
            "P200-B3": validate_ddd_strategic_foundation(repo_root=root),
            "P200-B4": validate_domain_model_foundation(repo_root=root),
            "P200-B5": validate_federation_engine_foundation(repo_root=root),
            "P200-B6": validate_trust_fabric_foundation(repo_root=root),
            "P200-B7": validate_identity_providers_foundation(repo_root=root),
            "P200-B8": validate_cross_tenant_foundation(repo_root=root),
            "P200-B9": validate_security_zero_trust_foundation(repo_root=root),
            "P200-B10": validate_ohs_apis_events_cqrs_foundation(repo_root=root),
            "P200-B11": validate_ops_deployment_foundation(repo_root=root),
        }
        return phases

    def production_readiness(self, *, repo_root: Path | None = None) -> dict:
        root = repo_root or REPO_ROOT
        from contexts.identity_federation.domain.services.eiftp_quality_governance import (
            validate_quality_governance_foundation,
        )

        b12 = validate_quality_governance_foundation(repo_root=root)
        phase_pass = dict(b12.get("series_phases") or {})
        core_ok = bool(b12.get("passed"))
        readiness = self._load_yaml(
            "docs/architecture/identity/eiftp/SERIES_PRODUCTION_READINESS.v1.yaml"
        )
        backlog = list(
            readiness.get("foundation_backlog")
            or b12.get("foundation_backlog")
            or []
        )
        return {
            "prompt": "P200-B12",
            "adr": 226,
            "core_series_passed": core_ok,
            "phase_results": phase_pass,
            "b12": {
                "passed": b12.get("passed"),
                "verdict": b12.get("verdict"),
            },
            "foundation_backlog": backlog,
            "full_foundation_complete": False,
            "api_prefixes": readiness.get("api_prefixes") or [],
            "hard_boundaries": readiness.get("hard_boundaries") or [],
            "verdict": "ENTERPRISE_GRADE" if core_ok else "BELOW_THRESHOLD",
            "series_status": (
                "core_series_complete_with_foundation_backlog"
                if core_ok
                else "core_series_incomplete"
            ),
            "certificates": list(self._certificates[-20:]),
        }

    def metrics_snapshot(self) -> dict:
        from contexts.identity_federation.infrastructure.observability import (
            federation_ops_metrics,
            federation_quality_metrics,
        )

        return {
            "quality": federation_quality_metrics.snapshot(),
            "ops": federation_ops_metrics.snapshot(),
            "assessments_total": len(self._assessments),
            "certificates_total": len(self._certificates),
        }

    def record_assessment(
        self,
        *,
        tenant_id: str,
        assessor: str = "ci",
        checklist_ids: list[str] | None = None,
        passed: bool = True,
        notes: str = "",
    ) -> dict:
        if not tenant_id:
            raise ValueError("qa.tenant_required")
        dod = self.dod_checklist()
        ids = checklist_ids or [i["id"] for i in dod.get("module_dod") or []]
        entry = {
            "assessment_id": str(uuid4()),
            "tenant_id": tenant_id,
            "assessor": assessor,
            "checklist_ids": ids,
            "passed": passed,
            "notes": notes,
            "recorded_at": datetime.now(UTC).isoformat(),
        }
        self._assessments.append(entry)
        from contexts.identity_federation.infrastructure.observability import (
            federation_quality_metrics,
        )

        federation_quality_metrics.increment("qa_assessment_total")
        return entry

    def evaluate_gate(
        self,
        *,
        tenant_id: str,
        gate_id: str,
        evidence: dict | None = None,
        passed: bool | None = None,
    ) -> dict:
        if not tenant_id:
            raise ValueError("qa.tenant_required")
        if not gate_id:
            raise ValueError("qa.gate_id_required")
        gates = {g["id"]: g for g in self.quality_gates().get("gates") or []}
        if gate_id not in gates:
            raise ValueError(f"qa.gate_unknown:{gate_id}")
        gate = gates[gate_id]
        ok = bool(passed) if passed is not None else bool((evidence or {}).get("ok", True))
        entry = {
            "evaluation_id": str(uuid4()),
            "tenant_id": tenant_id,
            "gate_id": gate_id,
            "blocking": bool(gate.get("blocking", True)),
            "passed": ok,
            "acceptance": gate.get("acceptance"),
            "evidence": dict(evidence or {}),
            "recorded_at": datetime.now(UTC).isoformat(),
        }
        self._gate_results.append(entry)
        from contexts.identity_federation.infrastructure.observability import (
            federation_quality_metrics,
        )

        federation_quality_metrics.increment("qa_gate_evaluate_total")
        if not ok:
            federation_quality_metrics.increment("qa_gate_blocked_total")
        return entry

    def certify_release(
        self,
        *,
        tenant_id: str,
        version: str,
        boards_approved: list[str] | None = None,
        require_core_series: bool = True,
    ) -> dict:
        if not tenant_id:
            raise ValueError("qa.tenant_required")
        readiness = self.production_readiness()
        boards = boards_approved or [
            "arb",
            "srb",
            "apigb",
            "aigb",
            "rgb",
        ]
        required = {"arb", "srb", "rgb"}
        boards_ok = required.issubset(set(boards))
        series_ok = readiness["core_series_passed"] if require_core_series else True
        passed = boards_ok and series_ok
        entry = {
            "certificate_id": str(uuid4()),
            "tenant_id": tenant_id,
            "version": version or "0.0.0",
            "boards_approved": boards,
            "core_series_passed": series_ok,
            "passed": passed,
            "gitops_promote_allowed": passed,
            "authz_permit_deny": None,
            "recorded_at": datetime.now(UTC).isoformat(),
            "verdict": "CERTIFIED" if passed else "REJECTED",
        }
        self._certificates.append(entry)
        from contexts.identity_federation.infrastructure.observability import (
            federation_quality_metrics,
        )

        federation_quality_metrics.increment("qa_release_certify_total")
        if passed:
            federation_quality_metrics.increment("qa_release_certify_passed_total")
        return entry

    def catalog(self) -> dict:
        arch = self.architecture()
        return {
            "prompt": "P200-B12",
            "adr": 226,
            "role": "federation_quality_governance_dod",
            "not": [
                "qa_platform_bc",
                "compliance_platform",
                "audit_platform",
                "authorization_pdp",
            ],
            "domains": arch.get("domains"),
            "platform_reuse": arch.get("platform_reuse"),
            "gates_count": len(self.quality_gates().get("gates") or []),
            "module_dod_count": len(self.dod_checklist().get("module_dod") or []),
            "apis": [
                "/api/v1/federation/qa/surface",
                "/api/v1/federation/qa/gates",
                "/api/v1/federation/qa/dod",
                "/api/v1/federation/qa/traceability",
                "/api/v1/federation/qa/testing",
                "/api/v1/federation/qa/governance",
                "/api/v1/federation/qa/compliance",
                "/api/v1/federation/qa/readiness",
                "/api/v1/federation/qa/metrics",
            ],
            "series_closeout": True,
        }

    def surface(self) -> dict:
        return deepcopy(self.catalog())


_platform: FederationQualityPlatform | None = None


def get_federation_quality_platform() -> FederationQualityPlatform:
    global _platform
    if _platform is None:
        _platform = FederationQualityPlatform()
    return _platform


def reset_federation_quality_platform() -> None:
    global _platform
    if _platform is not None:
        _platform.reset()
    _platform = None
