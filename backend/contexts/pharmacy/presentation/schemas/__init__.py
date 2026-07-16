"""Pharmacy API schemas."""
from pydantic import BaseModel, Field


class ReceivePrescriptionRequest(BaseModel):
    rx_number: str = Field(min_length=3, max_length=32)
    patient_ref: str = Field(min_length=1, max_length=64)
    drug_code: str = Field(min_length=1, max_length=32)
    drug_name: str = Field(min_length=1, max_length=128)
    quantity: float = Field(gt=0)
    source_encounter_ref: str | None = None


class DispenseRequest(BaseModel):
    prescription_id: str
    quantity_dispensed: float | None = Field(default=None, gt=0)
