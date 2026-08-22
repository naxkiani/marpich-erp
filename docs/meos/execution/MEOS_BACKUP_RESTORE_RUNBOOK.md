# MEOS Backup / Restore Runbook (product-side, P351)

Does **not** replace [MEOS_WAVE04_DR_RUNBOOK.md](./MEOS_WAVE04_DR_RUNBOOK.md).  
Workstation MinIO evidence is **not** G26 production backup.

## Backup

```bash
export PGHOST=127.0.0.1 PGPORT=5433   # LOCAL / DEMO only
# Production: set PGHOST to managed PostgreSQL (not :5433/:5444)
./scripts/meos-postgres-backup.sh
```

Produces gzip dump + manifest under `.meos-backups/` (gitignored) or `MEOS_BACKUP_DIR` / `MEOS_BACKUP_S3_URI`.

| Field | Product | Production (G26) |
|-------|---------|------------------|
| Backup ID | filename stamp in manifest | managed snapshot ID |
| Encryption | optional object-store SSE | required; NOT_VERIFIED here |
| Retention | `MEOS_BACKUP_KEEP` | provider policy; NOT_VERIFIED |
| Class | CONFIGURED / locally testable | PRODUCTION_VERIFIED only with real prod DB |

## Restore (local testable)

```bash
./scripts/meos-postgres-restore-drill.sh
```

Default restore target is a **separate** database (see Wave 04). Do not restore over production without authorization.

## Application config

Env files are gitignored. Restore secrets from the secret manager, never from git.

## Rollback vs restore

- App rollback: Helm `helm rollback marpich-iam 0 -n marpich` or Compose previous digest.  
- Data restore: this runbook. They are not the same.
