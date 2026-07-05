"""Banking Analytics integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class BankingAnalyticsReportGeneratedIntegration(IntegrationEvent):
    report_type: str
    capability: str

    @property
    def event_name(self) -> str:
        return "banking.analytics.report.generated"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "report_type": self.report_type,
            "capability": self.capability,
        }


@dataclass(frozen=True, kw_only=True)
class BankingAnalyticsInsightRaisedIntegration(IntegrationEvent):
    insight_type: str
    severity: str

    @property
    def event_name(self) -> str:
        return "banking.analytics.insight.raised"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "insight_type": self.insight_type,
            "severity": self.severity,
        }


@dataclass(frozen=True, kw_only=True)
class BankingAnalyticsRecommendationGeneratedIntegration(IntegrationEvent):
    recommendation_count: int
    capability: str

    @property
    def event_name(self) -> str:
        return "banking.analytics.recommendation.generated"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "recommendation_count": self.recommendation_count,
            "capability": self.capability,
        }


@dataclass(frozen=True, kw_only=True)
class BankingAnalyticsForecastCompletedIntegration(IntegrationEvent):
    horizon_days: int
    forecast_type: str

    @property
    def event_name(self) -> str:
        return "banking.analytics.forecast.completed"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "horizon_days": self.horizon_days,
            "forecast_type": self.forecast_type,
        }
