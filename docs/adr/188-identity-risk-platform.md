# ADR-188: Identity Risk Platform (Phase P7)

## Status

Accepted

## Context

Phases P1–P6 delivered Authorization PDP, Permission Registry, centralized auth provider, WebAuthn/OIDC authentication, PostgreSQL RLS, and SAML/LDAP/SCIM directory sync. ADR-187 follow-up requires **AI-assisted identity risk scoring** on authentication and directory events — explainable scores that can trigger step-up authentication recommendations without autonomous enforcement.

## Decision

Implement **Identity Risk Platform** at `/api/v1/identity-risk` as bounded context `identity_risk`.

### 10 Platform Capabilities

1. Risk Signal Catalog
2. Authentication Risk Scoring
3. Directory Sync Risk Scoring
4. Federation Risk Scoring
5. Anomaly Detection
6. Risk Score Registry
7. Step-Up Recommendation
8. Policy-Driven Risk
9. Identity Risk Dashboard
10. Identity Risk API

### Aggregates

- `RiskProfile`
- `RiskSignal`
- `RiskScore`
- `AnomalyAlert`

### Policy Keys

- `identity_risk.scoring.enabled`
- `identity_risk.score.threshold`
- `identity_risk.step_up.threshold`
- `identity_risk.directory.bulk_create_threshold`

### Events Published

- `identity_risk.score.computed`
- `identity_risk.anomaly.detected`
- `identity_risk.step_up.recommended`

### Events Subscribed

- `authentication.login.success`
- `directory.sync.completed`
- `integration.directory.synced`
- `directory.scim.user.provisioned`

### API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/identity-risk/catalog` | Capability catalog |
| POST | `/identity-risk/seed` | Bootstrap tenant profile |
| GET | `/identity-risk/dashboard` | Risk dashboard |
| GET | `/identity-risk/scores` | List computed scores |
| GET | `/identity-risk/alerts` | List anomaly alerts |
| POST | `/identity-risk/evaluate` | Manual/on-demand risk evaluation |

### Scoring Model

Rule-based, explainable scoring (no opaque ML in P7):

- **Authentication:** auth method weight (SAML > OIDC > password > WebAuthn), new-user bonus, failed-login velocity
- **Directory sync:** users created volume, bulk-create anomaly when above policy threshold
- **SCIM:** provision event weight

Scores above threshold generate `AnomalyAlert`; scores above step-up threshold emit `identity_risk.step_up.recommended` for Authorization PDP integration.

## Consequences

- **Positive:** Real-time risk signals from MEIAAP auth/directory flows; explainable factor breakdown per score.
- **Positive:** Event-driven architecture — no polling; subscribes to integration events.
- **Neutral:** Rule-based engine in P7; ML model integration deferred to `ai_security` delegation path.
- **Follow-up (P8+):** Multi-region HA for risk scoring workers; gateway enforcement of step-up recommendations.

## References

- ADR-162 Enterprise AI Security Assistant
- ADR-187 Enterprise Directory Platform
- MEIAAP Architecture Blueprint
