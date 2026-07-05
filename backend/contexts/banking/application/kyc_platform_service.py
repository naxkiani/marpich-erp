"""Enterprise KYC Platform application service."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from contexts.banking.domain.aggregates.kyc_platform_engine import (
    DocumentType,
    DueDiligenceLevel,
    KycAddressVerification,
    KycAuditEntry,
    KycBiometricHook,
    KycCase,
    KycCaseStatus,
    KycDocument,
    KycPeriodicReview,
    KycScreeningResult,
    KycWorkflowRequest,
    PepStatus,
    ReviewStatus,
    SanctionsStatus,
    VerificationStatus,
)
from contexts.banking.domain.events.kyc_integration_events import (
    KycBiometricHookRequestedIntegration,
    KycCaseApprovedIntegration,
    KycCaseOpenedIntegration,
    KycPepFlagRaisedIntegration,
    KycPeriodicReviewDueIntegration,
    KycSanctionsHitIntegration,
)
from contexts.banking.domain.ports.customer_account_repositories import ICustomerRepository
from contexts.banking.domain.ports.kyc_platform_repositories import (
    IKycAddressRepository,
    IKycAuditRepository,
    IKycBiometricRepository,
    IKycCaseRepository,
    IKycDocumentRepository,
    IKycReviewRepository,
    IKycScreeningRepository,
    IKycWorkflowRepository,
)
from contexts.banking.domain.services.kyc_platform_engine import (
    build_kyc_dashboard,
    classify_risk_from_policy,
    list_case_workflow,
    list_kyc_catalog,
    list_kyc_policy_keys,
    resolve_approval_levels,
    resolve_pep_status_from_policy,
    resolve_sanctions_status_from_policy,
)
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BankingKycPlatformApplicationService:
    def __init__(
        self,
        cases: IKycCaseRepository,
        documents: IKycDocumentRepository,
        addresses: IKycAddressRepository,
        screenings: IKycScreeningRepository,
        reviews: IKycReviewRepository,
        workflows: IKycWorkflowRepository,
        biometrics: IKycBiometricRepository,
        audits: IKycAuditRepository,
        customers: ICustomerRepository,
        policy: IPolicyEvaluator,
    ) -> None:
        self._cases = cases
        self._documents = documents
        self._addresses = addresses
        self._screenings = screenings
        self._reviews = reviews
        self._workflows = workflows
        self._biometrics = biometrics
        self._audits = audits
        self._customers = customers
        self._policy = policy

    async def _audit(
        self,
        *,
        tenant_id: str,
        case_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
    ) -> None:
        entry = KycAuditEntry.create(
            tenant_id=tenant_id,
            case_id=case_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
        )
        await self._audits.save(entry)

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_kyc_catalog())

    async def list_policy_keys(self) -> Result[list[dict]]:
        return Result.ok(list_kyc_policy_keys())

    async def list_workflow(self) -> Result[list[dict]]:
        return Result.ok(list_case_workflow())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        cases = await self._cases.list_by_tenant(tenant_id)
        documents = await self._documents.list_by_tenant(tenant_id)
        reviews = await self._reviews.list_by_tenant(tenant_id)
        screenings = await self._screenings.list_by_tenant(tenant_id)
        return Result.ok(
            build_kyc_dashboard(
                cases=[c.to_dict() for c in cases],
                documents=[d.to_dict() for d in documents],
                reviews=[r.to_dict() for r in reviews],
                screenings=[s.to_dict() for s in screenings],
            )
        )

    async def open_case(
        self,
        *,
        tenant_id: str,
        customer_id: str,
        due_diligence_level: str = DueDiligenceLevel.STANDARD.value,
        organization_id: str | None = None,
        branch_id: str | None = None,
    ) -> Result[dict]:
        customer = await self._customers.find_by_id(customer_id)
        if not customer or customer.tenant_id != tenant_id:
            return Result.fail("banking.errors.customer_not_found")

        identity_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="kyc.identity.verification_required",
            facts={
                "customer_type": customer.customer_type,
                "segment": customer.customer_type,
                "document_types": [],
            },
            organization_id=organization_id,
        )

        case_ref = self._cases.next_case_ref(tenant_id)
        case = KycCase.create(
            tenant_id=tenant_id,
            customer_id=customer_id,
            case_ref=case_ref,
            due_diligence_level=due_diligence_level,
            organization_id=organization_id or customer.organization_id,
            branch_id=branch_id or customer.branch_id,
        )
        case.record_policy_decision("kyc.identity.verification_required", identity_policy.to_dict())
        case.transition(KycCaseStatus.PENDING_DOCUMENTS.value)
        await self._cases.save(case)
        await self._audit(
            tenant_id=tenant_id, case_id=str(case.id), action="case.opened", detail=case_ref
        )

        await publish_integration_event(
            KycCaseOpenedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"kyc-case-{case.id}",
                case_id=str(case.id),
                customer_id=customer_id,
                case_ref=case_ref,
                due_diligence_level=due_diligence_level,
            )
        )
        return Result.ok(case.to_dict())

    async def list_cases(self, tenant_id: str) -> Result[list[dict]]:
        cases = await self._cases.list_by_tenant(tenant_id)
        return Result.ok([c.to_dict() for c in cases])

    async def get_case(self, case_id: str) -> Result[dict]:
        case = await self._cases.find_by_id(case_id)
        if not case:
            return Result.fail("banking.errors.kyc_case_not_found")
        docs = await self._documents.list_by_case(case_id)
        addresses = await self._addresses.list_by_case(case_id)
        screenings = await self._screenings.list_by_case(case_id)
        reviews = await self._reviews.list_by_case(case_id)
        workflows = await self._workflows.list_by_case(case_id)
        biometrics = await self._biometrics.list_by_case(case_id)
        return Result.ok(
            {
                **case.to_dict(),
                "documents": [d.to_dict() for d in docs],
                "addresses": [a.to_dict() for a in addresses],
                "screenings": [s.to_dict() for s in screenings],
                "reviews": [r.to_dict() for r in reviews],
                "workflows": [w.to_dict() for w in workflows],
                "biometric_hooks": [b.to_dict() for b in biometrics],
            }
        )

    async def submit_document(
        self,
        *,
        tenant_id: str,
        case_id: str,
        document_type: str,
        document_ref: str,
        issuing_country: str = "",
        expiry_date: str | None = None,
        metadata: dict | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_id(case_id)
        if not case or case.tenant_id != tenant_id:
            return Result.fail("banking.errors.kyc_case_not_found")

        try:
            DocumentType(document_type)
        except ValueError:
            return Result.fail("banking.errors.invalid_document_type")

        if expiry_date and document_type == DocumentType.PASSPORT.value:
            days_until = _days_until(expiry_date)
            passport_policy = await self._policy.evaluate(
                tenant_id=tenant_id,
                domain="bank",
                policy_key="kyc.document.passport_validity",
                facts={
                    "document_type": document_type,
                    "expiry_date": expiry_date,
                    "days_until_expiry": days_until,
                },
                organization_id=case.organization_id,
            )
            case.record_policy_decision("kyc.document.passport_validity", passport_policy.to_dict())
            if passport_policy.matched and passport_policy.outcome == "reject_expired":
                return Result.fail("banking.errors.passport_expired_or_invalid")

        document = KycDocument.create(
            tenant_id=tenant_id,
            case_id=case_id,
            customer_id=case.customer_id,
            document_type=document_type,
            document_ref=document_ref,
            issuing_country=issuing_country,
            expiry_date=expiry_date,
            metadata=metadata,
        )
        await self._documents.save(document)
        if case.status == KycCaseStatus.PENDING_DOCUMENTS.value:
            case.transition(KycCaseStatus.IN_REVIEW.value)
            await self._cases.save(case)
        await self._audit(
            tenant_id=tenant_id,
            case_id=case_id,
            action="document.submitted",
            detail=f"{document_type}:{document_ref}",
        )
        return Result.ok(document.to_dict())

    async def verify_document(
        self, *, document_id: str, verified_by: str, actor_id: str | None = None
    ) -> Result[dict]:
        document = await self._documents.find_by_id(document_id)
        if not document:
            return Result.fail("banking.errors.kyc_document_not_found")

        document.verify(verified_by=verified_by)
        await self._documents.save(document)

        case = await self._cases.find_by_id(document.case_id)
        if case:
            if document.document_type in {
                DocumentType.PASSPORT.value,
                DocumentType.NATIONAL_ID.value,
            }:
                case.mark_identity_verified()
            if document.document_type == DocumentType.ADDRESS_PROOF.value:
                case.mark_address_verified()
            await self._cases.save(case)

        await self._audit(
            tenant_id=document.tenant_id,
            case_id=document.case_id,
            action="document.verified",
            actor_id=actor_id or verified_by,
            detail=document.document_type,
        )
        return Result.ok(document.to_dict())

    async def submit_address(
        self,
        *,
        tenant_id: str,
        case_id: str,
        address_line: str,
        city: str,
        country: str,
        postal_code: str = "",
        proof_document_id: str | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_id(case_id)
        if not case or case.tenant_id != tenant_id:
            return Result.fail("banking.errors.kyc_case_not_found")

        address = KycAddressVerification.create(
            tenant_id=tenant_id,
            case_id=case_id,
            customer_id=case.customer_id,
            address_line=address_line,
            city=city,
            country=country,
            postal_code=postal_code,
            proof_document_id=proof_document_id,
        )
        await self._addresses.save(address)
        await self._audit(
            tenant_id=tenant_id, case_id=case_id, action="address.submitted", detail=country
        )
        return Result.ok(address.to_dict())

    async def verify_address(
        self, *, address_id: str, verified_by: str
    ) -> Result[dict]:
        address = await self._addresses.find_by_id(address_id)
        if not address:
            return Result.fail("banking.errors.kyc_address_not_found")

        address.verify(verified_by=verified_by)
        await self._addresses.save(address)

        case = await self._cases.find_by_id(address.case_id)
        if case:
            case.mark_address_verified()
            await self._cases.save(case)

        await self._audit(
            tenant_id=address.tenant_id,
            case_id=address.case_id,
            action="address.verified",
            actor_id=verified_by,
        )
        return Result.ok(address.to_dict())

    async def run_pep_screening(
        self,
        *,
        tenant_id: str,
        case_id: str,
        match_score: float = 0.0,
        match_details: dict | None = None,
        provider_ref: str = "",
        screened_by: str | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_id(case_id)
        if not case or case.tenant_id != tenant_id:
            return Result.fail("banking.errors.kyc_case_not_found")

        customer = await self._customers.find_by_id(case.customer_id)
        pep_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="kyc.pep.screening",
            facts={
                "match_score": match_score,
                "customer_type": customer.customer_type if customer else "individual",
                "role": (match_details or {}).get("role", ""),
            },
            organization_id=case.organization_id,
        )
        case.record_policy_decision("kyc.pep.screening", pep_policy.to_dict())
        pep_status = resolve_pep_status_from_policy(
            policy_outcome=pep_policy.outcome, match_score=match_score
        )
        case.apply_pep_screening(pep_status)

        result = KycScreeningResult.create(
            tenant_id=tenant_id,
            case_id=case_id,
            customer_id=case.customer_id,
            screening_type="pep",
            status=pep_status,
            provider_ref=provider_ref,
            match_score=match_score,
            match_details=match_details,
            screened_by=screened_by,
        )
        await self._screenings.save(result)
        await self._cases.save(case)
        await self._audit(
            tenant_id=tenant_id,
            case_id=case_id,
            action="pep.screened",
            actor_id=screened_by,
            detail=f"status={pep_status} score={match_score}",
        )

        if pep_status in {PepStatus.POTENTIAL_MATCH.value, PepStatus.CONFIRMED.value}:
            await publish_integration_event(
                KycPepFlagRaisedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=f"kyc-pep-{case_id}",
                    case_id=case_id,
                    customer_id=case.customer_id,
                    pep_status=pep_status,
                    match_score=match_score,
                )
            )
        return Result.ok({**result.to_dict(), "case": case.to_dict()})

    async def run_sanctions_screening(
        self,
        *,
        tenant_id: str,
        case_id: str,
        match_score: float = 0.0,
        match_details: dict | None = None,
        provider_ref: str = "",
        screened_by: str | None = None,
    ) -> Result[dict]:
        case = await self._cases.find_by_id(case_id)
        if not case or case.tenant_id != tenant_id:
            return Result.fail("banking.errors.kyc_case_not_found")

        sanctions_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="kyc.sanctions.screening",
            facts={
                "match_score": match_score,
                "list_name": (match_details or {}).get("list_name", ""),
                "country": (match_details or {}).get("country", ""),
            },
            organization_id=case.organization_id,
        )
        case.record_policy_decision("kyc.sanctions.screening", sanctions_policy.to_dict())
        sanctions_status = resolve_sanctions_status_from_policy(
            policy_outcome=sanctions_policy.outcome, match_score=match_score
        )
        case.apply_sanctions_screening(sanctions_status)

        result = KycScreeningResult.create(
            tenant_id=tenant_id,
            case_id=case_id,
            customer_id=case.customer_id,
            screening_type="sanctions",
            status=sanctions_status,
            provider_ref=provider_ref,
            match_score=match_score,
            match_details=match_details,
            screened_by=screened_by,
        )
        await self._screenings.save(result)
        await self._cases.save(case)
        await self._audit(
            tenant_id=tenant_id,
            case_id=case_id,
            action="sanctions.screened",
            actor_id=screened_by,
            detail=f"status={sanctions_status} score={match_score}",
        )

        if sanctions_status in {SanctionsStatus.POTENTIAL_MATCH.value, SanctionsStatus.BLOCKED.value}:
            await publish_integration_event(
                KycSanctionsHitIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=f"kyc-sanctions-{case_id}",
                    case_id=case_id,
                    customer_id=case.customer_id,
                    sanctions_status=sanctions_status,
                    match_score=match_score,
                )
            )
        return Result.ok({**result.to_dict(), "case": case.to_dict()})

    async def classify_risk(self, *, tenant_id: str, case_id: str) -> Result[dict]:
        case = await self._cases.find_by_id(case_id)
        if not case or case.tenant_id != tenant_id:
            return Result.fail("banking.errors.kyc_case_not_found")

        customer = await self._customers.find_by_id(case.customer_id)
        risk_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="kyc.risk.classification",
            facts={
                "customer_type": customer.customer_type if customer else "individual",
                "country": customer.organization_id or "unknown",
                "pep_status": case.pep_status,
                "transaction_volume": 0,
            },
            organization_id=case.organization_id,
        )
        case.record_policy_decision("kyc.risk.classification", risk_policy.to_dict())

        edd_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="kyc.dd.enhanced_threshold",
            facts={
                "risk_class": case.risk_class,
                "pep_status": case.pep_status,
                "amount": 0,
                "country_risk": "standard",
            },
            organization_id=case.organization_id,
        )
        case.record_policy_decision("kyc.dd.enhanced_threshold", edd_policy.to_dict())

        risk_class, requires_edd = classify_risk_from_policy(
            policy_outcome=risk_policy.outcome,
            policy_params=risk_policy.parameters,
        )
        if edd_policy.matched and edd_policy.outcome == "enhanced_due_diligence":
            requires_edd = True
        case.apply_risk_classification(risk_class=risk_class, requires_edd=requires_edd)
        await self._cases.save(case)
        await self._audit(
            tenant_id=tenant_id,
            case_id=case_id,
            action="risk.classified",
            detail=f"risk={risk_class} edd={requires_edd}",
        )
        return Result.ok(case.to_dict())

    async def submit_for_approval(
        self, *, case_id: str, actor_id: str | None = None
    ) -> Result[dict]:
        case = await self._cases.find_by_id(case_id)
        if not case:
            return Result.fail("banking.errors.kyc_case_not_found")
        if case.sanctions_status == SanctionsStatus.BLOCKED.value:
            return Result.fail("banking.errors.sanctions_blocked")

        if not case.identity_verified:
            return Result.fail("banking.errors.identity_not_verified")

        approval_policy = await self._policy.evaluate(
            tenant_id=case.tenant_id,
            domain="bank",
            policy_key="kyc.approval.required_level",
            facts={
                "risk_class": case.risk_class,
                "due_diligence_level": case.due_diligence_level,
                "pep_status": case.pep_status,
            },
            organization_id=case.organization_id,
        )
        case.record_policy_decision("kyc.approval.required_level", approval_policy.to_dict())
        required_levels = approval_policy.parameters.get(
            "required_levels",
            resolve_approval_levels(
                risk_class=case.risk_class,
                requires_edd=case.requires_edd,
                pep_status=case.pep_status,
            ),
        )

        try:
            case.submit_for_approval()
        except ValueError:
            return Result.fail("banking.errors.cannot_submit_kyc_case")

        workflow = KycWorkflowRequest.create(
            tenant_id=case.tenant_id,
            case_id=case_id,
            customer_id=case.customer_id,
            request_type="kyc_case_approval",
            required_levels=int(required_levels),
        )
        await self._workflows.save(workflow)
        await self._cases.save(case)
        await self._audit(
            tenant_id=case.tenant_id,
            case_id=case_id,
            action="case.submitted_for_approval",
            actor_id=actor_id,
            detail=f"levels={required_levels}",
        )
        return Result.ok({**case.to_dict(), "workflow": workflow.to_dict()})

    async def approve_case(
        self, *, case_id: str, approver_id: str, actor_id: str | None = None
    ) -> Result[dict]:
        case = await self._cases.find_by_id(case_id)
        if not case:
            return Result.fail("banking.errors.kyc_case_not_found")

        workflows = await self._workflows.list_by_case(case_id)
        pending = next((w for w in workflows if w.status == "pending"), None)
        if pending:
            try:
                pending.approve(approver_id=approver_id)
            except ValueError:
                return Result.fail("banking.errors.workflow_not_pending")
            await self._workflows.save(pending)
            if pending.status != "approved":
                return Result.ok({**case.to_dict(), "workflow": pending.to_dict()})

        review_policy = await self._policy.evaluate(
            tenant_id=case.tenant_id,
            domain="bank",
            policy_key="kyc.periodic.review_interval",
            facts={
                "risk_class": case.risk_class,
                "due_diligence_level": case.due_diligence_level,
            },
            organization_id=case.organization_id,
        )
        interval_days = int(review_policy.parameters.get("interval_days", 365))

        try:
            case.approve(approved_by=approver_id, review_interval_days=interval_days)
        except ValueError as exc:
            return Result.fail(f"banking.errors.{exc.args[0]}")

        await self._cases.save(case)

        review_ref = self._reviews.next_review_ref(case.tenant_id)
        review = KycPeriodicReview.create(
            tenant_id=case.tenant_id,
            case_id=case_id,
            customer_id=case.customer_id,
            review_ref=review_ref,
            due_date=case.expires_at or datetime.now(UTC) + timedelta(days=interval_days),
        )
        await self._reviews.save(review)

        customer = await self._customers.find_by_id(case.customer_id)
        if customer:
            customer.update_kyc_status("verified")
            await self._customers.save(customer)

        await self._audit(
            tenant_id=case.tenant_id,
            case_id=case_id,
            action="case.approved",
            actor_id=actor_id or approver_id,
        )

        await publish_integration_event(
            KycCaseApprovedIntegration(
                tenant_id=TenantId.create(case.tenant_id),
                correlation_id=f"kyc-approved-{case_id}",
                case_id=case_id,
                customer_id=case.customer_id,
                risk_class=case.risk_class,
                due_diligence_level=case.due_diligence_level,
                approved_by=approver_id,
            )
        )
        return Result.ok({**case.to_dict(), "review": review.to_dict()})

    async def reject_case(
        self, *, case_id: str, approver_id: str, reason: str = ""
    ) -> Result[dict]:
        case = await self._cases.find_by_id(case_id)
        if not case:
            return Result.fail("banking.errors.kyc_case_not_found")

        workflows = await self._workflows.list_by_case(case_id)
        pending = next((w for w in workflows if w.status == "pending"), None)
        if pending:
            pending.reject(approver_id=approver_id, reason=reason)
            await self._workflows.save(pending)

        try:
            case.reject(reason=reason)
        except ValueError:
            return Result.fail("banking.errors.not_pending_kyc_approval")
        await self._cases.save(case)
        await self._audit(
            tenant_id=case.tenant_id,
            case_id=case_id,
            action="case.rejected",
            actor_id=approver_id,
            detail=reason,
        )
        return Result.ok(case.to_dict())

    async def schedule_periodic_review(
        self, *, tenant_id: str, case_id: str, due_in_days: int | None = None
    ) -> Result[dict]:
        case = await self._cases.find_by_id(case_id)
        if not case or case.tenant_id != tenant_id:
            return Result.fail("banking.errors.kyc_case_not_found")

        if due_in_days is None:
            review_policy = await self._policy.evaluate(
                tenant_id=tenant_id,
                domain="bank",
                policy_key="kyc.periodic.review_interval",
                facts={
                    "risk_class": case.risk_class,
                    "due_diligence_level": case.due_diligence_level,
                },
                organization_id=case.organization_id,
            )
            due_in_days = int(review_policy.parameters.get("interval_days", 365))

        review_ref = self._reviews.next_review_ref(tenant_id)
        review = KycPeriodicReview.create(
            tenant_id=tenant_id,
            case_id=case_id,
            customer_id=case.customer_id,
            review_ref=review_ref,
            due_date=datetime.now(UTC) + timedelta(days=due_in_days),
        )
        await self._reviews.save(review)

        await publish_integration_event(
            KycPeriodicReviewDueIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"kyc-review-{review.id}",
                case_id=case_id,
                customer_id=case.customer_id,
                review_id=str(review.id),
                due_date=review.due_date.isoformat(),
            )
        )
        return Result.ok(review.to_dict())

    async def complete_periodic_review(
        self, *, review_id: str, completed_by: str, outcome: str
    ) -> Result[dict]:
        review = await self._reviews.find_by_id(review_id)
        if not review:
            return Result.fail("banking.errors.kyc_review_not_found")

        review.complete(completed_by=completed_by, outcome=outcome)
        await self._reviews.save(review)
        await self._audit(
            tenant_id=review.tenant_id,
            case_id=review.case_id,
            action="review.completed",
            actor_id=completed_by,
            detail=outcome,
        )
        return Result.ok(review.to_dict())

    async def request_biometric_hook(
        self,
        *,
        tenant_id: str,
        case_id: str,
        provider: str,
        hook_ref: str,
        callback_url: str = "",
    ) -> Result[dict]:
        case = await self._cases.find_by_id(case_id)
        if not case or case.tenant_id != tenant_id:
            return Result.fail("banking.errors.kyc_case_not_found")

        hook = KycBiometricHook.create(
            tenant_id=tenant_id,
            case_id=case_id,
            customer_id=case.customer_id,
            provider=provider,
            hook_ref=hook_ref,
            callback_url=callback_url,
        )
        await self._biometrics.save(hook)
        await self._audit(
            tenant_id=tenant_id,
            case_id=case_id,
            action="biometric.requested",
            detail=f"provider={provider}",
        )

        await publish_integration_event(
            KycBiometricHookRequestedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"kyc-bio-{hook.id}",
                case_id=case_id,
                customer_id=case.customer_id,
                hook_id=str(hook.id),
                provider=provider,
                callback_url=callback_url,
            )
        )
        return Result.ok(hook.to_dict())

    async def complete_biometric_hook(
        self,
        *,
        hook_id: str,
        status: str,
        result_payload: dict,
    ) -> Result[dict]:
        hook = await self._biometrics.find_by_id(hook_id)
        if not hook:
            return Result.fail("banking.errors.kyc_biometric_not_found")

        hook.complete(status=status, result_payload=result_payload)
        await self._biometrics.save(hook)

        if status == "verified":
            case = await self._cases.find_by_id(hook.case_id)
            if case:
                case.mark_identity_verified()
                await self._cases.save(case)

        await self._audit(
            tenant_id=hook.tenant_id,
            case_id=hook.case_id,
            action="biometric.completed",
            detail=f"status={status}",
        )
        return Result.ok(hook.to_dict())

    async def get_audit_trail(self, case_id: str) -> Result[list[dict]]:
        entries = await self._audits.list_by_case(case_id)
        return Result.ok([e.to_dict() for e in entries])

    async def evaluate_policy(
        self, *, tenant_id: str, policy_key: str, facts: dict
    ) -> Result[dict]:
        decision = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key=policy_key,
            facts=facts,
        )
        return Result.ok(decision.to_dict())

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        """KYC policies are seeded by Policy Engine on tenant provision (bank domain)."""
        return None


def _days_until(expiry_date: str) -> int:
    try:
        expiry = datetime.fromisoformat(expiry_date.replace("Z", "+00:00"))
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=UTC)
        return max(0, (expiry - datetime.now(UTC)).days)
    except ValueError:
        return 0
