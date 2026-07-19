"""Federation Security Control Plane — ZT, risk, CV, threats, AI, posture (P200-B9)."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.identity_federation.domain.services import (
    federation_security_engine,
    risk_based_federation_engine,
    trust_fabric_engine,
    zero_trust_federation_engine,
)
from contexts.identity_federation.domain.value_objects.security_vos import (
    COMPLIANCE_FRAMEWORKS,
    ZeroTrustGateAction,
)


class FederationSecurityControlPlane:
    """Central security authority for EIFTP hops — gate facts, not AuthZ Permit/Deny."""

    def evaluate_zero_trust(self, *, context: dict | None = None) -> dict:
        ctx = dict(context or {})
        base = zero_trust_federation_engine.evaluate_federation_zero_trust(
            identity_verified=bool(ctx.get("identity_verified", False)),
            device_trusted=bool(ctx.get("device_trusted", False)),
            application_trusted=bool(ctx.get("application_trusted", True)),
            location_allowed=bool(ctx.get("location_allowed", True)),
            behavior_anomaly=bool(ctx.get("behavior_anomaly", False)),
            session_valid=bool(ctx.get("session_valid", True)),
            network_trusted=bool(ctx.get("network_trusted", True)),
            organization_trusted=bool(ctx.get("organization_trusted", True)),
            risk_score=int(ctx.get("risk_score") or 0),
            trust_score=int(ctx.get("trust_score") or 50),
            policy_allowed=bool(ctx.get("policy_allowed", True)),
            step_up_threshold=int(ctx.get("step_up_threshold") or 70),
            deny_threshold=int(ctx.get("deny_threshold") or 90),
        )
        gate = self._enrich_gate_action(base=base, context=ctx)
        return {
            **base,
            "gate_action": gate,
            "resource_sensitivity": ctx.get("resource_sensitivity", "internal"),
            "tenant_context": ctx.get("tenant_id"),
            "ai_context": ctx.get("ai_context"),
            "time_utc": datetime.now(UTC).isoformat(),
            "never_trust_implicitly": True,
            "continuous": True,
            "authz_permit_deny": None,
            "decision_type": "federation_security_gate",
            "secure_defaults": zero_trust_federation_engine.secure_defaults(),
        }

    def _enrich_gate_action(self, *, base: dict, context: dict) -> str:
        action = base.get("action")
        risk = int(base.get("risk_score") or 0)
        sensitivity = str(context.get("resource_sensitivity") or "internal")
        ai_ctx = context.get("ai_context") or {}
        if action == "deny":
            if risk >= 95 or bool(ai_ctx.get("malicious")):
                return ZeroTrustGateAction.QUARANTINE.value
            if bool(context.get("escalate")):
                return ZeroTrustGateAction.ESCALATE.value
            return ZeroTrustGateAction.DENY.value
        if action == "step_up":
            if not context.get("mfa_satisfied", False):
                return ZeroTrustGateAction.REQUIRE_MFA.value
            if sensitivity in ("confidential", "restricted"):
                return ZeroTrustGateAction.REQUIRE_STEP_UP.value
            return ZeroTrustGateAction.CHALLENGE.value
        # allow path
        if sensitivity in ("confidential", "restricted") or context.get("conditions"):
            return ZeroTrustGateAction.ALLOW_WITH_CONDITIONS.value
        return ZeroTrustGateAction.ALLOW.value

    def evaluate_risk(self, *, signals: dict | None = None, subject: dict | None = None) -> dict:
        s = dict(signals or {})
        scored = risk_based_federation_engine.score_federation_risk(
            device_risk=int(s.get("device_risk") or 0),
            behavior_risk=int(s.get("behavior_risk") or 0),
            network_risk=int(s.get("network_risk") or 0),
            organization_risk=int(s.get("organization_risk") or 0),
            certificate_risk=int(s.get("certificate_risk") or 0),
            country_risk=int(s.get("country_risk") or 0),
            transaction_risk=int(s.get("transaction_risk") or 0),
        )
        adaptive = risk_based_federation_engine.adaptive_federation_decision(
            risk_score=scored["risk_score"],
            trust_score=int((subject or {}).get("trust_score") or 50),
        )
        return {
            **scored,
            "adaptive": adaptive,
            "subject": subject or {},
            "authz_permit_deny": None,
        }

    def continuous_verification(self, *, context: dict | None = None) -> dict:
        ctx = dict(context or {})
        zt = self.evaluate_zero_trust(context=ctx)
        trust = trust_fabric_engine.get_trust_fabric_engine().evaluate_continuous(
            inputs=dict(ctx.get("trust_inputs") or {}),
            prior_score=ctx.get("prior_trust_score"),
            zero_trust_ctx={
                "identity_verified": bool(ctx.get("identity_verified", False)),
                "device_trusted": bool(ctx.get("device_trusted", False)),
                "risk_score": zt["risk_score"],
                "trust_score": zt["trust_score"],
            },
        )
        crypto = federation_security_engine.validate_federation_request(
            state=ctx.get("state"),
            expected_state=ctx.get("expected_state"),
            nonce=ctx.get("nonce"),
            expected_nonce=ctx.get("expected_nonce"),
            audience=ctx.get("audience"),
            expected_audience=ctx.get("expected_audience"),
            signature_valid=bool(ctx.get("signature_valid", True)),
            replay_key=ctx.get("replay_key"),
            seen_replays=set(ctx.get("seen_replays") or []),
            token_exp=ctx.get("token_exp"),
        )
        revalidate = zt["gate_action"] not in (
            ZeroTrustGateAction.DENY.value,
            ZeroTrustGateAction.QUARANTINE.value,
        ) and crypto.get("valid", False)
        return {
            "triggered": True,
            "zero_trust": zt,
            "trust_fabric": trust,
            "crypto_validation": crypto,
            "session_revalidated": revalidate,
            "token_reassessed": True,
            "context_change": bool(ctx.get("context_changed")),
            "authz_permit_deny": None,
        }

    def detect_threat(self, *, indicators: dict | None = None) -> dict:
        ind = dict(indicators or {})
        threat_type = str(ind.get("threat_type") or "anomaly")
        score = int(ind.get("score") or 0)
        catalog = {
            "identity_threat": score >= 40,
            "insider_threat": bool(ind.get("insider")),
            "api_abuse": bool(ind.get("api_abuse")) or score >= 60,
            "credential_abuse": bool(ind.get("credential_abuse")),
            "ai_abuse": bool(ind.get("ai_abuse")),
            "privilege_escalation": bool(ind.get("privilege_escalation")),
            "session_hijack": bool(ind.get("session_hijack")),
        }
        detected = [k for k, v in catalog.items() if v] or (
            [threat_type] if score >= 50 else []
        )
        severity = (
            "critical"
            if score >= 85
            else "high"
            if score >= 70
            else "medium"
            if score >= 40
            else "low"
        )
        return {
            "detected": bool(detected),
            "threat_types": detected,
            "severity": severity,
            "score": score,
            "siem_ready": True,
            "integration": "via_integration_platform",
            "authz_permit_deny": None,
        }

    def assess_compliance_posture(self, *, control_results: dict | None = None) -> dict:
        """Local federation posture checklist — full program stays Compliance Platform."""
        results = dict(control_results or {})
        checklist = {
            "mtls_required": bool(results.get("mtls_required", True)),
            "pkce_required": bool(results.get("pkce_required", True)),
            "audit_events_emitted": bool(results.get("audit_events_emitted", True)),
            "tenant_isolation": bool(results.get("tenant_isolation", True)),
            "no_implicit_trust": bool(results.get("no_implicit_trust", True)),
            "ai_governance_enabled": bool(results.get("ai_governance_enabled", True)),
            "continuous_verification": bool(results.get("continuous_verification", True)),
            "secrets_not_in_logs": bool(results.get("secrets_not_in_logs", True)),
        }
        failed = [k for k, ok in checklist.items() if not ok]
        passed = len(checklist) - len(failed)
        status = "passed" if not failed else "failed"
        return {
            "frameworks": list(COMPLIANCE_FRAMEWORKS),
            "checklist": checklist,
            "controls_passed": passed,
            "controls_failed": len(failed),
            "violations": failed,
            "status": status,
            "evidence_owner": "compliance_platform",
            "authz_permit_deny": None,
        }

    def govern_ai_action(self, *, ai_context: dict | None = None) -> dict:
        ctx = dict(ai_context or {})
        identity_ok = bool(ctx.get("ai_identity_verified"))
        trust = int(ctx.get("trust_score") or 0)
        scope_ok = bool(ctx.get("within_capability_scope", True))
        prompt_ok = not bool(ctx.get("prompt_injection_suspected"))
        data_ok = bool(ctx.get("data_access_allowed", True))
        blocked_reasons: list[str] = []
        if not identity_ok:
            blocked_reasons.append("ai_identity_unverified")
        if trust < 40:
            blocked_reasons.append("ai_trust_too_low")
        if not scope_ok:
            blocked_reasons.append("capability_scope_exceeded")
        if not prompt_ok:
            blocked_reasons.append("prompt_governance_violation")
        if not data_ok:
            blocked_reasons.append("data_access_denied")
        blocked = bool(blocked_reasons)
        return {
            "allowed_to_proceed": not blocked,
            "blocked": blocked,
            "reasons": blocked_reasons,
            "gate_action": (
                ZeroTrustGateAction.DENY.value
                if blocked
                else ZeroTrustGateAction.ALLOW_WITH_CONDITIONS.value
            ),
            "explainable": True,
            "audit_required": True,
            "authz_permit_deny": None,
        }

    def security_posture(self, *, summary: dict | None = None) -> dict:
        s = dict(summary or {})
        return {
            "secure_defaults": zero_trust_federation_engine.secure_defaults(),
            "zero_trust_enabled": True,
            "continuous_verification": True,
            "controls_count": int(s.get("controls_count") or 0),
            "open_threats": int(s.get("open_threats") or 0),
            "last_compliance_status": s.get("last_compliance_status"),
            "crypto": {
                "mtls_required": True,
                "signature_algorithms": ["RS256", "ES256"],
                "replay_protection": True,
            },
            "authz_boundary": "separate_ways",
        }

    def surface(self) -> dict:
        return {
            "prompt": "P200-B9",
            "adr": 223,
            "gate_actions": [a.value for a in ZeroTrustGateAction],
            "frameworks": list(COMPLIANCE_FRAMEWORKS),
            "principles": [
                "security_by_design",
                "zero_trust_by_default",
                "continuous_verification",
                "no_implicit_trust",
                "ai_security_governance",
                "audit_via_platform",
                "compliance_framework_reuse",
            ],
            "knowledge_graph": {
                "identity_secured_by_policy": True,
                "api_protected_by_control": True,
                "ai_governed_by_policy": True,
            },
        }


_plane: FederationSecurityControlPlane | None = None


def get_federation_security_control_plane() -> FederationSecurityControlPlane:
    global _plane
    if _plane is None:
        _plane = FederationSecurityControlPlane()
    return _plane
