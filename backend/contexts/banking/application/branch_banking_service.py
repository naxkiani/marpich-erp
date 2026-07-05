"""Branch Banking Platform application service."""
from __future__ import annotations

from contexts.banking.domain.aggregates.branch_banking_engine import (
    BranchCashLimit,
    BranchDaySession,
    BranchEmployeeAssignment,
    BranchExtension,
    BranchKPIRecord,
    BranchOffice,
    BranchOfficeType,
    BranchVault,
    BranchVaultMovement,
    VaultMovementType,
)
from contexts.banking.domain.events.branch_banking_integration_events import (
    BankingBranchClosedIntegration,
    BankingBranchKPIRecordedIntegration,
    BankingBranchOpenedIntegration,
    BankingVaultMovementIntegration,
)
from contexts.banking.domain.ports.branch_banking_repositories import (
    IBranchAuditRepository,
    IBranchCashLimitRepository,
    IBranchDaySessionRepository,
    IBranchEmployeeAssignmentRepository,
    IBranchExtensionRepository,
    IBranchKPIRepository,
    IBranchOfficeRepository,
    IBranchVaultMovementRepository,
    IBranchVaultRepository,
)
from contexts.banking.domain.services.branch_banking_engine import (
    build_branch_analytics,
    build_branch_dashboard,
    list_branch_catalog,
    list_branch_policy_keys,
    validate_office_hierarchy,
)
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BankingBranchPlatformApplicationService:
    def __init__(
        self,
        offices: IBranchOfficeRepository,
        extensions: IBranchExtensionRepository,
        sessions: IBranchDaySessionRepository,
        vaults: IBranchVaultRepository,
        vault_movements: IBranchVaultMovementRepository,
        cash_limits: IBranchCashLimitRepository,
        assignments: IBranchEmployeeAssignmentRepository,
        kpis: IBranchKPIRepository,
        audits: IBranchAuditRepository,
        policy: IPolicyEvaluator,
    ) -> None:
        self._offices = offices
        self._extensions = extensions
        self._sessions = sessions
        self._vaults = vaults
        self._vault_movements = vault_movements
        self._cash_limits = cash_limits
        self._assignments = assignments
        self._kpis = kpis
        self._audits = audits
        self._policy = policy

    async def _audit(
        self, *, tenant_id: str, office_id: str, action: str, actor_id: str | None = None, detail: str = ""
    ) -> None:
        from contexts.banking.domain.aggregates.branch_banking_engine import BranchAuditEntry

        await self._audits.save(
            BranchAuditEntry.create(
                tenant_id=tenant_id, office_id=office_id, action=action, actor_id=actor_id, detail=detail
            )
        )

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_branch_catalog())

    async def list_policy_keys(self) -> Result[list[dict]]:
        return Result.ok(list_branch_policy_keys())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        offices = await self._offices.list_by_tenant(tenant_id)
        extensions = await self._extensions.list_by_tenant(tenant_id)
        vaults = await self._vaults.list_by_tenant(tenant_id)
        assignments = await self._assignments.list_by_tenant(tenant_id)
        kpis = await self._kpis.list_by_tenant(tenant_id)
        sessions = await self._sessions.list_by_tenant(tenant_id)
        return Result.ok(
            build_branch_dashboard(
                offices=[o.to_dict() for o in offices],
                extensions=[e.to_dict() for e in extensions],
                vaults=[v.to_dict() for v in vaults],
                assignments=[a.to_dict() for a in assignments],
                kpis=[k.to_dict() for k in kpis],
                sessions=[s.to_dict() for s in sessions],
            )
        )

    async def get_analytics(self, tenant_id: str) -> Result[dict]:
        offices = await self._offices.list_by_tenant(tenant_id)
        kpis = await self._kpis.list_by_tenant(tenant_id)
        vaults = await self._vaults.list_by_tenant(tenant_id)
        sessions = await self._sessions.list_by_tenant(tenant_id)
        return Result.ok(
            build_branch_analytics(
                offices=[o.to_dict() for o in offices],
                kpis=[k.to_dict() for k in kpis],
                vaults=[v.to_dict() for v in vaults],
                sessions=[s.to_dict() for s in sessions],
            )
        )

    async def create_office(
        self,
        *,
        tenant_id: str,
        office_type: str,
        name: str,
        code: str,
        parent_office_id: str | None = None,
        region: str = "",
        address: str = "",
        currency: str = "USD",
    ) -> Result[dict]:
        if office_type not in {t.value for t in BranchOfficeType}:
            return Result.fail("banking.errors.invalid_office_type")

        existing = await self._offices.find_by_code(tenant_id, code)
        if existing:
            return Result.fail("banking.errors.office_code_exists")

        parent_type = None
        if parent_office_id:
            parent = await self._offices.find_by_id(parent_office_id)
            if not parent or parent.tenant_id != tenant_id:
                return Result.fail("banking.errors.parent_office_not_found")
            parent_type = parent.office_type

        if not validate_office_hierarchy(office_type=office_type, parent_type=parent_type):
            return Result.fail("banking.errors.invalid_office_hierarchy")

        ref = self._offices.next_office_ref(tenant_id)
        office = BranchOffice.create(
            tenant_id=tenant_id,
            office_ref=ref,
            office_type=office_type,
            name=name,
            code=code,
            parent_office_id=parent_office_id,
            region=region,
            address=address,
            currency=currency,
        )
        await self._offices.save(office)

        vault_ref = self._vaults.next_vault_ref(tenant_id)
        vault_limit_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="branch.vault.limit",
            facts={"office_type": office_type},
        )
        vault_limit = float(vault_limit_policy.parameters.get("max_balance", 500000))
        vault = BranchVault.create(
            tenant_id=tenant_id,
            office_id=str(office.id),
            vault_ref=vault_ref,
            currency=currency,
            limit_amount=vault_limit,
        )
        await self._vaults.save(vault)
        await self._audit(
            tenant_id=tenant_id,
            office_id=str(office.id),
            action="office.created",
            detail=ref,
        )
        return Result.ok({**office.to_dict(), "vault": vault.to_dict()})

    async def list_offices(self, tenant_id: str) -> Result[list[dict]]:
        offices = await self._offices.list_by_tenant(tenant_id)
        return Result.ok([o.to_dict() for o in offices])

    async def get_office(self, *, office_id: str) -> Result[dict]:
        office = await self._offices.find_by_id(office_id)
        if not office:
            return Result.fail("banking.errors.office_not_found")
        extensions = await self._extensions.list_by_office(office_id)
        vault = await self._vaults.find_by_office(office_id)
        return Result.ok(
            {
                **office.to_dict(),
                "extensions": [e.to_dict() for e in extensions],
                "vault": vault.to_dict() if vault else None,
            }
        )

    async def add_extension(
        self,
        *,
        office_id: str,
        extension_type: str,
        label: str,
        terminal_id: str = "",
    ) -> Result[dict]:
        office = await self._offices.find_by_id(office_id)
        if not office:
            return Result.fail("banking.errors.office_not_found")

        ref = self._extensions.next_extension_ref(office.tenant_id)
        extension = BranchExtension.create(
            tenant_id=office.tenant_id,
            office_id=office_id,
            extension_ref=ref,
            extension_type=extension_type,
            label=label,
            terminal_id=terminal_id,
        )
        await self._extensions.save(extension)
        await self._audit(
            tenant_id=office.tenant_id,
            office_id=office_id,
            action="extension.added",
            detail=f"{extension_type}:{ref}",
        )
        return Result.ok(extension.to_dict())

    async def open_branch(
        self,
        *,
        office_id: str,
        operator_id: str,
        opening_balance: float = 0.0,
        notes: str = "",
    ) -> Result[dict]:
        office = await self._offices.find_by_id(office_id)
        if not office:
            return Result.fail("banking.errors.office_not_found")

        policy = await self._policy.evaluate(
            tenant_id=office.tenant_id,
            domain="bank",
            policy_key="branch.opening.checklist",
            facts={"office_id": office_id, "office_type": office.office_type},
        )
        if policy.outcome == "deny":
            return Result.fail("banking.errors.branch_opening_denied")

        try:
            office.open_branch()
        except ValueError:
            return Result.fail("banking.errors.branch_already_open")

        session_ref = self._sessions.next_session_ref(office.tenant_id)
        session = BranchDaySession.create(
            tenant_id=office.tenant_id,
            office_id=office_id,
            session_ref=session_ref,
            session_type="opening",
            opening_balance=opening_balance,
            operator_id=operator_id,
            notes=notes,
        )
        await self._sessions.save(session)
        await self._offices.save(office)
        await publish_integration_event(
            BankingBranchOpenedIntegration(
                tenant_id=TenantId.create(office.tenant_id),
                correlation_id=f"branch-open-{office.id}",
                office_id=office_id,
                office_ref=office.office_ref,
                office_type=office.office_type,
                operator_id=operator_id,
            )
        )
        await self._audit(
            tenant_id=office.tenant_id,
            office_id=office_id,
            action="branch.opened",
            actor_id=operator_id,
            detail=session_ref,
        )
        return Result.ok({**office.to_dict(), "session": session.to_dict()})

    async def close_branch(
        self,
        *,
        office_id: str,
        operator_id: str,
        closing_balance: float = 0.0,
        notes: str = "",
    ) -> Result[dict]:
        office = await self._offices.find_by_id(office_id)
        if not office:
            return Result.fail("banking.errors.office_not_found")

        policy = await self._policy.evaluate(
            tenant_id=office.tenant_id,
            domain="bank",
            policy_key="branch.closing.checklist",
            facts={"office_id": office_id},
        )
        if policy.outcome == "deny":
            return Result.fail("banking.errors.branch_closing_denied")

        try:
            office.close_branch()
        except ValueError:
            return Result.fail("banking.errors.branch_not_open")

        session_ref = self._sessions.next_session_ref(office.tenant_id)
        session = BranchDaySession.create(
            tenant_id=office.tenant_id,
            office_id=office_id,
            session_ref=session_ref,
            session_type="closing",
            closing_balance=closing_balance,
            operator_id=operator_id,
            notes=notes,
        )
        await self._sessions.save(session)
        await self._offices.save(office)
        await publish_integration_event(
            BankingBranchClosedIntegration(
                tenant_id=TenantId.create(office.tenant_id),
                correlation_id=f"branch-close-{office.id}",
                office_id=office_id,
                office_ref=office.office_ref,
                closing_balance=closing_balance,
                operator_id=operator_id,
            )
        )
        await self._audit(
            tenant_id=office.tenant_id,
            office_id=office_id,
            action="branch.closed",
            actor_id=operator_id,
            detail=session_ref,
        )
        return Result.ok({**office.to_dict(), "session": session.to_dict()})

    async def vault_movement(
        self,
        *,
        office_id: str,
        movement_type: str,
        amount: float,
        operator_id: str = "",
        narrative: str = "",
    ) -> Result[dict]:
        office = await self._offices.find_by_id(office_id)
        if not office:
            return Result.fail("banking.errors.office_not_found")
        vault = await self._vaults.find_by_office(office_id)
        if not vault:
            return Result.fail("banking.errors.vault_not_found")

        try:
            if movement_type in {VaultMovementType.DEPOSIT.value, VaultMovementType.TRANSFER_FROM_DRAWER.value}:
                vault.deposit(amount)
            elif movement_type in {VaultMovementType.WITHDRAWAL.value, VaultMovementType.TRANSFER_TO_DRAWER.value}:
                vault.withdraw(amount)
            else:
                return Result.fail("banking.errors.invalid_vault_movement")
        except ValueError as exc:
            return Result.fail(f"banking.errors.{str(exc)}")

        ref = self._vault_movements.next_movement_ref(office.tenant_id)
        movement = BranchVaultMovement.create(
            tenant_id=office.tenant_id,
            vault_id=str(vault.id),
            office_id=office_id,
            movement_ref=ref,
            movement_type=movement_type,
            amount=amount,
            currency=vault.currency,
            operator_id=operator_id,
            narrative=narrative,
        )
        await self._vault_movements.save(movement)
        await self._vaults.save(vault)
        await publish_integration_event(
            BankingVaultMovementIntegration(
                tenant_id=TenantId.create(office.tenant_id),
                correlation_id=f"vault-{movement.id}",
                vault_id=str(vault.id),
                office_id=office_id,
                movement_type=movement_type,
                amount=amount,
                currency=vault.currency,
            )
        )
        await self._audit(
            tenant_id=office.tenant_id,
            office_id=office_id,
            action="vault.movement",
            actor_id=operator_id,
            detail=f"{movement_type}:{amount}",
        )
        return Result.ok({**vault.to_dict(), "movement": movement.to_dict()})

    async def set_cash_limit(
        self,
        *,
        tenant_id: str,
        office_id: str,
        limit_type: str,
        max_amount: float,
        currency: str = "USD",
        extension_id: str | None = None,
    ) -> Result[dict]:
        office = await self._offices.find_by_id(office_id)
        if not office or office.tenant_id != tenant_id:
            return Result.fail("banking.errors.office_not_found")

        policy_key = "branch.cash.counter.limit" if extension_id else "branch.cash.drawer.limit"
        policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key=policy_key,
            facts={"office_id": office_id, "max_amount": max_amount},
        )
        cap = float(policy.parameters.get("max_drawer_balance", policy.parameters.get("max_amount", max_amount)))
        if cap > 0 and max_amount > cap:
            max_amount = cap

        ref = self._cash_limits.next_limit_ref(tenant_id)
        limit = BranchCashLimit.create(
            tenant_id=tenant_id,
            office_id=office_id,
            limit_ref=ref,
            limit_type=limit_type,
            max_amount=max_amount,
            currency=currency,
            extension_id=extension_id,
        )
        await self._cash_limits.save(limit)
        await self._audit(
            tenant_id=tenant_id,
            office_id=office_id,
            action="cash_limit.set",
            detail=ref,
        )
        return Result.ok(limit.to_dict())

    async def list_cash_limits(self, *, office_id: str) -> Result[list[dict]]:
        limits = await self._cash_limits.list_by_office(office_id)
        return Result.ok([l.to_dict() for l in limits])

    async def assign_employee(
        self,
        *,
        tenant_id: str,
        office_id: str,
        employee_id: str,
        role: str,
        extension_id: str | None = None,
    ) -> Result[dict]:
        office = await self._offices.find_by_id(office_id)
        if not office or office.tenant_id != tenant_id:
            return Result.fail("banking.errors.office_not_found")

        existing = await self._assignments.list_by_office(office_id)
        active_count = sum(1 for a in existing if a.active)
        policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="branch.employee.max_assignments",
            facts={"office_id": office_id, "active_count": active_count},
        )
        max_assignments = int(policy.parameters.get("max_assignments", 50))
        if active_count >= max_assignments:
            return Result.fail("banking.errors.max_assignments_reached")

        ref = self._assignments.next_assignment_ref(tenant_id)
        assignment = BranchEmployeeAssignment.create(
            tenant_id=tenant_id,
            office_id=office_id,
            assignment_ref=ref,
            employee_id=employee_id,
            role=role,
            extension_id=extension_id,
        )
        await self._assignments.save(assignment)
        await self._audit(
            tenant_id=tenant_id,
            office_id=office_id,
            action="employee.assigned",
            detail=f"{employee_id}:{role}",
        )
        return Result.ok(assignment.to_dict())

    async def list_assignments(self, *, office_id: str) -> Result[list[dict]]:
        assignments = await self._assignments.list_by_office(office_id)
        return Result.ok([a.to_dict() for a in assignments])

    async def record_kpi(
        self,
        *,
        tenant_id: str,
        office_id: str,
        metric_key: str,
        metric_value: float,
        target_value: float = 0.0,
        period: str = "daily",
    ) -> Result[dict]:
        office = await self._offices.find_by_id(office_id)
        if not office or office.tenant_id != tenant_id:
            return Result.fail("banking.errors.office_not_found")

        if target_value <= 0:
            policy = await self._policy.evaluate(
                tenant_id=tenant_id,
                domain="bank",
                policy_key="branch.kpi.targets",
                facts={"metric_key": metric_key, "office_type": office.office_type},
            )
            target_value = float(policy.parameters.get(metric_key, policy.parameters.get("default_target", 100)))

        ref = self._kpis.next_kpi_ref(tenant_id)
        kpi = BranchKPIRecord.create(
            tenant_id=tenant_id,
            office_id=office_id,
            kpi_ref=ref,
            metric_key=metric_key,
            metric_value=metric_value,
            target_value=target_value,
            period=period,
        )
        await self._kpis.save(kpi)
        await publish_integration_event(
            BankingBranchKPIRecordedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"kpi-{kpi.id}",
                office_id=office_id,
                metric_key=metric_key,
                metric_value=metric_value,
                target_value=target_value,
            )
        )
        await self._audit(
            tenant_id=tenant_id,
            office_id=office_id,
            action="kpi.recorded",
            detail=f"{metric_key}={metric_value}",
        )
        return Result.ok(kpi.to_dict())

    async def list_kpis(self, *, office_id: str) -> Result[list[dict]]:
        kpis = await self._kpis.list_by_office(office_id)
        return Result.ok([k.to_dict() for k in kpis])

    async def get_office_audit(self, *, office_id: str) -> Result[list[dict]]:
        office = await self._offices.find_by_id(office_id)
        if not office:
            return Result.fail("banking.errors.office_not_found")
        entries = await self._audits.list_by_office(office_id)
        return Result.ok([e.to_dict() for e in entries])

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = str(envelope.get("tenant_id", ""))
        if not tenant_id:
            return
        existing = await self._offices.find_by_code(tenant_id, "HO-001")
        if existing:
            return
        await self.create_office(
            tenant_id=tenant_id,
            office_type=BranchOfficeType.HEAD_OFFICE.value,
            name="Head Office",
            code="HO-001",
            region="central",
        )
