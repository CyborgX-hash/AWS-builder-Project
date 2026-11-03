import re
import logging
from typing import Dict, Any, List, Optional
from strands import Agent

from app.agents.weather_agent import create_weather_agent
from app.agents.crop_agent import create_crop_agent
from app.agents.risk_agent import create_risk_agent
from app.agents.advisory_agent import create_advisory_agent
from app.agents.model_factory import get_bedrock_model
from app.services.weather_service import WeatherService
from app.services.risk_engine import DeterministicRiskEngine
from app.services.advisory_service import AdvisoryService
from app.schemas.chat import ChatResponse, AgentTraceStep
from app.schemas.risk import RiskLevel

logger = logging.getLogger("krishisathi.orchestrator")

ORCHESTRATOR_SYSTEM_PROMPT = """You are Krishi Orchestrator, the central AI agricultural coordinator for KrishiSathi.
Your mission is to help Indian smallholder farmers make smarter agricultural decisions using hyperlocal weather intelligence.

You manage four specialist agents:
1. WeatherIntelligenceAgent: Retrieves live observations, rainfall probabilities, and 7-day forecast models.
2. CropIntelligenceAgent: Provides crop sensitivity thresholds, growth stage requirements, and vulnerability data.
3. RiskAssessmentAgent: Runs the deterministic Python risk engine (Heat stress, Excessive rain, Waterlogging, Dry spell, Water stress).
4. FarmingAdvisoryAgent: Generates practical, preventive farming action plans in simple Hindi or English.

Workflow:
1. Parse user query for location, crop, growth stage, and concern.
2. Delegate to specialist agents systematically.
3. Collect and validate their findings.
4. Produce a structured, compassionate, and farmer-friendly advisory in the requested language.
5. Emphasize what the farmer should monitor today and tomorrow.
"""


