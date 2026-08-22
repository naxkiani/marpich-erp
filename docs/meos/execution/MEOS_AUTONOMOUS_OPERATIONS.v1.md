# MEOS Autonomous Platform Operations (P400)

Policy-governed autonomy above the P399 Control Plane. Not a second infrastructure, observability, rollback, or AI cloud-access platform. Not GO-LIVE.

- CLI: `python3 scripts/meos-autonomous-operations.py status`
- Execution path: Launch Center → Autonomous Ops → Policy + Risk → Control Plane → P396/P397/P398
- AI path: AI → Control Plane → Policy → Risk → Approval → Execution. Never AI → direct cloud.

## Loop

OBSERVE → NORMALIZE → DETECT → CORRELATE → ANALYZE → PLAN → POLICY → APPROVAL → EXECUTE → VERIFY → ROLLBACK → AUDIT → LEARN

Production mutations never skip policy, risk, or verification.

## Automation levels

| Environment | Default level |
|---|---|
| LOCAL | LEVEL_2 observe + local simulation |
| DEMO | LEVEL_1 recommend only |
| TEST | LEVEL_2 controlled |
| STAGING | LEVEL_4 approval required |
| PRODUCTION | LEVEL_5 PRODUCTION_LOCKED |
| DISASTER_RECOVERY | LEVEL_4 explicit failover governance |

## Safety

- Kill switch: `AUTONOMOUS_OPERATIONS_KILL_SWITCH` → `NO_AUTOMATED_MUTATIONS`
- Pause: observe/detect/analyze continue; mutations stop
- Action tokens expire
- Stale plans return `PLAN_STALE`
- Simulation fixtures are labeled `SIMULATION` and are not production evidence

## Status

`P400_STATUS=AUTONOMOUS_PLATFORM_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED`
