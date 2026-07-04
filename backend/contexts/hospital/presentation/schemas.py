"""Hospital API schemas."""
from pydantic import BaseModel, Field


class RegisterPatientRequest(BaseModel):
    mrn: str = Field(min_length=3, max_length=32)
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str = Field(min_length=1, max_length=64)
    date_of_birth: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")


class AdmitPatientRequest(BaseModel):
    patient_id: str
    ward: str = Field(min_length=1, max_length=64)


class StartEncounterRequest(BaseModel):
    admission_id: str


class CompleteEncounterRequest(BaseModel):
    procedure_codes: list[str] = Field(default_factory=list)
    diagnosis_codes: list[str] = Field(default_factory=list)
