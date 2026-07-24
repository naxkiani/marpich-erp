# Audit — architecture notes

**Owning platform:** Audit (`audit`) — Enterprise Audit Platform  
**Law:** immutable append-only ledger; modules never keep local audit tables.

## Admin UI depth (P36)

`AuditDeskPage` → `/enterprise/audit`

| Surface | API |
|---------|-----|
| Query | `GET /api/v1/audit/entries` |
| Detail | `GET /api/v1/audit/entries/{id}` |
| Record (sync) | `POST /api/v1/audit/entries` |
| Stats | `GET /api/v1/audit/stats` |
| Export | `POST /api/v1/audit/exports` · `GET /api/v1/audit/exports/{id}` |

Draft: `marpich.audit.desk.draft` (filters + record form — never password)  
Workflow: Connect → Query → Inspect → Export (`StepProgress`)  
i18n: `audit.*` (en / fa / ar)

## Permissions

- `audit.entries.read` · `audit.entries.write`
- `audit.exports.write` · `audit.exports.read`

## Ingestion

Primary: integration event fan-out → ACL mapper → append.  
Secondary: direct `POST /entries` for sensitive sync paths only.
