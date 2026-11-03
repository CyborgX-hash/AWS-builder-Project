from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"


class RiskCategory(str, Enum):
    HEAT_STRESS = "heat_stress"
    EXCESSIVE_RAINFALL = "excessive_rainfall"
    WATERLOGGING = "waterlogging"
    DRY_SPELL = "dry_spell"
    WATER_STRESS = "water_stress"


class SingleRiskAssessment(BaseModel):
    category: RiskCategory
    category_title: str
    category_title_hi: str
    risk_level: RiskLevel
    risk_score: float = Field(..., ge=0.0, le=100.0, description="Deterministic risk score 0 to 100")
    relevant_weather_variables: Dict[str, Any]
    reason_en: str
    reason_hi: str
    recommended_monitoring_en: str
    recommended_monitoring_hi: str
    data_confidence: str  # "HIGH", "MODERATE", "LOW"
    is_provisional_rule: bool = False


class ComprehensiveRiskReport(BaseModel):
    crop: str
    growth_stage: str
    location: str
    overall_risk_level: RiskLevel
    assessments: List[SingleRiskAssessment]
    calculation_timestamp: str
    data_sources: List[str]
    limitations_disclaimer: str

