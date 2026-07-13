# EIF Acceptance Criteria — Measurable Implementation Checklist

**Fabric:** Enterprise Digital Identity Fabric (EIF)  
**Baseline:** MEIAAP P1–P8 (ADR-182–189)  
**Target:** EIF P9–P16  

---

## 1. Foundation (MEIAAP P1–P8) — ✅ Implemented

| ID | Criterion | Metric | Status |
|----|-----------|--------|--------|
| F-01 | Authorization PDP responds | `POST /authorization/check` p99 < 50ms | ✅ |
| F-02 | Permission registry resolves principals | `GET /permissions/principals/{id}` | ✅ |
| F-03 | Centralized auth provider typechecks | `@marpich/auth-provider` tsc clean | ✅ |
| F-04 | WebAuthn login issues tokens | `POST /authentication/webauthn/login/verify` | ✅ |
| F-05 | OIDC federation authorize URL | `POST /authentication/federation/oidc/authorize` | ✅ |
| F-06 | PostgreSQL RLS on identity tables | Migration 016 applied | ✅ |
| F-07 | Principal sync from identity | `POST /data-isolation/principals/sync` | ✅ |
| F-08 | SAML/LDAP/SCIM directory | Directory API smoke tests pass | ✅ |
| F-09 | Risk scoring on auth/directory events | `identity_risk.score.computed` emitted | ✅ |
| F-10 | Multi-region worker failover | Manual failover API completes | ✅ |
| F-11 | IAM integration test suite | 47+ tests pass | ✅ |
| F-12 | Zero hardcoded authz in MEIAAP contexts | Grep: no inline permission checks in IAM routers | ✅ |

---

## 2. Policy-Driven Control Plane

| ID | Criterion | Metric | Target |
|----|-----------|--------|--------|
| P-01 | All EIF contexts expose policy keys | Each `context.yaml` lists policy_keys | 16/16 |
| P-02 | Default policies seeded per tenant | `policy.seed` on tenant provision | 100% tenants |
| P-03 | PDP evaluation order documented | deny → rbac → abac → pbac → default | Enforced |
| P-04 | No domain module calls identity DB directly | Architecture test / lint rule | 0 violations |
| P-05 | Industry packs override policy defaults | Banking pack changes MFA threshold | Config test |

---

## 3. Persistence & RLS

| ID | Criterion | Metric | Target |
|----|-----------|--------|--------|
| D-01 | All EIF contexts have Postgres repos | `use_postgres()` adapters | P9–P12 |
| D-02 | Migration 017 applied | `identity.organizations` exists | Staging+ |
| D-03 | RLS blocks cross-tenant reads | Integration test with wrong tenant | 403/empty |
| D-04 | Session table partitioned | Monthly partitions auto-created | P10 |
| D-05 | Audit log 7-year retention | Kafka + Postgres partition policy | P11 |

---

## 4. API Contracts

| ID | Criterion | Metric | Target |
|----|-----------|--------|--------|
| A-01 | OpenAPI 3.1 per EIF context | `/api/openapi.json` includes all prefixes | P9 |
| A-02 | SCIM 2.0 Users/Groups | RFC 7643 compliance test | P6 ✅ Users |
| A-03 | GraphQL federation gateway | Identity subgraph in gateway | P12 |
| A-04 | gRPC IdentityService | `CheckAccess`, `ResolvePrincipal` | P12 |
| A-05 | WebSocket session events | `/ws/v1/sessions` push on revoke | P10 |
| A-06 | Contract tests per event | JSON Schema in `docs/architecture/events/` | 50+ schemas |

---

## 5. Event Architecture

| ID | Criterion | Metric | Target |
|----|-----------|--------|--------|
| E-01 | Outbox pattern in production | `event_bus_mode=outbox` | Prod |
| E-02 | Kafka topics per EIF_EVENT_CATALOG | All topics created | P9 |
| E-03 | Idempotent consumers | Duplicate event_id ignored | All handlers |
| E-04 | DLQ for failed IAM events | `marpich.identity.dlq` monitored | P9 |
| E-05 | Saga: identity registration | End-to-end test | P9 |
| E-06 | Event versioning | Breaking change → new event name | Documented |

---

## 6. Identity Lifecycle Workflows

| ID | Criterion | Metric | Target |
|----|-----------|--------|--------|
| L-01 | Registration → verify → activate | Saga completes < 30s | P9 |
| L-02 | Directory provision → principal sync | Event chain verified | ✅ |
| L-03 | Suspension revokes all sessions | `session.revoked` count = active sessions | P10 |
| L-04 | Deprovisioning cascade | credential + directory + identity | P9 |
| L-05 | Recovery with MFA step-up | Risk score > threshold → MFA required | P7 partial |

---

## 7. Security Controls

| ID | Criterion | Metric | Target |
|----|-----------|--------|--------|
| S-01 | MFA enforced by policy | `authentication.passkeys.required` | Per tenant |
| S-02 | WebAuthn RP ID per environment | Env-specific `webauthn_rp_id` | Staging+ |
| S-03 | SAML signature validation | `python3-saml` ACS verify | P9 |
| S-04 | Device trust score in session | `device.trust.changed` → session risk | P11 |
| S-05 | Certificate auth mTLS | `certificate` context validates chain | P12 |
| S-06 | Zero Trust: continuous evaluation | Re-auth on risk spike | P11 |
| S-07 | Secrets not in repo | Gitleaks CI pass | Every PR |
| S-08 | OWASP ASVS L2 IAM controls | Security audit checklist | Annual |

