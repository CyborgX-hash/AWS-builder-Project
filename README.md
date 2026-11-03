# KrishiSathi 
### AI-Powered Multi-Agent Climate Intelligence for Smallholder Farmers
> *"Turning Weather Intelligence into Smarter Farming Decisions."*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React-18.x-61dafb.svg)](https://react.dev)
[![AWS Hackathon](https://img.shields.io/badge/AWS%20Hackathon-Social%20Good%202026-FF9900.svg)](https://aws.amazon.com)
[![Tests Passing](https://img.shields.io/badge/Tests-41%20Passed-brightgreen.svg)]()

**KrishiSathi** is an agricultural climate intelligence platform built for smallholder farmers in India and underserved rural communities. Developed for the **AWS Strands Agents Social Good Hackathon 2026**, KrishiSathi bridges the critical gap between raw meteorological forecasts and localized, crop-specific farming decisions.

---

## 🌾 The Problem

In India, over **86% of farmers operate small and marginal land holdings (< 2 hectares)**. Traditional weather applications provide numbers like `"Rain 35 mm, Temperature 32°C"`, but fail to answer practical farmer questions:
- *Will upcoming rain damage my soybean crop at its current flowering stage?*
- *Is waterlogging likely in my heavy black clay soil over the next 48 hours?*
- *Should I withhold expensive urea fertilizer or pesticide sprays before the rain?*
- *Should I pause or adjust irrigation today?*

Generic LLM chatbots often hallucinate agronomic thresholds or make up chemical treatments. KrishiSathi replaces guesswork with a **collaborative multi-agent AI architecture** backed by a **deterministic mathematical risk engine**.

---

## 💡 The Solution

KrishiSathi translates real-time forecasts into crop-specific precautions and 3-day action plans using a **hierarchical multi-agent team**:
1. **Krishi Orchestrator**: Understands queries in Hindi or English, extracts entities, and coordinates specialist agents.
2. **Weather Intelligence Agent**: Retrieves live observations and 7-day numerical forecasts via Open-Meteo and IMD.
3. **Crop Intelligence Agent**: Provides crop thresholds, growth stage vulnerability, and agronomic knowledge from ICAR and FAO.
4. **Risk Assessment Agent**: Executes a **deterministic Python risk engine** (no hallucinated risk scores) evaluating heat stress, excessive rainfall, waterlogging, dry spells, and water stress.
5. **Farming Advisory Agent**: Synthesizes practical, preventive agricultural advisories and 3-day action roadmaps.

---

## 🏗️ Multi-Agent Architecture

```
                              ┌────────────────────────────────────────┐
                              │            Farmer / Web Client         │
                              │     (React, Vite, Tailwind, Recharts)  │
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

## 🤖 The Specialist Agents

| Agent | Module | Role & Core Responsibilities | Tools Used |
|---|---|---|---|
| **Krishi Orchestrator** | `backend/app/agents/orchestrator.py` | Query parsing, entity extraction, specialist task delegation, validation, bilingual synthesis | Strands Agents as Tools pattern |
| **Weather Agent** | `backend/app/agents/weather_agent.py` | Real-time weather, 7-day daily forecasts, 24h hourly trends, wind, evapotranspiration | `get_current_weather`, `get_weather_forecast`, `get_location_coordinates` |
| **Crop Agent** | `backend/app/agents/crop_agent.py` | Agronomic knowledge for Soybean, Rice, Wheat, Maize, Cotton across 5 growth stages | `get_crop_profile`, `get_growth_stage_info` |
| **Risk Agent** | `backend/app/agents/risk_agent.py` | Evaluates Heat Stress, Excessive Rain, Waterlogging, Dry Spells, Water Stress | `evaluate_climate_risks` (calls deterministic engine) |
| **Advisory Agent** | `backend/app/agents/advisory_agent.py` | Practical preventive farm actions and 3-day action plans in Hindi and English | `generate_farming_advisory` |

---

## 🔬 Deterministic Risk Engine (No Hallucinations)

Unlike typical AI chatbots that invent numerical risk numbers inside prompt text, KrishiSathi's risk engine (`backend/app/services/risk_engine.py`) is written in **deterministic Python**:
- **Heat Stress**: Evaluates forecasted daytime highs against critical stage-specific thresholds ($T_{max} \ge T_{crit}$, e.g. >36°C for soybean flowering).
- **Excessive Rainfall**: Compares 48h cumulative rainfall against stage tolerance and IMD Heavy Rain standards (>64.5 mm/24h).
- **Waterlogging**: Considers 72h rainfall, consecutive wet days, and crop susceptibility (Soybean/Maize high risk vs Rice flood tolerance).
- **Dry-Spell**: Tracks consecutive rainless days ($\ge 6$ days with $T_{avg} > 33^\circ\text{C}$).
- **Crop Water Stress**: Water balance deficit comparing cumulative $ET_0$ water requirements vs expected precipitation.

Risk Classification: **LOW (0-35)**, **MODERATE (36-69)**, **HIGH (70-100)**.

---

## 🚀 Key Features

- **Hyperlocal Climate Intelligence**: Real-time and 7-day weather telemetry for any Indian village, block, or district.
- **Crop-Specific Sensitivity**: Sourced agronomic thresholds from ICAR-IISR, ICAR-NRRI, ICAR-IIWBR, and FAO-56.
- **Actionable 3-Day Roadmap**: Day 1 (Next 24h), Day 2 (Next 48h), Day 3 (Next 72h) practical instructions.
- **Bilingual Interface**: Native support for **Hindi (हिन्दी)** and **English**, designed specifically for rural farmers.
- **Explainable Reports**: Transparent explanations of detected hazards, contributing weather factors, and confidence ratings.
- **Interactive Multi-Agent Chat**: Real-time trace visibility showing each agent's contribution step-by-step.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React, Recharts, Axios, React Router
- **Backend**: Python 3.11+, FastAPI, Pydantic 2.0, Uvicorn, httpx, SQLAlchemy, SQLite
- **AI & Multi-Agent**: AWS Strands Agents SDK & Amazon Bedrock (`anthropic.claude-3-5-sonnet-20241022-v2:0`)
- **Weather Data**: Open-Meteo Global Forecast Models & IMD Agromet reference baseline
- **Testing**: Pytest (41 automated test scenarios passing)
- **Deployment**: Docker, Docker Compose, Vercel, AWS App Runner / ECS

---

## 📁 Repository Structure

```
KrishiSathi/
├── frontend/                     # React + Vite + Tailwind UI
│   ├── src/
│   │   ├── components/           # WeatherCard, RiskIndicator, CropSelector, ChatAssistant
│   │   ├── pages/                # Landing, Dashboard, RiskReport, Advisory
│   │   └── services/api.js       # Axios client for FastAPI backend
│   └── package.json
├── backend/                      # FastAPI + Strands Multi-Agent system
│   ├── app/
│   │   ├── agents/               # Orchestrator & 4 Specialist Agents
│   │   ├── tools/                # Strands agent tool functions
│   │   ├── services/             # Deterministic Risk Engine & Weather Service
│   │   ├── knowledge/            # Crop profiles JSON & Advisory rules JSON
│   │   ├── schemas/              # Pydantic data schemas
│   │   └── api/routes.py         # REST API Endpoints
│   └── tests/                    # 41 Pytest unit & scenario tests
├── docs/                         # Architecture, Impact Metrics, Data Sources, Deployment
├── reports/                      # Sample agricultural advisory reports
├── Dockerfile                    # Production backend container
├── docker-compose.yml            # Local / Cloud single-command runner
├── vercel.json                   # Vercel frontend deployment config
└── README.md
```

---

## 🚦 Quickstart Guide

### 1. Clone the repository
```bash
git clone https://github.com/CyborgX-hash/AWS-builder-Project.git
cd AWS-builder-Project
```

### 2. Run Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```
API Documentation will be live at `http://localhost:8000/docs`.

### 3. Run Frontend
```bash
cd ../frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

### 4. Or Run Everything via Docker Compose
```bash
docker-compose up --build
```

---

## 🧪 Testing Suite (41 Scenarios Passed)

Execute the full automated test suite:
```bash
PYTHONPATH=backend backend/.venv/bin/pytest backend/tests -v
```

Test coverage includes:
- Heavy rainfall on Soybean flowering triggering HIGH waterlogging risk
- Heatwave (42°C) on Maize during silking
- Extended dry spell on Soybean pod filling
- Rice submergence vs flood tolerance during tillering
- Unseasonal harvest rain on mature Wheat
- Terminal heat stress during grain milking
- Fallback coordinates and resilient offline weather handling
- Bilingual Hindi and English multi-agent query execution

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
