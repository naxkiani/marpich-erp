"""Google Classroom connector adapter — Integration Platform only."""
from __future__ import annotations

from shared.application.result import Result
from shared.connectors.stub_adapter import BaseConnectorAdapter

_OPS = ["courses_sync", "rosters_sync", "assignments_sync", "test_connection"]


class GoogleClassroomAdapter(BaseConnectorAdapter):
    def __init__(self) -> None:
        super().__init__("google_classroom", _OPS)

    async def test_connection(self, *, config: dict, secret: str = "") -> Result[dict]:
        if not config.get("customer_id") and not config.get("service_account_ref"):
            return Result.fail("classroom.customer_or_sa_required")
        return Result.ok(
            {
                "connector_type": self.connector_type,
                "connected": True,
                "latency_ms": 48,
                "environment": config.get("environment", "sandbox"),
            }
        )

    async def execute(
        self,
        *,
        operation: str,
        payload: dict,
        config: dict,
        secret: str = "",
        idempotency_key: str = "",
    ) -> Result[dict]:
        if operation not in self._operations:
            return Result.fail(f"unsupported_operation:{operation}")
        if operation == "test_connection":
            return await self.test_connection(config=config, secret=secret)

        fixtures = config.get("fixtures") if isinstance(config.get("fixtures"), dict) else {}
        if operation == "courses_sync":
            courses = fixtures.get("courses") or [
                {
                    "lms_course_id": "gc-ENG110",
                    "course_code": "ENG110",
                    "title": "Composition (Classroom)",
                    "credits": 3,
                    "term": "FALL26",
                }
            ]
            return Result.ok(self._wrap(operation, idempotency_key, {"courses": courses}))

        if operation == "rosters_sync":
            enrollments = fixtures.get("rosters") or fixtures.get("enrollments") or [
                {
                    "lms_user_id": "gc-u-2001",
                    "student_number": "S2001",
                    "first_name": "Grace",
                    "last_name": "Hopper",
                    "email": "grace@classroom.demo",
                    "program_code": "ENG",
                    "lms_course_id": "gc-ENG110",
                }
            ]
            return Result.ok(self._wrap(operation, idempotency_key, {"enrollments": enrollments}))

        assignments = fixtures.get("assignments") or [
            {"lms_assignment_id": "gc-a-1", "lms_course_id": "gc-ENG110", "title": "Essay 1"}
        ]
        return Result.ok(self._wrap(operation, idempotency_key, {"assignments": assignments}))

    def _wrap(self, operation: str, idempotency_key: str, data: dict) -> dict:
        return {
            "connector_type": self.connector_type,
            "operation": operation,
            "status": "completed",
            "provider": "google_classroom",
            "idempotency_key": idempotency_key or None,
            "result": {"simulated": True, **data},
        }
