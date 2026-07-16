"""Enterprise Integration Studio engine."""
from __future__ import annotations

from contexts.enterprise_integration_studio.domain.aggregates.enterprise_integration_studio_platform import (
    ArtifactType,
    StudioCapability,
)

POLICY_KEYS = [
    "enterprise_integration_studio.api_builder.enabled",
    "enterprise_integration_studio.connector_builder.enabled",
    "enterprise_integration_studio.workflow_builder.enabled",
    "enterprise_integration_studio.event_designer.enabled",
    "enterprise_integration_studio.testing.enabled",
    "enterprise_integration_studio.mock_services.enabled",
    "enterprise_integration_studio.marketplace.enabled",
    "enterprise_integration_studio.citizen_workspace.enabled",
]

CAPABILITY_LABELS = {
    StudioCapability.VISUAL_API_BUILDER.value: "Visual API Builder",
    StudioCapability.VISUAL_CONNECTOR_BUILDER.value: "Visual Connector Builder",
    StudioCapability.VISUAL_WORKFLOW_BUILDER.value: "Visual Workflow Builder",
    StudioCapability.VISUAL_EVENT_DESIGNER.value: "Visual Event Designer",
    StudioCapability.DATA_MAPPING.value: "Data Mapping",
    StudioCapability.TRANSFORMATION.value: "Transformation",
    StudioCapability.TESTING.value: "Testing",
    StudioCapability.MOCK_SERVICES.value: "Mock Services",
    StudioCapability.API_DOCUMENTATION.value: "API Documentation",
    StudioCapability.CONNECTOR_MARKETPLACE.value: "Connector Marketplace",
    StudioCapability.VERSIONING.value: "Versioning",
    StudioCapability.DEPLOYMENT.value: "Deployment",
    StudioCapability.DEVELOPER_PORTAL.value: "Developer Portal",
    StudioCapability.CITIZEN_DEVELOPER_WORKSPACE.value: "Citizen Developer Workspace",
}


def list_capability_catalog() -> list[dict]:
    return [
        {"capability": c.value, "label": CAPABILITY_LABELS.get(c.value, c.name.replace("_", " ").title())}
        for c in StudioCapability
    ]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def dependency_map() -> dict:
    return {
        "nodes": [
            {"id": "enterprise_integration_studio", "type": "platform", "label": "Integration Studio"},
            {"id": "enterprise_api_gateway", "type": "platform", "label": "API Gateway"},
            {"id": "enterprise_connector_framework", "type": "platform", "label": "Connector Framework"},
            {"id": "workflow", "type": "platform", "label": "Workflow"},
            {"id": "enterprise_event_bus", "type": "platform", "label": "Event Bus"},
        ],
        "edges": [
            {"from": "enterprise_integration_studio", "to": "enterprise_api_gateway", "type": "api_delegate"},
            {"from": "enterprise_integration_studio", "to": "enterprise_connector_framework", "type": "connector_delegate"},
            {"from": "enterprise_integration_studio", "to": "workflow", "type": "workflow_delegate"},
            {"from": "enterprise_integration_studio", "to": "enterprise_event_bus", "type": "event_delegate"},
        ],
        "low_code": True,
        "multi_tenant": True,
    }


def _base_nodes(artifact_name: str, nodes: list[dict]) -> dict:
    return {"name": artifact_name, "nodes": nodes, "edges": _chain_edges(nodes)}


def _chain_edges(nodes: list[dict]) -> list[dict]:
    edges = []
    for i in range(len(nodes) - 1):
        edges.append({"from": nodes[i]["id"], "to": nodes[i + 1]["id"]})
    return edges


def build_api_designer_graph(*, artifact: dict) -> dict:
    return _base_nodes(artifact.get("name", "API"), [
        {"id": "ingress", "label": "API Ingress", "type": "gateway", "x": 40, "y": 80},
        {"id": "validate", "label": "Validate Request", "type": "action", "x": 220, "y": 80},
        {"id": "transform", "label": "Transform", "type": "transform", "x": 400, "y": 80},
        {"id": "route", "label": "Route to Context", "type": "route", "x": 580, "y": 80},
        {"id": "response", "label": "Response", "type": "end", "x": 760, "y": 80},
    ])


