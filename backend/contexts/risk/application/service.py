"""Enterprise Risk Platform application service."""
from __future__ import annotations

from contexts.risk.domain.aggregates.risk_platform import (
    EnterpriseRiskItem,
    RiskCategory,
    RiskMatrixSnapshot,
    RiskPrediction,
    RiskTenantProfile,
)
from contexts.risk.domain.events.risk_integration_events import (
    RiskItemEscalatedIntegration,
    RiskItemRegisteredIntegration,
    RiskMatrixUpdatedIntegration,
    RiskPredictionGeneratedIntegration,
)
from contexts.risk.domain.ports.risk_repositories import (
    IEnterpriseRiskItemRepository,
    IRiskMatrixSnapshotRepository,
    IRiskPredictionRepository,
    IRiskTenantProfileRepository,
)
from contexts.risk.domain.services import risk_engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class RiskApplicationService:
    def __init__(
        self,
        profiles: IRiskTenantProfileRepository,
        risks: IEnterpriseRiskItemRepository,
        matrices: IRiskMatrixSnapshotRepository,
        predictions: IRiskPredictionRepository,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._risks = risks
        self._matrices = matrices
        self._predictions = predictions
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        params = {
            "escalation_threshold": 12,
            "matrix_size": 5,
            "confidence_threshold": 0.7,
            "heatmap_top_n": 10,
            "auto_escalate": True,
        }
        pmap = {
            "risk.escalation.threshold": ("escalation_threshold", "threshold"),
            "risk.matrix.size": ("matrix_size", "size"),
            "risk.ai.confidence_threshold": ("confidence_threshold", "confidence_threshold"),
            "risk.heatmap.top_n": ("heatmap_top_n", "top_n"),
            "risk.register.auto_escalate": ("auto_escalate", "auto_escalate"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(
                tenant_id=tenant_id, domain="tax", policy_key=key, facts={}
            )
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": risk_engine.list_capability_catalog(),
            "categories": risk_engine.list_categories(),
            "policy_keys": risk_engine.list_policy_keys(),
            "shared_service": True,
            "delegation": {
                "treasury_risk": True,
                "fx_risk": True,
                "grc_compliance": True,
                "local_risk_duplication": False,
            },
        })

    async def get_dependency_map(self) -> Result[dict]:
        return Result.ok(risk_engine.dependency_map())

    async def seed(self, tenant_id: str) -> Result[dict]:
        existing = await self._profiles.find_by_tenant(tenant_id)
        if existing:
            return Result.ok({
                "seeded": False,
                "profile": existing.to_dict(),
                "risks": len(await self._risks.list_by_tenant(tenant_id)),
            })

        params = await self._policy_params(tenant_id)
        ref = self._profiles.next_profile_ref(tenant_id)
        profile = RiskTenantProfile.create(
            tenant_id=tenant_id,
            profile_ref=ref,
            enabled_categories=[c.value for c in RiskCategory],
        )
        profile.matrix_size = int(params.get("matrix_size", 5))
        profile.escalation_threshold = int(params.get("escalation_threshold", 12))
        await self._profiles.save(profile)

        seeded = 0
        threshold = int(params.get("escalation_threshold", 12))
        for seed_risk in risk_engine.DEFAULT_SEED_RISKS:
            risk_ref = self._risks.next_risk_ref(tenant_id)
            score = risk_engine.compute_risk_score(seed_risk["likelihood"], seed_risk["impact"])
            severity = risk_engine.severity_from_score(score, threshold)
            item = EnterpriseRiskItem.register(
                tenant_id=tenant_id,
                risk_ref=risk_ref,
                title=seed_risk["title"],
                category=seed_risk["category"],
                likelihood=seed_risk["likelihood"],
                impact=seed_risk["impact"],
                risk_score=score,
                severity=severity,
                source_module="risk_platform",
                delegated_to=seed_risk.get("delegated_to"),
            )
            await self._risks.save(item)
            seeded += 1

        return Result.ok({
            "seeded": True,
            "profile": profile.to_dict(),
            "risks_seeded": seeded,
            "enabled_categories": len(profile.enabled_categories),
        })

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = await self._policy_params(tenant_id)
        risks = [r.to_dict() for r in await self._risks.list_by_tenant(tenant_id)]
        matrix = risk_engine.build_risk_matrix(
            risks=risks, matrix_size=int(params.get("matrix_size", 5))
        )
        heatmap = risk_engine.build_heatmap(
            risks=risks, top_n=int(params.get("heatmap_top_n", 10))
        )
        predictions = [p.to_dict() for p in await self._predictions.list_by_tenant(tenant_id)]
        return Result.ok(
            risk_engine.build_dashboard(
                profile=profile.to_dict() if profile else None,
                risks=risks,
                matrix=matrix,
                heatmap=heatmap,
                predictions=predictions,
            )
        )

    async def list_register(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._risks.list_by_tenant(tenant_id)
        return Result.ok([i.to_dict() for i in items])

    async def register_risk(
        self,
        tenant_id: str,
        *,
        title: str,
        category: str,
        likelihood: int,
        impact: int,
        owner_id: str = "",
        source_module: str = "",
        mitigation_plan: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        if category not in {c.value for c in RiskCategory}:
            return Result.fail("invalid_category")

        params = await self._policy_params(tenant_id)
        threshold = int(params.get("escalation_threshold", 12))
        score = risk_engine.compute_risk_score(likelihood, impact)
        severity = risk_engine.severity_from_score(score, threshold)
        delegated = risk_engine.CATEGORY_DELEGATION.get(category)

        risk_ref = self._risks.next_risk_ref(tenant_id)
        item = EnterpriseRiskItem.register(
            tenant_id=tenant_id,
            risk_ref=risk_ref,
            title=title,
            category=category,
            likelihood=likelihood,
            impact=impact,
            risk_score=score,
            severity=severity,
            owner_id=owner_id,
            source_module=source_module,
            mitigation_plan=mitigation_plan,
            delegated_to=delegated,
        )
        await self._risks.save(item)

        corr = correlation_id or risk_ref
        await publish_integration_event(
            RiskItemRegisteredIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                risk_ref=risk_ref,
                category=category,
                risk_score=score,
                severity=severity,
            )
        )

        if bool(params.get("auto_escalate")) and score >= threshold:
            item.escalate()
            await self._risks.save(item)
            await publish_integration_event(
                RiskItemEscalatedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=corr,
                    risk_ref=risk_ref,
                    category=category,
                    risk_score=score,
                )
            )

        return Result.ok(item.to_dict())

    async def escalate_risk(self, tenant_id: str, risk_ref: str, *, correlation_id: str = "") -> Result[dict]:
        item = await self._risks.find_by_ref(tenant_id, risk_ref)
        if not item:
            return Result.fail("risk_not_found")
        item.escalate()
        await self._risks.save(item)

        corr = correlation_id or risk_ref
        await publish_integration_event(
            RiskItemEscalatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                risk_ref=risk_ref,
                category=item.category,
                risk_score=item.risk_score,
            )
        )
        return Result.ok(item.to_dict())

    async def get_matrix(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = await self._policy_params(tenant_id)
        matrix_size = profile.matrix_size if profile else int(params.get("matrix_size", 5))
        risks = [r.to_dict() for r in await self._risks.list_by_tenant(tenant_id)]
        matrix_data = risk_engine.build_risk_matrix(risks=risks, matrix_size=matrix_size)

        matrix_ref = self._matrices.next_matrix_ref(tenant_id)
        snapshot = RiskMatrixSnapshot.build(
            tenant_id=tenant_id,
            matrix_ref=matrix_ref,
            matrix_size=matrix_size,
            cells=matrix_data["cells"],
            total_risks=matrix_data["total_mapped"],
        )
        await self._matrices.save(snapshot)

        await publish_integration_event(
            RiskMatrixUpdatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=matrix_ref,
                matrix_ref=matrix_ref,
                total_mapped=matrix_data["total_mapped"],
            )
        )
        return Result.ok({**matrix_data, "snapshot": snapshot.to_dict()})

    async def get_heatmap(self, tenant_id: str) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        risks = [r.to_dict() for r in await self._risks.list_by_tenant(tenant_id)]
        return Result.ok(
            risk_engine.build_heatmap(risks=risks, top_n=int(params.get("heatmap_top_n", 10)))
        )

    async def predict(
        self,
        tenant_id: str,
        *,
        category: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile and not profile.ai_enabled:
            return Result.fail("ai_disabled")

        params = await self._policy_params(tenant_id)
        risks = [r.to_dict() for r in await self._risks.list_by_tenant(tenant_id)]
        result = risk_engine.ai_risk_prediction(
            category=category,
            risks=risks,
            escalation_threshold=int(params.get("escalation_threshold", 12)),
            confidence_threshold=float(params.get("confidence_threshold", 0.7)),
        )

        pred_ref = self._predictions.next_prediction_ref(tenant_id)
        prediction = RiskPrediction.generate(
            tenant_id=tenant_id,
            prediction_ref=pred_ref,
            category=result.get("category", category or "all"),
            predicted_score=result["predicted_score"],
            trend=result["trend"],
            recommendations=result.get("recommendations", []),
            factors=result.get("factors", []),
            confidence=result.get("confidence", 0.8),
        )
        await self._predictions.save(prediction)

        corr = correlation_id or pred_ref
        await publish_integration_event(
            RiskPredictionGeneratedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                prediction_ref=pred_ref,
                category=prediction.category,
                predicted_score=prediction.predicted_score,
                trend=prediction.trend,
            )
        )
        return Result.ok({**result, "prediction": prediction.to_dict()})

    async def list_predictions(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._predictions.list_by_tenant(tenant_id)
        return Result.ok([p.to_dict() for p in items])

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope.get("tenant_id", "")
        if tenant_id:
            await self.seed(tenant_id)
