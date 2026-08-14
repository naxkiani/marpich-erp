"""Cyber Security P210-A Strategy foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/361-enterprise-cyber-security-strategy.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_STRATEGY.md",
    "docs/architecture/cyber_security/CYBER_STRATEGY_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_STRATEGY_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_STRATEGY_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_STRATEGY_VALIDATION.v1.yaml",
    "docs/architecture/cyber_security/P210_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_strategy.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_strategy_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_strategy_acl.py",
    "backend/contexts/cyber_security/application/cs_strategy_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/cyber_defense",
    "backend/contexts/threat_defense",
    "backend/contexts/soc_platform",
    "backend/contexts/siem_platform",
    "backend/contexts/soar_platform",
    "backend/contexts/xdr",
    "backend/contexts/edr",
    "backend/contexts/ndr",
    "backend/contexts/security_ops",
    "backend/contexts/security_operations",
    "backend/contexts/mdr_platform",
    "backend/contexts/cyber_fabric",
)


def validate_cs_strategy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_strategy_aggregates import (
        CsAiSecurityRequiredRoot,
        CsCloudNativeRoot,
        CsEnterpriseSocRoot,
        CsMeasurableControlRoot,
        CsResponseAutomationRoot,
        CsTelemetryCoverageRoot,
        CsThreatIntelIntegratedRoot,
        CsZeroTrustRequiredRoot,
    )
    from contexts.cyber_security.domain.services import (
        cs_platform_strategy as strat,
    )

    cat = strat.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-A"
        and cat.get("adr") == 361
        and cat.get("sor") == "cyber_security"
        and cat["zero_trust_required"] is True
        and cat["enterprise_soc_required"] is True
        and cat["ai_security_required"] is True
        and cat["threat_intelligence_isolated_forbidden"] is True
        and cat["incident_response_manual_only_forbidden"] is True
        and cat["security_telemetry_incomplete_forbidden"] is True
        and cat["security_controls_unmeasurable_forbidden"] is True
        and cat["non_cloud_native_forbidden"] is True
        and cat["principles"]["zero_trust"] is True
        and cat["soc"]["enterprise_scale_required"] is True
        and cat["ai"]["ai_security_required"] is True
        and cat["threat_intelligence"]["not_isolated"] is True
        and cat["soar"]["manual_only_forbidden"] is True
        and cat["event_sources"]["not_incomplete"] is True
        and cat["security"]["not_unmeasurable"] is True
        and cat["security"]["not_non_cloud_native"] is True
        and cat["capability_domains"]["count"] >= 20
        and cat["ddd"]["aggregate_count"] >= 8
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 16
        and "security_architecture_not_zero_trust"
        in cat["quality_gates"]["reject_if"]
        and "soc_not_enterprise_scale" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    zt_bad = _bad(
        CsZeroTrustRequiredRoot.enforce,
        tenant_id="t1",
        plane_ref="p1",
        zero_trust=False,
    )
    zt = CsZeroTrustRequiredRoot.enforce(tenant_id="t1", plane_ref="p2")
    zt_ok = not zt_bad and zt.is_missing_zero_trust() is False

    soc_bad = _bad(
        CsEnterpriseSocRoot.enable,
        tenant_id="t1",
        soc_ref="s1",
        enterprise_scale=False,
    )
    soc = CsEnterpriseSocRoot.enable(tenant_id="t1", soc_ref="s2")
    soc_ok = not soc_bad and soc.is_not_enterprise() is False

    ai_bad = _bad(
        CsAiSecurityRequiredRoot.enable,
        tenant_id="t1",
        surface_ref="a1",
        ai_security=False,
    )
    ai = CsAiSecurityRequiredRoot.enable(tenant_id="t1", surface_ref="a2")
    ai_ok = not ai_bad and ai.is_omitted() is False

    intel_bad = _bad(
        CsThreatIntelIntegratedRoot.bind,
        tenant_id="t1",
        binding_ref="i1",
        isolated=True,
    )
    intel = CsThreatIntelIntegratedRoot.bind(tenant_id="t1", binding_ref="i2")
    intel_ok = not intel_bad and intel.is_isolated() is False

    resp_bad = _bad(
        CsResponseAutomationRoot.enable,
        tenant_id="t1",
        policy_ref="r1",
        manual_only=True,
    )
    resp = CsResponseAutomationRoot.enable(tenant_id="t1", policy_ref="r2")
    resp_ok = not resp_bad and resp.is_manual_only() is False

    tel_bad = _bad(
        CsTelemetryCoverageRoot.declare,
        tenant_id="t1",
        coverage_ref="c1",
        complete=False,
    )
    tel = CsTelemetryCoverageRoot.declare(tenant_id="t1", coverage_ref="c2")
    tel_ok = not tel_bad and tel.is_incomplete() is False

    ctrl_bad = _bad(
        CsMeasurableControlRoot.register,
        tenant_id="t1",
        control_ref="m1",
        measurable=False,
    )
    ctrl = CsMeasurableControlRoot.register(tenant_id="t1", control_ref="m2")
    ctrl_ok = not ctrl_bad and ctrl.is_unmeasurable() is False

    cloud_bad = _bad(
        CsCloudNativeRoot.require,
        tenant_id="t1",
        profile_ref="cn1",
        cloud_native=False,
    )
    cloud = CsCloudNativeRoot.require(tenant_id="t1", profile_ref="cn2")
    cloud_ok = not cloud_bad and cloud.is_non_cloud_native() is False

    aggregates_ok = (
        zt_ok
        and soc_ok
        and ai_ok
        and intel_ok
        and resp_ok
        and tel_ok
        and ctrl_ok
        and cloud_ok
    )

    acl_path = root / "backend/contexts/cyber_security/infrastructure/acl/cs_strategy_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "vendor_sdk_embed_forbidden" in acl_text
        and "ir_lifecycle_owned_by_security_incident" in acl_text
        and "manual_only_forbidden" in acl_text
        and "ai_security_required" in acl_text
        and "observability_is_not_cyber_sor" in acl_text
        and "via_audit_platform" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/strategy"' in router
        and "/strategy/capabilities" in router
        and "/strategy/soc" in router
        and "/strategy/threat-intelligence" in router
        and "/strategy/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_STRATEGY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never invent sibling Cyber Defense / SOC / SIEM / SOAR / XDR BCs"
        in law
        and "Never omit Zero Trust" in law
        and "Never omit enterprise-scale SOC" in law
        and "Never omit AI security" in law
        and "Never isolate threat intelligence" in law
        and "Never leave incident response manual-only" in law
        and "Never leave security telemetry incomplete" in law
        and "Never leave security controls unmeasurable" in law
        and "Never ship non-cloud-native cyber architecture" in law
    )

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and doc_ok
    )
    return {
        "prompt": "P210-A",
        "adr": 361,
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