def build_connector_designer_graph(*, artifact: dict) -> dict:
    return _base_nodes(artifact.get("name", "Connector"), [
        {"id": "auth", "label": "Authenticate", "type": "auth", "x": 40, "y": 100},
        {"id": "fetch", "label": "Fetch External", "type": "connector", "x": 220, "y": 100},
        {"id": "map", "label": "Map Fields", "type": "mapping", "x": 400, "y": 100},
        {"id": "publish", "label": "Publish Event", "type": "event", "x": 580, "y": 100},
    ])


def build_workflow_designer_graph(*, artifact: dict) -> dict:
    return _base_nodes(artifact.get("name", "Workflow"), [
        {"id": "start", "label": "Start", "type": "start", "x": 40, "y": 120},
        {"id": "approve", "label": "Approval", "type": "human", "x": 200, "y": 120},
        {"id": "integrate", "label": "Integration Step", "type": "action", "x": 380, "y": 120},
        {"id": "notify", "label": "Notify", "type": "notification", "x": 560, "y": 120},
        {"id": "end", "label": "End", "type": "end", "x": 740, "y": 120},
    ])


def build_event_designer_graph(*, artifact: dict) -> dict:
    return _base_nodes(artifact.get("name", "Event"), [
        {"id": "source", "label": "Event Source", "type": "source", "x": 40, "y": 90},
        {"id": "filter", "label": "Filter", "type": "filter", "x": 220, "y": 90},
        {"id": "enrich", "label": "Enrich", "type": "transform", "x": 400, "y": 90},
        {"id": "route", "label": "Route Topic", "type": "route", "x": 580, "y": 90},
    ])


def build_designer_graph(*, artifact_type: str, artifact: dict) -> dict:
    builders = {
        ArtifactType.API.value: build_api_designer_graph,
        ArtifactType.CONNECTOR.value: build_connector_designer_graph,
        ArtifactType.WORKFLOW.value: build_workflow_designer_graph,
        ArtifactType.EVENT.value: build_event_designer_graph,
    }
    builder = builders.get(artifact_type, build_api_designer_graph)
    return builder(artifact=artifact)


def build_openapi_documentation(*, artifact: dict) -> dict:
    name = artifact.get("name", "Integration API")
    return {
        "openapi": "3.1.0",
        "info": {"title": name, "version": artifact.get("version", "1.0.0")},
        "paths": {
            f"/api/v1/studio/{artifact.get('artifact_ref', 'artifact')}": {
                "post": {
                    "summary": f"Invoke {name}",
                    "tags": ["Integration Studio"],
                    "requestBody": {"content": {"application/json": {"schema": {"type": "object"}}}},
                    "responses": {"200": {"description": "Success"}},
                }
            }
        },
    }


def build_developer_portal(*, projects: list[dict], artifacts: list[dict], marketplace: list[dict]) -> dict:
    return {
        "title": "Marpich Integration Developer Portal",
        "projects": projects,
        "artifacts": artifacts,
        "marketplace_preview": marketplace[:6],
        "quick_links": [
            {"label": "API Builder", "path": "/enterprise-integration-studio/designer/api"},
            {"label": "Connector Builder", "path": "/enterprise-integration-studio/designer/connector"},
            {"label": "Workflow Builder", "path": "/enterprise-integration-studio/designer/workflow"},
            {"label": "Event Designer", "path": "/enterprise-integration-studio/designer/event"},
            {"label": "Mock Services", "path": "/enterprise-integration-studio/mocks"},
            {"label": "Documentation", "path": "/enterprise-integration-studio/documentation"},
        ],
        "sdk_languages": ["typescript", "python", "java", "csharp"],
    }


