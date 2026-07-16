"""Laboratory API schemas."""
from pydantic import BaseModel, Field


class PlaceOrderRequest(BaseModel):
    order_number: str = Field(min_length=3, max_length=32)
    patient_ref: str = Field(min_length=1, max_length=64)
    test_code: str = Field(min_length=1, max_length=32)
    source_encounter_ref: str | None = None


class ReceiveSampleRequest(BaseModel):
    order_id: str
    accession_number: str = Field(min_length=3, max_length=32)
    specimen_type: str = Field(min_length=1, max_length=64)


class FinalizeResultRequest(BaseModel):
    result_value: str = Field(min_length=1, max_length=256)
    result_unit: str | None = Field(default=None, max_length=32)