---

## 8. AI Integration

| ID | Criterion | Metric | Target |
|----|-----------|--------|--------|
| AI-01 | Risk scores explainable | Every score has `factors[]` | ✅ |
| AI-02 | Step-up recommendation enforced | Gateway blocks if ignored | P11 |
| AI-03 | Access review assistant | `ai_identity` suggests certifications | P13 |
| AI-04 | AI agent principal type | `ai_identity.agents` table | Migration 017 |
| AI-05 | No autonomous IAM mutations | `autonomous_execution: false` | All AI outputs |

---

## 9. Frontend

| ID | Criterion | Metric | Target |
|----|-----------|--------|--------|
| FE-01 | All dashboards use `useAuth` | 0 direct token access in admin portal | P9 |
| FE-02 | RTL layout for fa-IR | `dir=rtl` admin shell | ✅ partial |
| FE-03 | WCAG 2.1 AA login flow | axe-core audit pass | P10 |
| FE-04 | Dark mode identity settings | Theme toggle persists | P10 |
| FE-05 | Passkey registration UX | Browser WebAuthn E2E | P4 ✅ |

---

## 10. Testing

| ID | Criterion | Metric | Target |
|----|-----------|--------|--------|
| T-01 | Unit coverage IAM contexts | > 80% domain services | CI gate |
| T-02 | Integration smoke per context | 1+ test per API prefix | ✅ |
| T-03 | Contract tests events | JSON Schema validation | P9 |
| T-04 | Load: PDP 1000 rps | p99 < 100ms @ 1k rps | P12 |
| T-05 | Security: OWASP ZAP IAM routes | 0 high findings | Pre-release |
| T-06 | Chaos: kill directory leader | Failover < 60s | P8 ✅ manual |

---

## 11. DevSecOps

| ID | Criterion | Metric | Target |
|----|-----------|--------|--------|
| O-01 | Docker image per IAM service | `marpich-identity-*` images | P12 |
| O-02 | Helm chart `marpich-iam` | K8s deploy staging | P12 |
| O-03 | Terraform: RDS + RLS | IaC for identity Postgres | P12 |
| O-04 | GitHub Actions IAM test job | Runs on every PR | ✅ |
| O-05 | OpenTelemetry traces IAM | Trace ID in access_decisions | P10 |
| O-06 | Vault/KMS for signing keys | JWT keys from HSM | Prod |

---

## 12. Performance & HA

| ID | Criterion | Metric | Target |
|----|-----------|--------|--------|
| H-01 | Horizontal PDP replicas | 3+ pods, no sticky sessions | P12 |
| H-02 | Redis session cache | Cache hit > 90% session lookups | P10 |
| H-03 | Connection pool sizing | PgBouncer max 100/tenant | Prod |
| H-04 | Multi-region active-passive | RPO < 60s, RTO < 5min | P8 foundation |
| H-05 | Identity graph query < 200ms | 3-hop traversal benchmark | P13 |

---

## 13. Localization & White Label

| ID | Criterion | Metric | Target |
|----|-----------|--------|--------|
| I-01 | Login page i18n | en-US, fa-IR, ar-SA | P10 |
| I-02 | Jalali calendar in audit UI | Date picker locale | P11 |
| I-03 | White-label IdP branding | Tenant logo on login | P12 |
| I-04 | Industry pack labels | Banking vs Hospital terminology | P9 |

---

## 14. Industry Vertical Readiness

| Vertical | Pack ID | Key EIF Policies | Status |
|----------|---------|------------------|--------|
| Banking | `banking` | MFA required, SoD, 90-day cert | Planned |
| Islamic Banking | `islamic_banking` | Sharia audit trail, dual control | Planned |
| Currency Exchange | `currency_exchange` | AML risk scoring, device trust | Partial P7 |
| Government | `government` | PIV/CAC cert auth, FedRAMP logging | Planned |
| University | `university` | SAML/Shibboleth, student lifecycle | Partial P6 |
| Hospital | `hospital` | HIPAA consent, break-glass | ADR-161 partial |
| Construction | `construction` | Contractor temp access | Planned |
| Manufacturing | `manufacturing` | OT device identity | Planned |
| Retail | `retail` | POS device trust, shift sessions | Planned |
| Insurance | `insurance` | Agent delegation graph | Planned |
| Real Estate | `real_estate` | Broker/client relationship graph | Planned |
| NGO | `ngo` | Volunteer lifecycle, minimal PII | Planned |

---

## 15. Sign-Off Gates

| Gate | Required Criteria | Owner |
|------|-------------------|-------|
| **G1 — MEIAAP Complete** | F-01 through F-12 | ✅ Done |
| **G2 — EIF Persistence** | D-01 through D-03 | Platform Eng |
| **G3 — Production Security** | S-01 through S-08 | Security |
| **G4 — Multi-Region Prod** | H-04, O-06 | SRE |
| **G5 — Industry GA** | 3+ vertical packs pass L-01–L-05 | Product |

---

*Last updated: 2026-07-13 | Chief Identity Architect*
