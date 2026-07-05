"""Enterprise Financial Audit application service."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.financial_audit import (
    FinancialAuditAction,
    FinancialAuditEntry,
)
from contexts.financial_kernel.domain.ports.financial_audit_repositories import (
    IFinancialAuditRepository,
)
from contexts.financial_kernel.domain.services.financial_audit_engine import (
    assert_deletion_forbidden,
    build_immutable_audit_report,
    checksum_payload,
    compute_audit_tamper_hash,
    list_audit_catalog,
    verify_audit_chain,
    verify_audit_tamper,
)
from shared.application.result import Result


class FinancialAuditApplicationService:
    def __init__(self, audits: IFinancialAuditRepository) -> None:
        self._audits = audits

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_audit_catalog())

    async def record(
        self,
        *,
        tenant_id: str,
        resource_type: str,
        resource_id: str,
        action: str,
        actor_id: str,
        correlation_id: str = "",
        organization_id: str | None = None,
        ip_address: str | None = None,
        device: str | None = None,
        reason: str = "",
        before_state: dict | None = None,
        after_state: dict | None = None,
    ) -> Result[dict]:
        payload = {
            "resource_type": resource_type,
            "resource_id": resource_id,
            "action": action,
            "after_state": after_state,
        }
        payload_checksum = checksum_payload(payload)
        previous = await self._audits.last_tamper_hash(tenant_id)
        tamper_hash = compute_audit_tamper_hash(
            action=action,
            actor_id=actor_id,
            resource_id=resource_id,
            payload_checksum=payload_checksum,
            previous_hash=previous,
        )
        entry = FinancialAuditEntry.record(
            tenant_id=tenant_id,
            organization_id=organization_id,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            actor_id=actor_id,
            correlation_id=correlation_id,
            payload_checksum=payload_checksum,
            tamper_hash=tamper_hash,
            ip_address=ip_address,
            device=device,
            reason=reason,
            before_state=before_state,
            after_state=after_state,
        )
        await self._audits.save(entry)
        return Result.ok(entry.to_dict())

    async def get_entry(self, tenant_id: str, entry_id: str) -> Result[dict]:
        entry = await self._audits.find_by_id(entry_id)
        if not entry or entry.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.audit_entry_not_found")
        return Result.ok(entry.to_dict())

    async def list_by_tenant(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._audits.list_by_tenant(tenant_id)
        return Result.ok([e.to_dict() for e in items])

    async def get_resource_history(
        self,
        tenant_id: str,
        resource_type: str,
        resource_id: str,
    ) -> Result[dict]:
        items = await self._audits.list_by_resource(tenant_id, resource_type, resource_id)
        entry_dicts = [e.to_dict() for e in items]
        chain_valid, _ = verify_audit_chain(entry_dicts)
        report = build_immutable_audit_report(
            resource_type=resource_type,
            resource_id=resource_id,
            entries=entry_dicts,
            chain_valid=chain_valid,
        )
        return Result.ok(report)

    async def verify_entry_tamper(self, tenant_id: str, entry_id: str) -> Result[dict]:
        entry = await self._audits.find_by_id(entry_id)
        if not entry or entry.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.audit_entry_not_found")
        items = await self._audits.list_by_tenant(tenant_id)
        sorted_items = sorted(items, key=lambda e: e.occurred_at)
        previous_hash: str | None = None
        for item in sorted_items:
            if str(item.id) == entry_id:
                valid = verify_audit_tamper(
                    tamper_hash=item.tamper_hash,
                    action=item.action,
                    actor_id=item.actor_id,
                    resource_id=item.resource_id,
                    payload_checksum=item.payload_checksum,
                    previous_hash=previous_hash,
                )
                return Result.ok({"valid": valid, "entry_id": entry_id})
            previous_hash = item.tamper_hash
        return Result.fail("financial_kernel.errors.audit_chain_incomplete")

    async def verify_chain(self, tenant_id: str) -> Result[dict]:
        items = await self._audits.list_by_tenant(tenant_id)
        entry_dicts = [e.to_dict() for e in items]
        valid, issues = verify_audit_chain(entry_dicts)
        return Result.ok(
            {
                "valid": valid,
                "entry_count": len(entry_dicts),
                "issues": issues,
            }
        )

    async def attempt_delete(self, entry_id: str) -> Result[None]:
        try:
            assert_deletion_forbidden()
        except PermissionError:
            return Result.fail("financial_kernel.errors.audit_deletion_forbidden")
        return Result.ok(None)

    async def record_journal_created(
        self,
        *,
        tenant_id: str,
        journal_id: str,
        actor_id: str,
        correlation_id: str,
        organization_id: str | None = None,
        after_state: dict | None = None,
        ip_address: str | None = None,
        device: str | None = None,
        reason: str = "",
    ) -> Result[dict]:
        return await self.record(
            tenant_id=tenant_id,
            resource_type="journal",
            resource_id=journal_id,
            action=FinancialAuditAction.CREATED.value,
            actor_id=actor_id,
            correlation_id=correlation_id,
            organization_id=organization_id,
            ip_address=ip_address,
            device=device,
            reason=reason,
            after_state=after_state,
        )

    async def record_journal_posted(
        self,
        *,
        tenant_id: str,
        journal_id: str,
        actor_id: str,
        correlation_id: str,
        organization_id: str | None = None,
        after_state: dict | None = None,
        ip_address: str | None = None,
        device: str | None = None,
        reason: str = "",
    ) -> Result[dict]:
        return await self.record(
            tenant_id=tenant_id,
            resource_type="journal",
            resource_id=journal_id,
            action=FinancialAuditAction.POSTED.value,
            actor_id=actor_id,
            correlation_id=correlation_id,
            organization_id=organization_id,
            ip_address=ip_address,
            device=device,
            reason=reason,
            after_state=after_state,
        )

    async def record_journal_approved(
        self,
        *,
        tenant_id: str,
        journal_id: str,
        actor_id: str,
        correlation_id: str,
        organization_id: str | None = None,
        reason: str = "",
        ip_address: str | None = None,
        device: str | None = None,
    ) -> Result[dict]:
        return await self.record(
            tenant_id=tenant_id,
            resource_type="journal",
            resource_id=journal_id,
            action=FinancialAuditAction.APPROVED.value,
            actor_id=actor_id,
            correlation_id=correlation_id,
            organization_id=organization_id,
            ip_address=ip_address,
            device=device,
            reason=reason,
        )

    async def record_journal_reversed(
        self,
        *,
        tenant_id: str,
        journal_id: str,
        actor_id: str,
        correlation_id: str,
        organization_id: str | None = None,
        reason: str = "",
        before_state: dict | None = None,
        after_state: dict | None = None,
        ip_address: str | None = None,
        device: str | None = None,
    ) -> Result[dict]:
        return await self.record(
            tenant_id=tenant_id,
            resource_type="journal",
            resource_id=journal_id,
            action=FinancialAuditAction.REVERSED.value,
            actor_id=actor_id,
            correlation_id=correlation_id,
            organization_id=organization_id,
            ip_address=ip_address,
            device=device,
            reason=reason,
            before_state=before_state,
            after_state=after_state,
        )
