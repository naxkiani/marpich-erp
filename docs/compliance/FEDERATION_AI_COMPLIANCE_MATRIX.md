# Federation AI Identity Intelligence — Compliance Matrix (P198-C2)

| Framework | Control | Implementation |
|-----------|---------|----------------|
| ISO 27001 | Access control, audit | JWT + federation permissions + FederationAuditStore |
| ISO 27701 | Privacy info management | Privacy engine + retention policies + PIA |
| SOC 2 | Security monitoring | Intelligence metrics + trust/security dashboards |
| PCI DSS | Auth strength | Step-up / Zero Trust federation policies |
| GDPR | Lawful processing | Consent records, minimization, audit export |
| HIPAA | PHI access oversight | High-assurance trust contracts + audit |
| NIST CSF | Detect / Respond | AI anomaly + risk alerts + runbooks |
| OWASP ASVS | AuthN/AuthZ | Gateway + require_permissions defense-in-depth |
| OpenID Foundation | OIDC profiles | P198-B OIDC discovery/token/userinfo |

## Privacy Impact Assessment
Template: `federation_privacy_engine.privacy_impact_assessment()`

## Data Retention
See `federation_privacy_engine.retention_policies()` — audit 7y, sessions 90d, AI predictions 1y.
