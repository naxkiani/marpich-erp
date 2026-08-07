"""ACL: Scientific intelligence to platform peers (P218-K)."""
from __future__ import annotations

from typing import Any


def _peer(tenant_id: str, key: str, value: str, **laws: bool) -> dict[str, Any]:
    return {"tenant_id": tenant_id, key: value, **laws, "peer_ids_only": True}


def to_space_foundation(*, tenant_id: str, foundation_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "foundation_ref", foundation_ref, via_p218=True, never_replace_p218_foundation=True)


def to_space_mission(*, tenant_id: str, mission_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "mission_ref", mission_ref, via_p218_a=True, never_replace_p218_a_mission=True)


def to_space_strategy(*, tenant_id: str, strategy_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "strategy_ref", strategy_ref, via_p218_b=True, never_replace_p218_b_strategy=True)


def to_space_domain(*, tenant_id: str, domain_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "domain_ref", domain_ref, via_p218_c=True, never_replace_p218_c_domain=True)


def to_space_infrastructure(*, tenant_id: str, infra_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "infra_ref", infra_ref, via_p218_d=True, never_replace_p218_d_infrastructure=True)


def to_space_ai(*, tenant_id: str, space_ai_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "space_ai_ref", space_ai_ref, via_p218_e=True, never_replace_p218_e_space_ai=True, space_ai_via_p214z_acl_only=True, no_module_local_llm=True)


def to_satellite(*, tenant_id: str, satellite_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "satellite_ref", satellite_ref, via_p218_f=True, never_replace_p218_f_satellite=True)


def to_orbital(*, tenant_id: str, orbital_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "orbital_ref", orbital_ref, via_p218_g=True, never_replace_p218_g_orbital=True)


def to_communications(*, tenant_id: str, communications_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "communications_ref", communications_ref, via_p218_h=True, never_replace_p218_h_communications=True)


def to_navigation(*, tenant_id: str, navigation_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "navigation_ref", navigation_ref, via_p218_i=True, never_replace_p218_i_navigation=True)


def to_mission_intel(*, tenant_id: str, mission_intel_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "mission_intel_ref", mission_intel_ref, via_p218_j=True, never_replace_p218_j_mission_intel=True)


def to_biotechnology(*, tenant_id: str, bio_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "bio_ref", bio_ref, via_p217=True, never_replace_biotechnology=True)


def to_robotics_supreme(*, tenant_id: str, robotics_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "robotics_ref", robotics_ref, via_p216_z=True, never_replace_p216_z=True)


def to_quantum_supreme(*, tenant_id: str, supreme_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "supreme_ref", supreme_ref, via_p215_z=True, never_replace_p215_z=True)


def to_master_ai(*, tenant_id: str, master_ai_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "master_ai_ref", master_ai_ref, via_p214_z=True, never_replace_ai_platform=True, space_ai_via_p214z_acl_only=True, no_module_local_llm=True)


def to_integration(*, tenant_id: str, integration_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "integration_ref", integration_ref, via_integration=True, no_module_local_telemetry_stack=True, no_module_local_communications_radio_stack=True, no_module_local_gnss_receiver_stack=True)


def to_policy_engine(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return _peer(
        tenant_id, "policy_ref", policy_ref, via_policy_engine=True,
        never_ungated_autonomous_experiment_execution=True,
        never_skip_scientific_ethics_review=True,
        never_skip_peer_review_gate=True,
        never_skip_reproducibility_validation=True,
        never_violate_fair_data_principles=True,
    )


def to_workflow(*, tenant_id: str, workflow_ref: str) -> dict[str, Any]:
    return _peer(
        tenant_id, "workflow_ref", workflow_ref, via_workflow=True,
        never_ungated_autonomous_experiment_execution=True,
        never_skip_scientific_ethics_review=True,
        never_skip_peer_review_gate=True,
        never_skip_reproducibility_validation=True,
        never_disable_human_override=True,
    )


def to_audit(*, tenant_id: str, audit_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "audit_ref", audit_ref, via_audit=True, never_opaque_unexplainable_decisions=True)


def to_identity(*, tenant_id: str, identity_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "identity_ref", identity_ref, via_identity=True)


def to_core_platform(*, tenant_id: str, core_ref: str) -> dict[str, Any]:
    return _peer(tenant_id, "core_ref", core_ref, via_core_platform=True, never_replace_core_platform=True)


def to_enterprise_space(*, tenant_id: str, scientific_ref: str) -> dict[str, Any]:
    return _peer(
        tenant_id, "scientific_ref", scientific_ref,
        via_enterprise_space=True, module_local_scientific_forbidden=True,
        never_replace_p218_j_mission_intel=True,
        never_ungated_autonomous_experiment_execution=True,
        never_skip_scientific_ethics_review=True,
        never_skip_peer_review_gate=True,
        never_skip_reproducibility_validation=True,
        never_violate_fair_data_principles=True,
        space_ai_via_p214z_acl_only=True, no_module_local_llm=True,
    )
