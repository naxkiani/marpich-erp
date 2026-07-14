# Federation Intelligence Incident Runbook

## Symptoms
- Spike in federation failures
- Unexpected AI deny / step-up rates
- Copilot returning empty explanations

## Triage
1. Check `/federation/intelligence/metrics` and `/federation/fabric/metrics`
2. Review `/federation/fabric/audit` and intelligence audit summaries
3. Verify policies: `federation.ai.enabled`, risk thresholds
4. Confirm Adaptive Auth and Identity Risk ACLs healthy

## Mitigations
- Set `federation.ai.enabled` false (policy) to fall back to non-AI paths
- Rotate certificates via fabric certificate APIs
- Force global logout for compromised identities
- Open security incident via Security Incident platform

## Post-incident
- Export audit package
- Submit AI feedback labels on false positives
- Update quality gate evidence in ADR notes