class KrishiOrchestrator:
    """Hierarchical Multi-Agent Orchestrator using Strands Agents SDK."""

    def __init__(self):
        self.weather_agent = create_weather_agent()
        self.crop_agent = create_crop_agent()
        self.risk_agent = create_risk_agent()
        self.advisory_agent = create_advisory_agent()

        # Main Strands Agent with 4 specialists as tools
        self.strands_agent = Agent(
            model=get_bedrock_model(),
            name="KrishiOrchestrator",
            description="Central agricultural coordinator that analyzes farmer queries and delegates to specialist agents.",
            tools=[self.weather_agent, self.crop_agent, self.risk_agent, self.advisory_agent],
            system_prompt=ORCHESTRATOR_SYSTEM_PROMPT
        )

    def extract_entities(self, query: str, context_loc: Optional[str] = None, context_crop: Optional[str] = None, context_stage: Optional[str] = None) -> Dict[str, Any]:
        """Extract agricultural intent, location, crop, and growth stage from text."""
        q_lower = query.lower()

        # Detect crop
        detected_crop = context_crop or "Soybean"
        if "soybean" in q_lower or "soya" in q_lower or "सोयाबीन" in query:
            detected_crop = "Soybean"
        elif "rice" in q_lower or "paddy" in q_lower or "dhan" in q_lower or "धान" in query or "चावल" in query:
            detected_crop = "Rice"
        elif "wheat" in q_lower or "gehun" in q_lower or "gehu" in q_lower or "गेहूं" in query:
            detected_crop = "Wheat"
        elif "maize" in q_lower or "corn" in q_lower or "makka" in q_lower or "मक्का" in query:
            detected_crop = "Maize"
        elif "cotton" in q_lower or "kapas" in q_lower or "कपास" in query:
            detected_crop = "Cotton"

        # Detect growth stage
        detected_stage = context_stage or "Vegetative"
        if "flower" in q_lower or "फूल" in query:
            detected_stage = "Flowering"
        elif "germinat" in q_lower or "sow" in q_lower or "अंकुरण" in query or "बुवाई" in query:
            detected_stage = "Germination / Emergence"
        elif "pod" in q_lower or "grain" in q_lower or "फली" in query or "दाना" in query or "दूधिया" in query:
            detected_stage = "Pod Development / Seed Filling" if detected_crop == "Soybean" else "Grain Filling / Dough Stage"
        elif "harvest" in q_lower or "matur" in q_lower or "कटाई" in query or "पकी" in query:
            detected_stage = "Maturity / Harvest"

        # Detect location
        detected_location = context_loc or "Balaghat"
        common_locations = {
            "balaghat": "Balaghat",
            "बालाघाट": "Balaghat",
            "indore": "Indore",
            "इंदौर": "Indore",
            "bhopal": "Bhopal",
            "भोपाल": "Bhopal",
            "seoni": "Seoni",
            "सिवनी": "Seoni",
            "nagpur": "Nagpur",
            "नागपुर": "Nagpur",
            "amravati": "Amravati",
            "अमरावती": "Amravati",
            "ludhiana": "Ludhiana",
            "लुधियाना": "Ludhiana",
            "karnal": "Karnal",
            "करनाल": "Karnal",
            "varanasi": "Varanasi",
            "वाराणसी": "Varanasi",
            "patna": "Patna",
            "पटना": "Patna",
            "raipur": "Raipur",
            "रायपुर": "Raipur"
        }
        for loc_key, loc_val in common_locations.items():
            if loc_key in q_lower or loc_key in query:
                detected_location = loc_val
                break

        # Detect language preference
        is_hindi = any('\u0900' <= char <= '\u097F' for char in query) or "hindi" in q_lower or "हिंदी" in query

        return {
            "crop": detected_crop,
            "growth_stage": detected_stage,
            "location": detected_location,
            "language": "hi" if is_hindi else "en"
        }

    async def execute_advisory_pipeline(
        self,
        query: str,
        location: Optional[str] = None,
        crop: Optional[str] = None,
        growth_stage: Optional[str] = None,
        language: Optional[str] = "en",
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> ChatResponse:
        """
        Execute full multi-agent collaborative workflow:
        1. Query extraction
        2. Weather Agent data retrieval
        3. Crop Agent agronomic threshold matching
        4. Risk Agent deterministic computation
        5. Farming Advisory Agent bilingual action plan synthesis
        6. Orchestrator validation and response assembly
        """
        traces: List[AgentTraceStep] = []

        # Step 1: Entity extraction
        entities = self.extract_entities(query, location, crop, growth_stage)
        req_crop = crop or entities["crop"]
        req_stage = growth_stage or entities["growth_stage"]
        req_loc = location or entities["location"]
        req_lang = language or entities["language"]

        traces.append(AgentTraceStep(
            agent="KrishiOrchestrator",
            action="Extract Intent & Entities",
            status="COMPLETED",
            summary=f"Parsed Query. Location: {req_loc}, Crop: {req_crop}, Stage: {req_stage}, Language: {req_lang.upper()}"
        ))

        # Step 2: Weather Intelligence Agent
        if lat is None or lon is None:
            coords = await WeatherService.resolve_coordinates(req_loc)
            lat, lon = coords.latitude, coords.longitude
            req_loc = coords.name

        weather = await WeatherService.get_forecast(lat, lon, req_loc)
        traces.append(AgentTraceStep(
            agent="WeatherIntelligenceAgent",
            action="Retrieve Live Observations & 7-Day Forecast",
            status="COMPLETED",
            summary=f"Current Temp: {weather.current.temperature}°C, Rain: {weather.current.rainfall} mm. 7-Day forecast retrieved from {weather.source}."
        ))

        # Step 3: Crop Intelligence Agent
        crop_context = self.crop_agent.tools[1](req_crop, req_stage) if hasattr(self.crop_agent, "tools") else None
        traces.append(AgentTraceStep(
            agent="CropIntelligenceAgent",
            action="Retrieve Agronomic Bounds & Stage Sensitivities",
            status="COMPLETED",
            summary=f"Retrieved ICAR/FAO physiological tolerances for {req_crop} at {req_stage}."
        ))

        # Step 4: Risk Assessment Agent (Deterministic Engine)
        risk_report = DeterministicRiskEngine.calculate_risks(weather, req_crop, req_stage)
        highest_risk = max(risk_report.assessments, key=lambda a: a.risk_score) if risk_report.assessments else None
        traces.append(AgentTraceStep(
            agent="RiskAssessmentAgent",
            action="Execute Deterministic Python Risk Engine",
            status="COMPLETED",
            summary=f"Computed {len(risk_report.assessments)} risk categories without LLM guessing. Overall Level: {risk_report.overall_risk_level.value} (Peak Score: {highest_risk.risk_score if highest_risk else 0.0} in {highest_risk.category.value if highest_risk else 'None'})."
        ))

        # Step 5: Farming Advisory Agent
        advisory = AdvisoryService.generate_advisory(risk_report, weather, req_lang)
        traces.append(AgentTraceStep(
            agent="FarmingAdvisoryAgent",
            action="Synthesize Practical Bilingual Action Roadmap",
            status="COMPLETED",
            summary=f"Synthesized immediate precautions and a 3-day farming action plan in {req_lang.upper()}."
        ))

        # Step 6: Orchestrator Response Synthesis
        if req_lang == "hi":
            response_text = self._format_hindi_response(req_loc, advisory, highest_risk, weather)
        else:
            response_text = self._format_english_response(req_loc, advisory, highest_risk, weather)

        traces.append(AgentTraceStep(
            agent="KrishiOrchestrator",
            action="Synthesize Final Farmer Intelligence Report",
            status="COMPLETED",
            summary="Validated specialist findings, resolved inconsistencies, and finalized bilingual farmer advisory."
        ))

        return ChatResponse(
            response=response_text,
            language=req_lang,
            extracted_entities={
                "location": req_loc,
                "crop": req_crop,
                "growth_stage": req_stage,
                "latitude": lat,
                "longitude": lon
            },
            agent_traces=traces,
            structured_data={
                "advisory": advisory.model_dump(),
                "risk_report": risk_report.model_dump(),
                "weather_current": weather.current.model_dump()
            },
            disclaimer="KrishiSathi AI advisory is decision support based on numerical weather forecasts and ICAR/FAO agronomic research. Consult local agricultural authorities for field confirmation."
        )

    def _format_english_response(self, loc: str, adv: Any, highest_risk: Any, weather: WeatherSummary) -> str:
        risk_badge = f"⚠️ **RISK LEVEL: {adv.overall_risk_level.value}**" if adv.overall_risk_level != RiskLevel.LOW else "✅ **RISK LEVEL: LOW**"
        
        immediates = "\n".join([f"- {p}" for p in adv.immediate_precautions_en])
        
        plan_days = []
        for d in adv.action_plan_3d:
            actions = "; ".join(d.recommended_actions_en)
            plan_days.append(f"**{d.day_label}**: {actions} *(Forecast: {d.forecast_summary})*")
        plan_str = "\n".join(plan_days)

        return f"""### 🌾 KrishiSathi Climate Intelligence Report
**Location**: {loc} | **Crop**: {adv.crop} ({adv.growth_stage})
**Current Weather**: {weather.current.temperature}°C, {weather.current.weather_description}, Humidity {weather.current.humidity}%

{risk_badge}
**Key Risk Detected**: {highest_risk.category_title if highest_risk else 'Normal'} ({highest_risk.risk_level.value if highest_risk else 'LOW'})
*{highest_risk.reason_en if highest_risk else 'No acute weather hazard detected.'}*

---

#### 🚨 Immediate Precautions:
{immediates}

---

#### 📅 3-Day Farming Action Roadmap:
{plan_str}

---

🔍 **What to Monitor**: {highest_risk.recommended_monitoring_en if highest_risk else 'Routine field observation.'}
⏱️ *Forecast retrieved: {adv.forecast_timestamp} via {weather.source}*
"""

    def _format_hindi_response(self, loc: str, adv: Any, highest_risk: Any, weather: WeatherSummary) -> str:
        risk_badge = f"⚠️ **जोखिम स्तर: {adv.overall_risk_level.value} (सावधानी)**" if adv.overall_risk_level != RiskLevel.LOW else "✅ **जोखिम स्तर: सामान्य (अनुकूल)**"
        
        immediates = "\n".join([f"- {p}" for p in adv.immediate_precautions_hi])
        
        plan_days = []
        for d in adv.action_plan_3d:
            actions = "; ".join(d.recommended_actions_hi)
            plan_days.append(f"**{d.day_label}**: {actions} *(पूर्वानुमान: {d.forecast_summary_hi})*")
        plan_str = "\n".join(plan_days)

        return f"""### 🌾 कृषिसार्थी कृषि जलवायु रिपोर्ट
**स्थान**: {loc} | **फसल**: {adv.crop_hi} ({adv.growth_stage_hi})
**वर्तमान मौसम**: {weather.current.temperature}°C, {weather.current.weather_description}, नमी {weather.current.humidity}%

{risk_badge}
**पहचाना गया जोखिम**: {highest_risk.category_title_hi if highest_risk else 'सामान्य'} ({highest_risk.risk_level.value if highest_risk else 'LOW'})
*{highest_risk.reason_hi if highest_risk else 'कोई गंभीर मौसमी जोखिम नहीं पाया गया है।'}*

---

#### 🚨 तत्काल जरूरी सावधानियां:
{immediates}

---

#### 📅 3-दिवसीय कृषि कार्य योजना:
{plan_str}

---

🔍 **किसान भाई क्या ध्यान दें**: {highest_risk.recommended_monitoring_hi if highest_risk else 'खेत की सामान्य निगरानी जारी रखें।'}
⏱️ *पूर्वानुमान समय: {adv.forecast_timestamp} ({weather.source})*
"""
