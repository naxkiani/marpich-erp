"""Trust Fabric facade — continuous, explainable trust (P200-B6)."""
from __future__ import annotations

from contexts.identity_federation.domain.services import (
    trust_graph_engine,
    trust_management_engine,
    trust_score_engine,
    zero_trust_federation_engine,
)
from contexts.identity_federation.domain.value_objects.trust_levels import (
    can_transition,
    level_from_score,
    level_name,
)


class TrustFabricEngine:
    """Produces trust facts + explanations — never Permit/Deny."""

    def evaluate_continuous(
        self,
        *,
        inputs: dict | None = None,
        prior_score: int | None = None,
        weights: dict | None = None,
        zero_trust_ctx: dict | None = None,
    ) -> dict:
        score = trust_score_engine.compute_continuous_score(
            inputs=inputs, prior_score=prior_score, weights=weights
        )
        zt = zero_trust_federation_engine.evaluate_federation_zero_trust(**(zero_trust_ctx or {}))
        # Blend ZT adverse signals into explanation (facts only)
        if zt.get("action") == "deny":
            penalized = min(score["trust_score"], 25)
            score = {
                **score,
                "trust_score": penalized,
                "enterprise_level": level_from_score(penalized),
                "enterprise_level_name": level_name(level_from_score(penalized)),
                "factors": list(score["factors"]) + ["zero_trust_adverse"],
                "zero_trust": zt,
            }
        else:
            score = {**score, "zero_trust": zt}
        score["decision_type"] = "trust_facts"
        score["permit_deny"] = None
        return score

    def evaluate_hierarchy(self, **kwargs) -> dict:
        return trust_management_engine.evaluate_trust_hierarchy(**kwargs)

    def evaluate_enterprise_dimensions(self, **kwargs) -> dict:
        return trust_management_engine.evaluate_enterprise_trust(**kwargs)

    def transition_level(
        self, *, from_level: int, to_level: int, score: int, evidence_types: set[str]
    ) -> dict:
        return can_transition(
            from_level=from_level,
            to_level=to_level,
            score=score,
            evidence_types=evidence_types,
        )

    def empty_graph(self, tenant_id: str) -> dict:
        return trust_graph_engine.empty_graph(tenant_id)

    def graph_neighbors(self, graph: dict, **kwargs) -> dict:
        return trust_graph_engine.query_neighbors(graph, **kwargs)

    def graph_path(self, graph: dict, **kwargs) -> dict:
        return trust_graph_engine.find_path(graph, **kwargs)

    def graph_catalog(self) -> dict:
        return trust_graph_engine.catalog()


_fabric: TrustFabricEngine | None = None


def get_trust_fabric_engine() -> TrustFabricEngine:
    global _fabric
    if _fabric is None:
        _fabric = TrustFabricEngine()
    return _fabric
