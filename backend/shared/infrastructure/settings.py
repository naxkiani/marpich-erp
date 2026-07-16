"""Application settings."""
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)

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
    kafka_bootstrap_servers: str = Field(
        default="",
        validation_alias=AliasChoices(
            "kafka_bootstrap_servers",
            "KAFKA_BOOTSTRAP_SERVERS",
            "KAFKA_BROKERS",
        ),
    )
    kafka_topic_prefix: str = "marpich"

    # RabbitMQ fan-out (optional — queue-oriented delivery)
    rabbitmq_enabled: bool = False
    rabbitmq_url: str = ""
    rabbitmq_exchange: str = "marpich"

    # orchestration broker defaults: kafka | rabbitmq | auto
    marpich_orchestration_broker_mode: str = "auto"

    # OpenTelemetry (optional — production observability)
    otel_enabled: bool = False
    otel_service_name: str = "marpich-backend"
    otel_service_version: str = "0.1.0"
    otel_environment: str = "development"
    otel_exporter_otlp_endpoint: str = ""
    otel_console_export: bool = False
    otel_excluded_urls: str = "/api/v1/health,/api/docs,/api/redoc,/api/openapi.json"

    # startup: lazy (dev/tests) loads identity+policy+platform only; eager loads all services
    marpich_startup_mode: str = "lazy"
    # WebAuthn / passkeys (Phase P4)
    webauthn_rp_id: str = "localhost"
    webauthn_rp_name: str = "Marpich ERP"
    webauthn_origin: str = "http://localhost:3001"
    webauthn_challenge_ttl_seconds: int = 120
    # OIDC federation defaults
    oidc_default_scopes: str = "openid profile email"
    # SAML federation (Phase P6)
    saml_sp_entity_id: str = "urn:marpich:sp"
    saml_acs_url: str = "http://localhost:3001/login/saml/acs"
    saml_relay_state_ttl_seconds: int = 300
    # Multi-region identity resilience (Phase P8)
    marpich_region_id: str = "eu-west-1"
    # app profile: core | enterprise | financial | banking | industry | test | full
    marpich_app_profile: str = "full"
    # event discovery: cached (manifest) | scan (filesystem import on demand)
    marpich_event_discovery_mode: str = "cached"
    # PostgreSQL RLS (Phase P5) — defense-in-depth tenant isolation
    marpich_rls_enabled: bool = False
    marpich_principal_partition_modulus: int = 8
    # Redis (shared platform cache — AuthZ decision cache, rate limits, etc.)
    redis_url: str = ""
    authz_decision_cache_backend: str = "memory"  # memory | redis
    # orchestration worker: polls retry/delayed/scheduled queues
    marpich_orchestration_worker_enabled: bool = True
    marpich_orchestration_worker_poll_interval_ms: int = 1000
    marpich_orchestration_worker_batch_size: int = 50
    # Document Exchange — QR token MAC (HMAC) + content RSA-PSS (PEMs; HSM via Secrets later)
    document_signing_secret: str = Field(
        default="",
        validation_alias=AliasChoices(
            "document_signing_secret",
            "DOCUMENT_SIGNING_SECRET",
        ),
    )
    document_signing_private_key_pem: str = Field(
        default="",
        validation_alias=AliasChoices(
            "document_signing_private_key_pem",
            "DOCUMENT_SIGNING_PRIVATE_KEY_PEM",
        ),
    )
    document_signing_public_key_pem: str = Field(
        default="",
        validation_alias=AliasChoices(
            "document_signing_public_key_pem",
            "DOCUMENT_SIGNING_PUBLIC_KEY_PEM",
        ),
    )
    document_signing_key_id: str = Field(
        default="documents-signing-v1",
        validation_alias=AliasChoices(
            "document_signing_key_id",
            "DOCUMENT_SIGNING_KEY_ID",
        ),
    )
    # LiveKit realtime (Integration connector — never call from business modules)
    livekit_url: str = Field(
        default="",
        validation_alias=AliasChoices("livekit_url", "LIVEKIT_URL"),
    )
    livekit_api_key: str = Field(
        default="",
        validation_alias=AliasChoices("livekit_api_key", "LIVEKIT_API_KEY"),
    )
    livekit_api_secret: str = Field(
        default="",
        validation_alias=AliasChoices("livekit_api_secret", "LIVEKIT_API_SECRET"),
    )
    livekit_token_ttl_seconds: int = Field(
        default=3600,
        validation_alias=AliasChoices(
            "livekit_token_ttl_seconds",
            "LIVEKIT_TOKEN_TTL_SECONDS",
        ),
    )


settings = Settings()


def use_postgres() -> bool:
    return settings.persistence_backend.lower() == "postgres"


def use_rls() -> bool:
    return use_postgres() and settings.marpich_rls_enabled
