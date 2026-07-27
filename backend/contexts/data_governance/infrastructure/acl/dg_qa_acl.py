"""ACL: Data Governance QA ↔ peers (P212-O)."""
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
        "peer_ids_only": True,
    }


def to_secrets(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "key_ref": key_ref,
        "via_p209": True,
        "peer_ids_only": True,
    }


def to_cyber_security(*, tenant_id: str, posture_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "posture_ref": posture_ref,
        "via_p210": True,
        "peer_ids_only": True,
    }


def to_data_security(*, tenant_id: str, classification_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "classification_ref": classification_ref,
        "via_p211": True,
        "peer_ids_only": True,
    }


def to_compliance(*, tenant_id: str, control_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "control_ref": control_ref,
        "via_compliance_framework": True,
        "module_local_compliance_tables_forbidden": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, evidence_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "evidence_ref": evidence_ref,
        "via_audit_platform": True,
        "module_local_certification_store_forbidden": True,
        "peer_ids_only": True,
    }


def to_graph(*, tenant_id: str, entity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "entity_ref": entity_ref,
        "via_p212_j": True,
        "knowledge_graph_integration_present_required": True,
        "peer_ids_only": True,
    }


def to_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "twin_ref": twin_ref,
        "via_p212_l": True,
        "digital_twin_integration_present_required": True,
        "peer_ids_only": True,
    }


def to_deploy(*, tenant_id: str, deploy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "deploy_ref": deploy_ref,
        "via_p212_n": True,
        "peer_ids_only": True,
    }


def to_event_bus(*, tenant_id: str, topic_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "topic_ref": topic_ref,
        "via_enterprise_event_bus": True,
        "module_local_broker_forbidden": True,
        "peer_ids_only": True,
    }


def to_api_gateway(*, tenant_id: str, route_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "route_ref": route_ref,
        "via_api_gateway": True,
        "module_local_gateway_forbidden": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
        "peer_ids_only": True,
    }
