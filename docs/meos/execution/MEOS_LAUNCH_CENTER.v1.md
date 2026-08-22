# MEOS Universal Launch Center (P395)

Operational interface for the existing environment control plane. Not GO-LIVE.

- UI: `/enterprise/launch-center` in the existing admin portal
- API: `/api/v1/launch-center` on Core Platform presentation
- CLI: `python3 scripts/meos-environment-control.py`
- Snapshot: `python3 scripts/meos-launch-center.py`
- Orchestrator: `python3 scripts/meos-deployment-orchestrator.py`
- Release Factory: `python3 scripts/meos-release-factory.py`
- Control Plane: `python3 scripts/meos-control-plane.py status`
- Autonomous Ops: `python3 scripts/meos-autonomous-operations.py status`

## Centers

Dashboard · Environments · Providers · Releases · Deployments · Infrastructure · Databases · Secrets · DNS / TLS · Backups · Restore · Rollback · Observability · Drift · Security · Audit · Launch Plans · Jobs · Wizard

## Wizard

Provider → Region → Environment → Profile → Release → Resources → Database → Networking → Secrets → Cost → Security → Plan → Authorization → Provision → Deploy → Verify

No execution occurs before authorization. Production buttons stay disabled while governance locks are active.

## Honesty

- The UI cannot set `G26_READY`, cannot reset P0, and has no unconditional GO LIVE button.
- Production actions stay disabled while governance locks are active.
- Demo objects are labeled **SIMULATED**.
- Region discovery unavailable is shown as **REGION DISCOVERY UNAVAILABLE**.
- Unknown cost is **COST UNKNOWN**, never a fake zero.
- Secret values are never shown. No COPY SECRET. No PRINT SECRET.
- `latest` is not selectable unless an immutable digest is resolved.
- Observability reuses `/enterprise/observability`. This is not a second monitoring system.
- RBAC reuses Identity. Overlay roles: PLATFORM_VIEWER, PLATFORM_OPERATOR, RELEASE_MANAGER, INFRASTRUCTURE_OPERATOR, SECURITY_OPERATOR, DATABASE_OPERATOR, PLATFORM_ADMIN.

## Status

`P395_STATUS=LAUNCH_CENTER_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED`
