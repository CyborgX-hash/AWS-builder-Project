import time
from typing import Dict, Any, List, Optional
from app.schemas.weather import WeatherSummary, DailyForecastItem
from app.schemas.risk import (
    RiskLevel,
    RiskCategory,
    SingleRiskAssessment,
    ComprehensiveRiskReport
)
from app.tools.crop_tool import get_growth_stage_info, get_crop_profile


class DeterministicRiskEngine:
    """
    Independent mathematical agro-climatic risk computation engine.
    Calculates numerical risk scores and categorical thresholds without LLM hallucinations.
    """

    @staticmethod
    def calculate_risks(
        weather: WeatherSummary,
        crop_name: str,
        growth_stage_name: str
    ) -> ComprehensiveRiskReport:
        """
        Evaluate all 5 core agro-climatic risk categories against real weather forecasts
        and crop-stage specific agronomic thresholds.
        """
        crop_context = get_growth_stage_info(crop_name, growth_stage_name)
        stage_data = crop_context.get("stage", {})
        crop_clean = crop_context.get("crop", crop_name.title())

        assessments: List[SingleRiskAssessment] = []

        # 1. Evaluate Heat Stress
        heat_assessment = DeterministicRiskEngine._eval_heat_stress(weather, stage_data, crop_clean)
        assessments.append(heat_assessment)

        # 2. Evaluate Excessive Rainfall
        rain_assessment = DeterministicRiskEngine._eval_excessive_rainfall(weather, stage_data, crop_clean)
        assessments.append(rain_assessment)

        # 3. Evaluate Waterlogging
        waterlog_assessment = DeterministicRiskEngine._eval_waterlogging(weather, stage_data, crop_clean)
        assessments.append(waterlog_assessment)

        # 4. Evaluate Dry Spell
        dry_assessment = DeterministicRiskEngine._eval_dry_spell(weather, stage_data, crop_clean)
        assessments.append(dry_assessment)

        # 5. Evaluate Water Stress
        stress_assessment = DeterministicRiskEngine._eval_water_stress(weather, stage_data, crop_clean)
        assessments.append(stress_assessment)

        # Calculate Overall Risk Level based on maximum severity
        scores = [a.risk_score for a in assessments]
        max_score = max(scores) if scores else 0.0

        if max_score >= 70.0:
            overall_level = RiskLevel.HIGH
        elif max_score >= 35.0:
            overall_level = RiskLevel.MODERATE
        else:
            overall_level = RiskLevel.LOW

        return ComprehensiveRiskReport(
            crop=crop_clean,
            growth_stage=stage_data.get("stage_name", growth_stage_name),
            location=weather.location,
            overall_risk_level=overall_level,
            assessments=assessments,
            calculation_timestamp=time.strftime("%Y-%m-%d %H:%M:%S IST"),
            data_sources=[
                weather.source,
                f"ICAR/FAO Agronomic Thresholds for {crop_clean}"
            ],
            limitations_disclaimer=(
                "Screening calculations rely on numerical weather prediction models and published agronomic thresholds. "
                "Local field micro-climates, soil infiltration rates, and drainage topography can alter actual field impact. "
                "Consult local Krishi Vigyan Kendra (KVK) agronomists before critical chemical or harvest interventions."
            )
        )

    @staticmethod
    def _eval_heat_stress(weather: WeatherSummary, stage: Dict[str, Any], crop: str) -> SingleRiskAssessment:
        temp_opt_max = stage.get("temp_opt_max_c", 32.0)
        temp_max_threshold = stage.get("temp_max_c", 36.0)

        # Look at next 3 days max temperatures
        forecast_3d = weather.daily[:3]
        max_forecast_temp = max([d.temp_max for d in forecast_3d]) if forecast_3d else weather.current.temperature

        # Deterministic scoring
        if max_forecast_temp >= temp_max_threshold:
            excess = max_forecast_temp - temp_max_threshold
            score = min(100.0, 75.0 + (excess * 6.0))
            level = RiskLevel.HIGH
            reason_en = (
                f"Forecast peak temperature of {max_forecast_temp:.1f}°C exceeds critical threshold ({temp_max_threshold:.1f}°C) "
                f"for {crop} at {stage.get('stage_name', 'current stage')}. High risk of pollen sterility and canopy wilting."
            )
            reason_hi = (
                f"पूर्वानुमानित अधिकतम तापमान {max_forecast_temp:.1f}°C, {crop} के लिए सहनसीमा ({temp_max_threshold:.1f}°C) "
                f"से अधिक है। फूल झड़ने और पौधे के झुलसने का गंभीर खतरा है।"
            )
            monitor_en = "Inspect canopy midday wilting, leaf scorching, and abnormal flower drop."
            monitor_hi = "दोपहर के समय पत्तियों के मुरझाने और फूलों के झड़ने पर विशेष नजर रखें।"
        elif max_forecast_temp > temp_opt_max:
            fraction = (max_forecast_temp - temp_opt_max) / max(1.0, (temp_max_threshold - temp_opt_max))
            score = 35.0 + (fraction * 34.0)
            level = RiskLevel.MODERATE
            reason_en = (
                f"Temperature reaching {max_forecast_temp:.1f}°C is above optimal comfort zone ({temp_opt_max:.1f}°C). "
                f"Moderate physiological heat load detected."
            )
            reason_hi = (
                f"अधिकतम तापमान {max_forecast_temp:.1f}°C अनुकूलतम सीमा ({temp_opt_max:.1f}°C) से अधिक है। "
                f"हल्का गर्मी का तनाव संभव है।"
            )
            monitor_en = "Ensure soil moisture does not deplete rapidly during peak hours."
            monitor_hi = "खेत में दोपहर के समय नमी तेजी से कम न होने दें।"
        else:
            score = max(10.0, (max_forecast_temp / max(1.0, temp_opt_max)) * 25.0)
            level = RiskLevel.LOW
            reason_en = f"Peak temperature ({max_forecast_temp:.1f}°C) is within optimal vegetative range."
            reason_hi = f"अधिकतम तापमान ({max_forecast_temp:.1f}°C) फसल के लिए अनुकूल और सामान्य है।"
            monitor_en = "Routine crop health observation."
            monitor_hi = "सामान्य फसल निगरानी जारी रखें।"

        return SingleRiskAssessment(
            category=RiskCategory.HEAT_STRESS,
            category_title="Heat Stress Risk",
            category_title_hi="गर्मी एवं लू का जोखिम",
            risk_level=level,
            risk_score=round(score, 1),
            relevant_weather_variables={
                "max_forecast_temp_c": round(max_forecast_temp, 1),
                "opt_max_threshold_c": temp_opt_max,
                "critical_threshold_c": temp_max_threshold
            },
            reason_en=reason_en,
            reason_hi=reason_hi,
            recommended_monitoring_en=monitor_en,
            recommended_monitoring_hi=monitor_hi,
            data_confidence="HIGH",
            is_provisional_rule=False
        )

    @staticmethod
    def _eval_excessive_rainfall(weather: WeatherSummary, stage: Dict[str, Any], crop: str) -> SingleRiskAssessment:
        tolerance_24h = stage.get("excess_rain_tolerance_mm_day", 40.0)

        daily_2d = weather.daily[:2]
        max_single_day_rain = max([d.rainfall_sum for d in daily_2d]) if daily_2d else weather.current.rainfall
        sum_2d_rain = sum([d.rainfall_sum for d in daily_2d]) if daily_2d else weather.current.rainfall
        precip_prob_max = max([d.precipitation_probability_max for d in daily_2d]) if daily_2d else 0

        # IMD Rain categorization: >64.5mm is Heavy Rain, >115.5mm is Very Heavy
        if max_single_day_rain >= 64.5 or sum_2d_rain > (tolerance_24h * 1.5):
            score = min(100.0, 75.0 + ((sum_2d_rain - tolerance_24h) * 0.4))
            level = RiskLevel.HIGH
            reason_en = (
                f"Heavy rainfall alert: 48-hour cumulative rainfall of {sum_2d_rain:.1f} mm exceeds stage tolerance "
                f"({tolerance_24h:.1f} mm/day) with {precip_prob_max}% probability. High probability of surface runoff and lodging."
            )
            reason_hi = (
                f"भारी वर्षा की चेतावनी: 48 घंटों में कुल {sum_2d_rain:.1f} मिमी बारिश का अनुमान है, जो फसल की क्षमता "
                f"({tolerance_24h:.1f} मिमी/दिन) से अधिक है। जलभराव और फसल गिरने का खतरा है।"
            )
            monitor_en = "Check field bund integrity and clear all drainage exits immediately."
            monitor_hi = "खेत की मेड़ों को सुरक्षित करें और जल निकासी के रास्तों को तुरंत खोलें।"
        elif sum_2d_rain > (tolerance_24h * 0.7) or max_single_day_rain > 25.0:
            score = 45.0 + min(24.0, sum_2d_rain * 0.5)
            level = RiskLevel.MODERATE
            reason_en = (
                f"Moderate rainfall forecasted ({sum_2d_rain:.1f} mm over 48h). Soil moisture will reach full saturation."
            )
            reason_hi = (
                f"मध्यम वर्षा का अनुमान (48 घंटों में {sum_2d_rain:.1f} मिमी)। मिट्टी में नमी संतृप्ति स्तर तक पहुंचेगी।"
            )
            monitor_en = "Pause mechanical tillage and postpone fertilizer application."
            monitor_hi = "खेत में ट्रैक्टर जुताई रोकें और खाद का छिड़काव टालें।"
        else:
            score = max(5.0, sum_2d_rain * 1.2)
            level = RiskLevel.LOW
            reason_en = f"Low precipitation expected ({sum_2d_rain:.1f} mm over 48h). Favorable for routine field operations."
            reason_hi = f"हल्की या नगण्य बारिश का अनुमान ({sum_2d_rain:.1f} मिमी)। सामान्य कृषि कार्यों के लिए सुरक्षित।"
            monitor_en = "Standard field monitoring."
            monitor_hi = "सामान्य निगरानी रखें।"

        return SingleRiskAssessment(
            category=RiskCategory.EXCESSIVE_RAINFALL,
            category_title="Excessive Rainfall Risk",
            category_title_hi="अत्यधिक वर्षा का जोखिम",
            risk_level=level,
            risk_score=round(score, 1),
            relevant_weather_variables={
                "max_single_day_rain_mm": round(max_single_day_rain, 1),
                "sum_2d_rain_mm": round(sum_2d_rain, 1),
                "tolerance_mm_day": tolerance_24h,
                "precip_probability_max": precip_prob_max
            },
            reason_en=reason_en,
            reason_hi=reason_hi,
            recommended_monitoring_en=monitor_en,
            recommended_monitoring_hi=monitor_hi,
            data_confidence="HIGH",
            is_provisional_rule=False
        )

    @staticmethod
    def _eval_waterlogging(weather: WeatherSummary, stage: Dict[str, Any], crop: str) -> SingleRiskAssessment:
        daily_3d = weather.daily[:3]
        sum_3d_rain = sum([d.rainfall_sum for d in daily_3d]) if daily_3d else 0.0

        # Crop flood tolerance factor
        is_rice = "rice" in crop.lower() or "paddy" in crop.lower()

        if is_rice:
            # Rice loves shallow standing water, high risk only if extreme (>130mm in 3 days)
            if sum_3d_rain > 130.0:
                score = 72.0
                level = RiskLevel.HIGH
                reason_en = f"Submergence risk for young paddy: {sum_3d_rain:.1f} mm 3-day rainfall may cause deep flooding."
                reason_hi = f"धान की फसल डूबने का जोखिम: 3 दिनों में {sum_3d_rain:.1f} मिमी बारिश से गहरा जलभराव हो सकता है।"
            elif sum_3d_rain > 70.0:
                score = 40.0
                level = RiskLevel.MODERATE
                reason_en = f"Heavy rainfall ({sum_3d_rain:.1f} mm 3-day); keep drainage sluice active to maintain 3-5 cm water depth."
                reason_hi = f"मध्यम-तेज वर्षा; खेत में 3-5 सेमी से अधिक पानी न भरने दें।"
            else:
                score = 15.0
                level = RiskLevel.LOW
                reason_en = "Paddy fields are well adapted to current moisture levels."
                reason_hi = "धान की फसल के लिए वर्तमान जल स्तर सामान्य और अनुकूल है।"
        else:
            # Soybean, Maize, Cotton, Wheat are severely damaged by standing water
            if sum_3d_rain > 50.0:
                score = min(98.0, 72.0 + ((sum_3d_rain - 50.0) * 0.5))
                level = RiskLevel.HIGH
                reason_en = (
                    f"Critical waterlogging risk for {crop}: {sum_3d_rain:.1f} mm rainfall over 72h will cause "
                    f"root zone asphyxiation and collar rot in low-lying patches."
                )
                reason_hi = (
                    f"{crop} के लिए जलभराव का गंभीर खतरा: 72 घंटों में {sum_3d_rain:.1f} मिमी बारिश से जड़ों में "
                    f"हवा का संचार बंद हो जाएगा और जड़ सड़न की आशंका है।"
                )
            elif sum_3d_rain > 25.0:
                score = 45.0 + ((sum_3d_rain - 25.0) * 0.8)
                level = RiskLevel.MODERATE
                reason_en = f"Moderate water accumulation possible ({sum_3d_rain:.1f} mm over 3 days). Sluggish drainage in heavy clay soils."
                reason_hi = f"खेत में पानी ठहरने की आशंका ({sum_3d_rain:.1f} मिमी 3 दिनों में)। भारी मिट्टी में निकासी धीमी हो सकती है।"
            else:
                score = 10.0
                level = RiskLevel.LOW
                reason_en = "No prolonged surface standing water expected."
                reason_hi = "खेत में पानी भरने की कोई आशंका नहीं है।"

        monitor_en = "Inspect low-lying furrow ends and field corners for standing water."
        monitor_hi = "खेत के निचले कोनों और नालियों में खड़े पानी की तुरंत जांच करें।"

        return SingleRiskAssessment(
            category=RiskCategory.WATERLOGGING,
            category_title="Waterlogging & Drainage Risk",
            category_title_hi="जलभराव एवं जलनिकासी का जोखिम",
            risk_level=level,
            risk_score=round(score, 1),
            relevant_weather_variables={
                "sum_3d_rainfall_mm": round(sum_3d_rain, 1),
                "is_rice_tolerant": is_rice
            },
            reason_en=reason_en,
            reason_hi=reason_hi,
            recommended_monitoring_en=monitor_en,
            recommended_monitoring_hi=monitor_hi,
            data_confidence="HIGH",
            is_provisional_rule=False
        )

    @staticmethod
    def _eval_dry_spell(weather: WeatherSummary, stage: Dict[str, Any], crop: str) -> SingleRiskAssessment:
        daily_7d = weather.daily
        dry_days = sum(1 for d in daily_7d if d.rainfall_sum < 2.0)
        max_consecutive_dry = 0
        curr_streak = 0
        for d in daily_7d:
            if d.rainfall_sum < 2.0:
                curr_streak += 1
                if curr_streak > max_consecutive_dry:
                    max_consecutive_dry = curr_streak
            else:
                curr_streak = 0

        avg_temp = sum(d.temp_max for d in daily_7d) / max(1, len(daily_7d))

        if max_consecutive_dry >= 6 and avg_temp > 33.0:
            score = 75.0 + min(20.0, (avg_temp - 33.0) * 3.0)
            level = RiskLevel.HIGH
            reason_en = (
                f"Severe dry-spell alert: {max_consecutive_dry} consecutive rainless days forecast with average "
                f"daytime temperature of {avg_temp:.1f}°C. Soil moisture will drop rapidly below depletion threshold."
            )
            reason_hi = (
                f"गंभीर सूखे का जोखिम: लगातार {max_consecutive_dry} दिनों तक बारिश न होने और {avg_temp:.1f}°C औसत "
                f"तापमान का अनुमान है। मिट्टी की नमी तेजी से खत्म होगी।"
            )
            monitor_en = "Check soil moisture at 10-15 cm depth using the hand-feel method."
            monitor_hi = "खेत में 10-15 सेमी गहराई पर मिट्टी की नमी की जांच करें।"
        elif max_consecutive_dry >= 4:
            score = 42.0 + (max_consecutive_dry * 4.0)
            level = RiskLevel.MODERATE
            reason_en = f"Dry interval of {max_consecutive_dry} consecutive days. Evaporative demand increasing."
            reason_hi = f"लगातार {max_consecutive_dry} दिनों का सूखा अंतराल। नमी की मांग बढ़ रही है।"
            monitor_en = "Monitor crop for leaf roll in early afternoon."
            monitor_hi = "दोपहर में पत्तियों के सिकुड़ने की जांच करें।"
        else:
            score = 12.0
            level = RiskLevel.LOW
            reason_en = f"Adequate moisture intervals; dry streak limited to {max_consecutive_dry} days."
            reason_hi = f"नमी का संतुलन ठीक है; सूखे दिन मात्र {max_consecutive_dry} दिन हैं।"
            monitor_en = "Routine crop observation."
            monitor_hi = "सामान्य निगरानी रखें।"

        return SingleRiskAssessment(
            category=RiskCategory.DRY_SPELL,
            category_title="Dry-Spell Risk",
            category_title_hi="सूखा अंतराल का जोखिम",
            risk_level=level,
            risk_score=round(score, 1),
            relevant_weather_variables={
                "consecutive_dry_days": max_consecutive_dry,
                "total_dry_days_in_7d": dry_days,
                "average_temp_max_c": round(avg_temp, 1)
            },
            reason_en=reason_en,
            reason_hi=reason_hi,
            recommended_monitoring_en=monitor_en,
            recommended_monitoring_hi=monitor_hi,
            data_confidence="HIGH",
            is_provisional_rule=False
        )

    @staticmethod
    def _eval_water_stress(weather: WeatherSummary, stage: Dict[str, Any], crop: str) -> SingleRiskAssessment:
        daily_water_need = stage.get("daily_water_need_mm", 5.0)
        forecast_7d = weather.daily
        total_rain_7d = sum(d.rainfall_sum for d in forecast_7d)
        total_water_need_7d = daily_water_need * len(forecast_7d)

        # Deficit = Need - Rain
        deficit_mm = total_water_need_7d - total_rain_7d

        if deficit_mm > 25.0 and total_rain_7d < 5.0:
            score = min(95.0, 70.0 + (deficit_mm - 25.0))
            level = RiskLevel.HIGH
            reason_en = (
                f"Crop moisture deficit: 7-day water requirement is {total_water_need_7d:.1f} mm vs only {total_rain_7d:.1f} mm "
                f"expected rainfall. Net soil water deficit of {deficit_mm:.1f} mm requires supplemental irrigation."
            )
            reason_hi = (
                f"फसल में नमी की भारी कमी: 7 दिनों में {total_water_need_7d:.1f} मिमी पानी की आवश्यकता के मुकाबले केवल "
                f"{total_rain_7d:.1f} मिमी बारिश संभव है। {deficit_mm:.1f} मिमी की कमी पूरी करने हेतु सिंचाई आवश्यक है।"
            )
            monitor_en = "Check morning leaf turgidity and surface cracking in black clay soils."
            monitor_hi = "सुबह के समय पत्तियों का सीधापन और काली मिट्टी में दरारें देखें।"
        elif deficit_mm > 10.0:
            score = 38.0 + (deficit_mm * 1.2)
            level = RiskLevel.MODERATE
            reason_en = f"Mild moisture deficit of {deficit_mm:.1f} mm over 7 days. Irrigation planning advised."
            reason_hi = f"7 दिनों में {deficit_mm:.1f} मिमी की हल्की नमी कमी। सिंचाई की योजना बनाएं।"
            monitor_en = "Watch irrigation schedule."
            monitor_hi = "सिंचाई कार्यक्रम पर नजर रखें।"
        else:
            score = 10.0
            level = RiskLevel.LOW
            reason_en = f"Rainfall and soil moisture are sufficient to meet {crop}'s weekly crop water requirement."
            reason_hi = f"बारिश और मिट्टी की नमी {crop} की साप्ताहिक पानी की जरूरत को पूरा करने के लिए पर्याप्त है।"
            monitor_en = "Standard field observation."
            monitor_hi = "सामान्य निगरानी रखें।"

        return SingleRiskAssessment(
            category=RiskCategory.WATER_STRESS,
            category_title="Crop Water Stress",
            category_title_hi="फसल जल तनाव का जोखिम",
            risk_level=level,
            risk_score=round(score, 1),
            relevant_weather_variables={
                "daily_water_need_mm": daily_water_need,
                "total_7d_need_mm": round(total_water_need_7d, 1),
                "total_7d_rain_mm": round(total_rain_7d, 1),
                "moisture_deficit_mm": round(max(0.0, deficit_mm), 1)
            },
            reason_en=reason_en,
            reason_hi=reason_hi,
            recommended_monitoring_en=monitor_en,
            recommended_monitoring_hi=monitor_hi,
            data_confidence="HIGH",
            is_provisional_rule=False
        )

