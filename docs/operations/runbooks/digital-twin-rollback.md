# Twin deployment rollback runbook

```bash
helm rollback marpich-iam 0 --namespace marpich
```

Or ArgoCD: History → Rollback previous Sync.  

Disable `twinIntelligenceEnabled` / `twinSyncEnabled` via Feature Flags if behavioral rollback without redeploy is required.  

Verify: pods Ready · smoke `/api/v1/health` · sync lag recovering.
