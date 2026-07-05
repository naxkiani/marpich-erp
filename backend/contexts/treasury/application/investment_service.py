"""Enterprise Investment Management application service."""
from __future__ import annotations

from datetime import date

from contexts.treasury.domain.aggregates.investment_engine import (
    Investment,
    InvestmentStatus,
    InvestmentTransaction,
    InvestmentTransactionType,
    InvestmentType,
)
from contexts.treasury.domain.events.integration_events import (
    TreasuryAIAnalysisCompletedIntegration,
    TreasuryInvestmentMaturedIntegration,
    TreasuryInvestmentPurchasedIntegration,
)
from contexts.treasury.domain.ports.investment_repositories import (
    IInvestmentRepository,
    IInvestmentTransactionRepository,
)
from contexts.treasury.domain.ports.repositories import ITreasuryAccountRepository
from contexts.treasury.domain.services.investment_engine import (
    build_investment_dashboard,
    compute_daily_accrual,
    compute_maturity_tracking,
    compute_portfolio_performance,
    compute_risk_ratings,
    generate_ai_investment_analysis,
    list_investment_catalog,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class InvestmentApplicationService:
    def __init__(
        self,
        accounts: ITreasuryAccountRepository,
        investments: IInvestmentRepository,
        transactions: IInvestmentTransactionRepository,
    ) -> None:
        self._accounts = accounts
        self._investments = investments
        self._transactions = transactions

    async def _context(self, tenant_id: str) -> dict:
        investments = await self._investments.list_by_tenant(tenant_id)
        txns = await self._transactions.list_by_tenant(tenant_id)
        return {
            "investments": [i.to_dict() for i in investments],
            "transactions": [t.to_dict() for t in txns],
        }

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_investment_catalog())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            build_investment_dashboard(
                investments=ctx["investments"],
                transactions=ctx["transactions"],
            )
        )

    async def list_investments(
        self, tenant_id: str, portfolio_name: str | None = None
    ) -> Result[list[dict]]:
        if portfolio_name:
            items = await self._investments.list_by_portfolio(tenant_id, portfolio_name)
        else:
            items = await self._investments.list_by_tenant(tenant_id)
        return Result.ok([i.to_dict() for i in items])

    async def get_investment(self, investment_id: str) -> Result[dict]:
        inv = await self._investments.find_by_id(investment_id)
        if not inv:
            return Result.fail("treasury.errors.investment_not_found")
        return Result.ok(inv.to_dict())

    async def create_investment(
        self,
        *,
        tenant_id: str,
        portfolio_name: str,
        investment_type: str,
        name: str,
        instrument_code: str,
        principal_amount: float,
        currency: str,
        interest_rate: float = 0.0,
        purchase_date: str,
        maturity_date: str | None = None,
        risk_rating: str | None = None,
        treasury_account_id: str | None = None,
        notes: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        try:
            InvestmentType(investment_type)
        except ValueError:
            return Result.fail("treasury.errors.invalid_investment_type")

        if treasury_account_id:
            account = await self._accounts.find_by_id(treasury_account_id)
            if not account or account.tenant_id != tenant_id:
                return Result.fail("treasury.errors.treasury_account_not_found")
            if account.balance < principal_amount:
                return Result.fail("treasury.errors.insufficient_balance")
            account.debit(principal_amount)
            await self._accounts.save(account)

        inv = Investment.create(
            tenant_id=tenant_id,
            portfolio_name=portfolio_name,
            investment_type=investment_type,
            name=name,
            instrument_code=instrument_code,
            principal_amount=principal_amount,
            currency=currency,
            interest_rate=interest_rate,
            purchase_date=purchase_date,
            maturity_date=maturity_date,
            risk_rating=risk_rating,
            treasury_account_id=treasury_account_id,
            notes=notes,
        )
        await self._investments.save(inv)

        txn = InvestmentTransaction.create(
            tenant_id=tenant_id,
            investment_id=str(inv.id),
            transaction_type=InvestmentTransactionType.PURCHASE.value,
            amount=principal_amount,
            currency=currency,
            transaction_date=purchase_date,
            reference=f"PURCHASE-{instrument_code}",
        )
        await self._transactions.save(txn)

        await publish_integration_event(
            TreasuryInvestmentPurchasedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id or f"investment-purchase-{inv.id}",
                investment_id=str(inv.id),
                investment_type=investment_type,
                principal_amount=principal_amount,
                currency=currency,
                portfolio_name=portfolio_name,
            )
        )
        return Result.ok(inv.to_dict())

    async def accrue_interest(
        self, investment_id: str, *, tenant_id: str, days: int = 1, accrual_date: str | None = None
    ) -> Result[dict]:
        inv = await self._investments.find_by_id(investment_id)
        if not inv or inv.tenant_id != tenant_id:
            return Result.fail("treasury.errors.investment_not_found")

        amount = compute_daily_accrual(
            principal=inv.principal_amount,
            annual_rate=inv.interest_rate,
            days=days,
        )
        if amount <= 0:
            return Result.fail("treasury.errors.no_interest_to_accrue")

        try:
            inv.accrue_interest(amount)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        txn = InvestmentTransaction.create(
            tenant_id=tenant_id,
            investment_id=investment_id,
            transaction_type=InvestmentTransactionType.INTEREST_ACCRUAL.value,
            amount=amount,
            currency=inv.currency,
            transaction_date=accrual_date or date.today().isoformat(),
            reference=f"ACCRUAL-{inv.instrument_code}",
        )
        await self._investments.save(inv)
        await self._transactions.save(txn)
        return Result.ok({"investment": inv.to_dict(), "accrual_amount": amount, "transaction": txn.to_dict()})

    async def record_income(
        self,
        investment_id: str,
        *,
        tenant_id: str,
        amount: float,
        transaction_date: str | None = None,
        notes: str | None = None,
    ) -> Result[dict]:
        inv = await self._investments.find_by_id(investment_id)
        if not inv or inv.tenant_id != tenant_id:
            return Result.fail("treasury.errors.investment_not_found")
        if amount <= 0:
            return Result.fail("treasury.errors.invalid_income_amount")

        try:
            inv.record_income(amount)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        txn = InvestmentTransaction.create(
            tenant_id=tenant_id,
            investment_id=investment_id,
            transaction_type=InvestmentTransactionType.INCOME.value,
            amount=amount,
            currency=inv.currency,
            transaction_date=transaction_date or date.today().isoformat(),
            reference=f"INCOME-{inv.instrument_code}",
            notes=notes,
        )
        await self._investments.save(inv)
        await self._transactions.save(txn)
        return Result.ok({"investment": inv.to_dict(), "transaction": txn.to_dict()})

    async def mature_investment(
        self,
        investment_id: str,
        *,
        tenant_id: str,
        maturity_date: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        inv = await self._investments.find_by_id(investment_id)
        if not inv or inv.tenant_id != tenant_id:
            return Result.fail("treasury.errors.investment_not_found")

        try:
            proceeds = inv.mature()
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        if inv.treasury_account_id:
            account = await self._accounts.find_by_id(inv.treasury_account_id)
            if account and account.tenant_id == tenant_id:
                account.credit(proceeds)
                await self._accounts.save(account)

        txn = InvestmentTransaction.create(
            tenant_id=tenant_id,
            investment_id=investment_id,
            transaction_type=InvestmentTransactionType.MATURITY.value,
            amount=proceeds,
            currency=inv.currency,
            transaction_date=maturity_date or date.today().isoformat(),
            reference=f"MATURITY-{inv.instrument_code}",
        )
        await self._investments.save(inv)
        await self._transactions.save(txn)

        await publish_integration_event(
            TreasuryInvestmentMaturedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id or f"investment-maturity-{inv.id}",
                investment_id=str(inv.id),
                investment_type=inv.investment_type,
                maturity_proceeds=proceeds,
                currency=inv.currency,
            )
        )
        return Result.ok({"investment": inv.to_dict(), "maturity_proceeds": proceeds, "transaction": txn.to_dict()})

    async def get_maturity_tracking(self, tenant_id: str, horizon_days: int = 90) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(compute_maturity_tracking(investments=ctx["investments"], horizon_days=horizon_days))

    async def get_portfolio_performance(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(compute_portfolio_performance(investments=ctx["investments"]))

    async def get_risk_ratings(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(compute_risk_ratings(investments=ctx["investments"]))

    async def list_portfolios(self, tenant_id: str) -> Result[list[dict]]:
        ctx = await self._context(tenant_id)
        perf = compute_portfolio_performance(investments=ctx["investments"])
        return Result.ok(perf["portfolios"])

    async def list_income_transactions(self, investment_id: str) -> Result[list[dict]]:
        txns = await self._transactions.list_by_investment(investment_id)
        income_types = {
            InvestmentTransactionType.INCOME.value,
            InvestmentTransactionType.INTEREST_ACCRUAL.value,
            InvestmentTransactionType.MATURITY.value,
        }
        return Result.ok([t.to_dict() for t in txns if t.transaction_type in income_types])

    async def run_ai_analysis(
        self, tenant_id: str, *, correlation_id: str = ""
    ) -> Result[dict]:
        ctx = await self._context(tenant_id)
        accounts = await self._accounts.list_by_tenant(tenant_id)
        liquid = round(
            sum(a.balance for a in accounts if a.is_active and a.account_type in {"cash", "bank", "petty_cash"}),
            2,
        )
        analysis = generate_ai_investment_analysis(
            investments=ctx["investments"],
            liquid_balance=liquid,
        )
        await publish_integration_event(
            TreasuryAIAnalysisCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id or f"investment-ai-{tenant_id}",
                capability="ai_investment_analysis",
                result_summary=f"{len(analysis['recommendations'])} recommendations generated",
            )
        )
        return Result.ok(analysis)

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        if await self._investments.list_by_tenant(tenant_id):
            return

        samples = [
            {
                "portfolio_name": "Core Treasury Portfolio",
                "investment_type": InvestmentType.FIXED_DEPOSIT.value,
                "name": "6-Month Fixed Deposit",
                "instrument_code": "FD-6M-001",
                "principal_amount": 100000.0,
                "currency": "USD",
                "interest_rate": 4.5,
                "purchase_date": "2025-01-15",
                "maturity_date": "2025-07-15",
            },
            {
                "portfolio_name": "Core Treasury Portfolio",
                "investment_type": InvestmentType.GOVERNMENT_SECURITIES.value,
                "name": "Treasury Bill 91-Day",
                "instrument_code": "T-BILL-91",
                "principal_amount": 250000.0,
                "currency": "USD",
                "interest_rate": 3.8,
                "purchase_date": "2025-04-01",
                "maturity_date": "2025-07-01",
            },
            {
                "portfolio_name": "Income Portfolio",
                "investment_type": InvestmentType.BONDS.value,
                "name": "Corporate Bond Series A",
                "instrument_code": "BOND-A-2027",
                "principal_amount": 150000.0,
                "currency": "USD",
                "interest_rate": 5.2,
                "purchase_date": "2024-06-01",
                "maturity_date": "2027-06-01",
            },
            {
                "portfolio_name": "Growth Portfolio",
                "investment_type": InvestmentType.MUTUAL_FUNDS.value,
                "name": "Balanced Growth Fund",
                "instrument_code": "MUTF-BAL",
                "principal_amount": 75000.0,
                "currency": "USD",
                "interest_rate": 0.0,
                "purchase_date": "2025-03-01",
                "maturity_date": None,
            },
        ]

        for sample in samples:
            inv = Investment.create(tenant_id=tenant_id, **sample)
            await self._investments.save(inv)
            txn = InvestmentTransaction.create(
                tenant_id=tenant_id,
                investment_id=str(inv.id),
                transaction_type=InvestmentTransactionType.PURCHASE.value,
                amount=inv.principal_amount,
                currency=inv.currency,
                transaction_date=inv.purchase_date,
                reference=f"SEED-{inv.instrument_code}",
            )
            await self._transactions.save(txn)
