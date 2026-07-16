"""Data isolation engine."""
from __future__ import annotations

import zlib

from contexts.data_isolation.domain.aggregates.data_isolation_platform import IsolationCapability

POLICY_KEYS = [
    "data_isolation.rls.enabled",
    "data_isolation.principal_partitioning.enabled",
    "data_isolation.tenant_context.required",
]

CAPABILITY_LABELS = {
    IsolationCapability.RLS_CATALOG.value: "RLS Catalog",
    IsolationCapability.RLS_POLICY_REGISTRY.value: "RLS Policy Registry",
    IsolationCapability.PRINCIPAL_REGISTRY.value: "Principal Registry",
    IsolationCapability.PRINCIPAL_PARTITIONING.value: "Principal Partitioning",
    IsolationCapability.TENANT_CONTEXT_BINDING.value: "Tenant Context Binding",
    IsolationCapability.ISOLATION_VERIFICATION.value: "Isolation Verification",
    IsolationCapability.POLICY_DRIVEN_ISOLATION.value: "Policy-Driven Isolation",
    IsolationCapability.DATA_ISOLATION_DASHBOARD.value: "Data Isolation Dashboard",
    IsolationCapability.PRINCIPAL_SYNC.value: "Principal Sync",
    IsolationCapability.DATA_ISOLATION_API.value: "Data Isolation API",
}

RLS_PROTECTED_TABLES = [
    ("identity", "users", "tenant_isolation_users"),
    ("identity", "roles", "tenant_isolation_roles"),
    ("identity", "sessions", "tenant_isolation_sessions"),
    ("identity", "principals", "tenant_isolation_principals"),
    ("authorization", "access_decisions", "tenant_isolation_access_decisions"),
]


def list_capability_catalog() -> list[dict]:
    return [
        {"capability": c.value, "label": CAPABILITY_LABELS.get(c.value, c.name.replace("_", " ").title())}
        for c in IsolationCapability
    ]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def list_rls_policies() -> list[dict]:
    return [
        {"schema": schema, "table": table, "policy": policy, "session_var": "app.tenant_id"}
        for schema, table, policy in RLS_PROTECTED_TABLES
    ]


def partition_bucket(tenant_id: str, modulus: int) -> int:
    if modulus <= 0:
        return 0
    return zlib.crc32(tenant_id.encode("utf-8")) % modulus


def dependency_map() -> dict:
    return {
        "nodes": [
            {"id": "data_isolation", "type": "platform", "label": "Data Isolation"},
            {"id": "identity", "type": "platform", "label": "Identity Core"},
            {"id": "authorization", "type": "platform", "label": "Authorization PDP"},
        ],
        "edges": [
            {"from": "data_isolation", "to": "identity", "type": "principal_sync"},
            {"from": "authorization", "to": "data_isolation", "type": "decision_partition"},
        ],
    }


def build_dashboard(
    *,
    profile: dict | None,
    principals: list[dict],
    policies: list[dict],
    partition_modulus: int,
) -> dict:
    buckets: dict[int, int] = {}
    for principal in principals:
        bucket = int(principal.get("partition_bucket", 0))
        buckets[bucket] = buckets.get(bucket, 0) + 1
    return {
        "summary": {
            "capabilities": len(list_capability_catalog()),
            "rls_policies": len(policies),
            "principals": len(principals),
            "partition_modulus": partition_modulus,
            "partition_buckets_used": len(buckets),
        },
        "profile": profile,
        "partition_distribution": buckets,
        "rls_policies": policies,
    }
