# ADR-181: Enterprise Integration Studio Platform

## Status

Accepted

## Context

Marpich ERP has integration primitives across `enterprise_api_gateway`, `enterprise_connector_framework`, `workflow`, and `enterprise_event_bus`, but lacks a unified low-code studio for designing APIs, connectors, workflows, and events with data mapping, transformation, testing, mock services, documentation, marketplace, versioning, deployment, a developer portal, and a citizen developer workspace.

## Decision

Implement **Enterprise Integration Studio** at `/api/v1/enterprise-integration-studio`.

### 14 Platform Capabilities

1. Visual API Builder
2. Visual Connector Builder
3. Visual Workflow Builder
4. Visual Event Designer
5. Data Mapping
6. Transformation
7. Testing
8. Mock Services
9. API Documentation
10. Connector Marketplace
11. Versioning
12. Deployment
13. Developer Portal
14. Citizen Developer Workspace

### Aggregates

- `StudioProfile`
- `StudioProject`
- `StudioArtifact`
- `StudioVersion`
- `StudioDeployment`
- `StudioTestRun`
- `MarketplaceListing`

### Policy Keys

- `enterprise_integration_studio.api_builder.enabled`
- `enterprise_integration_studio.connector_builder.enabled`
- `enterprise_integration_studio.workflow_builder.enabled`
- `enterprise_integration_studio.event_designer.enabled`
- `enterprise_integration_studio.testing.enabled`
- `enterprise_integration_studio.mock_services.enabled`
- `enterprise_integration_studio.marketplace.enabled`
- `enterprise_integration_studio.citizen_workspace.enabled`

### Events

- `enterprise_integration_studio.artifact.created`
- `enterprise_integration_studio.test.completed`
- `enterprise_integration_studio.version.published`
- `enterprise_integration_studio.deployment.completed`
- `enterprise_integration_studio.dashboard.generated`

### Delegates

- API runtime → `enterprise_api_gateway`
- Connectors → `enterprise_connector_framework`
- Workflows → `workflow`
- Events → `enterprise_event_bus`

### Admin portal dashboard

- Route: `/enterprise/integration-studio`
- Client: `enterpriseIntegrationStudioClient.ts`
- Component: `EnterpriseIntegrationStudioDashboardPage.tsx`

## Consequences

- Single low-code surface for integration design, test, version, and deploy
- Developer portal and citizen workspace without duplicating runtime engines
- Visual designer graphs for API, connector, workflow, and event artifacts
