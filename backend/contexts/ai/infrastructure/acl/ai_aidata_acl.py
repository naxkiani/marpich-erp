"""ACL: AI Data Intelligence ↔ peers (P214-K)."""
from __future__ import annotations

from typing import Any


def to_identity(*, tenant_id: str, identity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "identity_ref": identity_ref,
        "via_p207": True,
        "peer_ids_only": True,
    }


def to_authorization(
    *, tenant_id: str, principal_ref: str, action: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "principal_ref": principal_ref,
        "action": action,
        "via_p208": True,
        "dataset_authorization": True,
        "peer_ids_only": True,
    }


def to_cryptographic_trust(
    *, tenant_id: str, secret_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "secret_ref": secret_ref,
        "via_p209": True,
        "peer_ids_only": True,
    }


def to_cyber_security(*, tenant_id: str, control_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "control_ref": control_ref,
        "via_p210": True,
        "peer_ids_only": True,
    }


def to_data_security(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211": True,
        "ai_asset_protection": True,
        "peer_ids_only": True,
    }


def to_data_governance(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p212": True,
        "mesh_product_contract": True,
        "peer_ids_only": True,
    }


def to_metadata(*, tenant_id: str, lineage_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "lineage_ref": lineage_ref,
        "via_p212_k": True,
        "lineage_integration": True,
        "peer_ids_only": True,
    }


def to_analytics(*, tenant_id: str, metric_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "metric_ref": metric_ref,
        "via_p213": True,
        "peer_ids_only": True,
    }


def to_ops_deploy(*, tenant_id: str, release_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "release_ref": release_ref,
        "via_p213_o": True,
        "peer_ids_only": True,
    }


def to_mlops(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_p214_d": True,
        "feature_consumption": True,
        "peer_ids_only": True,
    }


def to_genai(*, tenant_id: str, corpus_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "corpus_ref": corpus_ref,
        "via_p214_e": True,
        "peer_ids_only": True,
    }


def to_agents(*, tenant_id: str, agent_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "agent_ref": agent_ref,
        "via_p214_f": True,
        "peer_ids_only": True,
    }


def to_knowledge(*, tenant_id: str, knowledge_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "knowledge_ref": knowledge_ref,
        "via_p214_g": True,
        "rag_corpus_product": True,
        "peer_ids_only": True,
    }


def to_governance(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_p214_h": True,
        "synthetic_rai_review": True,
        "peer_ids_only": True,
    }


def to_aisec(*, tenant_id: str, security_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "security_ref": security_ref,
        "via_p214_i": True,
        "poisoning_defense": True,
        "peer_ids_only": True,
    }


def to_aiops(*, tenant_id: str, pipeline_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "pipeline_ref": pipeline_ref,
        "via_p214_j": True,
        "pipeline_health": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(*, tenant_id: str, aidata_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "aidata_ref": aidata_ref,
        "via_enterprise_ai": True,
        "module_local_feature_store_forbidden": True,
        "peer_ids_only": True,
    }


def to_api_gateway(*, tenant_id: str, route_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "route_ref": route_ref,
        "via_api_gateway": True,
        "peer_ids_only": True,
    }
