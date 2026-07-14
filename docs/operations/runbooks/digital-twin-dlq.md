# Twin DLQ runbook

1. Inspect `marpich.twin.dlq.v1` depth and sample payloads (no PII in tickets).  
2. Classify: schema mismatch · auth · idempotent replay safe.  
3. Fix consumer / ACL · redeploy via GitOps.  
4. Replay via Message Orchestration tooling (tenant-scoped).  
5. Confirm SyncRun success and lag recovery.
