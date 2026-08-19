#!/usr/bin/env bash
# Deterministic migration inventory check. Does NOT apply SQL. Does NOT touch production.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MIGRATIONS="$ROOT/infrastructure/docker/migrations"
RUNNER="$ROOT/scripts/run-migrations.sh"

echo "MEOS migration-check (NON_PRODUCTION; no apply)"
if [[ ! -d "$MIGRATIONS" ]]; then
  echo "FAIL: migrations directory missing"
  exit 1
fi
if [[ ! -f "$RUNNER" ]]; then
  echo "FAIL: run-migrations.sh missing"
  exit 1
fi

mapfile -t files < <(find "$MIGRATIONS" -maxdepth 1 -name '*.sql' -printf '%f\n' | sort)
if [[ ${#files[@]} -eq 0 ]]; then
  echo "FAIL: no SQL migrations"
  exit 1
fi

prev=""
for f in "${files[@]}"; do
  prefix="${f%%_*}"
  if [[ ! "$prefix" =~ ^[0-9]{3}$ ]]; then
    echo "FAIL: unexpected name $f"
    exit 1
  fi
  if [[ -n "$prev" && "$prefix" < "$prev" ]]; then
    echo "FAIL: ordering $prev then $prefix"
    exit 1
  fi
  prev="$prefix"
  if ! grep -Fq "$f" "$RUNNER"; then
    # 000 is applied explicitly; 001 may be init-only
    if [[ "$f" != "000_schema_migrations.sql" ]]; then
      echo "WARN: $f not referenced in run-migrations.sh"
    fi
  fi
done

echo "COUNT=${#files[@]}"
echo "ORDER=sorted-numeric-prefix"
echo "APPLY=NOT_EXECUTED"
echo "DESTRUCTIVE_SCAN=NOT_RUN_AGAINST_PRODUCTION"
echo "STATUS=PASS"
