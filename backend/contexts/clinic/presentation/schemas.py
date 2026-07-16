"""Clinic API schemas."""
from pydantic import BaseModel, Field, model_validator


class RegisterPatientRequest(BaseModel):
    patient_number: str = Field(min_length=3, max_length=32)
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str = Field(min_length=1, max_length=64)
    date_of_birth: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    document_id: str | None = None


class ScheduleAppointmentRequest(BaseModel):
    patient_id: str
    provider_name: str = Field(min_length=1, max_length=128)
    scheduled_at: str


class StartEncounterRequest(BaseModel):
    appointment_id: str | None = None
    patient_id: str | None = None

    @model_validator(mode="after")
    def require_appointment_or_patient(self) -> StartEncounterRequest:
        if not self.appointment_id and not self.patient_id:
            raise ValueError("appointment_id or patient_id is required")
        return self


class CompleteEncounterRequest(BaseModel):
    diagnosis_codes: list[str] = Field(default_factory=list)


class CreateReferralRequest(BaseModel):
    encounter_id: str
    target_specialty: str = Field(min_length=1, max_length=128)
    reason: str = Field(min_length=1, max_length=512)
    send: bool = False
