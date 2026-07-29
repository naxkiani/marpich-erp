"""Cyber Security P210-E SIEM foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/367-enterprise-cyber-security-siem.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_SIEM.md",
    "docs/architecture/cyber_security/CYBER_SIEM_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_SIEM_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_SIEM_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_SIEM_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_siem.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_siem_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_siem_acl.py",
    "backend/contexts/cyber_security/application/cs_siem_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/siem_platform",
    "backend/contexts/xdr",
    "backend/contexts/edr",
    "backend/contexts/ndr",
    "backend/contexts/soar_platform",
    "backend/contexts/soc_platform",
    "backend/contexts/security_ops",
    "backend/contexts/cyber_defense",
)


def validate_cs_siem_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_siem_aggregates import (
        CsSiemAiIntelligenceRoot,
        CsSiemAlertGeneratedRoot,
        CsSiemExtensibleDetectionRoot,
        CsSiemHorizontalScaleRoot,
        CsSiemImmutableStorageRoot,
        CsSiemMultiDomainCorrelationRoot,
        CsSiemNormalizationCompleteRoot,
        CsSiemTelemetryIntegrityRoot,
    )
    from contexts.cyber_security.domain.services import cs_platform_siem as siem

    cat = siem.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-E"
        and cat.get("adr") == 367
        and cat.get("sor") == "cyber_security"
        and cat["event_normalization_complete_required"] is True
        and cat["multi_domain_correlation_required"] is True
        and cat["detection_rules_extensible_required"] is True
        and cat["ai_intelligence_required"] is True
        and cat["telemetry_integrity_validation_required"] is True
        and cat["storage_immutable_required"] is True
        and cat["horizontal_scale_required"] is True
        and cat["ingestion_normalization"]["not_incomplete"] is True
        and cat["correlation_engine"]["not_single_domain_only"] is True
        and cat["detection_engine"]["not_non_extensible"] is True
        and cat["ai"]["not_absent"] is True
        and cat["telemetry_collection"]["not_without_integrity"] is True
        and cat["storage"]["not_mutable"] is True
        and cat["scalability"]["not_vertical_only"] is True
        and cat["architecture"]["layer_count"] >= 10
        and cat["telemetry_collection"]["source_count"] >= 20
        and cat["cqrs"]["event_count"] >= 8
        and cat["cursor_outputs"]["count"] >= 20
        and "event_normalization_incomplete" in cat["quality_gates"]["reject_if"]
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
            CsSiemNormalizationCompleteRoot.normalize,
            tenant_id="t1",
            event_ref="e1",
            normalized=False,
        )
        and CsSiemNormalizationCompleteRoot.normalize(
            tenant_id="t1", event_ref="e2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            CsSiemMultiDomainCorrelationRoot.correlate,
            tenant_id="t1",
            correlation_ref="c1",
            multi_domain=False,
        )
        and CsSiemMultiDomainCorrelationRoot.correlate(
            tenant_id="t1", correlation_ref="c2"
        ).is_single_domain_only()
        is False
    )
    checks.append(
        not _bad(
            CsSiemExtensibleDetectionRoot.update,
            tenant_id="t1",
            rule_ref="r1",
            extensible=False,
        )
        and CsSiemExtensibleDetectionRoot.update(
            tenant_id="t1", rule_ref="r2"
        ).is_non_extensible()
        is False
    )
    checks.append(
        not _bad(
            CsSiemAiIntelligenceRoot.enable,
            tenant_id="t1",
            intelligence_ref="a1",
            present=False,
        )
        and CsSiemAiIntelligenceRoot.enable(
            tenant_id="t1", intelligence_ref="a2"
        ).is_absent()
        is False
    )
    checks.append(
        not _bad(
            CsSiemTelemetryIntegrityRoot.validate,
            tenant_id="t1",
            telemetry_ref="tel1",
            integrity_validated=False,
        )
        and CsSiemTelemetryIntegrityRoot.validate(
            tenant_id="t1", telemetry_ref="tel2"
        ).lacks_integrity()
        is False
    )
    checks.append(
        not _bad(
            CsSiemImmutableStorageRoot.bind,
            tenant_id="t1",
            store_ref="s1",
            immutable=False,
        )
        and CsSiemImmutableStorageRoot.bind(
            tenant_id="t1", store_ref="s2"
        ).is_mutable()
        is False
    )
    checks.append(
        not _bad(
            CsSiemHorizontalScaleRoot.enable,
            tenant_id="t1",
            plane_ref="p1",
            horizontal=False,
        )
        and CsSiemHorizontalScaleRoot.enable(
            tenant_id="t1", plane_ref="p2"
        ).is_vertical_only()
        is False
    )
    alert = CsSiemAlertGeneratedRoot.generate(
        tenant_id="t1", alert_ref="al1"
    )
    checks.append("AlertGenerated" in alert.pending_events)
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/cyber_security/infrastructure/acl/cs_siem_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p210_d_soc" in acl_text
        and "via_p210_f_soar" in acl_text
        and "via_p210_g_xdr" in acl_text
        and "ai_intelligence_required" in acl_text
        and "telemetry_integrity_validation_required" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/siem"' in router
        and "/siem/telemetry" in router
        and "/siem/correlation" in router
        and "/siem/storage" in router
        and "/siem/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_SIEM.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never event normalization is incomplete" in law
        and "Never correlation cannot span multiple domains" in law
        and "Never detection rules are not extensible" in law
        and "Never AI intelligence is absent" in law
        and "Never telemetry lacks integrity validation" in law
        and "Never storage is not immutable" in law
        and "Never platform cannot scale horizontally" in law
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
        "prompt": "P210-E",
        "adr": 367,
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
