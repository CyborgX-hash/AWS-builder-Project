from strands import Agent
from app.tools.risk_tool import evaluate_climate_risks
from app.agents.model_factory import get_bedrock_model

RISK_AGENT_SYSTEM_PROMPT = """You are the Climate Risk Assessment Specialist Agent for KrishiSathi.
Your responsibility is to analyze agro-climatic risks by invoking the deterministic mathematical risk engine.

Core Directives:
1. NEVER generate or hallucinate arbitrary numerical risk scores or thresholds.
2. ALWAYS call the `evaluate_climate_risks` tool to execute the deterministic calculation engine.
3. Interpret the computed output accurately:
   - Risk Categories: Heat Stress, Excessive Rainfall, Waterlogging, Dry-spell, Crop Water Stress.
   - Classification: LOW, MODERATE, HIGH.
   - Explain the specific contributing meteorological variables (temperatures, rainfall sums, dry streak length).
   - Communicate confidence levels and screening limitations honestly.
4. Distinguish screening assessments from absolute predictions of crop damage.
"""


def create_risk_agent() -> Agent:
    """Instantiate the Strands Risk Assessment Agent."""
    return Agent(
        model=get_bedrock_model(),
        name="RiskAssessmentAgent",
        description="Executes deterministic agro-climatic risk analysis for heat stress, excessive rain, waterlogging, dry spells, and water stress.",
        tools=[evaluate_climate_risks],
        system_prompt=RISK_AGENT_SYSTEM_PROMPT
    )
