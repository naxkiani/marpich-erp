"""AI application service — platform assist + P214-A foundation catalog."""
from __future__ import annotations

from contexts.ai.domain.aggregates.assist_session import AssistSession
from contexts.ai.domain.events.integration_events import InsightGeneratedIntegration
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class AiApplicationService:
    def __init__(self) -> None:
        self._sessions: dict[str, AssistSession] = {}

    def reset(self) -> None:
        self._sessions.clear()

    async def list_catalog(self) -> Result[dict]:
        from contexts.ai.domain.services import (
            ai_platform_domain as domain,
        )
        from contexts.ai.domain.services import (
            ai_platform_foundation as foundation,
        )
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mission,
        )
        from contexts.ai.domain.services import ai_platform_mlops as mlops

        return Result.ok(
            {
                "sor": "ai",
                "capability": "CAP-PLT-AI-001",
                "platform_foundation": {
                    "prompt_id": "P214-A",
                    "adr": 421,
                    "sor": "ai",
                    "product": foundation.PRODUCT,
                    "principle": foundation.PRINCIPLE,
                    "fabric": foundation.FABRIC,
                    "routes": foundation.foundation_surface().get("routes"),
                    "forbidden_sibling_bc": list(
                        foundation.catalog()["forbidden_sibling_bc"]
                    ),
                },
                "platform_mission": {
                    "prompt_id": "P214-B",
                    "adr": 422,
                    "sor": "ai",
                    "product": mission.PRODUCT,
                    "fabric": mission.FABRIC,
                    "mission": mission.MISSION_STATEMENT,
                    "vision": mission.VISION_STATEMENT,
                    "routes": mission.mission_surface().get("routes"),
                    "forbidden_sibling_bc": list(
                        mission.catalog()["forbidden_sibling_bc"]
                    ),
                },
                "platform_domain": {
                    "prompt_id": "P214-C",
                    "adr": 423,
                    "sor": "ai",
                    "product": domain.PRODUCT,
                    "principle": domain.PRINCIPLE,
                    "fabric": domain.FABRIC,
                    "routes": domain.domain_surface().get("routes"),
                    "forbidden_sibling_bc": list(
                        domain.catalog()["forbidden_sibling_bc"]
                    ),
                },
                "platform_mlops": {
                    "prompt_id": "P214-D",
                    "adr": 424,
                    "sor": "ai",
                    "product": mlops.PRODUCT,
                    "principle": mlops.PRINCIPLE,
                    "fabric": mlops.FABRIC,
                    "routes": mlops.mlops_surface().get("routes"),
                    "forbidden_sibling_bc": list(
                        mlops.catalog()["forbidden_sibling_bc"]
                    ),
                },
            }
        )

    def platform_foundation(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        cat = mod.catalog()
        return {
            "prompt_id": cat["prompt_id"],
            "adr": cat["adr"],
            "sor": cat["sor"],
            "capability": cat["capability"],
            "principle": cat["principle"],
            "fabric": cat["fabric"],
            "builds_on": cat["builds_on"],
            "context_count": cat["bounded_contexts"]["context_count"],
            "ai_paas_count": cat["ai_paas"]["capability_count"],
            "microservice_count": cat["microservices"]["service_count"],
            "production_readiness": cat["production_readiness"],
        }

    def foundation_vision(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.vision()

    def foundation_domain(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.domain_model()

    def foundation_bounded_contexts(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.bounded_contexts()

    def foundation_ai_paas(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.ai_paas()

    def foundation_ml(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.ml_platform()

    def foundation_generative(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.generative_ai()

    def foundation_llm(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.llm_management()

    def foundation_data(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.ai_data()

    def foundation_vectors(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.vector_intelligence()

    def foundation_agents(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.agent_foundation()

    def foundation_knowledge(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.knowledge_integration()

    def foundation_digital_twin(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.digital_twin_integration()

    def foundation_cqrs(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.cqrs()

    def foundation_events(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.events()

    def foundation_microservices(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.microservices()

    def foundation_api(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.api_first()

    def foundation_security(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.security()

    def foundation_deployment(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.deployment()

    def foundation_testing(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.testing()

    def foundation_outputs(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.cursor_outputs()

    def foundation_production_readiness(self) -> dict:
        from contexts.ai.domain.services import ai_platform_foundation as mod

        return mod.production_readiness()

    def foundation_readiness(self) -> dict:
        from contexts.ai.application.ai_foundation_foundation import (
            validate_ai_foundation_foundation,
        )

        return validate_ai_foundation_foundation()

    def platform_mission(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        cat = mod.catalog()
        return {
            "prompt_id": cat["prompt_id"],
            "adr": cat["adr"],
            "sor": cat["sor"],
            "capability": cat["capability"],
            "fabric": cat["fabric"],
            "mission": cat["mission"]["statement"],
            "vision": cat["vision"]["statement"],
            "builds_on": cat["builds_on"],
            "objective_count": cat["strategic_objectives"]["count"],
            "capability_domain_count": cat["capability_map"]["domain_count"],
            "maturity_level_count": cat["maturity_model"]["level_count"],
            "roadmap_phase_count": cat["transformation_roadmap"]["phase_count"],
            "production_readiness": cat["production_readiness"],
        }

    def mission_statement(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.mission()

    def mission_vision(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.vision()

    def mission_objectives(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.strategic_objectives()

    def mission_capability_map(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.capability_map()

    def mission_operating_model(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.operating_model()

    def mission_coe(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.center_of_excellence()

    def mission_maturity(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.maturity_model()

    def mission_value(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.value_framework()

    def mission_use_cases(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.use_case_framework()

    def mission_governance(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.governance_model()

    def mission_meos_alignment(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.meos_alignment()

    def mission_knowledge(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.knowledge_strategy()

    def mission_roadmap(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.transformation_roadmap()

    def mission_responsible_ai(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.responsible_ai()

    def mission_investment(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.investment_model()

    def mission_security(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.security_strategy()

    def mission_metrics(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.success_metrics()

    def mission_outputs(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.cursor_outputs()

    def mission_production_readiness(self) -> dict:
        from contexts.ai.domain.services import (
            ai_platform_mission_scope as mod,
        )

        return mod.production_readiness()

    def mission_readiness(self) -> dict:
        from contexts.ai.application.ai_mission_foundation import (
            validate_ai_mission_foundation,
        )

        return validate_ai_mission_foundation()

    def platform_domain(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        cat = mod.catalog()
        return {
            "prompt_id": cat["prompt_id"],
            "adr": cat["adr"],
            "sor": cat["sor"],
            "capability": cat["capability"],
            "principle": cat["principle"],
            "fabric": cat["fabric"],
            "builds_on": cat["builds_on"],
            "core_domain": cat["domain_map"]["core_domain"],
            "supporting_count": cat["domain_map"]["supporting_count"],
            "context_count": cat["bounded_contexts"]["context_count"],
            "microservice_count": cat["microservice_mapping"]["service_count"],
            "event_count": cat["events"]["core_event_count"],
            "production_readiness": cat["production_readiness"],
        }

    def domain_map(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.domain_map()

    def domain_core(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.core_domain_model()

    def domain_strategic(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return {
            "strategic_domains": mod.domain_map()["strategic_domains"],
            "strategic_count": mod.domain_map()["strategic_count"],
        }

    def domain_bounded_contexts(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.bounded_contexts()

    def domain_tactical(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.tactical_ddd()

    def domain_models(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.model_domain()

    def domain_generative(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.generative_domain()

    def domain_agents(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.agent_domain()

    def domain_knowledge(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.knowledge_domain()

    def domain_data(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.data_domain()

    def domain_security(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.security_domain()

    def domain_events(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.events()

    def domain_microservices(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.microservice_mapping()

    def domain_integration(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.integration()

    def domain_governance(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.governance()

    def domain_cqrs(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.cqrs()

    def domain_outputs(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.cursor_outputs()

    def domain_production_readiness(self) -> dict:
        from contexts.ai.domain.services import ai_platform_domain as mod

        return mod.production_readiness()

    def domain_readiness(self) -> dict:
        from contexts.ai.application.ai_domain_foundation import (
            validate_ai_domain_foundation,
        )

        return validate_ai_domain_foundation()

    def platform_mlops(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        cat = mod.catalog()
        return {
            "prompt_id": cat["prompt_id"],
            "adr": cat["adr"],
            "sor": cat["sor"],
            "capability": cat["capability"],
            "principle": cat["principle"],
            "fabric": cat["fabric"],
            "builds_on": cat["builds_on"],
            "context_count": cat["bounded_contexts"]["context_count"],
            "lifecycle_stage_count": cat["lifecycle"]["stage_count"],
            "microservice_count": cat["microservices"]["service_count"],
            "pipeline_count": cat["pipelines"]["pipeline_count"],
            "production_readiness": cat["production_readiness"],
        }

    def mlops_vision(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.vision()

    def mlops_domain(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.domain_model()

    def mlops_bounded_contexts(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.bounded_contexts()

    def mlops_lifecycle(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.lifecycle()

    def mlops_experiments(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.experiment_platform()

    def mlops_features(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.feature_store()

    def mlops_training(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.training_platform()

    def mlops_registry(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.model_registry()

    def mlops_validation(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.validation_platform()

    def mlops_deployment(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.deployment_platform()

    def mlops_monitoring(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.monitoring_platform()

    def mlops_continuous_training(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.continuous_training()

    def mlops_pipelines(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.pipelines()

    def mlops_cqrs(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.cqrs()

    def mlops_events(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.events()

    def mlops_microservices(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.microservices()

    def mlops_security(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.security()

    def mlops_infrastructure(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.deployment()

    def mlops_testing(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.testing()

    def mlops_outputs(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.cursor_outputs()

    def mlops_production_readiness(self) -> dict:
        from contexts.ai.domain.services import ai_platform_mlops as mod

        return mod.production_readiness()

    def mlops_readiness(self) -> dict:
        from contexts.ai.application.ai_mlops_foundation import (
            validate_ai_mlops_foundation,
        )

        return validate_ai_mlops_foundation()

    async def assist(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        module_id: str,
        surface: str,
        prompt: str,
        actor_user_id: str | None = None,
        context: dict | None = None,
    ) -> Result[dict]:
        text = (prompt or "").strip()
        if not text:
            return Result.fail("ai.errors.empty_prompt")
        ctx = context or {}
        refs = []
        for key in ("student_id", "course_id", "document_id", "sale_id"):
            if ctx.get(key):
                refs.append(f"{key}={ctx[key]}")
        ref_note = f" Context refs: {', '.join(refs)}." if refs else ""
        reply = (
            f"[Marpich AI · {module_id}/{surface}] I received your question about "
            f"«{text[:180]}».{ref_note} "
            "This is the Core AI platform assist surface — provider models are wired "
            "through the AI Service, not embedded in business modules."
        )
        session = AssistSession.create(
            tenant_id=tenant_id,
            module_id=module_id,
            surface=surface,
            prompt=text,
            reply=reply,
            actor_user_id=actor_user_id,
        )
        self._sessions[str(session.id)] = session
        await publish_integration_event(
            InsightGeneratedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                actor_user_id=actor_user_id,
                session_id=session.id,
                module_id=session.module_id,
                surface=session.surface,
                summary=reply[:240],
            )
        )
        return Result.ok(session.to_dict())
