"""Enterprise Financial Documents application service."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.financial_document import (
    FinancialDocument,
    FinancialDocumentStatus,
    FinancialDocumentType,
    FinancialDocumentVersion,
)
from contexts.financial_kernel.domain.events.integration_events import (
    FinancialDocumentApprovalRequestedIntegration,
    FinancialDocumentApprovedIntegration,
    FinancialDocumentCreatedIntegration,
    FinancialDocumentIssuedIntegration,
    FinancialDocumentSignedIntegration,
    FinancialDocumentVersionCreatedIntegration,
)
from contexts.financial_kernel.domain.ports.financial_document_repositories import (
    IFinancialDocumentRepository,
    IFinancialDocumentVersionRepository,
)
from contexts.financial_kernel.domain.services.financial_document_engine import (
    checksum_content,
    generate_document_number,
    generate_pdf,
    generate_qr_token,
    new_workflow_id,
    requires_approval,
    sign_document,
    verify_qr_token,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class FinancialDocumentApplicationService:
    def __init__(
        self,
        documents: IFinancialDocumentRepository,
        versions: IFinancialDocumentVersionRepository,
    ) -> None:
        self._documents = documents
        self._versions = versions

    async def create_document(
        self,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        idempotency_key: str,
        document_type: str,
        currency: str,
        total_amount: float,
        counterparty_name: str,
        reference: str,
        lines: list[dict] | None = None,
        metadata: dict | None = None,
        counterparty_id: str | None = None,
        created_by: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        existing = await self._documents.find_by_idempotency(tenant_id, idempotency_key)
        if existing:
            return Result.ok(await self._document_detail(existing))

        try:
            FinancialDocumentType(document_type)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_document_type")

        seq = await self._documents.next_sequence(tenant_id, document_type)
        doc_number = generate_document_number(document_type, seq)

        document = FinancialDocument.create(
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            document_type=document_type,
            document_number=doc_number,
            currency=currency,
            total_amount=total_amount,
            counterparty_name=counterparty_name,
            reference=reference,
            lines=lines,
            metadata=metadata,
            counterparty_id=counterparty_id,
            created_by=created_by,
        )

        version = await self._create_version(document, created_by=created_by)
        document.set_current_version(version.id)
        document.set_qr_token(
            generate_qr_token(
                document_id=str(document.id),
                version_number=version.version_number,
                checksum=version.checksum,
                tenant_id=tenant_id,
            )
        )

        await self._documents.save(document)
        await self._versions.save(version)

        await publish_integration_event(
            FinancialDocumentCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=str(document.id),
                document_type=document_type,
                document_number=doc_number,
                total_amount=total_amount,
                fin_doc_source_context=source_context,
                source_document_id=source_document_id,
            )
        )
        await publish_integration_event(
            FinancialDocumentVersionCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=str(document.id),
                version_id=str(version.id),
                version_number=version.version_number,
                checksum=version.checksum,
            )
        )
        return Result.ok(await self._document_detail(document))

    async def add_version(
        self,
        *,
        tenant_id: str,
        document_id: str,
        lines: list[dict] | None = None,
        total_amount: float | None = None,
        metadata: dict | None = None,
        created_by: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        document = await self._documents.find_by_id(document_id)
        if not document or document.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.document_not_found")
        if document.status == FinancialDocumentStatus.VOIDED:
            return Result.fail("financial_kernel.errors.document_voided")

        if lines is not None:
            document.lines = lines
        if total_amount is not None:
            document.total_amount = round(total_amount, 2)
        if metadata is not None:
            document.metadata.update(metadata)

        version = await self._create_version(document, created_by=created_by)
        document.set_current_version(version.id)
        document.set_qr_token(
            generate_qr_token(
                document_id=str(document.id),
                version_number=version.version_number,
                checksum=version.checksum,
                tenant_id=tenant_id,
            )
        )
        if document.status == FinancialDocumentStatus.ISSUED:
            document.status = FinancialDocumentStatus.DRAFT

        await self._versions.save(version)
        await self._documents.save(document)

        await publish_integration_event(
            FinancialDocumentVersionCreatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=str(document.id),
                version_id=str(version.id),
                version_number=version.version_number,
                checksum=version.checksum,
            )
        )
        return Result.ok(await self._document_detail(document))

    async def request_approval(
        self,
        *,
        tenant_id: str,
        document_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        document = await self._documents.find_by_id(document_id)
        if not document or document.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.document_not_found")

        workflow_id = new_workflow_id()
        try:
            document.request_approval(workflow_id)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_status_for_approval")

        await self._documents.save(document)
        await publish_integration_event(
            FinancialDocumentApprovalRequestedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=str(document.id),
                document_type=document.document_type,
                workflow_id=workflow_id,
            )
        )
        return Result.ok(document.to_dict())

    async def complete_approval(
        self,
        *,
        tenant_id: str,
        document_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        document = await self._documents.find_by_id(document_id)
        if not document or document.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.document_not_found")

        try:
            document.approve()
        except ValueError:
            return Result.fail("financial_kernel.errors.not_pending_approval")

        await self._documents.save(document)
        await publish_integration_event(
            FinancialDocumentApprovedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=str(document.id),
                document_type=document.document_type,
            )
        )
        return Result.ok(document.to_dict())

    async def sign_document(
        self,
        *,
        tenant_id: str,
        document_id: str,
        signer_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        document = await self._documents.find_by_id(document_id)
        if not document or document.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.document_not_found")
        if not document.current_version_id:
            return Result.fail("financial_kernel.errors.no_version")

        version = await self._versions.find_by_id(str(document.current_version_id))
        if not version:
            return Result.fail("financial_kernel.errors.version_not_found")

        signature = sign_document(
            document_id=str(document.id),
            version_checksum=version.checksum,
            signer_id=signer_id,
        )
        try:
            document.sign(signature)
        except ValueError:
            return Result.fail("financial_kernel.errors.invalid_status_for_signature")

        await self._documents.save(document)
        await publish_integration_event(
            FinancialDocumentSignedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=str(document.id),
                signer_id=signer_id,
                version_checksum=version.checksum,
            )
        )
        return Result.ok(await self._document_detail(document))

    async def issue_document(
        self,
        *,
        tenant_id: str,
        document_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        document = await self._documents.find_by_id(document_id)
        if not document or document.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.document_not_found")

        if requires_approval(document.document_type) and document.status not in (
            FinancialDocumentStatus.SIGNED,
            FinancialDocumentStatus.APPROVED,
        ):
            return Result.fail("financial_kernel.errors.approval_required")

        try:
            document.issue(allow_draft=not requires_approval(document.document_type))
        except ValueError:
            return Result.fail("financial_kernel.errors.not_ready_to_issue")

        await self._documents.save(document)
        await publish_integration_event(
            FinancialDocumentIssuedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                document_id=str(document.id),
                document_type=document.document_type,
                document_number=document.document_number,
                total_amount=document.total_amount,
            )
        )
        return Result.ok(await self._document_detail(document))

    async def void_document(self, *, tenant_id: str, document_id: str) -> Result[dict]:
        document = await self._documents.find_by_id(document_id)
        if not document or document.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.document_not_found")
        try:
            document.void()
        except ValueError:
            return Result.fail("financial_kernel.errors.already_voided")
        await self._documents.save(document)
        return Result.ok(document.to_dict())

    async def get_document(self, tenant_id: str, document_id: str) -> Result[dict]:
        document = await self._documents.find_by_id(document_id)
        if not document or document.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.document_not_found")
        return Result.ok(await self._document_detail(document))

    async def list_documents(self, tenant_id: str) -> Result[list[dict]]:
        docs = await self._documents.list_by_tenant(tenant_id)
        return Result.ok([d.to_dict() for d in docs])

    async def get_pdf(self, tenant_id: str, document_id: str) -> Result[dict]:
        document = await self._documents.find_by_id(document_id)
        if not document or document.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.document_not_found")
        if not document.current_version_id:
            return Result.fail("financial_kernel.errors.no_version")

        version = await self._versions.find_by_id(str(document.current_version_id))
        if not version:
            return Result.fail("financial_kernel.errors.version_not_found")

        return Result.ok(
            {
                "document_id": str(document.id),
                "document_number": document.document_number,
                "file_name": f"{document.document_number}.pdf",
                "content_type": "application/pdf",
                "pdf_base64": version.pdf_base64,
                "checksum": version.checksum,
            }
        )

    async def verify_qr(self, token: str) -> Result[dict]:
        parsed = verify_qr_token(token)
        if not parsed:
            return Result.fail("financial_kernel.errors.invalid_qr_token")

        document = await self._documents.find_by_id(parsed["document_id"])
        if not document or document.tenant_id != parsed["tenant_id"]:
            return Result.fail("financial_kernel.errors.document_not_found")

        versions = await self._versions.list_by_document(parsed["tenant_id"], parsed["document_id"])
        match = next((v for v in versions if v.version_number == parsed["version_number"]), None)
        if not match or match.checksum != parsed["checksum"]:
            return Result.fail("financial_kernel.errors.qr_checksum_mismatch")

        return Result.ok(
            {
                "valid": True,
                "document_id": str(document.id),
                "document_number": document.document_number,
                "document_type": document.document_type,
                "status": document.status.value,
                "total_amount": document.total_amount,
                "currency": document.currency,
                "version_number": parsed["version_number"],
                "checksum": parsed["checksum"],
                "issued_at": document.issued_at.isoformat() if document.issued_at else None,
            }
        )

    async def _create_version(
        self,
        document: FinancialDocument,
        *,
        created_by: str | None,
    ) -> FinancialDocumentVersion:
        version_number = await self._versions.next_version_number(
            document.tenant_id, str(document.id)
        )
        snapshot = document.to_dict()
        cs = checksum_content(snapshot)
        pdf = generate_pdf(snapshot)
        return FinancialDocumentVersion.create(
            tenant_id=document.tenant_id,
            document_id=document.id,
            version_number=version_number,
            content_snapshot=snapshot,
            checksum=cs,
            pdf_base64=pdf,
            created_by=created_by,
        )

    async def _document_detail(self, document: FinancialDocument) -> dict:
        versions = await self._versions.list_by_document(document.tenant_id, str(document.id))
        return {
            "document": document.to_dict(),
            "versions": [v.to_dict() for v in versions],
            "qr_verification_url": (
                f"/api/v1/financial-kernel/financial-documents/verify/{document.qr_token}"
                if document.qr_token
                else None
            ),
        }
