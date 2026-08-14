"""Cyber Security P210-B Mission/Vision/Scope foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/362-enterprise-cyber-security-mission-vision-scope.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_MISSION_VISION_SCOPE.md",
    "docs/architecture/cyber_security/CYBER_MVS_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_MVS_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_MVS_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_MVS_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_mission_scope.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_mission_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_mission_acl.py",
    "backend/contexts/cyber_security/application/cs_mission_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/cyber_defense",
    "backend/contexts/soc_platform",
    "backend/contexts/siem_platform",
    "backend/contexts/soar_platform",
    "backend/contexts/xdr",
    "backend/contexts/edr",
    "backend/contexts/ndr",
    "backend/contexts/security_ops",
)


def validate_cs_mission_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_mission_aggregates import (
        CsAiSecurityPresentRoot,
        CsDomainsUnifiedRoot,
        CsKpiRegisterRoot,
        CsMissionMeasurableRoot,
        CsObjectivesMeosAlignedRoot,
        CsScopeCompleteRoot,
        CsVisionEnterpriseScaleRoot,
        CsZeroTrustPresentRoot,
    )
    from contexts.cyber_security.domain.services import (
        cs_platform_mission_scope as mscope,
    )

    cat = mscope.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-B"
        and cat.get("adr") == 362
        and cat.get("sor") == "cyber_security"
        and cat["mission_measurable_required"] is True
        and cat["vision_enterprise_scale_required"] is True
        and cat["enterprise_scope_complete_required"] is True
        and cat["security_domains_fragmented_forbidden"] is True
        and cat["zero_trust_absent_forbidden"] is True
        and cat["ai_security_omitted_forbidden"] is True
        and cat["strategic_objectives_meos_aligned_required"] is True
        and cat["mission"]["measurable"] is True
        and cat["vision"]["enterprise_scale"] is True
        and cat["enterprise_scope"]["not_incomplete"] is True
        and cat["security_domains"]["not_fragmented"] is True
        and cat["operating_principles"]["not_absent_zero_trust"] is True
        and cat["operating_principles"]["not_ai_omitted"] is True
        and cat["strategic_objectives"]["meos_aligned"] is True
        and cat["enterprise_scope"]["count"] >= 20
        and cat["security_domains"]["count"] >= 15
        and cat["ddd"]["aggregate_count"] >= 8
        and cat["cqrs"]["event_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 20
        and "mission_not_measurable" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    m_bad = _bad(
        CsMissionMeasurableRoot.publish,
        tenant_id="t1",
        mission_ref="m1",
        measurable=False,
    )
    mission = CsMissionMeasurableRoot.publish(tenant_id="t1", mission_ref="m2")
    m_ok = not m_bad and mission.is_unmeasurable() is False

    v_bad = _bad(
        CsVisionEnterpriseScaleRoot.publish,
        tenant_id="t1",
        vision_ref="v1",
        enterprise_scale=False,
    )
    vision = CsVisionEnterpriseScaleRoot.publish(tenant_id="t1", vision_ref="v2")
    v_ok = not v_bad and vision.is_non_enterprise() is False

    s_bad = _bad(
        CsScopeCompleteRoot.declare,
        tenant_id="t1",
        scope_ref="s1",
        complete=False,
        item_count=5,
    )
    scope = CsScopeCompleteRoot.declare(tenant_id="t1", scope_ref="s2")
    s_ok = not s_bad and scope.is_incomplete() is False

    d_bad = _bad(
        CsDomainsUnifiedRoot.register,
        tenant_id="t1",
        map_ref="d1",
        fragmented=True,
        domain_count=3,
    )
    domains = CsDomainsUnifiedRoot.register(tenant_id="t1", map_ref="d2")
    d_ok = not d_bad and domains.is_fragmented() is False

    z_bad = _bad(
        CsZeroTrustPresentRoot.adopt,
        tenant_id="t1",
        principle_ref="z1",
        zero_trust=False,
    )
    zt = CsZeroTrustPresentRoot.adopt(tenant_id="t1", principle_ref="z2")
    z_ok = not z_bad and zt.is_absent() is False

    a_bad = _bad(
        CsAiSecurityPresentRoot.enable,
        tenant_id="t1",
        surface_ref="a1",
        ai_security=False,
    )
    ai = CsAiSecurityPresentRoot.enable(tenant_id="t1", surface_ref="a2")
    a_ok = not a_bad and ai.is_omitted() is False

    o_bad = _bad(
        CsObjectivesMeosAlignedRoot.align,
        tenant_id="t1",
        register_ref="o1",
        aligned=False,
    )
    obj = CsObjectivesMeosAlignedRoot.align(tenant_id="t1", register_ref="o2")
    o_ok = not o_bad and obj.is_misaligned() is False

    kpi = CsKpiRegisterRoot.register(tenant_id="t1", kpi_ref="k1")
    kpi_ok = "KpiRegistered" in kpi.pending_events

    aggregates_ok = m_ok and v_ok and s_ok and d_ok and z_ok and a_ok and o_ok and kpi_ok

    acl_path = root / "backend/contexts/cyber_security/infrastructure/acl/cs_mission_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "ir_lifecycle_owned_by_security_incident" in acl_text
        and "ai_security_required" in acl_text
        and "via_p210_a_strategy" in acl_text
        and "via_audit_platform" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/mission"' in router
        and "/mission/scope" in router
        and "/mission/security-domains" in router
        and "/mission/kpis" in router
        and "/mission/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_MISSION_VISION_SCOPE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never mission is absent or unmeasurable" in law
        and "Never vision is not enterprise-scale" in law
        and "Never enterprise scope is incomplete" in law
        and "Never security domains are fragmented" in law
        and "Never Zero Trust is absent" in law
        and "Never AI security is omitted" in law
        and "Never strategic objectives are misaligned with MEOS" in law
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
        "prompt": "P210-B",
        "adr": 362,
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