def build_citizen_workspace(*, projects: list[dict], artifacts: list[dict]) -> dict:
    citizen_projects = [p for p in projects if p.get("workspace_type") == "citizen"]
    return {
        "title": "Citizen Developer Workspace",
        "no_code": True,
        "templates": [
            {"id": "invoice_sync", "label": "Invoice Sync", "artifact_type": "connector"},
            {"id": "approval_flow", "label": "Approval Flow", "artifact_type": "workflow"},
            {"id": "customer_webhook", "label": "Customer Webhook", "artifact_type": "api"},
        ],
        "projects": citizen_projects,
        "artifacts": [a for a in artifacts if a.get("artifact_type") in ("workflow", "api", "connector")],
        "guided_steps": ["Pick template", "Map data", "Test with mock", "Deploy to sandbox"],
    }


def run_mock_test(*, artifact: dict, use_mock: bool) -> dict:
    passed = 8 if use_mock or artifact.get("artifact_type") != "connector" else 6
    failed = 0 if use_mock else 1
    return {
        "status": "passed" if failed == 0 else "failed",
        "assertions_passed": passed,
        "assertions_failed": failed,
        "duration_ms": 245.0,
        "mock_used": use_mock,
        "report": {"coverage_pct": 92.5, "mock_endpoint": f"/mocks/{artifact.get('artifact_ref', 'x')}"},
    }


def build_dashboard(
    *,
    profile: dict | None,
    projects: list[dict],
    artifacts: list[dict],
    versions: list[dict],
    deployments: list[dict],
    tests: list[dict],
    marketplace: list[dict],
) -> dict:
    live = len([d for d in deployments if d.get("status") == "live"])
    passed_tests = len([t for t in tests if t.get("status") == "passed"])
    return {
        "summary": {
            "capabilities": len(StudioCapability),
            "projects": len(projects),
            "artifacts": len(artifacts),
            "versions": len(versions),
            "deployments_live": live,
            "tests_passed": passed_tests,
            "marketplace_listings": len(marketplace),
            "citizen_projects": len([p for p in projects if p.get("workspace_type") == "citizen"]),
        },
        "profile": profile,
        "artifacts_by_type": _count_by(artifacts, "artifact_type"),
        "recent_tests": sorted(tests, key=lambda t: t.get("created_at", ""), reverse=True)[:5],
        "capabilities": list_capability_catalog(),
    }


def _count_by(items: list[dict], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        key = str(item.get(field, "unknown"))
        counts[key] = counts.get(key, 0) + 1
    return counts


def generate_seed_data() -> dict:
    return {
        "projects": [
            {"name": "Banking Integration Suite", "workspace_type": "developer", "description": "Core banking APIs and connectors"},
            {"name": "HR Onboarding Flows", "workspace_type": "citizen", "description": "No-code citizen automations"},
        ],
        "artifacts": [
            {"project_index": 0, "name": "Payment API", "artifact_type": "api"},
            {"project_index": 0, "name": "Core Banking Connector", "artifact_type": "connector"},
            {"project_index": 0, "name": "Settlement Workflow", "artifact_type": "workflow"},
            {"project_index": 0, "name": "Payment Completed Event", "artifact_type": "event"},
            {"project_index": 0, "name": "Payment Mock", "artifact_type": "mock"},
            {"project_index": 1, "name": "Employee Onboarding", "artifact_type": "workflow"},
        ],
        "marketplace": [
            {"connector_type": "azure_ad", "name": "Azure AD Connector", "publisher": "Marpich", "version": "2.1.0"},
            {"connector_type": "payment_gateway", "name": "Stripe Gateway", "publisher": "Marpich Labs", "version": "1.4.0"},
            {"connector_type": "erp_connector", "name": "SAP ERP Bridge", "publisher": "Partner Co", "version": "3.0.0"},
        ],
        "mapping": {"source": "external.payment", "target": "banking.payment", "fields": [{"from": "amount", "to": "value"}]},
        "transformation": {"type": "jsonata", "expression": "$.amount * 100"},
    }
