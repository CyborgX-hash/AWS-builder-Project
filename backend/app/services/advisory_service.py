import json
import os
import time
from typing import Dict, Any, List, Optional
from app.schemas.risk import ComprehensiveRiskReport, RiskLevel, RiskCategory
from app.schemas.weather import WeatherSummary
from app.schemas.advisory import AdvisoryResponse, FarmingActionPlanDay
from app.tools.crop_tool import get_growth_stage_info

ADVISORY_RULES_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge", "advisory_rules.json")


def load_advisory_rules() -> Dict[str, Any]:
    with open(ADVISORY_RULES_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("rules", {})


class AdvisoryService:
    """
    Translates deterministic risk assessments and weather forecasts into actionable
    agricultural advisories and a multi-day farming roadmap.
    """

    @staticmethod
    def generate_advisory(
        risk_report: ComprehensiveRiskReport,
        weather: WeatherSummary,
        preferred_language: str = "en"
    ) -> AdvisoryResponse:
        rules = load_advisory_rules()
        crop = risk_report.crop
        stage = risk_report.growth_stage

        crop_info = get_growth_stage_info(crop, stage)
        crop_hi = crop_info.get("crop_hi", crop)
        stage_hi = crop_info.get("stage", {}).get("stage_name_hi", stage)

        immediate_en: List[str] = []
        immediate_hi: List[str] = []

        day1_en: List[str] = []
        day1_hi: List[str] = []
        day2_en: List[str] = []
        day2_hi: List[str] = []
        day3_en: List[str] = []
        day3_hi: List[str] = []

        active_high_risks = [a for a in risk_report.assessments if a.risk_level == RiskLevel.HIGH]
        active_mod_risks = [a for a in risk_report.assessments if a.risk_level == RiskLevel.MODERATE]

        # Prioritize High risks first, then Moderate
        evaluated_risks = active_high_risks if active_high_risks else active_mod_risks

        if not evaluated_risks:
            # Low risk across the board
            immediate_en.append("Current weather conditions are highly favorable. Proceed with normal agricultural operations.")
            immediate_hi.append("वर्तमान मौसम फसल के लिए अनुकूल है। सामान्य कृषि कार्य नियमित रूप से जारी रखें।")

            day1_en.append("Perform routine crop scouting and inspect leaf canopy.")
            day1_hi.append("फसल का सामान्य निरीक्षण करें और पत्तियों की बढ़वार देखें।")

            day2_en.append("Carry out scheduled weeding or intercultural operations under dry soil.")
            day2_hi.append("खेत में खरपतवार नियंत्रण या गुड़ाई का कार्य करें।")

            day3_en.append("Check soil moisture status before next routine irrigation cycle.")
            day3_hi.append("अगली सामान्य सिंचाई से पहले खेत की नमी की स्थिति जांचें।")
        else:
            for risk in evaluated_risks:
                cat_key = risk.category.value
                level_key = risk.risk_level.value

                cat_rules = rules.get(cat_key, {}).get(level_key, {})
                if cat_rules:
                    immediate_en.extend(cat_rules.get("immediate_en", []))
                    immediate_hi.extend(cat_rules.get("immediate_hi", []))

                    if "planning_day1_en" in cat_rules:
                        day1_en.append(cat_rules["planning_day1_en"])
                        day1_hi.append(cat_rules["planning_day1_hi"])
                    if "planning_day2_en" in cat_rules:
                        day2_en.append(cat_rules["planning_day2_en"])
                        day2_hi.append(cat_rules["planning_day2_hi"])
                    if "planning_day3_en" in cat_rules:
                        day3_en.append(cat_rules["planning_day3_en"])
                        day3_hi.append(cat_rules["planning_day3_hi"])

        # Construct 3-day action roadmap based on daily forecasts
        forecast_days = weather.daily[:3]
        action_plan: List[FarmingActionPlanDay] = []

        day_labels = [("Day 1 (Next 24h)", "दिन 1 (अगले 24 घंटे)"),
                      ("Day 2 (Next 48h)", "दिन 2 (अगले 48 घंटे)"),
                      ("Day 3 (Next 72h)", "दिन 3 (अगले 72 घंटे)")]

        day_actions_en = [day1_en, day2_en, day3_en]
        day_actions_hi = [day1_hi, day2_hi, day3_hi]

        for i, daily in enumerate(forecast_days):
            en_label, hi_label = day_labels[i] if i < len(day_labels) else (f"Day {i+1}", f"दिन {i+1}")
            summary_en = f"{daily.weather_description}, Max {daily.temp_max:.1f}°C, Rain: {daily.rainfall_sum:.1f} mm ({daily.precipitation_probability_max}% prob)"
            summary_hi = f"{daily.weather_description}, अधि. {daily.temp_max:.1f}°C, बारिश: {daily.rainfall_sum:.1f} मिमी ({daily.precipitation_probability_max}% संभावना)"

            actions_en = day_actions_en[i] if (i < len(day_actions_en) and day_actions_en[i]) else ["Maintain general field oversight."]
            actions_hi = day_actions_hi[i] if (i < len(day_actions_hi) and day_actions_hi[i]) else ["खेत की सामान्य निगरानी जारी रखें।"]

            monitor_en = "Drainage channels and surface moisture" if daily.rainfall_sum > 10 else "Canopy temperature and leaf wilting"
            monitor_hi = "जल निकासी की नालियां और नमी" if daily.rainfall_sum > 10 else "पत्तियों का मुरझाना और दोपहर की धूप"

            action_plan.append(
                FarmingActionPlanDay(
                    day=i + 1,
                    day_label=en_label if preferred_language == "en" else hi_label,
                    date_str=daily.date,
                    forecast_summary=summary_en,
                    forecast_summary_hi=summary_hi,
                    recommended_actions_en=actions_en,
                    recommended_actions_hi=actions_hi,
                    what_to_monitor_en=monitor_en,
                    what_to_monitor_hi=monitor_hi
                )
            )

        # General precautions
        general_precautions_en = [
            "Never apply agrochemicals or foliar urea when rain is forecast within 6-12 hours.",
            "Maintain bunds to harvest clean runoff where appropriate, while keeping field drainage furrows operational.",
            "Verify real-time IMD district alerts on Mausam/Meghdoot before initiating major harvest operations."
        ]
        general_precautions_hi = [
            "यदि अगले 6-12 घंटों में बारिश का अनुमान हो तो कभी भी कीटनाशक या यूरिया का छिड़काव न करें।",
            "खेत की मेड़ों को मजबूत रखें ताकि मिट्टी का कटाव न हो, और जलनिकासी की नालियां खुली रखें।",
            "बड़ी कटाई या मड़ाई से पहले मौसम विभाग के मेघदूत या मौसम पोर्टल पर जिले की चेतावनी अवश्य देखें।"
        ]

        summary_en = (
            f"Advisory for {crop} ({stage}) at {risk_report.location}: Overall risk is {risk_report.overall_risk_level.value}. "
            f"Primary focus should be on {evaluated_risks[0].category.value.replace('_', ' ').title() if evaluated_risks else 'routine crop care'}."
        )
        summary_hi = (
            f"{risk_report.location} में {crop_hi} ({stage_hi}) हेतु सलाह: कुल जोखिम स्तर {risk_report.overall_risk_level.value} है। "
            f"मुख्य प्राथमिकता {evaluated_risks[0].category_title_hi if evaluated_risks else 'सामान्य फसल देखभाल'} पर होनी चाहिए।"
        )

        official_advisory_note_en = (
            "NOTICE: KrishiSathi provides predictive climate decision support based on numerical models and ICAR/FAO agronomic research. "
            "It does not replace state agricultural extension officers or IMD Agromet bulletins."
        )
        official_advisory_note_hi = (
            "सूचना: कृषिसार्थी मौसम मॉडल और कृषि अनुसंधान पर आधारित सलाह प्रदान करता है। "
            "यह स्थानीय कृषि अधिकारियों या मौसम विभाग के आधिकारिक बुलेटिन का विकल्प नहीं है।"
        )

        return AdvisoryResponse(
            crop=crop,
            crop_hi=crop_hi,
            growth_stage=stage,
            growth_stage_hi=stage_hi,
            location=risk_report.location,
            overall_risk_level=risk_report.overall_risk_level,
            summary_en=summary_en,
            summary_hi=summary_hi,
            immediate_precautions_en=immediate_en,
            immediate_precautions_hi=immediate_hi,
            action_plan_3d=action_plan,
            general_precautions_en=general_precautions_en,
            general_precautions_hi=general_precautions_hi,
            official_advisory_note_en=official_advisory_note_en,
            official_advisory_note_hi=official_advisory_note_hi,
            forecast_timestamp=risk_report.calculation_timestamp,
            data_sources=risk_report.data_sources
        )

