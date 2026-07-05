"""Multi-Currency Treasury application service."""
from __future__ import annotations

from datetime import date

from contexts.treasury.domain.aggregates.multi_currency_engine import (
    BASE_CURRENCY,
    ExchangeRate,
    FxTransaction,
    FxTransactionType,
    RateType,
)
from contexts.treasury.domain.aggregates.treasury_account import TreasuryAccount, TreasuryAccountType
from contexts.treasury.domain.events.integration_events import (
    TreasuryAIAnalysisCompletedIntegration,
    TreasuryFxDealSettledIntegration,
)
from contexts.treasury.domain.ports.investment_repositories import IInvestmentRepository
from contexts.treasury.domain.ports.multi_currency_repositories import (
    IExchangeRateRepository,
    IFxTransactionRepository,
)
from contexts.treasury.domain.ports.repositories import ITreasuryAccountRepository
from contexts.treasury.domain.services.multi_currency_engine import (
    DEFAULT_MARKET_RATES,
    build_fx_dashboard,
    build_fx_report,
    compute_currency_positions,
    compute_revaluation,
    convert_amount,
    generate_ai_fx_recommendations,
    list_multi_currency_catalog,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class MultiCurrencyApplicationService:
    def __init__(
        self,
        accounts: ITreasuryAccountRepository,
        investments: IInvestmentRepository,
        rates: IExchangeRateRepository,
        transactions: IFxTransactionRepository,
    ) -> None:
        self._accounts = accounts
        self._investments = investments
        self._rates = rates
        self._transactions = transactions

    async def _context(self, tenant_id: str) -> dict:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        investments = await self._investments.list_by_tenant(tenant_id)
        rates = await self._rates.list_by_tenant(tenant_id)
        txns = await self._transactions.list_by_tenant(tenant_id)
        rate_dicts = [r.to_dict() for r in rates]
        positions = compute_currency_positions(
            accounts=accounts,
            investments=[i.to_dict() for i in investments],
            rates=rate_dicts,
        )
        txn_dicts = [t.to_dict() for t in sorted(txns, key=lambda x: x.created_at, reverse=True)]
        return {
            "accounts": accounts,
            "investments": investments,
            "rates": rate_dicts,
            "transactions": txn_dicts,
            "positions": positions,
        }

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_multi_currency_catalog())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            build_fx_dashboard(
                positions=ctx["positions"],
                transactions=ctx["transactions"],
                rates=ctx["rates"],
            )
        )

    async def get_positions(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(ctx["positions"])

    async def list_rates(
        self, tenant_id: str, rate_type: str | None = None
    ) -> Result[list[dict]]:
        if rate_type:
            try:
                RateType(rate_type)
            except ValueError:
                return Result.fail("treasury.errors.invalid_rate_type")
            rates = await self._rates.list_by_type(tenant_id, rate_type)
        else:
            rates = await self._rates.list_by_tenant(tenant_id)
        return Result.ok(
            [r.to_dict() for r in sorted(rates, key=lambda x: (x.rate_type, x.effective_date), reverse=True)]
        )

    async def create_rate(
        self,
        *,
        tenant_id: str,
        quote_currency: str,
        rate: float,
        rate_type: str,
        effective_date: str | None = None,
        source: str = "",
        base_currency: str = BASE_CURRENCY,
    ) -> Result[dict]:
        try:
            RateType(rate_type)
        except ValueError:
            return Result.fail("treasury.errors.invalid_rate_type")
        if rate <= 0:
            return Result.fail("treasury.errors.invalid_exchange_rate")

        entry = ExchangeRate.create(
            tenant_id=tenant_id,
            base_currency=base_currency,
            quote_currency=quote_currency,
            rate=rate,
            rate_type=rate_type,
            effective_date=effective_date or date.today().isoformat(),
            source=source or rate_type,
        )
        await self._rates.save(entry)
        return Result.ok(entry.to_dict())

    async def convert_currency(
        self,
        *,
        tenant_id: str,
        from_currency: str,
        to_currency: str,
        amount: float,
        rate_type: str | None = None,
        transaction_date: str | None = None,
        notes: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        if amount <= 0:
            return Result.fail("treasury.errors.invalid_amount")
        ctx = await self._context(tenant_id)
        try:
            converted, fx_rate = convert_amount(
                amount=amount,
                from_currency=from_currency.upper(),
                to_currency=to_currency.upper(),
                rates=ctx["rates"],
                rate_type=rate_type or RateType.MARKET.value,
            )
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        txn = FxTransaction.create(
            tenant_id=tenant_id,
            transaction_type=FxTransactionType.CONVERSION.value,
            from_currency=from_currency,
            to_currency=to_currency,
            from_amount=amount,
            to_amount=converted,
            exchange_rate=fx_rate,
            rate_type=rate_type or RateType.MARKET.value,
            reference=f"FX-CONV-{from_currency}-{to_currency}",
            transaction_date=transaction_date or date.today().isoformat(),
            notes=notes,
        )
        await self._transactions.save(txn)
        await self._publish_fx_event(tenant_id, txn, correlation_id)
        return Result.ok(txn.to_dict())

    async def cross_currency_transfer(
        self,
        *,
        tenant_id: str,
        from_account_id: str,
        to_account_id: str,
        amount: float,
        rate_type: str | None = None,
        transaction_date: str | None = None,
        notes: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        if amount <= 0:
            return Result.fail("treasury.errors.invalid_amount")

        from_acct = await self._accounts.find_by_id(from_account_id)
        to_acct = await self._accounts.find_by_id(to_account_id)
        if not from_acct or from_acct.tenant_id != tenant_id:
            return Result.fail("treasury.errors.treasury_account_not_found")
        if not to_acct or to_acct.tenant_id != tenant_id:
            return Result.fail("treasury.errors.treasury_account_not_found")
        if from_acct.balance < amount:
            return Result.fail("treasury.errors.insufficient_balance")

        ctx = await self._context(tenant_id)
        try:
            converted, fx_rate = convert_amount(
                amount=amount,
                from_currency=from_acct.currency,
                to_currency=to_acct.currency,
                rates=ctx["rates"],
                rate_type=rate_type or RateType.MARKET.value,
            )
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        from_acct.debit(amount)
        to_acct.credit(converted)
        await self._accounts.save(from_acct)
        await self._accounts.save(to_acct)

        txn = FxTransaction.create(
            tenant_id=tenant_id,
            transaction_type=FxTransactionType.CROSS_CURRENCY_TRANSFER.value,
            from_currency=from_acct.currency,
            to_currency=to_acct.currency,
            from_amount=amount,
            to_amount=converted,
            exchange_rate=fx_rate,
            rate_type=rate_type or RateType.MARKET.value,
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            reference=f"FX-XFER-{from_acct.currency}-{to_acct.currency}",
            transaction_date=transaction_date or date.today().isoformat(),
            notes=notes,
        )
        await self._transactions.save(txn)
        await self._publish_fx_event(tenant_id, txn, correlation_id)
        return Result.ok(txn.to_dict())

    async def run_revaluation(
        self,
        *,
        tenant_id: str,
        currency: str,
        new_rate: float,
        rate_type: str = RateType.MARKET.value,
        transaction_date: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        if new_rate <= 0:
            return Result.fail("treasury.errors.invalid_exchange_rate")

        ctx = await self._context(tenant_id)
        currency = currency.upper()
        pos = next((p for p in ctx["positions"]["positions"] if p["currency"] == currency), None)
        if not pos:
            return Result.fail("treasury.errors.currency_position_not_found")

        prior_rate = next(
            (
                r["rate"]
                for r in ctx["rates"]
                if r["quote_currency"] == currency and r["rate_type"] == rate_type
            ),
            None,
        )
        if not prior_rate and currency != BASE_CURRENCY:
            return Result.fail("treasury.errors.rate_not_found")

        prior_rate = prior_rate or 1.0
        result = compute_revaluation(
            currency=currency,
            book_balance=pos["local_balance"],
            prior_rate=prior_rate,
            new_rate=new_rate,
        )

        txn_type = FxTransactionType.REVALUATION.value
        if result["result_type"]:
            txn_type = result["result_type"]

        txn = FxTransaction.create(
            tenant_id=tenant_id,
            transaction_type=txn_type,
            from_currency=currency,
            to_currency=BASE_CURRENCY,
            from_amount=pos["local_balance"],
            to_amount=result["new_base_value"],
            exchange_rate=new_rate,
            rate_type=rate_type,
            gain_loss=result["gain_loss"],
            reference=f"FX-REVAL-{currency}",
            transaction_date=transaction_date or date.today().isoformat(),
            notes=f"Revaluation {prior_rate} → {new_rate}",
        )
        await self._transactions.save(txn)

        if currency != BASE_CURRENCY:
            rate_entry = ExchangeRate.create(
                tenant_id=tenant_id,
                base_currency=BASE_CURRENCY,
                quote_currency=currency,
                rate=new_rate,
                rate_type=rate_type,
                effective_date=transaction_date or date.today().isoformat(),
                source="revaluation",
            )
            await self._rates.save(rate_entry)

        if result["gain_loss"] != 0:
            await self._publish_fx_event(tenant_id, txn, correlation_id)

        return Result.ok({**result, "transaction": txn.to_dict()})

    async def get_fx_report(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            build_fx_report(
                positions=ctx["positions"],
                transactions=ctx["transactions"],
                rates=ctx["rates"],
            )
        )

    async def list_transactions(self, tenant_id: str) -> Result[list[dict]]:
        ctx = await self._context(tenant_id)
        return Result.ok(ctx["transactions"])

    async def run_ai_recommendations(
        self, tenant_id: str, *, correlation_id: str = ""
    ) -> Result[dict]:
        ctx = await self._context(tenant_id)
        analysis = generate_ai_fx_recommendations(
            positions=ctx["positions"],
            rates=ctx["rates"],
            transactions=ctx["transactions"],
        )
        await publish_integration_event(
            TreasuryAIAnalysisCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id or f"fx-ai-{tenant_id}",
                capability="ai_fx_recommendations",
                result_summary=f"{len(analysis['recommendations'])} FX recommendations generated",
            )
        )
        return Result.ok(analysis)

    async def _publish_fx_event(
        self, tenant_id: str, txn: FxTransaction, correlation_id: str
    ) -> None:
        await publish_integration_event(
            TreasuryFxDealSettledIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id or f"fx-deal-{txn.id}",
                transaction_id=str(txn.id),
                from_currency=txn.from_currency,
                to_currency=txn.to_currency,
                from_amount=txn.from_amount,
                to_amount=txn.to_amount,
                exchange_rate=txn.exchange_rate,
                gain_loss=txn.gain_loss,
            )
        )

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        if await self._rates.list_by_tenant(tenant_id):
            return

        today = date.today().isoformat()
        hist_date = "2025-01-01"

        for quote, market_rate in DEFAULT_MARKET_RATES.items():
            await self._rates.save(
                ExchangeRate.create(
                    tenant_id=tenant_id,
                    base_currency=BASE_CURRENCY,
                    quote_currency=quote,
                    rate=market_rate,
                    rate_type=RateType.MARKET.value,
                    effective_date=today,
                    source="market_feed",
                )
            )
            cb_rate = round(market_rate * 0.998, 6)
            await self._rates.save(
                ExchangeRate.create(
                    tenant_id=tenant_id,
                    base_currency=BASE_CURRENCY,
                    quote_currency=quote,
                    rate=cb_rate,
                    rate_type=RateType.CENTRAL_BANK.value,
                    effective_date=today,
                    source="central_bank",
                )
            )
            await self._rates.save(
                ExchangeRate.create(
                    tenant_id=tenant_id,
                    base_currency=BASE_CURRENCY,
                    quote_currency=quote,
                    rate=round(market_rate * 0.95, 6),
                    rate_type=RateType.HISTORICAL.value,
                    effective_date=hist_date,
                    source="historical_archive",
                )
            )

        accounts = await self._accounts.list_by_tenant(tenant_id)
        has_eur = any(a.currency == "EUR" for a in accounts)
        if not has_eur:
            eur_account = TreasuryAccount.create(
                tenant_id=tenant_id,
                code="EUR-OPERATING",
                name="EUR Operating Account",
                account_type=TreasuryAccountType.BANK.value,
                currency="EUR",
                bank_name="Euro Bank",
            )
            eur_account.balance = 25000.0
            await self._accounts.save(eur_account)

            gbp_account = TreasuryAccount.create(
                tenant_id=tenant_id,
                code="GBP-OPERATING",
                name="GBP Operating Account",
                account_type=TreasuryAccountType.BANK.value,
                currency="GBP",
                bank_name="Sterling Bank",
            )
            gbp_account.balance = 15000.0
            await self._accounts.save(gbp_account)
