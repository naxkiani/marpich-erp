"""Enterprise Bank Account Management application service."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.bank_account import (
    AuthorizedSignatory,
    Bank,
    BankAccount,
    BankAccountDocument,
    BankBranch,
)
from contexts.treasury.domain.events.integration_events import (
    BankAccountActivatedIntegration,
    BankAccountApprovalRequestedIntegration,
)
from contexts.treasury.domain.ports.bank_account_repositories import (
    IBankAccountDocumentRepository,
    IBankAccountRepository,
    IBankBranchRepository,
    IBankRepository,
    ISignatoryRepository,
)
from contexts.treasury.domain.services.bank_account_engine import (
    assert_account_type,
    list_bank_account_catalog,
    validate_account_identifiers,
    validate_swift,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BankAccountApplicationService:
    def __init__(
        self,
        banks: IBankRepository,
        branches: IBankBranchRepository,
        accounts: IBankAccountRepository,
        signatories: ISignatoryRepository,
        documents: IBankAccountDocumentRepository,
    ) -> None:
        self._banks = banks
        self._branches = branches
        self._accounts = accounts
        self._signatories = signatories
        self._documents = documents

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_bank_account_catalog())

    async def create_bank(
        self,
        *,
        tenant_id: str,
        code: str,
        name: str,
        country: str = "US",
        organization_id: str | None = None,
        swift_bic: str | None = None,
    ) -> Result[dict]:
        if await self._banks.find_by_code(tenant_id, code):
            return Result.fail("treasury.errors.bank_exists")
        ok, err = validate_swift(swift_bic)
        if not ok:
            return Result.fail(f"treasury.errors.{err}")
        bank = Bank.create(
            tenant_id=tenant_id,
            code=code,
            name=name,
            country=country,
            organization_id=organization_id,
            swift_bic=swift_bic,
        )
        await self._banks.save(bank)
        return Result.ok(bank.to_dict())

    async def list_banks(
        self, tenant_id: str, organization_id: str | None = None
    ) -> Result[list[dict]]:
        banks = await self._banks.list_by_tenant(tenant_id, organization_id)
        return Result.ok([b.to_dict() for b in banks])

    async def get_bank(self, tenant_id: str, bank_id: str) -> Result[dict]:
        bank = await self._banks.find_by_id(bank_id)
        if not bank or bank.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_not_found")
        return Result.ok(bank.to_dict())

    async def create_branch(
        self,
        *,
        tenant_id: str,
        bank_id: str,
        code: str,
        name: str,
        organization_id: str | None = None,
        address: str | None = None,
        routing_number: str | None = None,
        swift_bic: str | None = None,
    ) -> Result[dict]:
        bank = await self._banks.find_by_id(bank_id)
        if not bank or bank.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_not_found")
        if await self._branches.find_by_code(tenant_id, bank_id, code):
            return Result.fail("treasury.errors.branch_exists")
        errors = validate_account_identifiers(routing_number=routing_number, swift_bic=swift_bic)
        if errors:
            return Result.fail(f"treasury.errors.{errors[0]}")
        branch = BankBranch.create(
            tenant_id=tenant_id,
            bank_id=bank_id,
            code=code,
            name=name,
            organization_id=organization_id or bank.organization_id,
            address=address,
            routing_number=routing_number,
            swift_bic=swift_bic or bank.swift_bic,
        )
        await self._branches.save(branch)
        return Result.ok(branch.to_dict())

    async def list_branches(
        self, tenant_id: str, bank_id: str, organization_id: str | None = None
    ) -> Result[list[dict]]:
        bank = await self._banks.find_by_id(bank_id)
        if not bank or bank.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_not_found")
        branches = await self._branches.list_by_bank(tenant_id, bank_id)
        if organization_id:
            branches = [b for b in branches if b.organization_id == organization_id]
        return Result.ok([b.to_dict() for b in branches])

    async def create_account(
        self,
        *,
        tenant_id: str,
        bank_id: str,
        code: str,
        name: str,
        account_type: str,
        currency: str = "USD",
        organization_id: str | None = None,
        branch_id: str | None = None,
        iban: str | None = None,
        swift_bic: str | None = None,
        routing_number: str | None = None,
        account_number: str | None = None,
        virtual_account_ref: str | None = None,
        gl_account_code: str | None = None,
        opening_balance: float = 0.0,
        require_approval: bool = True,
    ) -> Result[dict]:
        bank = await self._banks.find_by_id(bank_id)
        if not bank or bank.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_not_found")
        if branch_id:
            branch = await self._branches.find_by_id(branch_id)
            if not branch or branch.tenant_id != tenant_id or branch.bank_id != bank_id:
                return Result.fail("treasury.errors.branch_not_found")
        if await self._accounts.find_by_code(tenant_id, code):
            return Result.fail("treasury.errors.bank_account_exists")
        try:
            assert_account_type(account_type)
        except ValueError:
            return Result.fail("treasury.errors.invalid_account_type")
        errors = validate_account_identifiers(
            iban=iban, swift_bic=swift_bic, routing_number=routing_number
        )
        if errors:
            return Result.fail(f"treasury.errors.{errors[0]}")
        account = BankAccount.create_draft(
            tenant_id=tenant_id,
            bank_id=bank_id,
            code=code,
            name=name,
            account_type=account_type,
            currency=currency,
            organization_id=organization_id or bank.organization_id,
            branch_id=branch_id,
            iban=iban,
            swift_bic=swift_bic or bank.swift_bic,
            routing_number=routing_number,
            account_number=account_number,
            virtual_account_ref=virtual_account_ref,
            gl_account_code=gl_account_code,
            opening_balance=opening_balance,
            require_approval=require_approval,
        )
        await self._accounts.save(account)
        return Result.ok(account.to_dict(mask_sensitive=True))

    async def list_accounts(
        self,
        tenant_id: str,
        *,
        organization_id: str | None = None,
        bank_id: str | None = None,
        mask_sensitive: bool = True,
    ) -> Result[list[dict]]:
        if bank_id:
            accounts = await self._accounts.list_by_bank(tenant_id, bank_id)
        else:
            accounts = await self._accounts.list_by_tenant(tenant_id, organization_id)
        return Result.ok([a.to_dict(mask_sensitive=mask_sensitive) for a in accounts])

    async def get_account(
        self, tenant_id: str, account_id: str, *, reveal_sensitive: bool = False
    ) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_account_not_found")
        return Result.ok(account.to_dict(mask_sensitive=not reveal_sensitive))

    async def submit_account(self, tenant_id: str, account_id: str, correlation_id: str = "") -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_account_not_found")
        try:
            account.submit_for_approval()
        except ValueError:
            return Result.fail("treasury.errors.invalid_status_transition")
        await self._accounts.save(account)
        await publish_integration_event(
            BankAccountApprovalRequestedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                bank_account_id=str(account.id),
                code=account.code,
                account_type=account.account_type,
            )
        )
        return Result.ok(account.to_dict(mask_sensitive=True))

    async def approve_account(
        self,
        tenant_id: str,
        account_id: str,
        *,
        actor_id: str,
        workflow_instance_id: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_account_not_found")
        try:
            account.approve(actor_id, workflow_instance_id)
        except ValueError:
            return Result.fail("treasury.errors.invalid_status_transition")
        await self._accounts.save(account)
        await publish_integration_event(
            BankAccountActivatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                bank_account_id=str(account.id),
                code=account.code,
                currency=account.currency,
            )
        )
        return Result.ok(account.to_dict(mask_sensitive=True))

    async def reject_account(self, tenant_id: str, account_id: str) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_account_not_found")
        try:
            account.reject()
        except ValueError:
            return Result.fail("treasury.errors.invalid_status_transition")
        await self._accounts.save(account)
        return Result.ok(account.to_dict(mask_sensitive=True))

    async def suspend_account(self, tenant_id: str, account_id: str) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_account_not_found")
        try:
            account.suspend()
        except ValueError:
            return Result.fail("treasury.errors.invalid_status_transition")
        await self._accounts.save(account)
        return Result.ok(account.to_dict(mask_sensitive=True))

    async def close_account(self, tenant_id: str, account_id: str) -> Result[dict]:
        account = await self._accounts.find_by_id(account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_account_not_found")
        try:
            account.close()
        except ValueError:
            return Result.fail("treasury.errors.invalid_status_transition")
        await self._accounts.save(account)
        return Result.ok(account.to_dict(mask_sensitive=True))

    async def add_signatory(
        self,
        *,
        tenant_id: str,
        bank_account_id: str,
        name: str,
        role: str = "signatory",
        organization_id: str | None = None,
        email: str | None = None,
        authority_limit: float | None = None,
    ) -> Result[dict]:
        account = await self._accounts.find_by_id(bank_account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_account_not_found")
        signatory = AuthorizedSignatory.create(
            tenant_id=tenant_id,
            bank_account_id=bank_account_id,
            name=name,
            role=role,
            organization_id=organization_id or account.organization_id,
            email=email,
            authority_limit=authority_limit,
        )
        await self._signatories.save(signatory)
        return Result.ok(signatory.to_dict())

    async def approve_signatory(
        self, tenant_id: str, signatory_id: str, actor_id: str
    ) -> Result[dict]:
        signatory = await self._signatories.find_by_id(signatory_id)
        if not signatory or signatory.tenant_id != tenant_id:
            return Result.fail("treasury.errors.signatory_not_found")
        signatory.approve(actor_id)
        await self._signatories.save(signatory)
        return Result.ok(signatory.to_dict())

    async def list_signatories(self, tenant_id: str, bank_account_id: str) -> Result[list[dict]]:
        account = await self._accounts.find_by_id(bank_account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_account_not_found")
        signatories = await self._signatories.list_by_account(bank_account_id)
        return Result.ok([s.to_dict() for s in signatories])

    async def attach_document(
        self,
        *,
        tenant_id: str,
        bank_account_id: str,
        document_type: str,
        reference: str,
        organization_id: str | None = None,
        file_name: str | None = None,
    ) -> Result[dict]:
        account = await self._accounts.find_by_id(bank_account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_account_not_found")
        document = BankAccountDocument.attach(
            tenant_id=tenant_id,
            bank_account_id=bank_account_id,
            document_type=document_type,
            reference=reference,
            organization_id=organization_id or account.organization_id,
            file_name=file_name,
        )
        await self._documents.save(document)
        return Result.ok(document.to_dict())

    async def verify_document(
        self, tenant_id: str, document_id: str, actor_id: str
    ) -> Result[dict]:
        document = await self._documents.find_by_id(document_id)
        if not document or document.tenant_id != tenant_id:
            return Result.fail("treasury.errors.document_not_found")
        document.verify(actor_id)
        await self._documents.save(document)
        return Result.ok(document.to_dict())

    async def list_documents(self, tenant_id: str, bank_account_id: str) -> Result[list[dict]]:
        account = await self._accounts.find_by_id(bank_account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.bank_account_not_found")
        documents = await self._documents.list_by_account(bank_account_id)
        return Result.ok([d.to_dict() for d in documents])
