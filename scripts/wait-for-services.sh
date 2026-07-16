#!/usr/bin/env bash
# Wait for local Marpich platform dependencies (Postgres, Redis, Kafka).
set -euo pipefail

PGHOST="${PGHOST:-127.0.0.1}"
PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-marpich}"
PGDATABASE="${PGDATABASE:-marpich_platform}"
REDIS_URL="${REDIS_URL:-redis://127.0.0.1:6379}"
KAFKA_BOOTSTRAP_SERVERS="${KAFKA_BOOTSTRAP_SERVERS:-${KAFKA_BROKERS:-127.0.0.1:9092}}"

wait_postgres() {
  echo "Waiting for Postgres at ${PGHOST}:${PGPORT}..."
  for _ in $(seq 1 60); do
    if pg_isready -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" >/dev/null 2>&1; then
      echo "Postgres is ready."
      return 0
    fi
    sleep 2
  done
  echo "Postgres did not become ready in time." >&2
  return 1
}

wait_redis() {
  local host port
  host="$(echo "$REDIS_URL" | sed -E 's#redis://([^:/]+).*#\1#')"
  port="$(echo "$REDIS_URL" | sed -E 's#redis://[^:]+:([0-9]+).*#\1#')"
  port="${port:-6379}"
  echo "Waiting for Redis at ${host}:${port}..."
  for _ in $(seq 1 30); do
    if redis-cli -h "$host" -p "$port" ping 2>/dev/null | grep -q PONG; then
      echo "Redis is ready."
      return 0
    fi
    sleep 2
  done
  echo "Redis did not become ready in time." >&2
  return 1
}

wait_kafka() {
  local host port
  host="${KAFKA_BOOTSTRAP_SERVERS%:*}"
  port="${KAFKA_BOOTSTRAP_SERVERS##*:}"
  echo "Waiting for Kafka at ${host}:${port}..."
  for _ in $(seq 1 30); do
    if command -v kafka-topics.sh >/dev/null 2>&1; then
      if kafka-topics.sh --bootstrap-server "${host}:${port}" --list >/dev/null 2>&1; then
        echo "Kafka is ready."
        return 0
      fi
    elif nc -z "$host" "$port" 2>/dev/null; then
      echo "Kafka port is open (topic check skipped)."
      return 0
    fi
    sleep 2
  done
  echo "Kafka did not become ready in time." >&2
  return 1
}

wait_postgres
wait_redis
wait_kafka
