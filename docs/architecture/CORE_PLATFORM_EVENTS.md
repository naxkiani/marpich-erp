# Core Platform — Integration Events

Complete event catalog for platform services. All events use envelope v1 (see [CORE_PLATFORM.md](./CORE_PLATFORM.md)).

## Identity & Access Plane

| Event | Publisher | Key subscribers |
|-------|-----------|-----------------|
| `identity.user.created` | Identity | hr, crm, audit, search, notifications |
| `identity.user.updated` | Identity | search, authorization |
| `identity.user.deactivated` | Identity | authentication, audit |
| `identity.mfa.enabled` | Identity | audit, notifications |
| `authentication.login.succeeded` | Authentication | audit, analytics |
| `authentication.login.failed` | Authentication | audit, ai |
| `authentication.session.revoked` | Authentication | audit |
| `authentication.api_key.created` | Authentication | audit, integration |
| `permission.catalog.registered` | Permission | authorization |
| `permission.role.created` | Permission | audit |
| `permission.role.assigned` | Permission | authorization, identity, audit |
| `permission.role.revoked` | Permission | authorization, audit |
| `authorization.policy.created` | Authorization | audit |
| `authorization.access.denied` | Authorization | audit, analytics |

## Control Plane

| Event | Publisher | Key subscribers |
|-------|-----------|-----------------|
| `platform.tenant.provisioned` | Tenant | identity, settings, documents, localization, audit, file_storage |
| `platform.module.activated` | Tenant | permission, settings, workflow, search |
| `platform.tenant.suspended` | Tenant | authentication, integration |
| `organization.org.created` | Organization | settings, audit |
| `organization.unit.created` | Organization | hr, finance, hospital |
| `organization.member.added` | Organization | identity, authorization, notifications |
| `organization.member.removed` | Organization | authorization, audit |
| `settings.config.updated` | Settings | all modules (cache bust) |
| `settings.feature.toggled` | Settings | analytics, audit |
| `localization.bundle.updated` | Localization | settings |

## Data & Content Plane

| Event | Publisher | Key subscribers |
|-------|-----------|-----------------|
| `file_storage.object.committed` | File Storage | documents, media, ai |
| `file_storage.object.deleted` | File Storage | audit, search |
| `documents.document.uploaded` | Document | search, ai, media, audit |
| `documents.document.signed` | Document | workflow, audit, notifications |
| `documents.document.archived` | Document | search, audit |
| `documents.version.created` | Document | audit, file_storage |
| `media.asset.uploaded` | Media | search, documents |
| `media.transcode.completed` | Media | notifications, documents |
| `media.asset.deleted` | Media | file_storage, search |
| `search.index.updated` | Search | analytics |
| `search.reindex.completed` | Search | notifications |

## Operations Plane

| Event | Publisher | Key subscribers |
|-------|-----------|-----------------|
| `notifications.message.sent` | Notification | analytics, audit |
| `notifications.message.failed` | Notification | integration, audit |
| `notifications.inbox.created` | Notification | search |
| `audit.export.completed` | Audit | notifications |
| `workflow.process.started` | Workflow | audit, analytics |
| `workflow.task.assigned` | Workflow | notifications, search |
| `workflow.task.completed` | Workflow | module handlers |
| `workflow.process.completed` | Workflow | audit, integration |
| `workflow.sla.breached` | Workflow | notifications, analytics |
| `integration.webhook.delivered` | Integration | audit, analytics |
| `integration.webhook.failed` | Integration | notifications, audit |
| `integration.sync.completed` | Integration | audit |
| `analytics.alert.triggered` | Analytics | notifications |
| `analytics.report.generated` | Analytics | notifications, documents |
| `ai.insight.generated` | AI | notifications, analytics |
| `ai.fraud.detected` | AI | notifications, audit, workflow |
| `ai.prediction.completed` | AI | module handlers |
| `reporting.run.completed` | Report Engine | notifications, documents, audit |
| `reporting.run.failed` | Report Engine | notifications, audit |

## Event Fan-Out (platform consumers)

These services subscribe to **many** events:

```
Audit Service      ← all events (compliance trail)
Search Service     ← entity CRUD events (index)
Analytics Service  ← business events (metrics)
Integration Service← per webhook subscription
Notification Service← configurable routing rules
```

## Topic & Consumer Group Naming

```
Topic:     marpich.{event_name}.v{version}
Consumer:  marpich.{subscriber_context}.{event_name}
Group ID:  {tenant_id}.{subscriber_context}  (optional isolation)
```

## Idempotency Key

Consumers MUST store processed `(tenant_id, event_id)` in a local `inbox_processed` table before side effects.
