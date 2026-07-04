"""Application settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    jwt_secret: str = "change-me-in-production-use-256-bit-key"
    jwt_access_ttl: int = 900
    jwt_refresh_ttl: int = 604800
    jwt_issuer: str = "marpich-identity"

    # persistence: memory (default/tests) | postgres (production)
    persistence_backend: str = "memory"
    database_url: str = "postgresql+asyncpg://marpich:marpich@127.0.0.1:5432/marpich_platform"

    # event fabric: direct (dev/tests) | outbox (production durable publish)
    event_bus_mode: str = "direct"
    outbox_poll_interval_ms: int = 500
    outbox_batch_size: int = 100
    outbox_dispatch_immediate: bool = True

    # Kafka fan-out (optional — external consumers)
    kafka_enabled: bool = False
    kafka_bootstrap_servers: str = ""

    # OpenTelemetry (optional — production observability)
    otel_enabled: bool = False
    otel_service_name: str = "marpich-backend"
    otel_service_version: str = "0.1.0"
    otel_environment: str = "development"
    otel_exporter_otlp_endpoint: str = ""
    otel_console_export: bool = False
    otel_excluded_urls: str = "/api/v1/health,/api/docs,/api/redoc,/api/openapi.json"


settings = Settings()


def use_postgres() -> bool:
    return settings.persistence_backend.lower() == "postgres"
