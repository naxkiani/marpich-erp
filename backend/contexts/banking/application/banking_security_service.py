"""Banking Security Platform application service."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.banking.domain.aggregates.banking_security_engine import (
    EmergencyFreeze,
    LimitUsageTracker,
    SecurityApprovalRequest,
    SecurityAuditEntry,
    SecurityDevice,
    SecuritySession,
    TransactionMonitorAlert,
)
from contexts.banking.domain.events.banking_security_integration_events import (
    BankingSecurityAlertRaisedIntegration,
    BankingSecurityApprovalCompletedIntegration,
    BankingSecurityApprovalSubmittedIntegration,
    BankingSecurityAuditRecordedIntegration,
    BankingSecurityFreezeActivatedIntegration,
)
from contexts.banking.domain.ports.banking_security_repositories import (
    IEmergencyFreezeRepository,
    ILimitUsageRepository,
    ISecurityApprovalRepository,
    ISecurityAuditRepository,
    ISecurityDeviceRepository,
    ISecuritySessionRepository,
    ITransactionMonitorRepository,
)
from contexts.banking.domain.services.banking_security_engine import (
    assess_risk,
    build_security_dashboard,
    check_daily_limit,
    check_transaction_limit,
    check_velocity,
    checksum_payload,
    compute_tamper_hash,
    encrypt_payload,
    evaluate_access,
    list_security_catalog,
    list_security_policy_keys,
    resolve_required_approvals,
    sign_operation,
    verify_tamper,
)
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BankingSecurityPlatformApplicationService:
    def __init__(
        self,
        approvals: ISecurityApprovalRepository,
        devices: ISecurityDeviceRepository,
        sessions: ISecuritySessionRepository,
        alerts: ITransactionMonitorRepository,
        freezes: IEmergencyFreezeRepository,
        audits: ISecurityAuditRepository,
        limit_usage: ILimitUsageRepository,
        policy: IPolicyEvaluator,
    ) -> None:
        self._approvals = approvals
        self._devices = devices
        self._sessions = sessions
        self._alerts = alerts
        self._freezes = freezes
        self._audits = audits
        self._limit_usage = limit_usage
        self._policy = policy

    async def _record_audit(
        self,
        *,
        tenant_id: str,
        action: str,
        actor_id: str,
        resource_type: str,
        resource_id: str,
        payload: dict | None = None,
        detail: str = "",
    ) -> SecurityAuditEntry:
        checksum = checksum_payload(payload or {})
        previous = await self._audits.last_tamper_hash(tenant_id)
        tamper_hash = compute_tamper_hash(
            action=action,
            actor_id=actor_id,
            resource_id=resource_id,
            payload_checksum=checksum,
            previous_hash=previous,
        )
        ref = self._audits.next_audit_ref(tenant_id)
        entry = SecurityAuditEntry.create(
            tenant_id=tenant_id,
            audit_ref=ref,
            action=action,
            actor_id=actor_id,
            resource_type=resource_type,
            resource_id=resource_id,
            payload_checksum=checksum,
            tamper_hash=tamper_hash,
            detail=detail,
        )
        await self._audits.save(entry)
        await publish_integration_event(
            BankingSecurityAuditRecordedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"audit-{entry.id}",
                audit_id=str(entry.id),
                action=action,
                actor_id=actor_id,
                tamper_hash=tamper_hash,
            )
        )
        return entry

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_security_catalog())

    async def list_policy_keys(self) -> Result[list[dict]]:
        return Result.ok(list_security_policy_keys())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        return Result.ok(
            build_security_dashboard(
                approvals=[a.to_dict() for a in await self._approvals.list_by_tenant(tenant_id)],
                alerts=[a.to_dict() for a in await self._alerts.list_by_tenant(tenant_id)],
                sessions=[s.to_dict() for s in await self._sessions.list_by_tenant(tenant_id)],
                freezes=[f.to_dict() for f in await self._freezes.list_by_tenant(tenant_id)],
                audits=[a.to_dict() for a in await self._audits.list_by_tenant(tenant_id)],
            )
        )

    async def evaluate_access(
        self,
        *,
        tenant_id: str,
        roles: list[str],
        permission: str,
        attributes: dict,
    ) -> Result[dict]:
        rbac_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="security.maker_checker.rules",
            facts={"permission": permission},
        )
        abac_policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="security.device.trust",
            facts=attributes,
        )
        result = evaluate_access(
            roles=roles,
            permission=permission,
            attributes=attributes,
            rbac_rules=rbac_policy.parameters,
            abac_rules=abac_policy.parameters,
        )
        await self._record_audit(
            tenant_id=tenant_id,
            action="access.evaluated",
            actor_id=attributes.get("user_id", "system"),
            resource_type="access",
            resource_id=permission,
            payload=result,
        )
        return Result.ok(result)

    async def check_limits(
        self,
        *,
        tenant_id: str,
        user_id: str,
        amount: float,
        currency: str = "USD",
    ) -> Result[dict]:
        today = datetime.now(UTC).date().isoformat()
        tracker = await self._limit_usage.get_for_user(tenant_id, user_id, today)
        if not tracker:
            tracker = LimitUsageTracker(
                id=UniqueId.generate(),
                tenant_id=tenant_id,
                user_id=user_id,
                usage_date=today,
                currency=currency,
            )

        tx_policy = await self._policy.evaluate(
            tenant_id=tenant_id, domain="bank", policy_key="security.transaction.limit", facts={"amount": amount}
        )
        daily_policy = await self._policy.evaluate(
            tenant_id=tenant_id, domain="bank", policy_key="security.daily.limit", facts={"user_id": user_id}
        )
        velocity_policy = await self._policy.evaluate(
            tenant_id=tenant_id, domain="bank", policy_key="security.velocity.limit", facts={"user_id": user_id}
        )

        single_limit = float(tx_policy.parameters.get("max_amount", 50000))
        daily_limit = float(daily_policy.parameters.get("max_daily", 100000))
        velocity_limit = int(velocity_policy.parameters.get("max_count", 50))

        ok, err = check_transaction_limit(amount=amount, single_limit=single_limit)
        if not ok:
            return Result.fail(f"banking.errors.{err}")
        ok, err = check_daily_limit(
            daily_total=tracker.daily_total, amount=amount, daily_limit=daily_limit
        )
        if not ok:
            return Result.fail(f"banking.errors.{err}")
        ok, err = check_velocity(velocity_count=tracker.velocity_count, velocity_limit=velocity_limit)
        if not ok:
            return Result.fail(f"banking.errors.{err}")

        return Result.ok(
            {
                "allowed": True,
                "daily_total": tracker.daily_total,
                "velocity_count": tracker.velocity_count,
                "limits": {
                    "single": single_limit,
                    "daily": daily_limit,
                    "velocity": velocity_limit,
                },
            }
        )

    async def register_device(
        self, *, tenant_id: str, user_id: str, device_fingerprint: str
    ) -> Result[dict]:
        existing = await self._devices.find_by_fingerprint(tenant_id, user_id, device_fingerprint)
        if existing:
            return Result.ok(existing.to_dict())
        ref = self._devices.next_device_ref(tenant_id)
        device = SecurityDevice.create(
            tenant_id=tenant_id,
            user_id=user_id,
            device_ref=ref,
            device_fingerprint=device_fingerprint,
        )
        await self._devices.save(device)
        return Result.ok(device.to_dict())

    async def verify_device(
        self, *, tenant_id: str, user_id: str, device_fingerprint: str
    ) -> Result[dict]:
        device = await self._devices.find_by_fingerprint(tenant_id, user_id, device_fingerprint)
        if not device:
            return Result.fail("banking.errors.device_not_found")
        policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="security.device.trust",
            facts={"user_id": user_id, "device_fingerprint": device_fingerprint},
        )
        if policy.outcome == "deny":
            return Result.fail("banking.errors.device_not_trusted")
        device.verify()
        await self._devices.save(device)
        await self._record_audit(
            tenant_id=tenant_id,
            action="device.verified",
            actor_id=user_id,
            resource_type="device",
            resource_id=str(device.id),
        )
        return Result.ok(device.to_dict())

    async def register_session(
        self,
        *,
        tenant_id: str,
        user_id: str,
        device_id: str | None = None,
        ip_address: str = "",
    ) -> Result[dict]:
        ref = self._sessions.next_session_ref(tenant_id)
        session = SecuritySession.create(
            tenant_id=tenant_id,
            user_id=user_id,
            session_ref=ref,
            device_id=device_id,
            ip_address=ip_address,
        )
        await self._sessions.save(session)
        return Result.ok(session.to_dict())

    async def session_heartbeat(
        self, *, session_id: str, risk_score: float | None = None
    ) -> Result[dict]:
        session = await self._sessions.find_by_id(session_id)
        if not session:
            return Result.fail("banking.errors.session_not_found")
        session.heartbeat(risk_score=risk_score)
        await self._sessions.save(session)
        return Result.ok(session.to_dict())

    async def monitor_transaction(
        self,
        *,
        tenant_id: str,
        user_id: str,
        action_type: str,
        amount: float,
        currency: str = "USD",
        risk_score: float = 0.0,
        factors: list[dict] | None = None,
    ) -> Result[dict]:
        policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="security.monitoring.threshold",
            facts={"action_type": action_type, "amount": amount, "risk_score": risk_score},
        )
        threshold = float(policy.parameters.get("alert_threshold", 40))
        ref = self._alerts.next_alert_ref(tenant_id)
        alert = TransactionMonitorAlert.create(
            tenant_id=tenant_id,
            alert_ref=ref,
            user_id=user_id,
            action_type=action_type,
            amount=amount,
            currency=currency,
            risk_score=risk_score,
            factors=factors,
        )
        if risk_score < threshold:
            alert.status = "open"
            await publish_integration_event(
                BankingSecurityAlertRaisedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=f"alert-{alert.id}",
                    alert_id=str(alert.id),
                    alert_ref=ref,
                    action_type=action_type,
                    risk_score=risk_score,
                )
            )
        else:
            alert.status = "clear"
        await self._alerts.save(alert)
        return Result.ok(alert.to_dict())

    async def assess_risk_auth(
        self,
        *,
        tenant_id: str,
        user_id: str,
        amount: float,
        device_trusted: bool,
        session_id: str | None = None,
    ) -> Result[dict]:
        session_risk = 100.0
        if session_id:
            session = await self._sessions.find_by_id(session_id)
            if session:
                session_risk = session.risk_score
        today = datetime.now(UTC).date().isoformat()
        tracker = await self._limit_usage.get_for_user(tenant_id, user_id, today)
        velocity = tracker.velocity_count if tracker else 0
        policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="security.risk.threshold",
            facts={"amount": amount, "device_trusted": device_trusted},
        )
        result = assess_risk(
            amount=amount,
            device_trusted=device_trusted,
            session_risk=session_risk,
            velocity_count=velocity,
            thresholds=policy.parameters,
        )
        return Result.ok(result)

    async def submit_approval(
        self,
        *,
        tenant_id: str,
        action_type: str,
        resource_id: str,
        maker_id: str,
        payload: dict | None = None,
        required_approvals: int | None = None,
    ) -> Result[dict]:
        checksum = checksum_payload(payload or {})
        if required_approvals is None:
            policy = await self._policy.evaluate(
                tenant_id=tenant_id,
                domain="bank",
                policy_key="security.critical.approval_required",
                facts={"action_type": action_type, "amount": (payload or {}).get("amount", 0)},
            )
            required_approvals = resolve_required_approvals(
                action_type=action_type,
                amount=float((payload or {}).get("amount", 0)),
                policy_params=policy.parameters,
            )
            if required_approvals == 0:
                required_approvals = 1

        ref = self._approvals.next_request_ref(tenant_id)
        request = SecurityApprovalRequest.create(
            tenant_id=tenant_id,
            request_ref=ref,
            action_type=action_type,
            resource_id=resource_id,
            maker_id=maker_id,
            payload_checksum=checksum,
            required_approvals=required_approvals,
        )
        signature = sign_operation(resource_id=resource_id, checksum=checksum, signer_id=maker_id)
        request.digital_signature = signature
        await self._approvals.save(request)
        await publish_integration_event(
            BankingSecurityApprovalSubmittedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"approval-{request.id}",
                request_id=str(request.id),
                request_ref=ref,
                action_type=action_type,
                maker_id=maker_id,
            )
        )
        await self._record_audit(
            tenant_id=tenant_id,
            action="approval.submitted",
            actor_id=maker_id,
            resource_type="approval",
            resource_id=str(request.id),
            payload={"action_type": action_type},
        )
        return Result.ok(request.to_dict())

    async def approve_request(self, *, request_id: str, approver_id: str) -> Result[dict]:
        request = await self._approvals.find_by_id(request_id)
        if not request:
            return Result.fail("banking.errors.approval_not_found")
        try:
            request.approve(approver_id)
        except ValueError as exc:
            return Result.fail(f"banking.errors.{str(exc)}")
        await self._approvals.save(request)
        if request.status == "approved":
            await publish_integration_event(
                BankingSecurityApprovalCompletedIntegration(
                    tenant_id=TenantId.create(request.tenant_id),
                    correlation_id=f"approval-done-{request.id}",
                    request_id=str(request.id),
                    request_ref=request.request_ref,
                    status=request.status,
                    approvers=request.approvers,
                )
            )
        await self._record_audit(
            tenant_id=request.tenant_id,
            action="approval.approved",
            actor_id=approver_id,
            resource_type="approval",
            resource_id=request_id,
        )
        return Result.ok(request.to_dict())

    async def authorize_critical_action(
        self,
        *,
        tenant_id: str,
        user_id: str,
        roles: list[str],
        action_type: str,
        resource_id: str,
        amount: float = 0.0,
        attributes: dict | None = None,
        device_fingerprint: str = "",
        session_id: str | None = None,
        payload: dict | None = None,
    ) -> Result[dict]:
        active_freeze = await self._freezes.find_active(tenant_id)
        if active_freeze:
            return Result.fail("banking.errors.emergency_freeze_active")

        access = await self.evaluate_access(
            tenant_id=tenant_id,
            roles=roles,
            permission=f"banking.{action_type}.execute",
            attributes={"user_id": user_id, **(attributes or {})},
        )
        if not access.unwrap().get("allowed"):
            return Result.fail("banking.errors.access_denied")

        limits = await self.check_limits(tenant_id=tenant_id, user_id=user_id, amount=amount)
        if not limits.succeeded:
            return limits

        device_trusted = False
        if device_fingerprint:
            device = await self._devices.find_by_fingerprint(tenant_id, user_id, device_fingerprint)
            device_trusted = bool(device and device.trusted)

        risk = await self.assess_risk_auth(
            tenant_id=tenant_id,
            user_id=user_id,
            amount=amount,
            device_trusted=device_trusted,
            session_id=session_id,
        )
        risk_data = risk.unwrap()
        if risk_data["level"] == "block":
            return Result.fail("banking.errors.risk_blocked")

        policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="security.critical.approval_required",
            facts={"action_type": action_type, "amount": amount},
        )
        required = resolve_required_approvals(
            action_type=action_type, amount=amount, policy_params=policy.parameters
        )
        approval_required = required > 0

        result_payload = {
            "authorized": not approval_required,
            "approval_required": approval_required,
            "required_approvals": required or 1,
            "risk": risk_data,
            "limits": limits.unwrap(),
        }

        if approval_required:
            approval = await self.submit_approval(
                tenant_id=tenant_id,
                action_type=action_type,
                resource_id=resource_id,
                maker_id=user_id,
                payload=payload or {"amount": amount},
                required_approvals=required or 1,
            )
            if not approval.succeeded:
                return approval
            result_payload["approval"] = approval.unwrap()
        else:
            today = datetime.now(UTC).date().isoformat()
            tracker = await self._limit_usage.get_for_user(tenant_id, user_id, today)
            if not tracker:
                tracker = LimitUsageTracker(
                    id=UniqueId.generate(),
                    tenant_id=tenant_id,
                    user_id=user_id,
                    usage_date=today,
                )
            tracker.add_transaction(amount)
            await self._limit_usage.save(tracker)
            await self._record_audit(
                tenant_id=tenant_id,
                action="action.authorized",
                actor_id=user_id,
                resource_type=action_type,
                resource_id=resource_id,
                payload=result_payload,
            )

        await self.monitor_transaction(
            tenant_id=tenant_id,
            user_id=user_id,
            action_type=action_type,
            amount=amount,
            risk_score=risk_data["risk_score"],
            factors=risk_data.get("factors"),
        )
        return Result.ok(result_payload)

    async def sign_payload(self, *, resource_id: str, payload: dict, signer_id: str) -> Result[dict]:
        checksum = checksum_payload(payload)
        return Result.ok(sign_operation(resource_id=resource_id, checksum=checksum, signer_id=signer_id))

    async def encrypt_data(self, *, payload: dict) -> Result[dict]:
        return Result.ok({"encrypted": encrypt_payload(payload)})

    async def activate_freeze(
        self, *, tenant_id: str, activated_by: str, reason: str = "", scope: str = "tenant"
    ) -> Result[dict]:
        existing = await self._freezes.find_active(tenant_id)
        if existing:
            return Result.fail("banking.errors.freeze_already_active")
        policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="security.emergency.freeze",
            facts={"activated_by": activated_by},
        )
        if policy.outcome == "deny":
            return Result.fail("banking.errors.freeze_denied")
        ref = self._freezes.next_freeze_ref(tenant_id)
        freeze = EmergencyFreeze.create(
            tenant_id=tenant_id,
            freeze_ref=ref,
            scope=scope,
            reason=reason,
            activated_by=activated_by,
        )
        await self._freezes.save(freeze)
        await publish_integration_event(
            BankingSecurityFreezeActivatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"freeze-{freeze.id}",
                freeze_id=str(freeze.id),
                freeze_ref=ref,
                scope=scope,
                activated_by=activated_by,
            )
        )
        await self._record_audit(
            tenant_id=tenant_id,
            action="freeze.activated",
            actor_id=activated_by,
            resource_type="freeze",
            resource_id=str(freeze.id),
            detail=reason,
        )
        return Result.ok(freeze.to_dict())

    async def release_freeze(self, *, tenant_id: str, released_by: str) -> Result[dict]:
        freeze = await self._freezes.find_active(tenant_id)
        if not freeze:
            return Result.fail("banking.errors.no_active_freeze")
        freeze.release()
        await self._freezes.save(freeze)
        await self._record_audit(
            tenant_id=tenant_id,
            action="freeze.released",
            actor_id=released_by,
            resource_type="freeze",
            resource_id=str(freeze.id),
        )
        return Result.ok(freeze.to_dict())

    async def get_audit_trail(self, tenant_id: str) -> Result[list[dict]]:
        entries = await self._audits.list_by_tenant(tenant_id)
        return Result.ok([e.to_dict() for e in entries])

    async def verify_audit_trail(self, tenant_id: str) -> Result[dict]:
        entries = sorted(
            await self._audits.list_by_tenant(tenant_id), key=lambda e: e.created_at
        )
        previous: str | None = None
        valid = True
        for entry in entries:
            if not verify_tamper(
                tamper_hash=entry.tamper_hash,
                action=entry.action,
                actor_id=entry.actor_id,
                resource_id=entry.resource_id,
                payload_checksum=entry.payload_checksum,
                previous_hash=previous,
            ):
                valid = False
                break
            previous = entry.tamper_hash
        return Result.ok({"valid": valid, "entry_count": len(entries)})

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        pass
