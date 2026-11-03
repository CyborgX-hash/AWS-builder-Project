from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class GrowthStageDetail(BaseModel):
    stage_name: str
    stage_name_hi: str
    duration_days: str
    temp_min_c: float
    temp_opt_min_c: float
    temp_opt_max_c: float
    temp_max_c: float
    daily_water_need_mm: float
    excess_rain_tolerance_mm_day: float
    vulnerable_risks: List[str]
    stage_monitoring_tips: List[str]
    stage_monitoring_tips_hi: List[str]


class CropProfileSchema(BaseModel):
    crop_name: str
    crop_name_hi: str
    scientific_name: str
    category: str
    major_regions: List[str]
    growth_stages: List[GrowthStageDetail]
    soil_preferences: str
    sourced_references: List[str]
    notes: Optional[str] = None

