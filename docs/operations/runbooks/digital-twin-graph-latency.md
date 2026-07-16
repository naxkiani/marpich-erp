# Twin graph latency runbook

1. Confirm `TwinGraphLatencyHigh` and p95 panel on intelligence dashboard.  
2. Check Policy `twin.graph.max_hops` and query fan-out.  
3. Verify Directory Graph hydrate latency (ADR-194).  
4. Scale API pods if CPU-bound; reduce hop budget temporarily via Feature Flag/Policy.  
5. If saturation on projected edges store: schedule graph rebuild off-peak.
