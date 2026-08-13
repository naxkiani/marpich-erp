"""Authorization PDP application service."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from contexts.authorization.domain.aggregates.authorization_platform import (
    AbacPolicy,
    AccessDecision,
    AuthorizationProfile,
    RelationTuple,
)
from contexts.authorization.domain.events.authorization_integration_events import (
    AccessDeniedIntegration,
    AccessGrantedIntegration,
    AuthorizationDashboardGeneratedIntegration,
    RelationChangedIntegration,
)
from contexts.authorization.domain.ports.authorization_repositories import (
    IAbacPolicyRepository,
    IAccessDecisionRepository,
    IAuthorizationProfileRepository,
    IPrincipalAccessPort,
    IRelationTupleRepository,
)
from contexts.authorization.domain.services import authorization_engine as engine
from contexts.authorization.domain.services import rebac_engine, rule_compiler
from contexts.authorization.domain.services.decision_cache import (
    IDecisionCache,
    InMemoryDecisionCache,
    build_cache_key,
)
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class AuthorizationApplicationService:
    def __init__(
        self,
        profiles: IAuthorizationProfileRepository,
        abac_policies: IAbacPolicyRepository,
        decisions: IAccessDecisionRepository,
        principals: IPrincipalAccessPort,
        policy_evaluator: IPolicyEvaluator,
        relations: IRelationTupleRepository,
        decision_cache: IDecisionCache | None = None,
    ) -> None:
        self._profiles = profiles
        self._abac_policies = abac_policies
        self._decisions = decisions
        self._principals = principals
        self._policy = policy_evaluator
        self._relations = relations
        self._cache = decision_cache or InMemoryDecisionCache()

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "rbac_enabled": profile.rbac_enabled if profile else True,
            "rebac_enabled": profile.rebac_enabled if profile else True,
            "abac_enabled": profile.abac_enabled if profile else True,
            "pbac_enabled": profile.pbac_enabled if profile else True,
            "default_decision": profile.default_decision if profile else "deny",
        }
        pmap = {
            "authorization.rbac.enabled": ("rbac_enabled", "enabled"),
            "authorization.abac.enabled": ("abac_enabled", "enabled"),
            "authorization.pbac.enabled": ("pbac_enabled", "enabled"),
            "authorization.default_decision": ("default_decision", "decision"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> AuthorizationProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = AuthorizationProfile.create(
            tenant_id=tenant_id,
            profile_ref=self._profiles.next_profile_ref(tenant_id),
        )
        await self._profiles.save(profile)
        return profile

    async def handle_tenant_provisioned(self, event: dict) -> None:
        tenant_id = event.get("tenant_id") or event.get("payload", {}).get("tenant_id")
        if tenant_id:
            await self.seed(tenant_id)

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": engine.list_capability_catalog(),
            "policy_keys": engine.list_policy_keys(),
            "evaluation_order": engine.dependency_map()["evaluation_order"],
            "rule_compiler": rule_compiler.catalog(),
            "rebac": {
                "action_relation_map": rebac_engine.ACTION_RELATION_MAP,
                "resource_uri": "marpich://{object_type}/{object_id}",
            },
            "decision_cache": {"ttl_profile_field": "decision_cache_ttl_seconds"},
            "delegation": {
                "principal_permissions": "identity",
                "pbac_rules": "policy",
                "local_duplication": False,
            },
        })

    async def get_dependency_map(self) -> Result[dict]:
        return Result.ok(engine.dependency_map())

    async def seed(self, tenant_id: str) -> Result[dict]:
        await self._ensure_profile(tenant_id)
        seed_data = engine.generate_seed_data()
        created = 0
        for pdata in seed_data["abac_policies"]:
            policy = AbacPolicy.create(
                tenant_id=tenant_id,
                policy_ref=self._abac_policies.next_policy_ref(tenant_id),
                name=pdata["name"],
                effect=pdata["effect"],
                permission_pattern=pdata["permission_pattern"],
                conditions=pdata["conditions"],
                priority=pdata.get("priority", 100),
            )
            await self._abac_policies.save(policy)
            created += 1
        return Result.ok({"seeded": True, "abac_policies": created})

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        policies = [p.to_dict() for p in await self._abac_policies.list_by_tenant(tenant_id)]
        decisions = [d.to_dict() for d in await self._decisions.list_by_tenant(tenant_id)]
        dashboard = engine.build_dashboard(profile=profile.to_dict() if profile else None, policies=policies, decisions=decisions)
        await publish_integration_event(
            AuthorizationDashboardGeneratedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                decisions_total=dashboard["summary"]["decisions_total"],
                policies_total=dashboard["summary"]["abac_policies"],
            )
        )
        return Result.ok(dashboard)

    async def _build_facts(
        self,
        tenant_id: str,
        principal_id: str,
        context: dict | None,
    ) -> dict:
        attrs = await self._principals.resolve_principal_attributes(tenant_id, principal_id)
        facts = {**attrs, **(context or {})}
        if "hour_utc" not in facts:
            facts["hour_utc"] = datetime.now(UTC).hour
        return facts

    async def _resolve_policy_key(self, tenant_id: str, permission_code: str, context: dict | None) -> str | None:
        explicit = (context or {}).get("policy_key")
        if explicit:
            return str(explicit)
        parts = permission_code.split(".")
        if len(parts) >= 2:
            return f"{parts[0]}.{parts[1]}.access.enabled"
        return None

    async def check_access(
        self,
        tenant_id: str,
        *,
        principal_id: str,
        resource: str = "",
        action: str = "",
        permission_code: str | None = None,
        context: dict | None = None,
        simulate: bool = False,
        record: bool = True,
    ) -> Result[dict]:
        perm = engine.resolve_permission_code(
            permission_code=permission_code,
            resource=resource,
            action=action,
        )
        profile_entity = await self._profiles.find_by_tenant(tenant_id)
        profile = profile_entity.to_dict() if profile_entity else None
        policy_params = await self._policy_params(tenant_id)
        if profile:
            profile = {**profile, **policy_params}

        permissions = await self._principals.resolve_permissions(tenant_id, principal_id)
        if not permissions:
            return Result.fail("principal_not_found")

        facts = await self._build_facts(tenant_id, principal_id, context)
        abac_policies = [p.to_dict() for p in await self._abac_policies.list_by_tenant(tenant_id)]

        cache_ttl = int((profile or {}).get("decision_cache_ttl_seconds") or 30)
        cache_key = build_cache_key(
            tenant_id=tenant_id,
            principal_id=principal_id,
            permission_code=perm,
            resource=resource,
            action=action,
            facts=facts,
        )
        if not simulate and record and cache_ttl > 0:
            cached = await self._cache.get(cache_key)
            if cached:
                cached = {**cached, "cache_hit": True}
                return Result.ok(cached)

        object_type = str(facts.get("object_type") or "")
        object_id = str(facts.get("object_id") or "")
        parsed = rebac_engine.parse_resource_uri(resource)
        if parsed and not object_type:
            object_type, object_id = parsed
        relation_tuples: list[dict] = []
        if object_type and object_id:
            relation_tuples = [
                t.to_dict()
                for t in await self._relations.list_by_object(tenant_id, object_type, object_id)
            ]

        policy_key = await self._resolve_policy_key(tenant_id, perm, context)
        policy_decision = None
        if policy_key and (profile or {}).get("pbac_enabled", True):
            pd = await self._policy.evaluate(
                tenant_id=tenant_id,
                domain=perm.split(".")[0] if "." in perm else "platform",
                policy_key=policy_key,
                facts=facts,
            )
            policy_decision = pd.to_dict()

        result = engine.evaluate_access(
            profile=profile,
            permissions=permissions,
            abac_policies=abac_policies,
            permission_code=perm,
            resource=resource,
            action=action,
            facts=facts,
            policy_decision=policy_decision,
            policy_key=policy_key,
            relation_tuples=relation_tuples,
            principal_id=principal_id,
            simulate=simulate,
        )
        result["cache_hit"] = False

        if record and not simulate:
            decision = AccessDecision.record(
                tenant_id=tenant_id,
                decision_ref=self._decisions.next_decision_ref(tenant_id),
                principal_id=principal_id,
                permission_code=perm,
                resource=resource,
                action=action,
                decision=result["decision"],
                model=result["model"],
                reason_codes=result["reason_codes"],
                policy_keys=result["policy_keys"],
                obligations=result["obligations"],
                facts=facts,
            )
            await self._decisions.save(decision)
            result["decision_ref"] = decision.decision_ref
            correlation_id = str(uuid.uuid4())
            if result["decision"] == "allow":
                await publish_integration_event(
                    AccessGrantedIntegration(
                        tenant_id=TenantId(tenant_id),
                        correlation_id=correlation_id,
                        decision_ref=decision.decision_ref,
                        principal_id=principal_id,
                        permission_code=perm,
                    )
                )
            else:
                await publish_integration_event(
                    AccessDeniedIntegration(
                        tenant_id=TenantId(tenant_id),
                        correlation_id=correlation_id,
                        decision_ref=decision.decision_ref,
                        principal_id=principal_id,
                        permission_code=perm,
                        reason_codes=result["reason_codes"],
                    )
                )

        if not simulate and record and cache_ttl > 0:
            await self._cache.set(cache_key, {k: v for k, v in result.items() if k != "cache_hit"}, cache_ttl)

        return Result.ok(result)

    async def check_access_batch(
        self,
        tenant_id: str,
        *,
        principal_id: str,
        checks: list[dict],
        simulate: bool = False,
    ) -> Result[list[dict]]:
        results = []
        for item in checks:
            result = await self.check_access(
                tenant_id,
                principal_id=principal_id,
                resource=item.get("resource", ""),
                action=item.get("action", ""),
                permission_code=item.get("permission_code"),
                context=item.get("context"),
                simulate=simulate,
                record=not simulate,
            )
            if not result.succeeded:
                results.append({"error": result.error, **item})
            else:
                results.append(result.unwrap())
        return Result.ok(results)

    async def write_relation(
        self,
        tenant_id: str,
        *,
        object_type: str,
        object_id: str,
        relation: str,
        subject_type: str,
        subject_id: str,
    ) -> Result[dict]:
        existing = await self._relations.find_exact(
            tenant_id,
            object_type=object_type,
            object_id=object_id,
            relation=relation,
            subject_type=subject_type,
            subject_id=subject_id,
        )
        if existing and existing.active:
            return Result.ok(existing.to_dict())
        if existing and not existing.active:
            existing.active = True
            await self._relations.save(existing)
            tuple_ = existing
        else:
            tuple_ = RelationTuple.write(
                tenant_id=tenant_id,
                relation_ref=self._relations.next_relation_ref(tenant_id),
                object_type=object_type,
                object_id=object_id,
                relation=relation,
                subject_type=subject_type,
                subject_id=subject_id,
            )
            await self._relations.save(tuple_)
        await self._cache.invalidate_tenant(tenant_id)
        await publish_integration_event(
            RelationChangedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                relation_ref=tuple_.relation_ref,
                change="written",
                object_type=tuple_.object_type,
                object_id=tuple_.object_id,
                relation=tuple_.relation,
                subject_id=tuple_.subject_id,
            )
        )
        return Result.ok(tuple_.to_dict())

    async def revoke_relation(
        self,
        tenant_id: str,
        *,
        object_type: str,
        object_id: str,
        relation: str,
        subject_type: str,
        subject_id: str,
    ) -> Result[dict]:
        existing = await self._relations.find_exact(
            tenant_id,
            object_type=object_type,
            object_id=object_id,
            relation=relation,
            subject_type=subject_type,
            subject_id=subject_id,
        )
        if not existing:
            return Result.fail("relation_not_found")
        existing.revoke()
        await self._relations.save(existing)
        await self._cache.invalidate_tenant(tenant_id)
        await publish_integration_event(
            RelationChangedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                relation_ref=existing.relation_ref,
                change="revoked",
                object_type=existing.object_type,
                object_id=existing.object_id,
                relation=existing.relation,
                subject_id=existing.subject_id,
            )
        )
        return Result.ok(existing.to_dict())

    async def list_relations_for_object(
        self, tenant_id: str, object_type: str, object_id: str
    ) -> Result[list[dict]]:
        items = await self._relations.list_by_object(tenant_id, object_type, object_id)
        return Result.ok([t.to_dict() for t in items])

    async def invalidate_decision_cache(self, tenant_id: str) -> Result[dict]:
        await self._cache.invalidate_tenant(tenant_id)
        return Result.ok({"invalidated": True, "tenant_id": tenant_id})

    async def list_abac_policies(self, tenant_id: str) -> Result[list[dict]]:
        policies = await self._abac_policies.list_by_tenant(tenant_id)
        return Result.ok([p.to_dict() for p in policies])

    async def create_abac_policy(
        self,
        tenant_id: str,
        *,
        name: str,
        effect: str,
        permission_pattern: str,
        conditions: list[dict] | None = None,
        priority: int = 100,
    ) -> Result[dict]:
        try:
            compiled = rule_compiler.compile_conditions(conditions)
        except rule_compiler.RuleCompilationError as exc:
            return Result.fail(f"invalid_abac_conditions:{exc}")
        if effect not in {"allow", "deny"}:
            return Result.fail("invalid_abac_effect")
        policy = AbacPolicy.create(
            tenant_id=tenant_id,
            policy_ref=self._abac_policies.next_policy_ref(tenant_id),
            name=name,
            effect=effect,
            permission_pattern=permission_pattern,
            conditions=compiled.to_dicts(),
            priority=priority,
        )
        await self._abac_policies.save(policy)
        await self._cache.invalidate_tenant(tenant_id)
        return Result.ok(policy.to_dict())

    async def compile_abac_rules(self, conditions: list[dict] | None) -> Result[dict]:
        try:
            compiled = rule_compiler.compile_conditions(conditions)
        except rule_compiler.RuleCompilationError as exc:
            return Result.fail(f"invalid_abac_conditions:{exc}")
        return Result.ok({"conditions": compiled.to_dicts(), "valid": True})

    async def list_decisions(self, tenant_id: str) -> Result[list[dict]]:
        decisions = await self._decisions.list_by_tenant(tenant_id)
        return Result.ok([d.to_dict() for d in decisions])
