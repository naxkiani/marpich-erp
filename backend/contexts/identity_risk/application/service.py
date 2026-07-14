"""Identity risk application service."""
from __future__ import annotations

import uuid

from contexts.identity_risk.domain.aggregates.identity_risk_platform import (
    AnomalyAlert,
    RiskProfile,
    RiskScore,
    RiskSignal,
    RiskLevel,
)
from contexts.identity_risk.domain.events.identity_risk_integration_events import (
    AnomalyDetectedIntegration,
    RiskScoreComputedIntegration,
    StepUpRecommendedIntegration,
)
from contexts.identity_risk.domain.ports.identity_risk_repositories import (
    IAnomalyAlertRepository,
    IRiskProfileRepository,
    IRiskScoreRepository,
    IRiskSignalRepository,
)
from contexts.identity_risk.domain.services import identity_risk_engine as engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class IdentityRiskApplicationService:
    def __init__(
        self,
        profiles: IRiskProfileRepository,
        signals: IRiskSignalRepository,
        scores: IRiskScoreRepository,
        alerts: IAnomalyAlertRepository,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._signals = signals
        self._scores = scores
        self._alerts = alerts
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "scoring_enabled": profile.scoring_enabled if profile else True,
            "score_threshold": profile.score_threshold if profile else 50,
            "step_up_threshold": profile.step_up_threshold if profile else 75,
            "bulk_create_threshold": profile.bulk_create_threshold if profile else 10,
        }
        pmap = {
            "identity_risk.scoring.enabled": ("scoring_enabled", "enabled"),
            "identity_risk.score.threshold": ("score_threshold", "threshold"),
            "identity_risk.step_up.threshold": ("step_up_threshold", "threshold"),
            "identity_risk.directory.bulk_create_threshold": ("bulk_create_threshold", "threshold"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> RiskProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = RiskProfile.create(
            tenant_id=tenant_id,
            profile_ref=self._profiles.next_profile_ref(tenant_id),
        )
        await self._profiles.save(profile)
        return profile

    async def handle_tenant_provisioned(self, event: dict) -> None:
        tenant_id = event.get("tenant_id") or event.get("payload", {}).get("tenant_id")
        if tenant_id:
            await self.seed(tenant_id)

    async def handle_authentication_login_success(self, event: dict) -> None:
        tenant_id = str(event.get("tenant_id") or "")
        payload = event.get("payload") or event
        if not tenant_id:
            return
        await self.score_authentication(
            tenant_id,
            user_id=str(payload.get("user_id", "")) or None,
            auth_method=str(payload.get("auth_method", "password")),
            is_new_user=bool(payload.get("is_new_user", False)),
            failed_attempts_24h=int(payload.get("failed_attempts_24h", 0)),
        )

    async def handle_directory_sync_completed(self, event: dict) -> None:
        tenant_id = str(event.get("tenant_id") or "")
        payload = event.get("payload") or event
        if not tenant_id:
            return
        await self.score_directory_sync(
            tenant_id,
            users_synced=int(payload.get("users_synced", 0)),
            users_created=int(payload.get("users_created", 0)),
            source_type=str(payload.get("source_type", "ldap")),
        )

    async def handle_scim_user_provisioned(self, event: dict) -> None:
        tenant_id = str(event.get("tenant_id") or "")
        payload = event.get("payload") or event
        if not tenant_id:
            return
        await self.score_scim_provision(
            tenant_id,
            user_id=str(payload.get("user_id", "")),
            email=str(payload.get("email", "")),
            is_new_user=bool(payload.get("is_new_user", True)),
        )

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": engine.list_capability_catalog(),
            "policy_keys": engine.list_policy_keys(),
            "risk_signals": engine.list_risk_signals(),
            "dependency_map": engine.dependency_map(),
        })

    async def seed(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        return Result.ok({"seeded": True, "profile_ref": profile.profile_ref})

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        score_rows = await self._scores.list_by_tenant(tenant_id)
        alert_rows = await self._alerts.list_by_tenant(tenant_id)
        dashboard = engine.build_dashboard(
            profile=profile.to_dict(),
            scores=[s.to_dict() for s in score_rows],
            alerts=[a.to_dict() for a in alert_rows],
        )
        return Result.ok(dashboard)

    async def list_scores(self, tenant_id: str) -> Result[list[dict]]:
        rows = await self._scores.list_by_tenant(tenant_id)
        return Result.ok([row.to_dict() for row in rows])

    async def list_alerts(self, tenant_id: str) -> Result[list[dict]]:
        rows = await self._alerts.list_by_tenant(tenant_id)
        return Result.ok([row.to_dict() for row in rows])

    async def _persist_score(
        self,
        tenant_id: str,
        *,
        source: str,
        event_name: str,
        user_id: str | None,
        score_value: int,
        factors: list[dict],
        explanation: str,
        raw_payload: dict,
    ) -> Result[dict]:
        policy = await self._policy_params(tenant_id)
        if not policy["scoring_enabled"]:
            return Result.fail("identity_risk.errors.scoring_disabled")

        signal = RiskSignal.capture(
            tenant_id=tenant_id,
            signal_ref=self._signals.next_signal_ref(tenant_id),
            source=source,
            event_name=event_name,
            user_id=user_id,
            factors=factors,
            raw_payload=raw_payload,
        )
        await self._signals.save(signal)

        risk_level = engine.classify_risk_level(score_value, threshold=policy["score_threshold"])
        step_up = score_value >= policy["step_up_threshold"]
        score = RiskScore.compute(
            tenant_id=tenant_id,
            score_ref=self._scores.next_score_ref(tenant_id),
            signal_ref=signal.signal_ref,
            score=score_value,
            risk_level=risk_level,
            explanation=explanation,
            factors=factors,
            step_up_recommended=step_up,
            user_id=user_id,
        )
        await self._scores.save(score)

        correlation_id = str(uuid.uuid4())
        await publish_integration_event(
            RiskScoreComputedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id,
                score_ref=score.score_ref,
                signal_ref=signal.signal_ref,
                score=score.score,
                risk_level=score.risk_level,
                user_id=user_id,
            )
        )

        if risk_level in {RiskLevel.HIGH.value, RiskLevel.CRITICAL.value}:
            alert = AnomalyAlert.raise_alert(
                tenant_id=tenant_id,
                alert_ref=self._alerts.next_alert_ref(tenant_id),
                score_ref=score.score_ref,
                title=f"Elevated identity risk ({risk_level})",
                severity=risk_level,
                description=explanation,
            )
            await self._alerts.save(alert)
            await publish_integration_event(
                AnomalyDetectedIntegration(
                    tenant_id=TenantId(tenant_id),
                    correlation_id=correlation_id,
                    alert_ref=alert.alert_ref,
                    score_ref=score.score_ref,
                    severity=alert.severity,
                    title=alert.title,
                )
            )

        if step_up:
            await publish_integration_event(
                StepUpRecommendedIntegration(
                    tenant_id=TenantId(tenant_id),
                    correlation_id=correlation_id,
                    score_ref=score.score_ref,
                    user_id=user_id,
                    score=score.score,
                )
            )

        return Result.ok(score.to_dict())

    async def score_authentication(
        self,
        tenant_id: str,
        *,
        user_id: str | None,
        auth_method: str,
        is_new_user: bool = False,
        failed_attempts_24h: int = 0,
    ) -> Result[dict]:
        await self._ensure_profile(tenant_id)
        score_value, factors, explanation = engine.score_authentication_event(
            auth_method=auth_method,
            is_new_user=is_new_user,
            failed_attempts_24h=failed_attempts_24h,
        )
        return await self._persist_score(
            tenant_id,
            source="authentication",
            event_name="authentication.login.success",
            user_id=user_id,
            score_value=score_value,
            factors=factors,
            explanation=explanation,
            raw_payload={
                "auth_method": auth_method,
                "is_new_user": is_new_user,
                "failed_attempts_24h": failed_attempts_24h,
            },
        )

    async def score_directory_sync(
        self,
        tenant_id: str,
        *,
        users_synced: int,
        users_created: int,
        source_type: str = "ldap",
    ) -> Result[dict]:
        profile = await self._ensure_profile(tenant_id)
        policy = await self._policy_params(tenant_id)
        bulk_threshold = int(policy.get("bulk_create_threshold", profile.bulk_create_threshold))
        score_value, factors, explanation = engine.score_directory_sync_event(
            users_synced=users_synced,
            users_created=users_created,
            bulk_create_threshold=bulk_threshold,
        )
        return await self._persist_score(
            tenant_id,
            source="directory",
            event_name="directory.sync.completed",
            user_id=None,
            score_value=score_value,
            factors=factors,
            explanation=explanation,
            raw_payload={
                "users_synced": users_synced,
                "users_created": users_created,
                "source_type": source_type,
            },
        )

    async def score_scim_provision(
        self,
        tenant_id: str,
        *,
        user_id: str,
        email: str,
        is_new_user: bool = True,
    ) -> Result[dict]:
        await self._ensure_profile(tenant_id)
        score_value, factors, explanation = engine.score_scim_provision_event(is_new_user=is_new_user)
        return await self._persist_score(
            tenant_id,
            source="scim",
            event_name="directory.scim.user.provisioned",
            user_id=user_id or None,
            score_value=score_value,
            factors=factors,
            explanation=explanation,
            raw_payload={"email": email, "is_new_user": is_new_user},
        )

    async def score_federation(
        self,
        tenant_id: str,
        *,
        auth_method: str = "oidc",
        protocol: str | None = None,
        is_new_user: bool = False,
        partner_unverified: bool = False,
        certificate_untrusted: bool = False,
        cross_border: bool = False,
        user_id: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        await self._ensure_profile(tenant_id)
        proto = protocol or auth_method
        score_value, factors, explanation = engine.score_federation_event(
            protocol=proto,
            partner_unverified=partner_unverified,
            certificate_untrusted=certificate_untrusted,
            cross_border=cross_border,
            is_new_user=is_new_user,
        )
        return await self._persist_score(
            tenant_id,
            source="federation",
            event_name="federation.external_auth.succeeded",
            user_id=user_id,
            score_value=score_value,
            factors=factors,
            explanation=explanation,
            raw_payload={
                "protocol": proto,
                "is_new_user": is_new_user,
                "partner_unverified": partner_unverified,
                "certificate_untrusted": certificate_untrusted,
                "cross_border": cross_border,
                "correlation_id": correlation_id,
            },
        )

    async def evaluate_manual(self, tenant_id: str, *, event_type: str, payload: dict) -> Result[dict]:
        if event_type == "authentication":
            return await self.score_authentication(
                tenant_id,
                user_id=payload.get("user_id"),
                auth_method=str(payload.get("auth_method", "password")),
                is_new_user=bool(payload.get("is_new_user", False)),
                failed_attempts_24h=int(payload.get("failed_attempts_24h", 0)),
            )
        if event_type == "directory_sync":
            return await self.score_directory_sync(
                tenant_id,
                users_synced=int(payload.get("users_synced", 0)),
                users_created=int(payload.get("users_created", 0)),
                source_type=str(payload.get("source_type", "ldap")),
            )
        if event_type == "scim":
            return await self.score_scim_provision(
                tenant_id,
                user_id=str(payload.get("user_id", "")),
                email=str(payload.get("email", "")),
                is_new_user=bool(payload.get("is_new_user", True)),
            )
        return Result.fail("identity_risk.errors.unknown_event_type")
