# Notifications — architecture notes

**Owning platform:** Notifications (`notifications`) — Core Notification Platform  
**Law:** modules never send email/SMS/push directly; all delivery goes through this context.

## Admin UI depth (P35)

`NotificationsDeskPage` → `/enterprise/notifications`

| Surface | API |
|---------|-----|
| Inbox | `GET /api/v1/notifications/inbox` |
| Mark read | `PATCH /api/v1/notifications/inbox/{id}/read` |
| Send | `POST /api/v1/notifications/send` |
| Templates | `GET /api/v1/notifications/templates` |
| Deliveries | `GET /api/v1/notifications/deliveries` |

Draft: `marpich.notifications.desk.draft` (compose + filters — never password)  
Workflow: Connect → Browse → Compose → Deliver (`StepProgress`)  
i18n: `notifications.*` (en / fa / ar)

## Permissions

- Inbox: authenticated user (own + tenant broadcast)
- `notifications.send`
- `notifications.templates.read`
- `notifications.deliveries.read`

## Events

`notifications.message.sent` · `notifications.inbox.created` · `notifications.message.failed` — consumed by Audit / Analytics ACLs.
