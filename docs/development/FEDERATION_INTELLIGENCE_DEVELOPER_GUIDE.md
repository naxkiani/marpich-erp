# Federation Intelligence Developer Guide (P198-C2)

## Module
`backend/contexts/identity_federation/`

## Key services
- `FabricIntelligenceApplicationService` — predict, analytics, copilot
- `IdentityFederationAIService` — AI Platform ACL (14 surfaces)
- Engines: `ai_identity_intelligence_engine`, `identity_analytics_engine`, `ai_identity_copilot`, `federation_privacy_engine`

## Never
- Hardcode AI thresholds — use `federation.ai.*` policies
- Call OpenAI/Anthropic SDKs from this module — use Core AI Platform
- Import peer domain packages — use ACL adapters

## Tests
```bash
cd backend && .venv/bin/python -m pytest contexts/identity_federation/tests/ -q
```

## Frontend
- Admin: `frontend/apps/admin_portal/src/app/enterprise/federation/`
- End user: `frontend/apps/admin_portal/src/app/account/security/`
