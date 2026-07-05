"""Interest Calculation Engine application service."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.banking.domain.aggregates.interest_calculation_engine import (
    CalcMode,
    InterestCalculationAudit,
    InterestRateChange,
    InterestRateProfile,
    RateType,
)
from contexts.banking.domain.events.interest_integration_events import (
    BankingInterestCalculatedIntegration,
    BankingInterestRateChangedIntegration,
    BankingInterestSimulatedIntegration,
)
from contexts.banking.domain.ports.interest_calculation_repositories import (
    IInterestCalculationAuditRepository,
    IInterestRateChangeRepository,
    IInterestRateProfileRepository,
)
from contexts.banking.domain.services.interest_calculation_engine import (
    build_interest_dashboard,
    list_interest_catalog,
    list_interest_policy_keys,
    resolve_floating_rate,
    resolve_historical_rate,
    resolve_promotional_rate,
    run_interest_calculation,
)
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BankingInterestCalculationApplicationService:
    def __init__(
        self,
        profiles: IInterestRateProfileRepository,
        rate_changes: IInterestRateChangeRepository,
        audits: IInterestCalculationAuditRepository,
        policy: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._rate_changes = rate_changes
        self._audits = audits
        self._policy = policy

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_interest_catalog())

    async def list_policy_keys(self) -> Result[list[dict]]:
        return Result.ok(list_interest_policy_keys())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profiles = await self._profiles.list_by_tenant(tenant_id)
        audits = await self._audits.list_by_tenant(tenant_id)
        changes = await self._rate_changes.list_by_tenant(tenant_id)
        return Result.ok(
            build_interest_dashboard(
                profiles=[p.to_dict() for p in profiles],
                audits=[a.to_dict() for a in audits],
                rate_changes=[c.to_dict() for c in changes],
            )
        )

    async def create_rate_profile(
        self,
        *,
        tenant_id: str,
        product_context: str,
        rate_type: str,
        rate_annual: float,
        spread_bps: float = 0.0,
        index_ref: str = "",
        index_rate_annual: float | None = None,
        promotional_until: datetime | None = None,
        promotional_rate_annual: float | None = None,
        currency: str = "USD",
    ) -> Result[dict]:
        resolved_rate = rate_annual
        if rate_type == RateType.FLOATING.value:
            index = index_rate_annual
            if index is None:
                float_policy = await self._policy.evaluate(
                    tenant_id=tenant_id,
                    domain="bank",
                    policy_key="interest.rate.floating",
                    facts={"product_context": product_context, "index_ref": index_ref},
                )
                index = float(float_policy.parameters.get("index_rate_annual", rate_annual))
                spread_bps = float(float_policy.parameters.get("spread_bps", spread_bps))
            resolved_rate = resolve_floating_rate(index_rate_annual=index, spread_bps=spread_bps)
        elif rate_type == RateType.PROMOTIONAL.value:
            promo_policy = await self._policy.evaluate(
                tenant_id=tenant_id,
                domain="bank",
                policy_key="interest.rate.promotional",
                facts={"product_context": product_context},
            )
            if promotional_rate_annual is None:
                promotional_rate_annual = float(
                    promo_policy.parameters.get("promotional_rate_annual", rate_annual)
                )

        ref = self._profiles.next_profile_ref(tenant_id)
        profile = InterestRateProfile.create(
            tenant_id=tenant_id,
            profile_ref=ref,
            product_context=product_context,
            rate_type=rate_type,
            rate_annual=resolved_rate,
            spread_bps=spread_bps,
            index_ref=index_ref,
            promotional_until=promotional_until,
            promotional_rate_annual=promotional_rate_annual,
            currency=currency,
        )
        await self._profiles.save(profile)
        return Result.ok(profile.to_dict())

    async def record_rate_change(
        self,
        *,
        profile_id: str,
        new_rate_annual: float,
        rate_type: str | None = None,
        effective_from: datetime | None = None,
        reason: str = "",
        changed_by: str | None = None,
    ) -> Result[dict]:
        profile = await self._profiles.find_by_id(profile_id)
        if not profile:
            return Result.fail("banking.errors.interest_profile_not_found")

        eff = effective_from or datetime.now(UTC)
        new_type = rate_type or profile.rate_type
        change = InterestRateChange.create(
            tenant_id=profile.tenant_id,
            profile_id=profile_id,
            previous_rate_annual=profile.rate_annual,
            new_rate_annual=new_rate_annual,
            rate_type=new_type,
            effective_from=eff,
            reason=reason,
            changed_by=changed_by,
        )
        profile.update_rate(rate_annual=new_rate_annual, rate_type=new_type)
        await self._rate_changes.save(change)
        await self._profiles.save(profile)

        await publish_integration_event(
            BankingInterestRateChangedIntegration(
                tenant_id=TenantId.create(profile.tenant_id),
                correlation_id=f"interest-rate-{change.id}",
                profile_id=profile_id,
                profile_ref=profile.profile_ref,
                previous_rate_annual=change.previous_rate_annual,
                new_rate_annual=change.new_rate_annual,
                rate_type=new_type,
                effective_from=eff.isoformat(),
            )
        )
        return Result.ok({"profile": profile.to_dict(), "change": change.to_dict()})

    async def _resolve_effective_rate(
        self,
        *,
        tenant_id: str,
        profile: InterestRateProfile | None,
        product_context: str,
        rate_annual_override: float | None,
        as_of: datetime | None = None,
    ) -> tuple[float, str]:
        if profile:
            changes = await self._rate_changes.list_by_profile(str(profile.id))
            historical_rate, historical_type = resolve_historical_rate(
                profile_rate_annual=profile.rate_annual,
                rate_changes=[c.to_dict() for c in changes],
                as_of=as_of,
            )
            promo_rate, promo_type = resolve_promotional_rate(
                base_rate_annual=historical_rate,
                promotional_rate_annual=profile.promotional_rate_annual,
                promotional_until=profile.promotional_until,
                as_of=as_of,
            )
            return promo_rate, promo_type or historical_type or profile.rate_type

        if rate_annual_override is not None:
            return rate_annual_override, RateType.FIXED.value

        policy_key = (
            "deposit.interest.rate"
            if product_context == "deposit"
            else "loan.interest.rate"
            if product_context == "loan"
            else "interest.rate.fixed"
        )
        rate_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key=policy_key,
            facts={"product_context": product_context},
        )
        return float(rate_policy.parameters.get("rate_annual", 0.0)), RateType.FIXED.value

    async def calculate(
        self,
        *,
        tenant_id: str,
        product_context: str,
        principal: float,
        frequency: str,
        method: str | None = None,
        periods: int = 1,
        days: int | None = None,
        profile_id: str | None = None,
        rate_annual: float | None = None,
        days_overdue: int = 0,
        profit_pool: float = 0.0,
        source_ref: str = "",
        currency: str = "USD",
        actor_id: str | None = None,
        as_of: datetime | None = None,
    ) -> Result[dict]:
        return await self._execute_calculation(
            tenant_id=tenant_id,
            mode=CalcMode.PRODUCTION.value,
            product_context=product_context,
            principal=principal,
            frequency=frequency,
            method=method,
            periods=periods,
            days=days,
            profile_id=profile_id,
            rate_annual=rate_annual,
            days_overdue=days_overdue,
            profit_pool=profit_pool,
            source_ref=source_ref,
            currency=currency,
            actor_id=actor_id,
            as_of=as_of,
        )

    async def simulate(
        self,
        *,
        tenant_id: str,
        product_context: str,
        principal: float,
        frequency: str,
        method: str | None = None,
        periods: int = 1,
        days: int | None = None,
        profile_id: str | None = None,
        rate_annual: float | None = None,
        days_overdue: int = 0,
        profit_pool: float = 0.0,
        currency: str = "USD",
        actor_id: str | None = None,
    ) -> Result[dict]:
        return await self._execute_calculation(
            tenant_id=tenant_id,
            mode=CalcMode.SIMULATION.value,
            product_context=product_context,
            principal=principal,
            frequency=frequency,
            method=method,
            periods=periods,
            days=days,
            profile_id=profile_id,
            rate_annual=rate_annual,
            days_overdue=days_overdue,
            profit_pool=profit_pool,
            source_ref="simulation",
            currency=currency,
            actor_id=actor_id,
        )

    async def _execute_calculation(
        self,
        *,
        tenant_id: str,
        mode: str,
        product_context: str,
        principal: float,
        frequency: str,
        method: str | None,
        periods: int,
        days: int | None,
        profile_id: str | None,
        rate_annual: float | None,
        days_overdue: int,
        profit_pool: float,
        source_ref: str,
        currency: str,
        actor_id: str | None,
        as_of: datetime | None = None,
    ) -> Result[dict]:
        if principal <= 0:
            return Result.fail("banking.errors.invalid_principal")

        profile = await self._profiles.find_by_id(profile_id) if profile_id else None
        if profile_id and not profile:
            return Result.fail("banking.errors.interest_profile_not_found")

        method_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="interest.calculation.method",
            facts={"product_context": product_context, "frequency": frequency},
        )
        resolved_method = method or method_policy.parameters.get("method", "simple")

        grace_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="interest.grace.period",
            facts={"product_context": product_context},
        )
        grace_days = int(grace_policy.parameters.get("grace_days", 0))

        penalty_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="interest.penalty.rate",
            facts={"product_context": product_context, "days_overdue": days_overdue},
        )
        penalty_multiplier = float(penalty_policy.parameters.get("penalty_multiplier", 1.5))

        compound_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="interest.compounding.frequency",
            facts={"product_context": product_context},
        )
        compounding_periods = int(compound_policy.parameters.get("periods_per_year", 12))

        profit_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="interest.profit_sharing",
            facts={"product_context": product_context, "profit_pool": profit_pool},
        )
        profit_share_pct = float(profit_policy.parameters.get("profit_share_pct", 0.0))

        effective_rate, effective_type = await self._resolve_effective_rate(
            tenant_id=tenant_id,
            profile=profile,
            product_context=product_context,
            rate_annual_override=rate_annual,
            as_of=as_of,
        )

        result = run_interest_calculation(
            principal=principal,
            rate_annual=effective_rate,
            rate_type=effective_type,
            frequency=frequency,
            method=resolved_method,
            periods=periods,
            days=days,
            grace_days=grace_days,
            days_overdue=days_overdue,
            penalty_multiplier=penalty_multiplier,
            penalty_outcome=penalty_policy.outcome,
            profit_pool=profit_pool,
            profit_share_pct=profit_share_pct,
            compounding_periods_per_year=compounding_periods,
        )

        policy_snapshot = {
            "method": resolved_method,
            "grace_days": grace_days,
            "penalty_multiplier": penalty_multiplier,
            "compounding_periods_per_year": compounding_periods,
            "profit_share_pct": profit_share_pct,
        }

        calc_ref = self._audits.next_calc_ref(tenant_id)
        audit = InterestCalculationAudit.create(
            tenant_id=tenant_id,
            calc_ref=calc_ref,
            mode=mode,
            product_context=product_context,
            principal=principal,
            currency=currency,
            frequency=frequency,
            method=resolved_method,
            rate_annual=effective_rate,
            rate_type=effective_type,
            effective_days=result["effective_days"],
            grace_days_applied=result["grace_days_applied"],
            interest_amount=result["interest_amount"],
            penalty_interest=result["penalty_interest"],
            profit_share_amount=result["profit_share_amount"],
            profile_id=profile_id,
            source_ref=source_ref,
            policy_snapshot=policy_snapshot,
            calculation_detail=result["calculation_detail"],
            actor_id=actor_id,
        )
        await self._audits.save(audit)

        if mode == CalcMode.SIMULATION.value:
            await publish_integration_event(
                BankingInterestSimulatedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=f"interest-sim-{audit.id}",
                    audit_id=str(audit.id),
                    calc_ref=calc_ref,
                    product_context=product_context,
                    interest_amount=result["interest_amount"],
                    currency=currency,
                )
            )
        else:
            await publish_integration_event(
                BankingInterestCalculatedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=f"interest-calc-{audit.id}",
                    audit_id=str(audit.id),
                    calc_ref=calc_ref,
                    product_context=product_context,
                    principal=principal,
                    interest_amount=result["interest_amount"],
                    penalty_interest=result["penalty_interest"],
                    currency=currency,
                    mode=mode,
                )
            )

        return Result.ok({**result, "audit": audit.to_dict()})

    async def list_rate_profiles(self, tenant_id: str) -> Result[list[dict]]:
        profiles = await self._profiles.list_by_tenant(tenant_id)
        return Result.ok([p.to_dict() for p in profiles])

    async def get_rate_profile(self, profile_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_id(profile_id)
        if not profile:
            return Result.fail("banking.errors.interest_profile_not_found")
        changes = await self._rate_changes.list_by_profile(profile_id)
        audits = await self._audits.list_by_profile(profile_id)
        return Result.ok(
            {
                **profile.to_dict(),
                "rate_changes": [c.to_dict() for c in changes],
                "calculations": [a.to_dict() for a in audits[:10]],
            }
        )

    async def list_rate_history(self, profile_id: str) -> Result[list[dict]]:
        profile = await self._profiles.find_by_id(profile_id)
        if not profile:
            return Result.fail("banking.errors.interest_profile_not_found")
        changes = await self._rate_changes.list_by_profile(profile_id)
        return Result.ok([c.to_dict() for c in changes])

    async def list_audit_history(
        self, tenant_id: str, *, source_ref: str | None = None
    ) -> Result[list[dict]]:
        if source_ref:
            audits = await self._audits.list_by_source_ref(tenant_id, source_ref)
        else:
            audits = await self._audits.list_by_tenant(tenant_id)
        return Result.ok([a.to_dict() for a in audits])

    async def get_audit(self, audit_id: str) -> Result[dict]:
        audit = await self._audits.find_by_id(audit_id)
        if not audit:
            return Result.fail("banking.errors.interest_audit_not_found")
        return Result.ok(audit.to_dict())

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        pass
