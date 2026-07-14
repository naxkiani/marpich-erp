from pydantic import BaseModel, Field
class CreateTwinRequest(BaseModel):
    identity_ref: str
    attributes: dict = Field(default_factory=dict)
class SyncTwinRequest(BaseModel):
    projection: dict = Field(default_factory=dict)
    source_event: str
class SimulateTwinRequest(BaseModel):
    scenario_type: str
    proposed_change: dict = Field(default_factory=dict)
class DetectDriftRequest(BaseModel):
    observed_projection: dict = Field(default_factory=dict)
    source_event: str
