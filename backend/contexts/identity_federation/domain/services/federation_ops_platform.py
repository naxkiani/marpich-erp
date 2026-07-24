"""Federation Ops / Deploy / SRE / DR facade (P200-B11) — not Platform Engineering BC."""
from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml

REPO_ROOT = Path(__file__).resolve().parents[5]


class FederationOpsPlatform:
    """Deploy profile · pipeline · observability · SLO · DR · AI ops signals."""

    def __init__(self) -> None:
        self._incidents: list[dict[str, Any]] = []
        self._dr_drills: list[dict[str, Any]] = []
        self._ai_recommendations: list[dict[str, Any]] = []

    def reset(self) -> None:
        self._incidents.clear()
        self._dr_drills.clear()
        self._ai_recommendations.clear()

    def _load_yaml(self, relative: str) -> dict:
        path = REPO_ROOT / relative
        if not path.exists():
            return {}
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return data if isinstance(data, dict) else {}

    def deployment_profile(self) -> dict:
        arch = self._load_yaml("docs/architecture/identity/eiftp/OPS_ARCHITECTURE.v1.yaml")
        k8s = dict(arch.get("kubernetes") or {})
        return {
            "prompt": "P200-B11",
            "adr": 225,
            "helm_chart": k8s.get(
                "helm_chart", "infrastructure/kubernetes/helm/marpich-iam/"
            ),
            "namespace": k8s.get("namespace", "marpich-iam"),
            "gitops": k8s.get("gitops")
            or {
                "argocd": "infrastructure/argocd/marpich-iam-application.yaml",
                "flux": "infrastructure/fluxcd/marpich-iam-helmrelease.yaml",
            },
            "autoscaling": k8s.get("autoscaling") or ["HPA", "VPA", "cluster_autoscaler"],
            "security": k8s.get("security")
            or [
                "pod_security_restricted",
                "network_policies",
                "mesh_mtls",
                "admission_policy_as_code",
            ],
            "multi_region": True,
            "manual_deploy_forbidden": True,
            "secrets_in_git_forbidden": True,
        }

    def pipeline_profile(self) -> dict:
        arch = self._load_yaml("docs/architecture/identity/eiftp/OPS_ARCHITECTURE.v1.yaml")
        dsc = dict(arch.get("devsecops") or {})
        return {
            "github_workflow": dsc.get(
                "github_workflow",
                ".github/workflows/identity-federation-enterprise.yml",
            ),
            "azure_pipeline": dsc.get(
                "azure_pipeline",
                "infrastructure/azure-pipelines/identity-federation.yml",
            ),
            "stages": dsc.get("stages")
            or [
                "source",
                "build",
                "static_analysis",
                "unit_tests",
                "dependency_scan",
                "secret_scan",
                "container_build",
                "container_scan",
                "integration_tests",
                "artifact_signing",
                "gitops_promote",
                "verify",
                "rollback",
            ],
            "gitops_promote": True,
            "artifact_signing": True,
            "forbidden": dsc.get("forbidden")
            or ["manual_production_kubectl_apply_as_sole_path", "secrets_in_git"],
        }

    def observability_profile(self) -> dict:
        arch = self._load_yaml("docs/architecture/identity/eiftp/OPS_ARCHITECTURE.v1.yaml")
        obs = dict(arch.get("observability") or {})
        return {
            "otel": obs.get(
                "otel", "backend/shared/infrastructure/observability/telemetry.py"
            ),
            "metrics_catalog": obs.get(
                "metrics_catalog",
                "docs/architecture/observability/METRICS_CATALOG.yaml#identity_federation_metrics",
            ),
            "scrape_paths": obs.get("scrape_paths")
            or [
                "/api/v1/federation/metrics",
                "/api/v1/federation/ops/metrics",
            ],
            "dashboards": obs.get("dashboards")
            or [
                "infrastructure/observability/grafana/dashboards/identity-federation.json",
                "infrastructure/observability/grafana/dashboards/identity-federation-trust.json",
            ],
            "alerts": obs.get(
                "alerts",
                "infrastructure/observability/prometheus/alerts/identity-federation.yml",
            ),
            "tracing": "OpenTelemetry → platform Tempo/Jaeger",
            "logging": "structured logging → platform Loki/OpenSearch",
            "not_owned_here": [
                "metrics_tsdb",
                "log_store",
                "trace_backend",
                "alertmanager",
            ],
        }

    def sre_profile(self) -> dict:
        sre_cat = self._load_yaml(
            "docs/architecture/identity/eiftp/OPS_SRE_CATALOG.v1.yaml"
        )
        arch = self._load_yaml("docs/architecture/identity/eiftp/OPS_ARCHITECTURE.v1.yaml")
        sre = dict(arch.get("sre") or {})
        return {
            "slis": sre_cat.get("slis") or [],
            "slos": sre_cat.get("slos")
            or [
                {"id": "slo.availability", "target": sre.get("availability_slo", 0.9999)},
                {"id": "slo.login_p95_ms", "target": sre.get("login_p95_ms", 200)},
                {"id": "slo.token_p95_ms", "target": sre.get("token_p95_ms", 100)},
            ],
            "error_budget": sre_cat.get("error_budget")
            or {
                "policy": "freeze_risky_deploys_when_budget_exhausted",
                "window_days": sre.get("error_budget_period_days", 28),
            },
            "incident_classes": sre_cat.get("incident_classes") or [],
            "runbooks": sre_cat.get("runbooks")
            or [
                "docs/deployment/IDENTITY_FEDERATION_DEPLOYMENT_GUIDE.md",
                "docs/deployment/IDENTITY_FEDERATION_DR_GUIDE.md",
            ],
        }

    def slo_status(self, *, availability_ratio: float | None = None) -> dict:
        profile = self.sre_profile()
        target = 0.9999
        for slo in profile.get("slos") or []:
            if slo.get("id") == "slo.availability":
                target = float(slo.get("target") or target)
                break
        observed = 1.0 if availability_ratio is None else float(availability_ratio)
        exhausted = observed < target
        budget_remaining = 0.0 if exhausted else max(0.0, round(observed - target, 6))
        return {
            "availability_target": target,
            "availability_observed": observed,
            "error_budget_remaining": budget_remaining,
            "error_budget_exhausted": exhausted,
            "freeze_risky_deploys": exhausted,
            "window_days": int(
                (profile.get("error_budget") or {}).get("window_days") or 28
            ),
            "slos": profile.get("slos"),
        }

    def dr_profile(self) -> dict:
        arch = self._load_yaml("docs/architecture/identity/eiftp/OPS_ARCHITECTURE.v1.yaml")
        dr = dict(arch.get("dr") or {})
        return {
            "rpo_minutes": dr.get("rpo_minutes", 5),
            "rto_minutes": dr.get("rto_minutes", 30),
            "runbook": dr.get(
                "runbook", "docs/deployment/IDENTITY_FEDERATION_DR_GUIDE.md"
            ),
            "modes": dr.get("modes") or ["active_passive", "active_active_geo"],
            "checklist": [
                "announce_drill",
                "promote_standby_or_flip_dns",
                "verify_ops_health",
                "replay_outbox",
                "record_drill",
                "document_failback",
            ],
            "drills": list(self._dr_drills),
        }

    def ai_ops_profile(self) -> dict:
        arch = self._load_yaml("docs/architecture/identity/eiftp/OPS_ARCHITECTURE.v1.yaml")
        ai = arch.get("ai_ops") or {}
        if isinstance(ai, list):
            hooks = [x for x in ai if isinstance(x, str)]
        else:
            hooks = list(ai.get("hooks") or [])
        return {
            "hooks": hooks
            or [
                "incident_signal_correlation",
                "capacity_forecast_hooks",
                "log_anomaly_hints",
                "self_healing_recommendations",
            ],
            "inference": "AI Platform via ACL — no embedded LLM",
            "recommendations": list(self._ai_recommendations[-20:]),
        }

    def health(self) -> dict:
        deploy = self.deployment_profile()
        pipe = self.pipeline_profile()
        obs = self.observability_profile()
        checks = {
            "helm_chart_present": (REPO_ROOT / deploy["helm_chart"]).exists(),
            "argocd_present": (
                REPO_ROOT / deploy["gitops"]["argocd"]
            ).exists(),
            "flux_present": (REPO_ROOT / deploy["gitops"]["flux"]).exists(),
            "github_workflow_present": (
                REPO_ROOT / pipe["github_workflow"]
            ).exists(),
            "otel_bootstrap_present": (REPO_ROOT / obs["otel"]).exists(),
            "dr_runbook_present": (
                REPO_ROOT / self.dr_profile()["runbook"]
            ).exists(),
            "alerts_present": (REPO_ROOT / obs["alerts"]).exists(),
        }
        return {
            "status": "healthy" if all(checks.values()) else "degraded",
            "checks": checks,
            "quality_gates": [
                "gitops_required",
                "no_secrets_in_source",
                "distributed_tracing_required",
                "kubernetes_native",
                "multi_region_dr_plan",
                "automatic_rollback_path",
            ],
            "open_incidents": len(
                [i for i in self._incidents if i.get("status") == "open"]
            ),
        }

    def metrics_snapshot(self) -> dict:
        from contexts.identity_federation.infrastructure.observability import (
            federation_ops_metrics,
            federation_protocol_metrics,
            federation_trust_metrics,
        )

        return {
            "ops": federation_ops_metrics.snapshot(),
            "protocol": federation_protocol_metrics.snapshot(),
            "trust": federation_trust_metrics.snapshot(),
            "incidents_total": len(self._incidents),
            "dr_drills_total": len(self._dr_drills),
        }

    def signal_incident(
        self,
        *,
        tenant_id: str,
        incident_class: str,
        severity: str = "medium",
        summary: str = "",
        signals: dict | None = None,
    ) -> dict:
        if not tenant_id:
            raise ValueError("ops.tenant_required")
        entry = {
            "incident_id": str(uuid4()),
            "tenant_id": tenant_id,
            "incident_class": incident_class or "federation_outage",
            "severity": severity,
            "summary": summary,
            "signals": dict(signals or {}),
            "status": "open",
            "recorded_at": datetime.now(UTC).isoformat(),
        }
        self._incidents.append(entry)
        from contexts.identity_federation.infrastructure.observability import (
            federation_ops_metrics,
        )

        federation_ops_metrics.increment("ops_incident_signaled_total")
        return entry

    def record_dr_drill(
        self,
        *,
        tenant_id: str,
        mode: str = "active_passive",
        steps_completed: list[str] | None = None,
        passed: bool = True,
        notes: str = "",
    ) -> dict:
        if not tenant_id:
            raise ValueError("ops.tenant_required")
        entry = {
            "drill_id": str(uuid4()),
            "tenant_id": tenant_id,
            "mode": mode,
            "steps_completed": list(steps_completed or []),
            "passed": passed,
            "notes": notes,
            "recorded_at": datetime.now(UTC).isoformat(),
        }
        self._dr_drills.append(entry)
        from contexts.identity_federation.infrastructure.observability import (
            federation_ops_metrics,
        )

        federation_ops_metrics.increment("ops_dr_drill_total")
        if passed:
            federation_ops_metrics.increment("ops_dr_drill_passed_total")
        return entry

    def recommend_ai_ops(
        self,
        *,
        tenant_id: str,
        context: dict | None = None,
    ) -> dict:
        if not tenant_id:
            raise ValueError("ops.tenant_required")
        ctx = dict(context or {})
        hints: list[str] = []
        if ctx.get("outbox_lag_seconds", 0) > 60:
            hints.append("scale_outbox_dispatcher")
        if ctx.get("error_budget_exhausted"):
            hints.append("freeze_risky_deploys")
        if ctx.get("provider_health") == "down":
            hints.append("failover_secondary_idp_via_integration")
        if not hints:
            hints.append("monitor_slo_window")
        entry = {
            "recommendation_id": str(uuid4()),
            "tenant_id": tenant_id,
            "hints": hints,
            "inference_via": "ai_platform_acl",
            "authz_permit_deny": None,
            "recorded_at": datetime.now(UTC).isoformat(),
        }
        self._ai_recommendations.append(entry)
        from contexts.identity_federation.infrastructure.observability import (
            federation_ops_metrics,
        )

        federation_ops_metrics.increment("ops_ai_recommendation_total")
        return entry

    def catalog(self) -> dict:
        return {
            "prompt": "P200-B11",
            "adr": 225,
            "role": "federation_ops_surface",
            "not": [
                "platform_engineering_bc",
                "observability_platform",
                "secret_store",
                "authorization_pdp",
            ],
            "deployment": self.deployment_profile(),
            "pipeline": self.pipeline_profile(),
            "observability": self.observability_profile(),
            "sre": self.sre_profile(),
            "dr": {k: v for k, v in self.dr_profile().items() if k != "drills"},
            "ai_ops": self.ai_ops_profile(),
            "apis": [
                "/api/v1/federation/ops/surface",
                "/api/v1/federation/ops/deployment",
                "/api/v1/federation/ops/pipeline",
                "/api/v1/federation/ops/observability",
                "/api/v1/federation/ops/slo",
                "/api/v1/federation/ops/dr",
                "/api/v1/federation/ops/health",
                "/api/v1/federation/ops/metrics",
            ],
            "knowledge_graph": {
                "Cluster": "hosts Microservice",
                "Pipeline": "deploys Application",
                "Service": "runs_on Node",
                "Alert": "generated_by Metric",
                "Incident": "resolved_by Runbook",
            },
            "digital_twins": [
                "kubernetes_cluster",
                "cicd_pipeline",
                "service_mesh",
                "infrastructure",
                "deployment",
                "runtime_environment",
            ],
        }

    def surface(self) -> dict:
        return deepcopy(self.catalog())


_platform: FederationOpsPlatform | None = None


def get_federation_ops_platform() -> FederationOpsPlatform:
    global _platform
    if _platform is None:
        _platform = FederationOpsPlatform()
    return _platform


def reset_federation_ops_platform() -> None:
    global _platform
    if _platform is not None:
        _platform.reset()
    _platform = None
