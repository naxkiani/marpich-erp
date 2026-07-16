"""Enterprise Security Incident Platform application service."""
from __future__ import annotations

import hashlib

from contexts.security_incident.domain.aggregates.incident_platform import (
    IncidentClassification,
    IncidentEvidence,
    IncidentLessonLearned,
    IncidentNotification,
    IncidentSeverity,
    IncidentStatus,
    IncidentTenantProfile,
    SecurityIncident,
)
from contexts.security_incident.domain.events.incident_integration_events import (
    IncidentClassifiedIntegration,
    IncidentContainedIntegration,
    IncidentDetectedIntegration,
    IncidentEscalatedIntegration,
    IncidentEvidenceCollectedIntegration,
    IncidentNotificationSentIntegration,
    IncidentResolvedIntegration,
)
from contexts.security_incident.domain.ports.incident_repositories import (
    IIncidentEvidenceRepository,
    IIncidentLessonLearnedRepository,
    IIncidentNotificationRepository,
    IIncidentTenantProfileRepository,
    ISecurityIncidentRepository,
)
from contexts.security_incident.domain.services import incident_engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class SecurityIncidentApplicationService:
    def __init__(
        self,
        profiles: IIncidentTenantProfileRepository,
        incidents: ISecurityIncidentRepository,
        evidence: IIncidentEvidenceRepository,
        notifications: IIncidentNotificationRepository,
        lessons: IIncidentLessonLearnedRepository,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._incidents = incidents
        self._evidence = evidence
        self._notifications = notifications
        self._lessons = lessons
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        params = {
            "sensitivity_threshold": 0.7,
            "escalation_severity": "high",
            "response_hours": 4,
            "resolution_hours": 72,
            "auto_notify": True,
        }
        pmap = {
            "incident.detection.sensitivity_threshold": ("sensitivity_threshold", "sensitivity_threshold"),
            "incident.escalation.severity_threshold": ("escalation_severity", "severity_threshold"),
            "incident.sla.response_hours": ("response_hours", "response_hours"),
            "incident.sla.resolution_hours": ("resolution_hours", "resolution_hours"),
            "incident.notification.auto_notify": ("auto_notify", "auto_notify"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(
                tenant_id=tenant_id, domain="tax", policy_key=key, facts={}
            )
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": incident_engine.list_capability_catalog(),
            "classifications": incident_engine.list_classifications(),
            "policy_keys": incident_engine.list_policy_keys(),
            "shared_service": True,
            "delegation": {
                "security_attack_monitoring": True,
                "workflow_emergency_lock": True,
                "audit_trail": True,
                "local_incident_duplication": False,
            },
        })

    async def get_dependency_map(self) -> Result[dict]:
        return Result.ok(incident_engine.dependency_map())

    async def seed(self, tenant_id: str) -> Result[dict]:
        existing = await self._profiles.find_by_tenant(tenant_id)
        if existing:
            return Result.ok({
                "seeded": False,
                "profile": existing.to_dict(),
                "incidents": len(await self._incidents.list_by_tenant(tenant_id)),
            })

        params = await self._policy_params(tenant_id)
        ref = self._profiles.next_profile_ref(tenant_id)
        profile = IncidentTenantProfile.create(
            tenant_id=tenant_id,
            profile_ref=ref,
            enabled_classifications=[c.value for c in IncidentClassification],
        )
        profile.response_sla_hours = int(params.get("response_hours", 4))
        profile.resolution_sla_hours = int(params.get("resolution_hours", 72))
        profile.escalation_severity = str(params.get("escalation_severity", "high"))
        profile.auto_notify = bool(params.get("auto_notify", True))
        await self._profiles.save(profile)

        seeded = 0
        for seed_inc in incident_engine.DEFAULT_SEED_INCIDENTS:
            incident_ref = self._incidents.next_incident_ref(tenant_id)
            deadlines = incident_engine.compute_sla_deadlines(
                response_hours=profile.response_sla_hours,
                resolution_hours=profile.resolution_sla_hours,
            )
            item = SecurityIncident.detect(
                tenant_id=tenant_id,
                incident_ref=incident_ref,
                title=seed_inc["title"],
                description=seed_inc["description"],
                classification=seed_inc["classification"],
                severity=seed_inc["severity"],
                source_module="security_incident",
                delegated_to=seed_inc.get("delegated_to"),
                response_due_at=deadlines["response_due_at"],
                resolution_due_at=deadlines["resolution_due_at"],
            )
            item.status = seed_inc.get("status", IncidentStatus.DETECTED.value)
            item.sla_status = incident_engine.evaluate_sla(
                incident=item.to_dict(),
                response_hours=profile.response_sla_hours,
                resolution_hours=profile.resolution_sla_hours,
            )
            await self._incidents.save(item)
            seeded += 1

        return Result.ok({
            "seeded": True,
            "profile": profile.to_dict(),
            "incidents_seeded": seeded,
            "enabled_classifications": len(profile.enabled_classifications),
        })

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        incidents = [i.to_dict() for i in await self._incidents.list_by_tenant(tenant_id)]
        evidence = [e.to_dict() for e in await self._evidence.list_by_tenant(tenant_id)]
        notifications = [n.to_dict() for n in await self._notifications.list_by_tenant(tenant_id)]
        lessons = [l.to_dict() for l in await self._lessons.list_by_tenant(tenant_id)]
        return Result.ok(
            incident_engine.build_dashboard(
                profile=profile.to_dict() if profile else None,
                incidents=incidents,
                evidence=evidence,
                notifications=notifications,
                lessons=lessons,
            )
        )

    async def list_incidents(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._incidents.list_by_tenant(tenant_id)
        return Result.ok([i.to_dict() for i in items])

    async def get_incident(self, tenant_id: str, incident_ref: str) -> Result[dict]:
        item = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not item:
            return Result.fail("incident_not_found")
        return Result.ok(item.to_dict())

    async def detect_incident(
        self,
        tenant_id: str,
        *,
        title: str,
        description: str,
        classification: str,
        severity: str,
        detected_by: str = "",
        source_module: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        if classification not in {c.value for c in IncidentClassification}:
            return Result.fail("invalid_classification")
        if severity not in {s.value for s in IncidentSeverity}:
            return Result.fail("invalid_severity")

        params = await self._policy_params(tenant_id)
        profile = await self._profiles.find_by_tenant(tenant_id)
        response_hours = profile.response_sla_hours if profile else int(params.get("response_hours", 4))
        resolution_hours = profile.resolution_sla_hours if profile else int(params.get("resolution_hours", 72))
        deadlines = incident_engine.compute_sla_deadlines(
            response_hours=response_hours,
            resolution_hours=resolution_hours,
        )
        delegated = incident_engine.CLASSIFICATION_DELEGATION.get(classification)
        incident_ref = self._incidents.next_incident_ref(tenant_id)

        item = SecurityIncident.detect(
            tenant_id=tenant_id,
            incident_ref=incident_ref,
            title=title,
            description=description,
            classification=classification,
            severity=severity,
            detected_by=detected_by,
            source_module=source_module or "security_incident",
            delegated_to=delegated,
            response_due_at=deadlines["response_due_at"],
            resolution_due_at=deadlines["resolution_due_at"],
        )
        await self._incidents.save(item)

        corr = correlation_id or incident_ref
        await publish_integration_event(
            IncidentDetectedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                incident_ref=incident_ref,
                classification=classification,
                severity=severity,
            )
        )

        threshold = str(params.get("escalation_severity", "high"))
        if incident_engine.should_auto_escalate(severity, threshold):
            item.escalate()
            await self._incidents.save(item)
            await publish_integration_event(
                IncidentEscalatedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=corr,
                    incident_ref=incident_ref,
                    severity=severity,
                )
            )

        if bool(params.get("auto_notify", True)):
            await self._send_notification(
                tenant_id, incident_ref, item.title, severity, corr,
                recipient="security-team@enterprise.dev",
            )

        return Result.ok(item.to_dict())

    async def classify_incident(
        self,
        tenant_id: str,
        incident_ref: str,
        *,
        classification: str,
        severity: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        item = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not item:
            return Result.fail("incident_not_found")
        item.classify(classification, severity)
        item.delegated_to = incident_engine.CLASSIFICATION_DELEGATION.get(classification)
        await self._incidents.save(item)

        corr = correlation_id or incident_ref
        await publish_integration_event(
            IncidentClassifiedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                incident_ref=incident_ref,
                classification=classification,
                severity=severity,
            )
        )
        return Result.ok(item.to_dict())

    async def investigate_incident(
        self,
        tenant_id: str,
        incident_ref: str,
        *,
        assigned_to: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        item = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not item:
            return Result.fail("incident_not_found")
        item.start_investigation(assigned_to)
        await self._incidents.save(item)
        return Result.ok(item.to_dict())

    async def contain_incident(
        self,
        tenant_id: str,
        incident_ref: str,
        *,
        actions: list[str],
        correlation_id: str = "",
    ) -> Result[dict]:
        item = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not item:
            return Result.fail("incident_not_found")
        item.contain(actions)
        await self._incidents.save(item)

        corr = correlation_id or incident_ref
        await publish_integration_event(
            IncidentContainedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                incident_ref=incident_ref,
                actions=actions,
            )
        )
        return Result.ok(item.to_dict())

    async def recover_incident(
        self,
        tenant_id: str,
        incident_ref: str,
        *,
        actions: list[str],
        correlation_id: str = "",
    ) -> Result[dict]:
        item = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not item:
            return Result.fail("incident_not_found")
        item.recover(actions)
        await self._incidents.save(item)
        return Result.ok(item.to_dict())

    async def set_root_cause(
        self,
        tenant_id: str,
        incident_ref: str,
        *,
        root_cause: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        item = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not item:
            return Result.fail("incident_not_found")
        item.set_root_cause(root_cause)
        await self._incidents.save(item)
        return Result.ok(item.to_dict())

    async def run_forensics(
        self,
        tenant_id: str,
        incident_ref: str,
        *,
        correlation_id: str = "",
    ) -> Result[dict]:
        item = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not item:
            return Result.fail("incident_not_found")

        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile and not profile.forensics_enabled:
            return Result.fail("forensics_disabled")

        evidence = [e.to_dict() for e in await self._evidence.list_by_incident(tenant_id, incident_ref)]
        analysis = incident_engine.digital_forensics_analysis(
            incident=item.to_dict(), evidence=evidence
        )
        summary = f"{len(analysis['findings'])} findings from {analysis['evidence_reviewed']} evidence items"
        item.set_forensics(summary)
        await self._incidents.save(item)
        return Result.ok({**analysis, "forensics_summary": summary})

    async def escalate_incident(
        self,
        tenant_id: str,
        incident_ref: str,
        *,
        correlation_id: str = "",
    ) -> Result[dict]:
        item = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not item:
            return Result.fail("incident_not_found")
        item.escalate()
        await self._incidents.save(item)

        corr = correlation_id or incident_ref
        await publish_integration_event(
            IncidentEscalatedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                incident_ref=incident_ref,
                severity=item.severity,
            )
        )
        return Result.ok(item.to_dict())

    async def resolve_incident(
        self,
        tenant_id: str,
        incident_ref: str,
        *,
        root_cause: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        item = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not item:
            return Result.fail("incident_not_found")
        if root_cause:
            item.set_root_cause(root_cause)
        item.resolve()
        await self._incidents.save(item)

        corr = correlation_id or incident_ref
        await publish_integration_event(
            IncidentResolvedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                incident_ref=incident_ref,
                root_cause=item.root_cause,
            )
        )
        return Result.ok(item.to_dict())

    async def collect_evidence(
        self,
        tenant_id: str,
        incident_ref: str,
        *,
        evidence_type: str,
        description: str,
        collected_by: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        item = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not item:
            return Result.fail("incident_not_found")

        evidence_ref = self._evidence.next_evidence_ref(tenant_id)
        digest = hashlib.sha256(f"{evidence_ref}:{description}".encode()).hexdigest()[:16]
        ev = IncidentEvidence.collect(
            tenant_id=tenant_id,
            evidence_ref=evidence_ref,
            incident_ref=incident_ref,
            evidence_type=evidence_type,
            description=description,
            collected_by=collected_by,
            hash_digest=digest,
        )
        await self._evidence.save(ev)

        corr = correlation_id or evidence_ref
        await publish_integration_event(
            IncidentEvidenceCollectedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=corr,
                incident_ref=incident_ref,
                evidence_ref=evidence_ref,
                evidence_type=evidence_type,
            )
        )
        return Result.ok(ev.to_dict())

    async def list_evidence(self, tenant_id: str, incident_ref: str) -> Result[list[dict]]:
        items = await self._evidence.list_by_incident(tenant_id, incident_ref)
        return Result.ok([e.to_dict() for e in items])

    async def record_lesson(
        self,
        tenant_id: str,
        incident_ref: str,
        *,
        title: str,
        summary: str,
        recommendations: list[str],
        author_id: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        item = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not item:
            return Result.fail("incident_not_found")

        lesson_ref = self._lessons.next_lesson_ref(tenant_id)
        lesson = IncidentLessonLearned.record(
            tenant_id=tenant_id,
            lesson_ref=lesson_ref,
            incident_ref=incident_ref,
            title=title,
            summary=summary,
            recommendations=recommendations,
            author_id=author_id,
        )
        await self._lessons.save(lesson)
        return Result.ok(lesson.to_dict())

    async def list_lessons(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._lessons.list_by_tenant(tenant_id)
        return Result.ok([l.to_dict() for l in items])

    async def notify_incident(
        self,
        tenant_id: str,
        incident_ref: str,
        *,
        channel: str,
        recipient: str,
        subject: str = "",
        message: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        item = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not item:
            return Result.fail("incident_not_found")

        notif = await self._send_notification(
            tenant_id,
            incident_ref,
            subject or item.title,
            item.severity,
            correlation_id or incident_ref,
            channel=channel,
            recipient=recipient,
            message=message,
        )
        return Result.ok(notif)

    async def list_notifications(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._notifications.list_by_tenant(tenant_id)
        return Result.ok([n.to_dict() for n in items])

    async def get_sla_status(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = await self._policy_params(tenant_id)
        response_hours = profile.response_sla_hours if profile else int(params.get("response_hours", 4))
        resolution_hours = profile.resolution_sla_hours if profile else int(params.get("resolution_hours", 72))

        incidents = await self._incidents.list_by_tenant(tenant_id)
        sla_items = []
        for inc in incidents:
            status = incident_engine.evaluate_sla(
                incident=inc.to_dict(),
                response_hours=response_hours,
                resolution_hours=resolution_hours,
            )
            if inc.sla_status != status:
                inc.update_sla(status)
                await self._incidents.save(inc)
            sla_items.append({
                "incident_ref": inc.incident_ref,
                "title": inc.title,
                "severity": inc.severity,
                "status": inc.status,
                "sla_status": status,
                "response_due_at": inc.response_due_at,
                "resolution_due_at": inc.resolution_due_at,
            })

        breached = len([s for s in sla_items if s["sla_status"] == "breached"])
        at_risk = len([s for s in sla_items if s["sla_status"] == "at_risk"])

        return Result.ok({
            "response_sla_hours": response_hours,
            "resolution_sla_hours": resolution_hours,
            "incidents": sla_items,
            "summary": {
                "total": len(sla_items),
                "breached": breached,
                "at_risk": at_risk,
                "on_track": len(sla_items) - breached - at_risk,
            },
        })

    async def _send_notification(
        self,
        tenant_id: str,
        incident_ref: str,
        title: str,
        severity: str,
        correlation_id: str,
        *,
        channel: str = "email",
        recipient: str = "security-team@enterprise.dev",
        message: str = "",
    ) -> dict:
        notification_ref = self._notifications.next_notification_ref(tenant_id)
        notif = IncidentNotification.send(
            tenant_id=tenant_id,
            notification_ref=notification_ref,
            incident_ref=incident_ref,
            channel=channel,
            recipient=recipient,
            subject=f"[{severity.upper()}] Security Incident: {title}",
            message=message or f"Incident {incident_ref} requires attention. Severity: {severity}",
        )
        await self._notifications.save(notif)

        await publish_integration_event(
            IncidentNotificationSentIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                incident_ref=incident_ref,
                notification_ref=notification_ref,
                channel=channel,
            )
        )
        return notif.to_dict()

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope.get("tenant_id", "")
        if tenant_id:
            await self.seed(tenant_id)

    async def handle_security_attack_detected(self, envelope: dict) -> None:
        payload = envelope.get("payload", {})
        tenant_id = envelope.get("tenant_id", "")
        if not tenant_id:
            return
        await self.detect_incident(
            tenant_id,
            title=payload.get("title", "Security attack detected"),
            description=payload.get("description", "Attack event from security platform"),
            classification=IncidentClassification.CYBER.value,
            severity=IncidentSeverity.HIGH.value,
            source_module="security",
            detected_by="security_platform",
            correlation_id=envelope.get("correlation_id", ""),
        )
