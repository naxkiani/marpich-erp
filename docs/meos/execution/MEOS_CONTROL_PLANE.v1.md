# MEOS Universal Control Plane (P399)

Operational layer above Launch Center, Deployment Orchestrator, Release Factory, and Environment Factory. Not a second deployment engine, Kubernetes architecture, CI/CD, secrets, or observability platform. Not GO-LIVE.

- CLI: `python3 scripts/meos-control-plane.py status`
- Operator CLI remains: `python3 scripts/meos-control.py status`
- Human UI: `/enterprise/launch-center` consumes Control Plane state
- API: `/api/v1/launch-center/control-plane` (not `/api/v1/platform`, which remains tenant/industry-pack SoR)

## Contract

COMMAND → POLICY → PLAN → APPROVAL → EXECUTION → VERIFICATION → AUDIT

Never COMMAND → BLIND EXECUTION. Dry-run shows planned actions without mutation.

## Commands

`status` · `inventory` · `inspect` · `validate` · `plan` · `execute` · `verify` · `drift` · `history` · `capacity` · `cost` · `security` · `health`

`--dry-run` never mutates. Production execute stays **LOCKED**. Destroy/decommission require a reviewed plan plus separate authorization.

## Status

`P399_STATUS=CONTROL_PLANE_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED`
