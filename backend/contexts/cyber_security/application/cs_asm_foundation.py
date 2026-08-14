"""Cyber Security P210-I ASM/CTEM foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/369-enterprise-cyber-security-asm-ctem.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_ASM_CTEM.md",
    "docs/architecture/cyber_security/CYBER_ASM_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_ASM_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_ASM_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_ASM_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_asm.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_asm_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_asm_acl.py",
    "backend/contexts/cyber_security/application/cs_asm_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/asm",
    "backend/contexts/ctem",
    "backend/contexts/easm",
    "backend/contexts/caasm",
    "backend/contexts/threat_intel",
    "backend/contexts/siem_platform",
)


def validate_cs_asm_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_asm_aggregates import (
        CsAsmAssetDiscoveryCompleteRoot,
        CsAsmAttackPathRoot,
        CsAsmBusinessContextRiskRoot,
        CsAsmContinuousCtemRoot,
        CsAsmExplainableAiRoot,
        CsAsmExposureDetectedRoot,
        CsAsmExternalSurfaceContinuousRoot,
        CsAsmValidatedRemediationRoot,
    )
    from contexts.cyber_security.domain.services import cs_platform_asm as asm

    cat = asm.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-I"
        and cat.get("adr") == 369
        and cat.get("sor") == "cyber_security"
        and cat["asset_discovery_complete_required"] is True
        and cat["external_attack_surface_continuous_required"] is True
        and cat["risk_prioritization_business_context_required"] is True
        and cat["attack_path_analysis_required"] is True
        and cat["ai_recommendations_explainable_required"] is True
        and cat["remediation_validated_required"] is True
        and cat["ctem_lifecycle_continuous_required"] is True
        and cat["asset_discovery"]["not_incomplete"] is True
        and cat["attack_surface"]["not_non_continuous_easm"] is True
        and cat["risk_prioritization"]["not_ignoring_business_context"] is True
        and cat["attack_path_analysis"]["not_absent"] is True
        and cat["ai"]["not_unexplainable"] is True
        and cat["remediation"]["not_unvalidated"] is True
        and cat["ctem_lifecycle"]["not_one_pass"] is True
        and cat["architecture"]["layer_count"] >= 10
        and cat["asset_discovery"]["asset_type_count"] >= 20
        and cat["cqrs"]["event_count"] >= 8
        and cat["cursor_outputs"]["count"] >= 20
        and "asset_discovery_incomplete" in cat["quality_gates"]["reject_if"]
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
        not _bad(
            CsAsmAssetDiscoveryCompleteRoot.discover,
            tenant_id="t1",
            discovery_ref="d1",
            complete=False,
        )
        and CsAsmAssetDiscoveryCompleteRoot.discover(
            tenant_id="t1", discovery_ref="d2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            CsAsmExternalSurfaceContinuousRoot.monitor,
            tenant_id="t1",
            surface_ref="s1",
            continuous=False,
        )
        and CsAsmExternalSurfaceContinuousRoot.monitor(
            tenant_id="t1", surface_ref="s2"
        ).is_not_continuous()
        is False
    )
    checks.append(
        not _bad(
            CsAsmBusinessContextRiskRoot.calculate,
            tenant_id="t1",
            risk_ref="r1",
            business_context=False,
        )
        and CsAsmBusinessContextRiskRoot.calculate(
            tenant_id="t1", risk_ref="r2"
        ).ignores_business_context()
        is False
    )
    checks.append(
        not _bad(
            CsAsmAttackPathRoot.generate,
            tenant_id="t1",
            path_ref="p1",
            present=False,
        )
        and CsAsmAttackPathRoot.generate(
            tenant_id="t1", path_ref="p2"
        ).is_absent()
        is False
    )
    checks.append(
        not _bad(
            CsAsmExplainableAiRoot.advise,
            tenant_id="t1",
            advisory_ref="a1",
            explainable=False,
        )
        and CsAsmExplainableAiRoot.advise(
            tenant_id="t1", advisory_ref="a2"
        ).is_unexplainable()
        is False
    )
    checks.append(
        not _bad(
            CsAsmValidatedRemediationRoot.execute,
            tenant_id="t1",
            remediation_ref="m1",
            validated=False,
        )
        and CsAsmValidatedRemediationRoot.execute(
            tenant_id="t1", remediation_ref="m2"
        ).cannot_be_validated()
        is False
    )
    checks.append(
        not _bad(
            CsAsmContinuousCtemRoot.run,
            tenant_id="t1",
            cycle_ref="c1",
            continuous=False,
        )
        and CsAsmContinuousCtemRoot.run(
            tenant_id="t1", cycle_ref="c2"
        ).is_not_continuous()
        is False
    )
    exp = CsAsmExposureDetectedRoot.detect(
        tenant_id="t1", exposure_ref="e1", asset_ref="as1"
    )
    checks.append("ExposureDetected" in exp.pending_events)
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/cyber_security/infrastructure/acl/cs_asm_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p210_f_soar" in acl_text
        and "via_p210_h_intel" in acl_text
        and "explainable_required" in acl_text
        and "business_context_required" in acl_text
        and "remediation_validated_required" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/asm"' in router
        and "/asm/attack-surface" in router
        and "/asm/ctem" in router
        and "/asm/attack-paths" in router
        and "/asm/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_ASM_CTEM.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never asset discovery is incomplete" in law
        and "Never external attack surface is not continuously monitored" in law
        and "Never risk prioritization ignores business context" in law
        and "Never attack path analysis is absent" in law
        and "Never AI recommendations are not explainable" in law
        and "Never remediation cannot be validated" in law
        and "Never CTEM lifecycle is not continuous" in law
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
        "prompt": "P210-I",
        "adr": 369,
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
