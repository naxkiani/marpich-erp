"""Fabric Intelligence application service — AI, analytics, copilot (P198-C2)."""
from __future__ import annotations

from uuid import uuid4

from contexts.identity_federation.domain.ports.federation_repositories import (
    IClaimsMappingRepository,
    IFederationPartnerRepository,
    IFederationSessionRepository,
    IIdentityProviderRepository,
    ITrustRelationshipRepository,
)
from contexts.identity_federation.domain.services import ai_identity_copilot
from contexts.identity_federation.domain.services import ai_identity_intelligence_engine as ai_engine
from contexts.identity_federation.domain.services import identity_analytics_engine
from contexts.identity_federation.domain.services.ai_identity_intelligence_engine import (
    IdentityFeatureVector,
)
from contexts.identity_federation.infrastructure.observability import federation_ai_metrics
from contexts.identity_federation.infrastructure.persistence.federation_audit_store import (
    FederationAuditStore,
)
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event

from contexts.identity_federation.domain.events.federation_integration_events import (
    IdentityAiInsightGeneratedIntegration,
    IdentityAiPredictionCompletedIntegration,
)


class FabricIntelligenceApplicationService:
    def __init__(
        self,
        providers: IIdentityProviderRepository,
        partners: IFederationPartnerRepository,
        trusts: ITrustRelationshipRepository,
        sessions: IFederationSessionRepository,
        mappings: IClaimsMappingRepository,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._providers = providers
        self._partners = partners
        self._trusts = trusts
        self._sessions = sessions
        self._mappings = mappings
        self._policy = policy_evaluator

    async def _ai_params(self, tenant_id: str) -> dict:
        params = {
            "ai_enabled": True,
            "confidence_threshold": 0.7,
            "risk_alert_threshold": 70,
            "explainability_required": True,
        }
        pmap = {
            "federation.ai.enabled": ("ai_enabled", "enabled"),
            "federation.ai.confidence.threshold": ("confidence_threshold", "threshold"),
            "federation.ai.risk.alert.threshold": ("risk_alert_threshold", "threshold"),
            "federation.ai.explainability.required": ("explainability_required", "required"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(
                tenant_id=tenant_id, domain="platform", policy_key=key, facts={}
            )
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def list_models(self) -> Result[dict]:
        return Result.ok({
            "models": ai_engine.list_models(),
            "pipelines": ai_engine.ml_pipeline_manifest(),
        })

    async def predict(
        self,
        tenant_id: str,
        *,
        model_id: str = "identity_risk_predictor_v1",
        features: dict | None = None,
        correlation_id: str | None = None,
    ) -> Result[dict]:
        params = await self._ai_params(tenant_id)
        if not params.get("ai_enabled", True):
            return Result.fail("federation.errors.ai_disabled")
        allowed = set(IdentityFeatureVector.__dataclass_fields__.keys())
        cleaned = {k: v for k, v in (features or {}).items() if k in allowed}
        fv = IdentityFeatureVector(**cleaned)
        prediction = ai_engine.predict_identity_intelligence(
            fv,
            model_id=model_id,
            confidence_threshold=float(params.get("confidence_threshold", 0.7)),
        )
        prediction_id = f"pred-{uuid4().hex[:12]}"
        prediction["prediction_id"] = prediction_id
        federation_ai_metrics.increment("ai_inference_total")
        if prediction["risk_score"] >= int(params.get("risk_alert_threshold", 70)):
            federation_ai_metrics.increment("ai_high_risk_total")
        await publish_integration_event(
            IdentityAiPredictionCompletedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or "",
                prediction_id=prediction_id,
                model_id=model_id,
                risk_score=prediction["risk_score"],
                classification=prediction["classification"],
            )
        )
        FederationAuditStore.append(
            tenant_id=tenant_id,
            event_type="ai.prediction",
            decision=prediction["classification"],
            detail={"prediction_id": prediction_id, "model_id": model_id, "risk_score": prediction["risk_score"]},
            correlation_id=correlation_id or "",
        )
        return Result.ok(prediction)

    async def submit_feedback(
        self,
        tenant_id: str,
        *,
        prediction_id: str,
        useful: bool,
        label: str | None = None,
    ) -> Result[dict]:
        result = ai_engine.record_feedback(prediction_id=prediction_id, useful=useful, label=label)
        federation_ai_metrics.increment("ai_feedback_total")
        FederationAuditStore.append(
            tenant_id=tenant_id,
            event_type="ai.feedback",
            resource=prediction_id,
            detail=result,
        )
        return Result.ok(result)

    async def analytics(self, tenant_id: str) -> Result[dict]:
        providers = [p.to_dict() for p in await self._providers.list_by_tenant(tenant_id)]
        partners = [p.to_dict() for p in await self._partners.list_by_tenant(tenant_id)]
        trusts = [t.to_dict() for t in await self._trusts.list_by_tenant(tenant_id)]
        audit = FederationAuditStore.list_by_tenant(tenant_id, limit=100)
        analytics = identity_analytics_engine.build_identity_analytics(
            providers=providers,
            partners=partners,
            trusts=trusts,
            audit_entries=audit,
        )
        insights = identity_analytics_engine.synthesize_ai_insights(analytics)
        await publish_integration_event(
            IdentityAiInsightGeneratedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id="",
                insight_count=len(insights),
                insight_types=tuple(sorted({i["type"] for i in insights})),
            )
        )
        federation_ai_metrics.increment("ai_insight_total")
        return Result.ok({**analytics, "ai_insights": insights})

    async def executive_report(self, tenant_id: str) -> Result[dict]:
        analytics = (await self.analytics(tenant_id)).unwrap()
        return Result.ok(
            identity_analytics_engine.executive_report(
                analytics, insights=analytics.get("ai_insights")
            )
        )

    async def operational_report(self, tenant_id: str) -> Result[dict]:
        analytics = (await self.analytics(tenant_id)).unwrap()
        return Result.ok(identity_analytics_engine.operational_report(analytics))

    async def copilot(
        self,
        tenant_id: str,
        *,
        question: str,
        context: dict | None = None,
    ) -> Result[dict]:
        params = await self._ai_params(tenant_id)
        if not params.get("ai_enabled", True):
            return Result.fail("federation.errors.ai_disabled")
        ctx = dict(context or {})
        if "analytics" not in ctx:
            analytics_result = await self.analytics(tenant_id)
            if analytics_result.succeeded:
                ctx["analytics"] = analytics_result.unwrap()
        if "audit" not in ctx:
            ctx["audit"] = FederationAuditStore.list_by_tenant(tenant_id, limit=20)
        answer = ai_identity_copilot.assist_administrator(question=question, context=ctx)
        federation_ai_metrics.increment("ai_copilot_total")
        FederationAuditStore.append(
            tenant_id=tenant_id,
            event_type="ai.copilot",
            detail={"question": question[:200], "topic": answer.get("topic")},
        )
        return Result.ok(answer)

    async def explain_decision(self, tenant_id: str, *, decision: dict) -> Result[dict]:
        return Result.ok(ai_identity_copilot.explain_authentication_decision(decision=decision))

    async def explain_trust(self, tenant_id: str, *, trust: dict) -> Result[dict]:
        return Result.ok(ai_identity_copilot.explain_trust_score(trust=trust))

    async def suggest_policies(self, tenant_id: str) -> Result[dict]:
        analytics = (await self.analytics(tenant_id)).unwrap()
        return Result.ok({
            "suggestions": ai_identity_copilot.suggest_policy_improvements(analytics=analytics)
        })

    async def detect_config_problems(self, tenant_id: str) -> Result[dict]:
        provider_objs = await self._providers.list_by_tenant(tenant_id)
        providers = [p.to_dict() for p in provider_objs]
        mapping_count = 0
        for p in provider_objs:
            mapping_count += len(await self._mappings.list_by_provider(tenant_id, str(p.id)))
        problems = ai_identity_copilot.detect_configuration_problems(
            providers=providers, mappings_count=mapping_count
        )
        return Result.ok({"problems": problems, "count": len(problems)})

    async def security_recommendations(self, tenant_id: str) -> Result[dict]:
        analytics = (await self.analytics(tenant_id)).unwrap()
        return Result.ok({
            "recommendations": ai_identity_copilot.generate_security_recommendations(
                analytics=analytics
            )
        })

    async def summarize_audit(self, tenant_id: str) -> Result[dict]:
        entries = FederationAuditStore.list_by_tenant(tenant_id, limit=50)
        return Result.ok(ai_identity_copilot.summarize_audit_events(entries=entries))

    async def intelligence_dashboard(self, tenant_id: str) -> Result[dict]:
        analytics = (await self.analytics(tenant_id)).unwrap()
        models = ai_engine.list_models()
        metrics = federation_ai_metrics.snapshot()
        return Result.ok({
            "analytics": analytics,
            "models": models,
            "ai_metrics": metrics,
            "performance_targets": {
                "authentication_decision_ms": 150,
                "federation_routing_ms": 120,
                "token_exchange_ms": 100,
                "provisioning_sec": 5,
                "availability": "99.99%",
                "scale": {"users": "10M+", "sessions": "100M+", "events": "billions"},
            },
            "quality_gates": [
                "security", "architecture", "performance", "compliance",
                "accessibility", "documentation", "ai_explainability",
            ],
        })

    async def ai_metrics(self) -> Result[dict]:
        return Result.ok(federation_ai_metrics.snapshot())
