# Twin recover / self-heal runbook

1. Detect corrupt projection (drift, checksum, failed SyncRun).  
2. Emit/observe `identity_twin.recovery.started`.  
3. Call twin recover API → snapshot baseline → full SoR sync mode.  
4. Policy self-heal may auto-scale workers / pause consumers — verify `identity_twin.self_heal.executed`.  
5. Confirm `identity_twin.recovery.completed` and lag SLO restored.  
6. If AuthZ facets impacted: escalate Sev1 + BC plan.
