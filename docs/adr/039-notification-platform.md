# ADR-039: Enterprise Notification Platform — Omnichannel Queue

## Status

Accepted

## Context

Marpich modules must not embed SMTP, SMS, push, or chat SDKs. The existing `notifications` context delivers in-app inbox and console email with event ACL routing — but lacks canonical design for nine channel types, priority queue, scheduling, localization, retry/DLQ, delivery vs read tracking, AI/system alerts, and Integration Platform provider adapters.

Platform Charter requires routing all notifications through Notification Service.

## Decision

Adopt **`docs/architecture/ENTERPRISE_NOTIFICATION_PLATFORM.md`** as canonical notification law.

### Channels

In-App, Email, SMS, WhatsApp, Telegram, Push, Voice, System Alerts, AI Alerts.

External channels use **Integration Platform** connectors — Notification owns orchestration, not raw API keys.

### Cross-cutting

Templates, localization, variables, scheduling, priority, retry, tracking, read status (in-app), delivery status, failure recovery.

### Notification queue

Priority async queue — all sends enqueue before dispatch. Worker renders templates, routes to channel adapters, retries with backoff, DLQ on exhaustion.

### Module rule

Events or `POST /notifications/send` only — no direct provider calls in business modules.

## Consequences

- `NotificationQueue` aggregate implemented beyond context.yaml reference
- New Integration connector types: whatsapp, telegram, push, voice
- Queue worker registers with Core Worker Runtime
- Extended events: `notifications.message.delivered`, `notifications.dlq.enqueued`

## Alternatives considered

- Per-module notification — rejected (Platform Charter)
- Direct SendGrid in Notification without Integration — rejected (secret management, provider swap)
- Synchronous send only — rejected (retry, scheduling, SLA)
