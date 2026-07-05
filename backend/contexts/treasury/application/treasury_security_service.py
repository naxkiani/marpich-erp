"""Treasury Security application service."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.treasury_security_engine import (
    SecurityPolicyType,
    TreasuryAccessRule,
    TreasuryApprovalMatrix,
    TreasurySecurityAudit,
    TreasurySecurityLock,
    TreasurySecurityOperation,
    TreasurySecurityPolicy,
    TreasuryTransactionLimit,
)
from contexts.treasury.domain.events.integration_events import (
    TreasurySecurityAccessDeniedIntegration,
    TreasurySecurityFreezeActivatedIntegration,
    TreasurySecurityPolicyViolationIntegration,
)
from contexts.treasury.domain.ports.treasury_security_repositories import (
    IAccessRuleRepository,
    IApprovalMatrixRepository,
    ISecurityAuditRepository,
    ISecurityLockRepository,
    ISecurityOperationRepository,
    ISecurityPolicyRepository,
    ITransactionLimitRepository,
)
from contexts.treasury.domain.services.treasury_security_engine import (
    build_security_dashboard,
    build_security_policies_view,
    check_four_eyes,
    evaluate_operation_security,
    generate_digital_signature_hash,
    is_emergency_frozen,
    is_subject_locked,
    list_security_catalog,
    resolve_approval_matrix,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class TreasurySecurityApplicationService:
    def __init__(
        self,
        policies: ISecurityPolicyRepository,
        limits: ITransactionLimitRepository,
        matrix: IApprovalMatrixRepository,
        access_rules: IAccessRuleRepository,
        locks: ISecurityLockRepository,
        operations: ISecurityOperationRepository,
        audits: ISecurityAuditRepository,
    ) -> None:
        self._policies = policies
        self._limits = limits
        self._matrix = matrix
        self._access_rules = access_rules
        self._locks = locks
        self._operations = operations
        self._audits = audits

    async def _audit(
        self,
        *,
        tenant_id: str,
        action: str,
        actor_id: str | None = None,
        subject_ref: str = "",
        subject_type: str = "security",
        detail: str = "",
        sensitivity: str = "high",
    ) -> None:
        entry = TreasurySecurityAudit.create(
            tenant_id=tenant_id,
            action=action,
            actor_id=actor_id,
            subject_ref=subject_ref,
            subject_type=subject_type,
            detail=detail,
            sensitivity=sensitivity,
        )
        await self._audits.save(entry)

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_security_catalog())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        policies = await self._policies.list_by_tenant(tenant_id)
        limits = await self._limits.list_by_tenant(tenant_id)
        matrix = await self._matrix.list_by_tenant(tenant_id)
        operations = await self._operations.list_by_tenant(tenant_id)
        locks = await self._locks.list_by_tenant(tenant_id)
        audits = await self._audits.list_by_tenant(tenant_id)
        return Result.ok(
            build_security_dashboard(
                policies=[p.to_dict() for p in policies],
                limits=[l.to_dict() for l in limits],
                matrix=[m.to_dict() for m in matrix],
                operations=[o.to_dict() for o in operations],
                locks=[l.to_dict() for l in locks],
                audits=[a.to_dict() for a in audits],
            )
        )

    async def get_policies_view(self, tenant_id: str) -> Result[dict]:
        policies = await self._policies.list_by_tenant(tenant_id)
        return Result.ok(
            build_security_policies_view(policies=[p.to_dict() for p in policies])
        )

    async def list_policies(self, tenant_id: str) -> Result[list[dict]]:
        policies = await self._policies.list_by_tenant(tenant_id)
        return Result.ok([p.to_dict() for p in policies])

    async def create_policy(
        self,
        *,
        tenant_id: str,
        name: str,
        policy_type: str,
        rules: dict,
        description: str = "",
        actor_id: str | None = None,
    ) -> Result[dict]:
        try:
            SecurityPolicyType(policy_type)
        except ValueError:
            return Result.fail("treasury.errors.invalid_security_policy_type")

        policy = TreasurySecurityPolicy.create(
            tenant_id=tenant_id,
            name=name,
            policy_type=policy_type,
            rules=rules,
            description=description,
        )
        await self._policies.save(policy)
        await self._audit(
            tenant_id=tenant_id,
            action="policy_created",
            actor_id=actor_id,
            subject_ref=str(policy.id),
            subject_type="policy",
            detail=f"{policy_type}: {name}",
        )
        return Result.ok(policy.to_dict())

    async def list_limits(self, tenant_id: str) -> Result[list[dict]]:
        limits = await self._limits.list_by_tenant(tenant_id)
        return Result.ok([l.to_dict() for l in limits])

    async def create_limit(
        self,
        *,
        tenant_id: str,
        operation_type: str,
        name: str,
        max_amount: float,
        currency: str = "USD",
        daily_limit: float | None = None,
        actor_id: str | None = None,
    ) -> Result[dict]:
        limit = TreasuryTransactionLimit.create(
            tenant_id=tenant_id,
            operation_type=operation_type,
            name=name,
            max_amount=max_amount,
            currency=currency,
            daily_limit=daily_limit,
        )
        await self._limits.save(limit)
        await self._audit(
            tenant_id=tenant_id,
            action="limit_created",
            actor_id=actor_id,
            subject_ref=str(limit.id),
            subject_type="limit",
            detail=f"{operation_type} max {max_amount} {currency}",
        )
        return Result.ok(limit.to_dict())

    async def list_matrix(self, tenant_id: str) -> Result[list[dict]]:
        entries = await self._matrix.list_by_tenant(tenant_id)
        return Result.ok([m.to_dict() for m in entries])

    async def create_matrix_entry(
        self,
        *,
        tenant_id: str,
        operation_type: str,
        role: str,
        min_amount: float,
        max_amount: float,
        approval_level: int,
        currency: str = "USD",
        actor_id: str | None = None,
    ) -> Result[dict]:
        entry = TreasuryApprovalMatrix.create(
            tenant_id=tenant_id,
            operation_type=operation_type,
            role=role,
            min_amount=min_amount,
            max_amount=max_amount,
            approval_level=approval_level,
            currency=currency,
        )
        await self._matrix.save(entry)
        await self._audit(
            tenant_id=tenant_id,
            action="matrix_entry_created",
            actor_id=actor_id,
            subject_ref=str(entry.id),
            subject_type="approval_matrix",
            detail=f"{role} level {approval_level} for {operation_type}",
        )
        return Result.ok(entry.to_dict())

    async def list_access_rules(self, tenant_id: str) -> Result[list[dict]]:
        rules = await self._access_rules.list_by_tenant(tenant_id)
        return Result.ok([r.to_dict() for r in rules])

    async def create_access_rule(
        self,
        *,
        tenant_id: str,
        rule_type: str,
        name: str,
        roles: list[str] | None = None,
        attributes: dict | None = None,
        allowed_operations: list[str] | None = None,
        denied_operations: list[str] | None = None,
        actor_id: str | None = None,
    ) -> Result[dict]:
        if rule_type not in {"rbac", "abac"}:
            return Result.fail("treasury.errors.invalid_access_rule_type")

        rule = TreasuryAccessRule.create(
            tenant_id=tenant_id,
            rule_type=rule_type,
            name=name,
            roles=roles,
            attributes=attributes,
            allowed_operations=allowed_operations,
            denied_operations=denied_operations,
        )
        await self._access_rules.save(rule)
        await self._audit(
            tenant_id=tenant_id,
            action="access_rule_created",
            actor_id=actor_id,
            subject_ref=str(rule.id),
            subject_type="access_rule",
            detail=f"{rule_type}: {name}",
        )
        return Result.ok(rule.to_dict())

    async def evaluate_access(
        self,
        *,
        tenant_id: str,
        maker_id: str,
        checker_id: str | None,
        roles: list[str],
        attributes: dict,
        operation_type: str,
        amount: float,
        risk_score: float = 0.0,
        device_verified: bool = False,
        actor_id: str | None = None,
    ) -> Result[dict]:
        policies = await self._policies.list_by_tenant(tenant_id)
        limits = await self._limits.list_by_tenant(tenant_id)
        matrix = await self._matrix.list_by_tenant(tenant_id)
        access_rules = await self._access_rules.list_by_tenant(tenant_id)
        locks = await self._locks.list_by_tenant(tenant_id)

        result = evaluate_operation_security(
            maker_id=maker_id,
            checker_id=checker_id,
            roles=roles,
            attributes=attributes,
            operation_type=operation_type,
            amount=amount,
            risk_score=risk_score,
            device_verified=device_verified,
            policies=[p.to_dict() for p in policies],
            limits=[l.to_dict() for l in limits],
            matrix=[m.to_dict() for m in matrix],
            access_rules=[r.to_dict() for r in access_rules],
            locks=[l.to_dict() for l in locks],
            tenant_id=tenant_id,
        )

        await self._audit(
            tenant_id=tenant_id,
            action="access_evaluated",
            actor_id=actor_id or maker_id,
            subject_ref=operation_type,
            subject_type="evaluation",
            detail=f"allowed={result.get('allowed')} reason={result.get('reason', 'ok')}",
        )

        if not result.get("allowed"):
            await publish_integration_event(
                TreasurySecurityAccessDeniedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=f"security-eval-{tenant_id}",
                    operation_type=operation_type,
                    reason=result.get("reason", "denied"),
                    actor_id=actor_id or maker_id,
                )
            )

        return Result.ok(result)

    async def create_operation(
        self,
        *,
        tenant_id: str,
        operation_type: str,
        subject_ref: str,
        amount: float,
        currency: str,
        maker_id: str,
        roles: list[str],
        attributes: dict,
        risk_score: float = 0.0,
        device_verified: bool = False,
    ) -> Result[dict]:
        eval_result = await self.evaluate_access(
            tenant_id=tenant_id,
            maker_id=maker_id,
            checker_id=None,
            roles=roles,
            attributes=attributes,
            operation_type=operation_type,
            amount=amount,
            risk_score=risk_score,
            device_verified=device_verified,
            actor_id=maker_id,
        )
        if not eval_result.succeeded:
            return eval_result
        if not eval_result.unwrap().get("allowed"):
            reason = eval_result.unwrap().get("reason", "access_denied")
            await publish_integration_event(
                TreasurySecurityPolicyViolationIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=f"security-violation-{tenant_id}",
                    operation_type=operation_type,
                    violation_type=reason,
                    actor_id=maker_id,
                )
            )
            return Result.fail(f"treasury.errors.{reason}")

        matrix = await self._matrix.list_by_tenant(tenant_id)
        matrix_result = resolve_approval_matrix(
            amount=amount,
            operation_type=operation_type,
            matrix=[m.to_dict() for m in matrix],
        )
        required = max(matrix_result.get("approval_level", 1), 2)

        operation = TreasurySecurityOperation.create(
            tenant_id=tenant_id,
            operation_type=operation_type,
            subject_ref=subject_ref,
            amount=amount,
            currency=currency,
            maker_id=maker_id,
            required_approvers=required,
            risk_score=risk_score,
            device_verified=device_verified,
        )
        await self._operations.save(operation)
        await self._audit(
            tenant_id=tenant_id,
            action="operation_created",
            actor_id=maker_id,
            subject_ref=str(operation.id),
            subject_type="operation",
            detail=f"{operation_type} {amount} {currency}",
        )
        return Result.ok(operation.to_dict())

    async def submit_operation(
        self, operation_id: str, *, tenant_id: str, actor_id: str
    ) -> Result[dict]:
        operation = await self._operations.find_by_id(operation_id)
        if not operation or operation.tenant_id != tenant_id:
            return Result.fail("treasury.errors.security_operation_not_found")

        try:
            operation.submit_for_checker()
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        await self._operations.save(operation)
        await self._audit(
            tenant_id=tenant_id,
            action="operation_submitted",
            actor_id=actor_id,
            subject_ref=operation_id,
            subject_type="operation",
        )
        return Result.ok(operation.to_dict())

    async def approve_operation(
        self,
        operation_id: str,
        *,
        tenant_id: str,
        checker_id: str,
        with_signature: bool = True,
    ) -> Result[dict]:
        operation = await self._operations.find_by_id(operation_id)
        if not operation or operation.tenant_id != tenant_id:
            return Result.fail("treasury.errors.security_operation_not_found")

        signature_hash = None
        if with_signature:
            signature_hash = generate_digital_signature_hash(
                operation_id=operation_id, approver_id=checker_id
            )

        try:
            operation.approve_by_checker(
                checker_id=checker_id, signature_hash=signature_hash
            )
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        await self._operations.save(operation)
        await self._audit(
            tenant_id=tenant_id,
            action="operation_approved",
            actor_id=checker_id,
            subject_ref=operation_id,
            subject_type="operation",
            detail=f"checker={checker_id}",
        )

        if operation.status == "approved":
            four_eyes = check_four_eyes(
                approvers=[
                    a["approver_id"]
                    for a in operation.approvers
                    if "approver_id" in a
                ],
                required=operation.required_approvers,
            )
            if not four_eyes["valid"]:
                return Result.fail("treasury.errors.insufficient_approvers")

        return Result.ok(operation.to_dict())

    async def reject_operation(
        self,
        operation_id: str,
        *,
        tenant_id: str,
        checker_id: str,
        reason: str = "",
    ) -> Result[dict]:
        operation = await self._operations.find_by_id(operation_id)
        if not operation or operation.tenant_id != tenant_id:
            return Result.fail("treasury.errors.security_operation_not_found")

        try:
            operation.reject(checker_id=checker_id, reason=reason)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        await self._operations.save(operation)
        await self._audit(
            tenant_id=tenant_id,
            action="operation_rejected",
            actor_id=checker_id,
            subject_ref=operation_id,
            subject_type="operation",
            detail=reason,
        )
        return Result.ok(operation.to_dict())

    async def lock_transaction(
        self,
        *,
        tenant_id: str,
        subject_ref: str,
        subject_type: str,
        reason: str,
        locked_by: str,
    ) -> Result[dict]:
        lock = TreasurySecurityLock.create(
            tenant_id=tenant_id,
            lock_type="transaction_lock",
            subject_ref=subject_ref,
            subject_type=subject_type,
            reason=reason,
            locked_by=locked_by,
        )
        await self._locks.save(lock)
        await self._audit(
            tenant_id=tenant_id,
            action="transaction_locked",
            actor_id=locked_by,
            subject_ref=subject_ref,
            subject_type=subject_type,
            detail=reason,
        )
        return Result.ok(lock.to_dict())

    async def release_lock(
        self, lock_id: str, *, tenant_id: str, released_by: str
    ) -> Result[dict]:
        lock = await self._locks.find_by_id(lock_id)
        if not lock or lock.tenant_id != tenant_id:
            return Result.fail("treasury.errors.security_lock_not_found")

        try:
            lock.release(released_by=released_by)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        await self._locks.save(lock)
        await self._audit(
            tenant_id=tenant_id,
            action="lock_released",
            actor_id=released_by,
            subject_ref=lock.subject_ref,
            subject_type=lock.subject_type,
            detail=lock.reason,
        )
        return Result.ok(lock.to_dict())

    async def emergency_freeze(
        self, *, tenant_id: str, reason: str, locked_by: str
    ) -> Result[dict]:
        locks = await self._locks.list_by_tenant(tenant_id)
        if is_emergency_frozen(locks=[l.to_dict() for l in locks], tenant_id=tenant_id):
            return Result.fail("treasury.errors.emergency_freeze_already_active")

        lock = TreasurySecurityLock.create(
            tenant_id=tenant_id,
            lock_type="emergency_freeze",
            subject_ref=tenant_id,
            subject_type="tenant",
            reason=reason,
            locked_by=locked_by,
        )
        await self._locks.save(lock)
        await self._audit(
            tenant_id=tenant_id,
            action="emergency_freeze_activated",
            actor_id=locked_by,
            subject_ref=tenant_id,
            subject_type="tenant",
            detail=reason,
            sensitivity="critical",
        )
        await publish_integration_event(
            TreasurySecurityFreezeActivatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"security-freeze-{tenant_id}",
                reason=reason,
                activated_by=locked_by,
            )
        )
        return Result.ok(lock.to_dict())

    async def release_emergency_freeze(
        self, lock_id: str, *, tenant_id: str, released_by: str
    ) -> Result[dict]:
        return await self.release_lock(lock_id, tenant_id=tenant_id, released_by=released_by)

    async def list_locks(self, tenant_id: str) -> Result[list[dict]]:
        locks = await self._locks.list_by_tenant(tenant_id)
        return Result.ok([l.to_dict() for l in locks if l.is_active])

    async def list_operations(self, tenant_id: str) -> Result[list[dict]]:
        operations = await self._operations.list_by_tenant(tenant_id)
        return Result.ok(
            [o.to_dict() for o in sorted(operations, key=lambda x: x.created_at, reverse=True)]
        )

    async def get_operation(self, operation_id: str) -> Result[dict]:
        operation = await self._operations.find_by_id(operation_id)
        if not operation:
            return Result.fail("treasury.errors.security_operation_not_found")
        return Result.ok(operation.to_dict())

    async def get_audit_trail(
        self, tenant_id: str, *, subject_ref: str | None = None
    ) -> Result[list[dict]]:
        if subject_ref:
            entries = await self._audits.list_by_subject(subject_ref)
        else:
            entries = await self._audits.list_by_tenant(tenant_id)
        return Result.ok([e.to_dict() for e in entries])

    async def check_subject_locked(self, tenant_id: str, subject_ref: str) -> Result[dict]:
        locks = await self._locks.list_by_tenant(tenant_id)
        locked = is_subject_locked(
            locks=[l.to_dict() for l in locks], subject_ref=subject_ref
        )
        frozen = is_emergency_frozen(
            locks=[l.to_dict() for l in locks], tenant_id=tenant_id
        )
        return Result.ok({"locked": locked, "emergency_frozen": frozen})

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        if await self._policies.list_by_tenant(tenant_id):
            return

        policy_defaults = [
            (
                SecurityPolicyType.MAKER_CHECKER.value,
                "Maker-Checker Control",
                {"enforce": True, "same_user_blocked": True},
            ),
            (
                SecurityPolicyType.FOUR_EYES.value,
                "Four Eyes Principle",
                {"minimum_approvers": 2},
            ),
            (
                SecurityPolicyType.SEGREGATION_OF_DUTIES.value,
                "Segregation of Duties",
                {"conflict_matrix": "default"},
            ),
            (
                SecurityPolicyType.DIGITAL_SIGNATURE.value,
                "Digital Signature on Approval",
                {"algorithm": "sha256", "required_on_approval": True},
            ),
            (
                SecurityPolicyType.DEVICE_VERIFICATION.value,
                "Trusted Device Verification",
                {"required_for_amount_above": 10000},
            ),
            (
                SecurityPolicyType.RISK_BASED_AUTH.value,
                "Risk-Based Authentication",
                {"risk_threshold": 70, "step_up_required": True},
            ),
            (
                SecurityPolicyType.EMERGENCY_FREEZE.value,
                "Emergency Freeze Capability",
                {"scope": "tenant", "requires_admin": True},
            ),
        ]
        for ptype, name, rules in policy_defaults:
            policy = TreasurySecurityPolicy.create(
                tenant_id=tenant_id,
                name=name,
                policy_type=ptype,
                rules=rules,
            )
            await self._policies.save(policy)

        limit_defaults = [
            ("transfer", "Transfer Daily Limit", 100000, 250000),
            ("payment", "Payment Single Limit", 50000, None),
            ("investment", "Investment Limit", 500000, None),
            ("cash_movement", "Cash Movement Limit", 25000, 100000),
        ]
        for op_type, name, max_amt, daily in limit_defaults:
            limit = TreasuryTransactionLimit.create(
                tenant_id=tenant_id,
                operation_type=op_type,
                name=name,
                max_amount=max_amt,
                daily_limit=daily,
            )
            await self._limits.save(limit)

        matrix_defaults = [
            ("transfer", "treasury_officer", 0, 10000, 1),
            ("transfer", "treasury_manager", 10000, 100000, 2),
            ("transfer", "cfo", 100000, 999999999, 3),
            ("payment", "treasury_officer", 0, 25000, 1),
            ("payment", "treasury_manager", 25000, 999999999, 2),
            ("investment", "treasury_manager", 0, 999999999, 2),
        ]
        for op_type, role, min_amt, max_amt, level in matrix_defaults:
            entry = TreasuryApprovalMatrix.create(
                tenant_id=tenant_id,
                operation_type=op_type,
                role=role,
                min_amount=min_amt,
                max_amount=max_amt,
                approval_level=level,
            )
            await self._matrix.save(entry)

        rbac_rule = TreasuryAccessRule.create(
            tenant_id=tenant_id,
            rule_type="rbac",
            name="Treasury Officer Access",
            roles=["treasury_officer", "treasury_manager", "cfo"],
            allowed_operations=["transfer", "payment", "investment", "cash_movement"],
        )
        await self._access_rules.save(rbac_rule)

        abac_rule = TreasuryAccessRule.create(
            tenant_id=tenant_id,
            rule_type="abac",
            name="Business Hours Restriction",
            attributes={"business_hours": True},
            allowed_operations=["transfer", "payment"],
            denied_operations=["emergency_freeze"],
        )
        await self._access_rules.save(abac_rule)
