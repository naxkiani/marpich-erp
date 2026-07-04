"""Enterprise Financial Security application service."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.financial_security import (
    CloseType,
    MakerCheckerRequest,
    PeriodCloseRequest,
    PolicyType,
    SecurityAuditRecord,
    SecurityControlType,
    SecurityPolicy,
    SecurityRequestStatus,
    TransactionLock,
)
from contexts.financial_kernel.domain.events.integration_events import (
    FinancialSecurityAuditRecordedIntegration,
    FinancialSecurityMakerCheckerApprovedIntegration,
    FinancialSecurityMakerCheckerSubmittedIntegration,
    FinancialSecurityPeriodClosedIntegration,
    FinancialSecurityTamperDetectedIntegration,
    FinancialSecurityTransactionLockedIntegration,
)
from contexts.financial_kernel.domain.ports.financial_security_repositories import (
    IMakerCheckerRepository,
    IPeriodCloseRequestRepository,
    ISecurityAuditRepository,
    ISecurityPolicyRepository,
    ITransactionLockRepository,
)
from contexts.financial_kernel.domain.ports.repositories import IFiscalPeriodRepository, IFiscalYearRepository
from contexts.financial_kernel.domain.services.financial_security_engine import (
    checksum_payload,
    compute_tamper_hash,
    encrypt_payload,
    evaluate_abac_policy,
    evaluate_rbac_policy,
    sign_operation,
    validate_four_eyes,
    validate_maker_checker,
    verify_tamper,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class FinancialSecurityApplicationService:
    def __init__(
        self,
        audits: ISecurityAuditRepository,
        policies: ISecurityPolicyRepository,
        maker_checker: IMakerCheckerRepository,
        locks: ITransactionLockRepository,
        period_closes: IPeriodCloseRequestRepository,
        periods: IFiscalPeriodRepository,
        years: IFiscalYearRepository,
    ) -> None:
        self._audits = audits
        self._policies = policies
        self._maker_checker = maker_checker
        self._locks = locks
        self._period_closes = period_closes
        self._periods = periods
        self._years = years

    async def _record_audit(
        self,
        *,
        tenant_id: str,
        action: str,
        actor_id: str,
        resource_type: str,
        resource_id: str,
        payload_checksum: str,
        correlation_id: str = "",
        before_state: dict | None = None,
        after_state: dict | None = None,
    ) -> SecurityAuditRecord:
        previous = await self._audits.last_tamper_hash(tenant_id)
        tamper_hash = compute_tamper_hash(
            action=action,
            actor_id=actor_id,
            resource_id=resource_id,
            payload_checksum=payload_checksum,
            previous_hash=previous,
        )
        record = SecurityAuditRecord.record(
            tenant_id=tenant_id,
            action=action,
            actor_id=actor_id,
            resource_type=resource_type,
            resource_id=resource_id,
            payload_checksum=payload_checksum,
            tamper_hash=tamper_hash,
            correlation_id=correlation_id,
            before_state=before_state,
            after_state=after_state,
        )
        await self._audits.save(record)
        await publish_integration_event(
            FinancialSecurityAuditRecordedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                audit_id=str(record.id),
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
            )
        )
        return record

    async def _ensure_not_locked(self, tenant_id: str, resource_type: str, resource_id: str) -> Result[None]:
        lock = await self._locks.find_active(tenant_id, resource_type, resource_id)
        if lock:
            return Result.fail("financial_kernel.errors.resource_locked")
        return Result.ok(None)

    async def submit_maker_checker(
        self,
        *,
        tenant_id: str,
        control_type: str,
        resource_type: str,
        resource_id: str,
        idempotency_key: str,
        maker_id: str,
        payload: dict,
        checker_id: str | None = None,
        second_approver_id: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        existing = await self._maker_checker.find_by_idempotency(tenant_id, idempotency_key)
        if existing:
            return Result.ok(existing.to_dict())

        try:
            SecurityControlType(control_type)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_control_type")

        if checker_id:
            try:
                validate_maker_checker(maker_id, checker_id)
            except ValueError:
                return Result.fail("financial_kernel.errors.maker_checker_same_user")

        cs = checksum_payload(payload)
        encrypted = encrypt_payload(payload)

        request = MakerCheckerRequest.submit(
            tenant_id=tenant_id,
            control_type=control_type,
            resource_type=resource_type,
            resource_id=resource_id,
            idempotency_key=idempotency_key,
            maker_id=maker_id,
            payload=payload,
            payload_checksum=cs,
            encrypted_payload=encrypted,
            correlation_id=correlation_id,
            checker_id=checker_id,
            second_approver_id=second_approver_id,
        )
        await self._maker_checker.save(request)
        await self._record_audit(
            tenant_id=tenant_id,
            action="maker_checker.submitted",
            actor_id=maker_id,
            resource_type=resource_type,
            resource_id=resource_id,
            payload_checksum=cs,
            correlation_id=correlation_id,
            after_state={"control_type": control_type, "status": "pending"},
        )

        await publish_integration_event(
            FinancialSecurityMakerCheckerSubmittedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                request_id=str(request.id),
                control_type=control_type,
                maker_id=maker_id,
                resource_type=resource_type,
                resource_id=resource_id,
            )
        )
        return Result.ok(request.to_dict())

    async def approve_maker_checker(
        self,
        *,
        tenant_id: str,
        request_id: str,
        approver_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        request = await self._maker_checker.find_by_id(request_id)
        if not request or request.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.request_not_found")

        try:
            request.approve(approver_id)
        except ValueError as exc:
            return Result.fail(f"financial_kernel.errors.{exc.args[0]}")

        if request.status == SecurityRequestStatus.APPROVED:
            signature = sign_operation(
                resource_id=str(request.id),
                checksum=request.payload_checksum,
                signer_id=approver_id,
            )
            request.sign(signature)

        await self._maker_checker.save(request)
        await self._record_audit(
            tenant_id=tenant_id,
            action="maker_checker.approved",
            actor_id=approver_id,
            resource_type=request.resource_type,
            resource_id=request.resource_id,
            payload_checksum=request.payload_checksum,
            correlation_id=correlation_id,
            after_state={"status": request.status.value},
        )

        if request.status == SecurityRequestStatus.APPROVED:
            await publish_integration_event(
                FinancialSecurityMakerCheckerApprovedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id,
                    request_id=str(request.id),
                    control_type=request.control_type,
                    approved_by=approver_id,
                )
            )
        return Result.ok(request.to_dict())

    async def reject_maker_checker(
        self,
        *,
        tenant_id: str,
        request_id: str,
        actor_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        request = await self._maker_checker.find_by_id(request_id)
        if not request or request.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.request_not_found")
        try:
            request.reject(actor_id)
        except ValueError as exc:
            return Result.fail(f"financial_kernel.errors.{exc.args[0]}")
        await self._maker_checker.save(request)
        await self._record_audit(
            tenant_id=tenant_id,
            action="maker_checker.rejected",
            actor_id=actor_id,
            resource_type=request.resource_type,
            resource_id=request.resource_id,
            payload_checksum=request.payload_checksum,
            correlation_id=correlation_id,
            after_state={"status": "rejected"},
        )
        return Result.ok(request.to_dict())

    async def lock_transaction(
        self,
        *,
        tenant_id: str,
        resource_type: str,
        resource_id: str,
        locked_by: str,
        reason: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        existing = await self._locks.find_active(tenant_id, resource_type, resource_id)
        if existing:
            return Result.fail("financial_kernel.errors.already_locked")

        lock = TransactionLock.lock(
            tenant_id=tenant_id,
            resource_type=resource_type,
            resource_id=resource_id,
            locked_by=locked_by,
            reason=reason,
        )
        await self._locks.save(lock)
        cs = checksum_payload({"resource_type": resource_type, "resource_id": resource_id, "reason": reason})
        await self._record_audit(
            tenant_id=tenant_id,
            action="transaction.locked",
            actor_id=locked_by,
            resource_type=resource_type,
            resource_id=resource_id,
            payload_checksum=cs,
            correlation_id=correlation_id,
        )
        await publish_integration_event(
            FinancialSecurityTransactionLockedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                lock_id=str(lock.id),
                resource_type=resource_type,
                resource_id=resource_id,
            )
        )
        return Result.ok(lock.to_dict())

    async def release_lock(
        self,
        *,
        tenant_id: str,
        lock_id: str,
        actor_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        lock = await self._locks.find_by_id(lock_id)
        if not lock or lock.tenant_id != tenant_id or not lock.is_active:
            return Result.fail("financial_kernel.errors.lock_not_found")
        lock.release()
        await self._locks.save(lock)
        cs = checksum_payload({"lock_id": lock_id})
        await self._record_audit(
            tenant_id=tenant_id,
            action="transaction.unlocked",
            actor_id=actor_id,
            resource_type=lock.resource_type,
            resource_id=lock.resource_id,
            payload_checksum=cs,
            correlation_id=correlation_id,
        )
        return Result.ok(lock.to_dict())

    async def request_period_close(
        self,
        *,
        tenant_id: str,
        close_type: str,
        target_id: str,
        requester_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        try:
            CloseType(close_type)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_close_type")

        if close_type == CloseType.PERIOD.value:
            period = await self._periods.find_by_id(target_id)
            if not period or period.tenant_id != tenant_id:
                return Result.fail("financial_kernel.errors.period_not_found")
            if period.status == "closed":
                return Result.fail("financial_kernel.errors.period_already_closed")
        else:
            year = await self._years.find_by_id(target_id)
            if not year or year.tenant_id != tenant_id:
                return Result.fail("financial_kernel.errors.fiscal_year_not_found")
            if year.status == "closed":
                return Result.fail("financial_kernel.errors.fiscal_year_already_closed")

        request = PeriodCloseRequest.request(
            tenant_id=tenant_id,
            close_type=close_type,
            target_id=target_id,
            requester_id=requester_id,
            correlation_id=correlation_id,
        )
        await self._period_closes.save(request)
        cs = checksum_payload({"close_type": close_type, "target_id": target_id})
        await self._record_audit(
            tenant_id=tenant_id,
            action="period_close.requested",
            actor_id=requester_id,
            resource_type=close_type,
            resource_id=target_id,
            payload_checksum=cs,
            correlation_id=correlation_id,
        )
        return Result.ok(request.to_dict())

    async def approve_period_close(
        self,
        *,
        tenant_id: str,
        request_id: str,
        approver_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        request = await self._period_closes.find_by_id(request_id)
        if not request or request.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.request_not_found")

        try:
            request.approve(approver_id)
        except ValueError as exc:
            return Result.fail(f"financial_kernel.errors.{exc.args[0]}")

        if request.status == SecurityRequestStatus.APPROVED:
            if request.close_type == CloseType.PERIOD.value:
                period = await self._periods.find_by_id(request.target_id)
                if period:
                    period.close()
                    await self._periods.save(period)
            else:
                year = await self._years.find_by_id(request.target_id)
                if year:
                    year.status = "closed"
                    await self._years.save(year)
                    for period in await self._periods.list_by_tenant(tenant_id):
                        if period.fiscal_year_id == request.target_id and period.status == "open":
                            period.close()
                            await self._periods.save(period)

            await publish_integration_event(
                FinancialSecurityPeriodClosedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id,
                    close_type=request.close_type,
                    target_id=request.target_id,
                    closed_by=approver_id,
                )
            )

        await self._period_closes.save(request)
        cs = checksum_payload({"request_id": request_id, "status": request.status.value})
        await self._record_audit(
            tenant_id=tenant_id,
            action="period_close.approved",
            actor_id=approver_id,
            resource_type=request.close_type,
            resource_id=request.target_id,
            payload_checksum=cs,
            correlation_id=correlation_id,
            after_state={"status": request.status.value},
        )
        return Result.ok(request.to_dict())

    async def create_policy(
        self,
        *,
        tenant_id: str,
        name: str,
        policy_type: str,
        resource_type: str,
        rules: dict,
        actor_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        try:
            PolicyType(policy_type)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_policy_type")

        policy = SecurityPolicy.create(
            tenant_id=tenant_id,
            name=name,
            policy_type=policy_type,
            resource_type=resource_type,
            rules=rules,
        )
        await self._policies.save(policy)
        cs = checksum_payload(rules)
        await self._record_audit(
            tenant_id=tenant_id,
            action="policy.created",
            actor_id=actor_id,
            resource_type="security_policy",
            resource_id=str(policy.id),
            payload_checksum=cs,
            correlation_id=correlation_id,
            after_state=policy.to_dict(),
        )
        return Result.ok(policy.to_dict())

    async def evaluate_access(
        self,
        *,
        tenant_id: str,
        resource_type: str,
        permission: str,
        role: str = "",
        attributes: dict | None = None,
    ) -> Result[dict]:
        policies = await self._policies.find_for_resource(tenant_id, resource_type)
        if not policies:
            return Result.ok({"allowed": True, "reason": "no_policy_default_allow"})

        for policy in policies:
            if policy.policy_type == PolicyType.RBAC.value:
                allowed = evaluate_rbac_policy(rules=policy.rules, permission=permission, role=role)
            else:
                allowed = evaluate_abac_policy(rules=policy.rules, attributes=attributes or {})
            if not allowed:
                return Result.ok(
                    {
                        "allowed": False,
                        "policy_id": str(policy.id),
                        "policy_name": policy.name,
                        "policy_type": policy.policy_type,
                    }
                )
        return Result.ok({"allowed": True, "policies_evaluated": len(policies)})

    async def verify_tamper(
        self,
        *,
        tenant_id: str,
        audit_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        records = await self._audits.list_by_tenant(tenant_id)
        record = next((r for r in records if str(r.id) == audit_id), None)
        if not record:
            return Result.fail("financial_kernel.errors.audit_not_found")

        idx = records.index(record)
        previous = records[idx - 1].tamper_hash if idx > 0 else None
        valid = verify_tamper(
            tamper_hash=record.tamper_hash,
            action=record.action,
            actor_id=record.actor_id,
            resource_id=record.resource_id,
            payload_checksum=record.payload_checksum,
            previous_hash=previous,
        )
        if not valid:
            await publish_integration_event(
                FinancialSecurityTamperDetectedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id,
                    audit_id=audit_id,
                    resource_id=record.resource_id,
                )
            )
        return Result.ok({"valid": valid, "audit_id": audit_id, "tamper_hash": record.tamper_hash})

    async def list_audit_trail(
        self,
        tenant_id: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
    ) -> Result[list[dict]]:
        if resource_type and resource_id:
            records = await self._audits.list_by_resource(tenant_id, resource_type, resource_id)
        else:
            records = await self._audits.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in records])

    async def list_maker_checker_requests(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._maker_checker.list_by_tenant(tenant_id)
        return Result.ok([i.to_dict() for i in items])

    async def guarded_modification(
        self,
        *,
        tenant_id: str,
        resource_type: str,
        resource_id: str,
        actor_id: str,
        action: str,
        payload: dict,
        correlation_id: str = "",
    ) -> Result[dict]:
        """Enforce: never allow financial data modification without audit."""
        lock_check = await self._ensure_not_locked(tenant_id, resource_type, resource_id)
        if not lock_check.succeeded:
            return lock_check

        cs = checksum_payload(payload)
        record = await self._record_audit(
            tenant_id=tenant_id,
            action=action,
            actor_id=actor_id,
            resource_type=resource_type,
            resource_id=resource_id,
            payload_checksum=cs,
            correlation_id=correlation_id,
            after_state=payload,
        )
        return Result.ok({"audited": True, "audit_id": str(record.id), "checksum": cs})
