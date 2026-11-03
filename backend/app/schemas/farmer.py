from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
import datetime


class FarmerBase(BaseModel):
    name: Optional[str] = None
    preferred_language: str = "en"
    location: str
    latitude: float
    longitude: float


class FarmerCreate(FarmerBase):
    crop_name: Optional[str] = None
    growth_stage: Optional[str] = None


class FarmerOut(FarmerBase):
    id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class AdvisoryGenerateRequest(BaseModel):
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    crop: str
    growth_stage: Optional[str] = "Vegetative"
    language: Optional[str] = "en"
