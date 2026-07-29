"""Cyber Security P210-D SOC foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/364-enterprise-cyber-security-soc.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_SOC.md",
    "docs/architecture/cyber_security/CYBER_SOC_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_SOC_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_SOC_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_SOC_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_soc.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_soc_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_soc_acl.py",
    "backend/contexts/cyber_security/application/cs_soc_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/soc_platform",
    "backend/contexts/cyber_defense",
    "backend/contexts/siem_platform",
    "backend/contexts/soar_platform",
    "backend/contexts/xdr",
    "backend/contexts/security_ops",
)


def validate_cs_soc_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_soc_aggregates import (
        CsAlertCorrelationRoot,
        CsSoc24x7Root,
        CsSocAiAssistanceRoot,
        CsSocAlertRoot,
        CsSocKnowledgeGraphRoot,
        CsSocMetricsCompleteRoot,
        CsSocResponseAutomationRoot,
        CsThreatHuntingRequiredRoot,
    )
    from contexts.cyber_security.domain.services import cs_platform_soc as soc

    cat = soc.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-D"
        and cat.get("adr") == 364
        and cat.get("sor") == "cyber_security"
        and cat["soc_24x7_required"] is True
        and cat["alert_correlation_required"] is True
        and cat["ai_assistance_required"] is True
        and cat["incident_response_manual_only_forbidden"] is True
        and cat["threat_hunting_required"] is True
        and cat["metrics_incomplete_forbidden"] is True
        and cat["knowledge_graph_integration_required"] is True
        and cat["architecture"]["not_non_24x7"] is True
        and cat["alert_management"]["not_uncorrelated"] is True
        and cat["ai"]["not_absent"] is True
        and cat["incident_management"]["not_manual_only"] is True
        and cat["threat_hunting"]["not_missing"] is True
        and cat["dashboards"]["not_incomplete"] is True
        and cat["knowledge_graph"]["not_absent"] is True
        and cat["architecture"]["layer_count"] >= 10
        and cat["telemetry"]["count"] >= 20
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "soc_not_24x7" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = []
    checks.append(
        (
            not _bad(CsSoc24x7Root.enable, tenant_id="t1", profile_ref="p1", operating_24x7=False)
            and CsSoc24x7Root.enable(tenant_id="t1", profile_ref="p2").is_non_24x7() is False
        )
    )
    checks.append(
        (
            not _bad(CsAlertCorrelationRoot.correlate, tenant_id="t1", alert_ref="a1", correlated=False)
            and CsAlertCorrelationRoot.correlate(tenant_id="t1", alert_ref="a2").cannot_correlate() is False
        )
    )
    checks.append(
        (
            not _bad(CsSocAiAssistanceRoot.enable, tenant_id="t1", surface_ref="s1", ai_assistance=False)
            and CsSocAiAssistanceRoot.enable(tenant_id="t1", surface_ref="s2").is_absent() is False
        )
    )
    checks.append(
        (
            not _bad(CsSocResponseAutomationRoot.enable, tenant_id="t1", policy_ref="r1", manual_only=True)
            and CsSocResponseAutomationRoot.enable(tenant_id="t1", policy_ref="r2").is_manual_only() is False
        )
    )
    checks.append(
        (
            not _bad(CsThreatHuntingRequiredRoot.start, tenant_id="t1", hunt_ref="h1", hunting_enabled=False)
            and CsThreatHuntingRequiredRoot.start(tenant_id="t1", hunt_ref="h2").is_missing() is False
        )
    )
    checks.append(
        (
            not _bad(CsSocMetricsCompleteRoot.register, tenant_id="t1", metrics_ref="m1", complete=False, metric_count=1)
            and CsSocMetricsCompleteRoot.register(tenant_id="t1", metrics_ref="m2").is_incomplete() is False
        )
    )
    checks.append(
        (
            not _bad(CsSocKnowledgeGraphRoot.link, tenant_id="t1", link_ref="k1", integrated=False)
            and CsSocKnowledgeGraphRoot.link(tenant_id="t1", link_ref="k2").is_absent() is False
        )
    )
    alert = CsSocAlertRoot.create(tenant_id="t1", alert_ref="al1")
    checks.append("AlertGenerated" in alert.pending_events)
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/cyber_security/infrastructure/acl/cs_soc_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "ir_lifecycle_owned_by_security_incident" in acl_text
        and "ai_assistance_required" in acl_text
        and "manual_only_forbidden" in acl_text
        and "via_knowledge_graph" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/soc"' in router
        and "/soc/alerts" in router
        and "/soc/hunting" in router
        and "/soc/ai" in router
        and "/soc/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_SOC.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never SOC is not capable of 24×7 operation" in law
        and "Never alerts cannot be correlated" in law
        and "Never AI assistance is absent" in law
        and "Never incident response is manual only" in law
        and "Never threat hunting is missing" in law
        and "Never metrics are incomplete" in law
        and "Never knowledge graph integration is absent" in law
    )

    passed = (
        not missing and not sibling and catalog_ok and aggregates_ok and acl_ok and router_ok and doc_ok
    )
    return {
        "prompt": "P210-D",
        "adr": 364,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "cyber_security",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
