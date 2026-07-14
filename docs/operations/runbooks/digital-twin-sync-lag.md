# Twin sync lag runbook

1. Confirm `twin_sync_lag_seconds` p95 and consumer group lag.  
2. Scale `twin-sync-workers` (HPA max / temporary replica bump).  
3. Check conflict rate — escalate manual_resolve if Policy stuck.  
4. Verify Integration connector health for external SoR.  
5. If Poison messages: move to DLQ runbook.
