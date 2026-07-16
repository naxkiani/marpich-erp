# Federation Intelligence Operator Guide (P198-C2)

## Dashboards
- Admin UI: `/enterprise/federation`
- APIs: `/api/v1/federation/intelligence/dashboard`, `/fabric/security/dashboard`

## Alerts
- High AI risk: `marpich_ai_high_risk_total`
- Zero Trust denies: fabric trust metrics
- Failed federations: audit decision=deny

## Common actions
1. Seed tenant: `POST /federation/seed`
2. Run prediction: `POST /federation/intelligence/predict`
3. Ask copilot: `POST /federation/intelligence/copilot`
4. Export audit: `/federation/intelligence/compliance/export-manifest`

## Performance targets
Auth decision <150ms · Routing <120ms · Token exchange <100ms · Availability 99.99%

## Incident response
1. Disable federation AI via policy `federation.ai.enabled=false` if model misfires
2. Preserve audit trail
3. Recalculate trust / revoke sessions via fabric APIs
4. Follow adaptive-auth incident runbook for coordinated response
