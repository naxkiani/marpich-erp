"""OpenTelemetry bootstrap — traces, metrics, FastAPI instrumentation."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from shared.infrastructure.settings import settings

if TYPE_CHECKING:
    from fastapi import FastAPI

logger = logging.getLogger(__name__)

_configured = False
_instrumented_app: FastAPI | None = None
_request_duration_histogram = None


def is_telemetry_enabled() -> bool:
    return settings.otel_enabled


def setup_observability(app: FastAPI) -> bool:
    """Configure OTel providers and instrument FastAPI. Returns True when active."""
    global _configured, _instrumented_app
    if _configured or not settings.otel_enabled:
        return False

    try:
        from opentelemetry import metrics, trace
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.sdk.metrics import MeterProvider
        from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    except ImportError:
        logger.warning(
            "OTEL_ENABLED=true but OpenTelemetry packages are missing. "
            "Install with: pip install marpich-backend[observability]"
        )
        return False

    resource = Resource.create(
        {
            "service.name": settings.otel_service_name,
            "service.version": settings.otel_service_version,
            "deployment.environment": settings.otel_environment,
        }
    )

    trace_provider = TracerProvider(resource=resource)
    if settings.otel_exporter_otlp_endpoint:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

        endpoint = _normalize_traces_endpoint(settings.otel_exporter_otlp_endpoint)
        trace_provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
        )
    elif settings.otel_console_export:
        trace_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(trace_provider)

    metric_readers = []
    if settings.otel_exporter_otlp_endpoint:
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

        endpoint = _normalize_metrics_endpoint(settings.otel_exporter_otlp_endpoint)
        metric_readers.append(
            PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=endpoint))
        )
    elif settings.otel_console_export:
        metric_readers.append(
            PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=60000)
        )

    if metric_readers:
        metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=metric_readers))

    FastAPIInstrumentor.instrument_app(
        app,
        tracer_provider=trace_provider,
        excluded_urls=settings.otel_excluded_urls,
    )
    _instrumented_app = app

    _init_gateway_metrics()
    _configured = True
    logger.info(
        "OpenTelemetry enabled for %s (otlp=%s, console=%s)",
        settings.otel_service_name,
        bool(settings.otel_exporter_otlp_endpoint),
        settings.otel_console_export,
    )
    return True


def shutdown_observability() -> None:
    """Flush and shutdown OTel providers."""
    global _configured, _instrumented_app, _request_duration_histogram
    if not _configured:
        return

    try:
        if _instrumented_app is not None:
            from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

            FastAPIInstrumentor.uninstrument_app(_instrumented_app)
            _instrumented_app = None

        from opentelemetry import metrics, trace

        trace_provider = trace.get_tracer_provider()
        shutdown_trace = getattr(trace_provider, "shutdown", None)
        if callable(shutdown_trace):
            shutdown_trace()

        meter_provider = metrics.get_meter_provider()
        shutdown_metrics = getattr(meter_provider, "shutdown", None)
        if callable(shutdown_metrics):
            shutdown_metrics()
    except Exception:  # noqa: BLE001 — shutdown boundary
        logger.exception("OpenTelemetry shutdown failed")
    finally:
        _configured = False
        _request_duration_histogram = None


def record_http_request(*, method: str, path: str, status: int, duration_ms: float) -> None:
    if _request_duration_histogram is None:
        return
    _request_duration_histogram.record(
        duration_ms,
        {
            "http.method": method,
            "http.route": path,
            "http.status_code": status,
        },
    )


def annotate_active_span(**attributes: str | int | float | bool) -> None:
    if not _configured:
        return
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span.is_recording():
            for key, value in attributes.items():
                span.set_attribute(key, value)
    except Exception:  # noqa: BLE001 — best-effort span attributes
        return


def _init_gateway_metrics() -> None:
    global _request_duration_histogram
    from opentelemetry import metrics

    meter = metrics.get_meter("marpich.gateway")
    _request_duration_histogram = meter.create_histogram(
        "http.server.duration",
        unit="ms",
        description="HTTP request duration recorded by platform gateway middleware",
    )


def _normalize_traces_endpoint(endpoint: str) -> str:
    base = endpoint.rstrip("/")
    if base.endswith("/v1/traces"):
        return base
    return f"{base}/v1/traces"


def _normalize_metrics_endpoint(endpoint: str) -> str:
    base = endpoint.rstrip("/")
    if base.endswith("/v1/metrics"):
        return base
    return f"{base}/v1/metrics"
