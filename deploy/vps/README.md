# Generic Linux VPS (provider-neutral)

**Not Kubernetes.** Reuses Compose + Caddy + existing backup scripts.

- INSTALL / STATUS: `../../scripts/meos-vps-bootstrap.sh`
- UPGRADE / ROLLBACK: `MEOS_IMAGE` / `MEOS_PREVIOUS_IMAGE` (digest, not `:latest`)
- BACKUP / RESTORE: `scripts/meos-postgres-backup.sh` · `scripts/meos-postgres-restore-drill.sh`
- TLS: `infrastructure/docker/compose/Caddyfile.vps.example`
- Secrets: copy `infrastructure/launch/env.production.example` (gitignored values)

Ubuntu + Docker Engine + Compose v2. Do not publish PostgreSQL publicly. Status: **READY_FOR_CREDENTIALS** until SSH/host exists.
