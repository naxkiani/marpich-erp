# Twin prediction error-budget runbook

1. Confirm failure ratio and AI Platform dependency health.  
2. Circuit-break twin AI path: `twin.intelligence.enabled=false` (Feature Flags).  
3. Verify `model_approval_ref` still valid in AI Governance.  
4. Check inference latency SLO vs AI quota.  
5. Re-enable after burn cools; open Sev3 PIR if recurring.
