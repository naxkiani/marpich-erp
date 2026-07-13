# ADR-180: Enterprise Scheduler Platform

## Status

Accepted

## Context

Marpich ERP has scheduled automation in `enterprise_automation_platform` and delayed queues in `enterprise_message_orchestration`, but lacks a unified enterprise scheduler for cron, calendar, recurring, event-triggered, and workflow-triggered jobs with retry, priority, dependency chains, distributed worker shards, job history, and monitoring.

## Decision

Implement **Enterprise Scheduler Platform** at `/api/v1/enterprise-scheduler`.

### 12 Platform Capabilities

1. Cron Jobs
2. Calendar Jobs
3. Recurring Jobs
4. Event Triggered Jobs
5. Workflow Triggered Jobs
6. Retry
7. Priority
8. Dependency
9. Distributed Scheduling
10. Job History
11. Monitoring
12. Scheduler Dashboard

### Aggregates

- `SchedulerProfile`
- `ScheduledJob`
- `JobDependency`
- `JobExecution`

### Policy Keys

- `enterprise_scheduler.cron.enabled`
- `enterprise_scheduler.calendar.enabled`
- `enterprise_scheduler.recurring.enabled`
- `enterprise_scheduler.event_trigger.enabled`
- `enterprise_scheduler.workflow_trigger.enabled`
- `enterprise_scheduler.retry.enabled`
- `enterprise_scheduler.priority.enabled`
- `enterprise_scheduler.distributed.enabled`

### Events

- `enterprise_scheduler.job.scheduled`
- `enterprise_scheduler.job.started`
- `enterprise_scheduler.job.completed`
- `enterprise_scheduler.job.failed`
- `enterprise_scheduler.dashboard.generated`

### Delegates

- Workflow triggers → `workflow`
- Delayed dispatch → `enterprise_message_orchestration`
- Monitoring → `enterprise_observability`

### Admin portal dashboard

- Route: `/enterprise/scheduler`
- Client: `enterpriseSchedulerClient.ts`
- Component: `EnterpriseSchedulerDashboardPage.tsx`

## Consequences

- Unified job scheduling API — modules never implement local cron daemons
- Dependency-aware triggering with job history and distributed worker shards
- Scheduler dashboard with monitoring, history, pause/resume, and manual trigger
