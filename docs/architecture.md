# KrishiSathi Multi-Agent Architecture

KrishiSathi employs a hierarchical multi-agent intelligence architecture built on the **AWS Strands Agents SDK** and **Amazon Bedrock**. The system bridges the gap between raw numerical meteorological outputs and localized, crop-specific farming decisions.

---

## Architecture Diagram

```
                              ┌────────────────────────────────────────┐
                              │            Farmer / User UI            │
                              │  (React, Vite, Tailwind, Recharts)     │
                              └───────────────────┬────────────────────┘
                                                  │ HTTP REST (JSON)
                              ┌───────────────────▼────────────────────┐
                              │            FastAPI Backend             │
                              │   (Routers, DB Session, CORS, SQLite)  │
                              └───────────────────┬────────────────────┘
                                                  │
                              ┌───────────────────▼────────────────────┐
                              │        Krishi Orchestrator Agent       │
                              │      (Strands Agents as Tools)         │
                              └───────┬───────┬────────┬───────┬───────┘
                                      │       │        │       │
              ┌───────────────────────┘       │        │       └────────────────────────┐
              │                               │        │                                │
              ▼                               ▼        ▼                                ▼
┌───────────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐
│ WeatherIntelligenceAgent  │   │  CropIntelligenceAgent    │   │   RiskAssessmentAgent     │   │   FarmingAdvisoryAgent    │
│ (Live, Hourly & 7D Daily) │   │ (Agronomic Sensitivities) │   │ (Deterministic Engine)    │   │ (Actionable Multi-Day)    │
└─────────────┬─────────────┘   └─────────────┬─────────────┘   └─────────────┬─────────────┘   └─────────────┬─────────────┘
              │                               │                               │                               │
              ▼                               ▼                               ▼                               ▼
       [Open-Meteo API]              [ICAR / FAO Knowledge]          [Math Risk Engine]             [Advisory Rule Base]
       [IMD AAS Baseline]            [5 Primary Crops JSON]          [0-100 Scored Models]          [Bilingual EN / HI]
```

---

## Specialist Agents Breakdown

### 1. Krishi Orchestrator (`backend/app/agents/orchestrator.py`)
- **Framework**: `strands.Agent`
- **Role**: Central coordinator managing intent extraction, pipeline delegation, result validation, and bilingual synthesis.
- **Tools**: Registers the 4 specialist agents as tools using the **Strands Agents as Tools** pattern.
- **Workflow**:
  1. Parses farmer query to extract location, crop, growth stage, and specific concerns (in Hindi or English).
  2. Resolves geolocation via `WeatherIntelligenceAgent`.
  3. Pulls physiological thresholds via `CropIntelligenceAgent`.
  4. Triggers mathematical risk computation via `RiskAssessmentAgent`.
  5. Translates findings into a 3-day action plan via `FarmingAdvisoryAgent`.
  6. Compiles traceable steps and returns structured response.

### 2. Weather Intelligence Agent (`backend/app/agents/weather_agent.py`)
- **Framework**: `strands.Agent`
- **Tools**:
  - `get_location_coordinates`: Resolves village/district to latitude and longitude.
  - `get_current_weather`: Fetches current temperature, humidity, rainfall, wind speed.
  - `get_weather_forecast`: Fetches 7-day daily forecast and next-24h hourly trends.
- **Data Source**: Open-Meteo Numerical Prediction Models & IMD Agromet reference baseline.
- **Integrity**: Caches responses for 15 minutes to prevent rate-limiting; never fabricates weather observations.

### 3. Crop Intelligence Agent (`backend/app/agents/crop_agent.py`)
- **Framework**: `strands.Agent`
- **Tools**:
  - `get_crop_profile`: Retrieves crop taxonomy, soil preferences, and ICAR/FAO citations.
  - `get_growth_stage_info`: Retrieves stage-specific optimal and critical temperature bounds, daily water requirement ($ET_c$), and excess rainfall tolerance.
- **Coverage**: Soybean, Rice (Paddy), Wheat, Maize, Cotton across 5 phenological growth stages.

### 4. Risk Assessment Agent (`backend/app/agents/risk_agent.py`)
- **Framework**: `strands.Agent`
- **Tools**:
  - `evaluate_climate_risks`: Calls the standalone deterministic Python risk engine (`DeterministicRiskEngine`).
- **Core Directive**: Numerical calculations are **100% deterministic code**—never hallucinated by an LLM prompt.
- **Categories Evaluated**:
  - Heat Stress ($T_{max} \ge T_{crit}$)
  - Excessive Rainfall ($R_{48h} > \text{Tolerance}_{stage}$)
  - Waterlogging (duration, accumulation, crop susceptibility)
  - Dry-Spell (consecutive dry days $\ge 6$ with high temperature)
  - Crop Water Stress (cumulative $ET_0$ vs precipitation deficit)

### 5. Farming Advisory Agent (`backend/app/agents/advisory_agent.py`)
- **Framework**: `strands.Agent`
- **Tools**:
  - `generate_farming_advisory`: Maps risk levels to practical farm-level precautions and 3-day action roadmaps.
- **Language Support**: Native Hindi (हिन्दी) and English.
- **Safety**: Recommends practical physical/drainage/irrigation interventions; never dispenses unverified chemical pesticides or replaces local KVK agronomists.

