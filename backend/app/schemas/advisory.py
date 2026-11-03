from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.risk import RiskLevel


class FarmingActionPlanDay(BaseModel):
    day: int
    day_label: str
    date_str: str
    forecast_summary: str
    forecast_summary_hi: str
    recommended_actions_en: List[str]
    recommended_actions_hi: List[str]
    what_to_monitor_en: str
    what_to_monitor_hi: str


class AdvisoryResponse(BaseModel):
    crop: str
    crop_hi: str
    growth_stage: str
    growth_stage_hi: str
    location: str
    overall_risk_level: RiskLevel
    summary_en: str
    summary_hi: str
    immediate_precautions_en: List[str]
    immediate_precautions_hi: List[str]
    action_plan_3d: List[FarmingActionPlanDay]
    general_precautions_en: List[str]
    general_precautions_hi: List[str]
    official_advisory_note_en: str
    official_advisory_note_hi: str
    forecast_timestamp: str
    data_sources: List[str]

