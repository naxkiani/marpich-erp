# Rollback (P354)

Configured, not production-tested. `ROLLBACK_STATUS = CONFIGURED`. Previous registry artifact: `NOT_AVAILABLE`.

Do not roll back production: there is no production cluster (G26 BLOCKED).

## Local / DEMO (NON_PRODUCTION)

```bash
MEOS_IMAGE=$MEOS_PREVIOUS_IMAGE docker compose -p meosprod \
  -f infrastructure/docker/compose/docker-compose.meos-prod.yml up -d
```

Workstation compose is **not** production. Ports `:5433` / `:5444` are NON_PRODUCTION.

## VPS / Hostinger VPS

```bash
MEOS_IMAGE=$MEOS_PREVIOUS_IMAGE docker compose -p meosprod up -d
```

Requires a previous `MEOS_IMAGE` with digest, not `:latest`.

## Kubernetes

```bash
helm rollback marpich-iam 0 --namespace marpich
```

Requires a prior Helm revision. `helm`/`kubectl` were not required to mint a local RC.

## Forbidden

- Inventing a previous digest
- Treating localhost restore as PRODUCTION_BACKUP
- Using `:latest` as rollback identity
