"""Exchange rate provider adapters — central bank and exchange APIs."""
from __future__ import annotations

from datetime import date
from typing import Protocol

from contexts.financial_kernel.domain.aggregates.currency import RateSource, RateType


class IExchangeRateProvider(Protocol):
    async def fetch_spot_rates(
        self, *, base_currency: str, target_currencies: list[str], provider: str
    ) -> list[dict]: ...


class StubExchangeRateProvider:
    """Stub provider simulating ECB / Open Exchange Rates APIs."""

    _DEFAULT_RATES: dict[str, float] = {
        "EUR": 0.92,
        "GBP": 0.79,
        "IRR": 42000.0,
        "AED": 3.67,
        "JPY": 149.5,
        "CHF": 0.88,
    }

    async def fetch_spot_rates(
        self, *, base_currency: str, target_currencies: list[str], provider: str
    ) -> list[dict]:
        today = date.today().isoformat()
        results = []
        for target in target_currencies:
            if target == base_currency:
                continue
            rate = self._DEFAULT_RATES.get(target)
            if rate is None:
                rate = round(abs(hash(f"{base_currency}{target}{provider}") % 10000) / 1000 + 0.5, 4)
            results.append(
                {
                    "from_currency": base_currency,
                    "to_currency": target,
                    "rate": rate,
                    "rate_type": RateType.SPOT.value,
                    "rate_source": RateSource.EXCHANGE_API.value,
                    "effective_date": today,
                    "provider": provider,
                }
            )
        return results


class CentralBankRateProvider:
    """Central bank rate feed stub (e.g. Fed, CBI, ECB reference)."""

    _CB_RATES: dict[str, dict[str, float]] = {
        "USD": {"EUR": 0.93, "IRR": 42500.0, "GBP": 0.80},
        "EUR": {"USD": 1.08, "GBP": 0.86, "IRR": 46000.0},
    }

    async def fetch_rates(
        self, *, base_currency: str, target_currencies: list[str], central_bank: str
    ) -> list[dict]:
        today = date.today().isoformat()
        table = self._CB_RATES.get(base_currency, {})
        results = []
        for target in target_currencies:
            if target == base_currency:
                continue
            rate = table.get(target)
            if rate is None:
                continue
            results.append(
                {
                    "from_currency": base_currency,
                    "to_currency": target,
                    "rate": rate,
                    "rate_type": RateType.CENTRAL_BANK.value,
                    "rate_source": RateSource.CENTRAL_BANK.value,
                    "effective_date": today,
                    "provider": central_bank,
                }
            )
        return results
