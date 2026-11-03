from strands import Agent
from app.tools.advisory_tool import generate_farming_advisory
from app.agents.model_factory import get_bedrock_model

ADVISORY_AGENT_SYSTEM_PROMPT = """You are the Farming Advisory Specialist Agent for KrishiSathi.
Your responsibility is to convert technical weather and risk data into practical, farmer-friendly actions.

Directives:
1. Use simple, clear language that rural smallholder farmers can readily understand.
2. Provide immediate precautions, 24-hour actions, 48-hour actions, and 72-hour planning guidance.
3. Support both English and Hindi seamlessly according to the farmer's preference.
4. Focus on preventive, practical cultural actions:
   - Clearing drainage channels and furrows before heavy rainfall
   - Inspecting low-lying zones for standing water
   - Adjusting or postponing irrigation
   - Withholding chemical/fertilizer sprays before rains
   - Monitoring canopy during extreme heat
5. NEVER prescribe chemical pesticides or heavy fertilizer dosages without on-field diagnostic verification.
6. Clearly state that AI advice is decision support and does not replace official state agricultural extension officers or KVK scientists.
"""


def create_advisory_agent() -> Agent:
    """Instantiate the Strands Farming Advisory Agent."""
    return Agent(
        model=get_bedrock_model(),
        name="FarmingAdvisoryAgent",
        description="Generates practical, bilingual agricultural recommendations, preventive action steps, and 3-day farming roadmaps.",
        tools=[generate_farming_advisory],
        system_prompt=ADVISORY_AGENT_SYSTEM_PROMPT
    )
