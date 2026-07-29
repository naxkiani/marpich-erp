"""Cyber Security P210-G XDR/EDR/NDR foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/366-enterprise-cyber-security-xdr.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_XDR.md",
    "docs/architecture/cyber_security/CYBER_XDR_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_XDR_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_XDR_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_XDR_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_xdr.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_xdr_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_xdr_acl.py",
    "backend/contexts/cyber_security/application/cs_xdr_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/xdr",
    "backend/contexts/edr",
    "backend/contexts/ndr",
    "backend/contexts/soar_platform",
    "backend/contexts/soc_platform",
    "backend/contexts/siem_platform",
    "backend/contexts/security_ops",
    "backend/contexts/cyber_defense",
)


def validate_cs_xdr_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_xdr_aggregates import (
        CsXdrAgentIntegrityRoot,
        CsXdrAiAnalyticsRoot,
        CsXdrEndpointTelemetryCompleteRoot,
        CsXdrEvolvableDetectionRoot,
        CsXdrNetworkVisibilityRoot,
        CsXdrResponseSafeguardsRoot,
        CsXdrThreatDetectedRoot,
        CsXdrUnifiedCorrelationRoot,
    )
    from contexts.cyber_security.domain.services import cs_platform_xdr as xdr

    cat = xdr.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-G"
        and cat.get("adr") == 366
        and cat.get("sor") == "cyber_security"
        and cat["endpoint_telemetry_complete_required"] is True
        and cat["network_visibility_sufficient_required"] is True
        and cat["xdr_correlation_unified_required"] is True
        and cat["ai_analytics_required"] is True
        and cat["detection_rules_evolvable_required"] is True
        and cat["automated_response_safeguards_required"] is True
        and cat["agent_integrity_verifiable_required"] is True
        and cat["edr"]["not_incomplete_telemetry"] is True
        and cat["ndr"]["not_insufficient_visibility"] is True
        and cat["xdr_correlation"]["not_siloed"] is True
        and cat["ai"]["not_absent"] is True
        and cat["detection_engine"]["not_unevolvable"] is True
        and cat["response_engine"]["not_unsafeguarded"] is True
        and cat["agent"]["not_unverifiable"] is True
        and cat["architecture"]["layer_count"] >= 10
        and cat["edr"]["capability_count"] >= 10
        and cat["ndr"]["surface_count"] >= 10
        and cat["cqrs"]["event_count"] >= 8
        and cat["cursor_outputs"]["count"] >= 20
        and "endpoint_telemetry_incomplete" in cat["quality_gates"]["reject_if"]
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
            CsXdrEndpointTelemetryCompleteRoot.collect,
            tenant_id="t1",
            endpoint_ref="e1",
            telemetry_complete=False,
        )
        and CsXdrEndpointTelemetryCompleteRoot.collect(
            tenant_id="t1", endpoint_ref="e2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            CsXdrNetworkVisibilityRoot.cover,
            tenant_id="t1",
            sensor_ref="s1",
            visibility_sufficient=False,
        )
        and CsXdrNetworkVisibilityRoot.cover(
            tenant_id="t1", sensor_ref="s2"
        ).is_insufficient()
        is False
    )
    checks.append(
        not _bad(
            CsXdrUnifiedCorrelationRoot.correlate,
            tenant_id="t1",
            correlation_ref="c1",
            siloed=True,
        )
        and CsXdrUnifiedCorrelationRoot.correlate(
            tenant_id="t1", correlation_ref="c2"
        ).is_siloed()
        is False
    )
    checks.append(
        not _bad(
            CsXdrAiAnalyticsRoot.enable,
            tenant_id="t1",
            analytics_ref="a1",
            present=False,
        )
        and CsXdrAiAnalyticsRoot.enable(
            tenant_id="t1", analytics_ref="a2"
        ).is_absent()
        is False
    )
    checks.append(
        not _bad(
            CsXdrEvolvableDetectionRoot.deploy,
            tenant_id="t1",
            rule_ref="r1",
            evolvable=False,
        )
        and CsXdrEvolvableDetectionRoot.deploy(
            tenant_id="t1", rule_ref="r2"
        ).is_unevolvable()
        is False
    )
    checks.append(
        not _bad(
            CsXdrResponseSafeguardsRoot.execute,
            tenant_id="t1",
            response_ref="x1",
            safeguards=False,
        )
        and CsXdrResponseSafeguardsRoot.execute(
            tenant_id="t1", response_ref="x2"
        ).lacks_safeguards()
        is False
    )
    checks.append(
        not _bad(
            CsXdrAgentIntegrityRoot.verify,
            tenant_id="t1",
            agent_ref="ag1",
            integrity_verifiable=False,
        )
        and CsXdrAgentIntegrityRoot.verify(
            tenant_id="t1", agent_ref="ag2"
        ).is_unverifiable()
        is False
    )
    threat = CsXdrThreatDetectedRoot.detect(
        tenant_id="t1", threat_ref="th1", endpoint_ref="e3"
    )
    checks.append("ThreatDetected" in threat.pending_events)
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/cyber_security/infrastructure/acl/cs_xdr_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p210_f_soar" in acl_text
        and "response_safeguards_required" in acl_text
        and "ai_analytics_required" in acl_text
        and "agent_integrity_verifiable_required" in acl_text
        and "endpoint_telemetry_complete_required" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/xdr"' in router
        and "/xdr/edr" in router
        and "/xdr/ndr" in router
        and "/xdr/correlation" in router
        and "/xdr/agent" in router
        and "/xdr/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_XDR.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never endpoint telemetry is incomplete" in law
        and "Never network visibility is insufficient" in law
        and "Never XDR correlation is siloed" in law
        and "Never AI analytics are absent" in law
        and "Never detection rules cannot evolve" in law
        and "Never automated response lacks safeguards" in law
        and "Never agent integrity cannot be verified" in law
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
        "prompt": "P210-G",
        "adr": 366,
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
