# KrishiSathi (कृषिसार्थी)
> *"Turning Weather Intelligence into Smarter Farming Decisions."*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.x-61dafb.svg)](https://react.dev)
[![AWS Hackathon](https://img.shields.io/badge/AWS%20Hackathon-Social%20Good%202026-FF9900.svg)](https://aws.amazon.com)

**KrishiSathi** is an AI-powered multi-agent agricultural climate intelligence platform built for smallholder farmers in India and underserved rural communities. Built for the **AWS Strands Agents Social Good Hackathon 2026**, KrishiSathi bridges the critical gap between raw meteorological data and actionable, crop-specific farming decisions.

---

## 🌾 The Problem

Smallholder farmers often make high-stakes agricultural decisions without actionable, localized weather intelligence. Traditional weather apps display temperatures and rainfall numbers, but they fail to answer practical farmer questions:
- *Will upcoming rainfall damage my crop at its current growth stage?*
- *Is waterlogging likely in my fields over the next 48 hours?*
- *Should I withhold or adjust irrigation?*
- *What specific preventive measures should I take today?*

## 💡 The Solution

KrishiSathi translates raw forecast data into deterministic, agronomic risk assessments and multi-day action plans using a **hierarchical multi-agent architecture**:
1. **Krishi Orchestrator**: Understands queries in Hindi or English, extracts intent, and coordinates specialist agents.
2. **Weather Intelligence Agent**: Fetches hyperlocal live and 7-day forecast data from Open-Meteo and IMD.
3. **Crop Intelligence Agent**: Provides crop thresholds, growth stage vulnerability, and agronomic knowledge.
4. **Risk Assessment Agent**: Executes a **deterministic Python risk engine** (no hallucinated risk scores) evaluating heat stress, excessive rainfall, waterlogging, dry spells, and water stress.
5. **Farming Advisory Agent**: Synthesizes practical, preventive agricultural advisories and 3-day action plans.

---

## 🚀 Key Features

- **Hyperlocal Climate Intelligence**: Real-time and 7-day weather forecasts via Open-Meteo & IMD for any Indian village, block, or district.
- **Crop-Specific Risk Analysis**: Sourced agronomic thresholds for Soybean, Rice (Paddy), Wheat, Maize, Cotton across specific growth stages.
- **Deterministic Risk Engine**: Mathematical risk scoring independent of LLM text generation.
- **Actionable Multi-Day Planner**: Step-by-step 24h/48h/72h farming action roadmaps.
- **Bilingual Interface & Assistant**: Native support for **Hindi (हिन्दी)** and **English**, designed specifically for rural farmers.
- **Explainable Reports**: Transparent explanations of detected weather hazards, contributing factors, and confidence levels.

---

## 🏗️ Architecture

```
                       ┌─────────────────────────┐
                       │   Farmer / Web Client   │
                       │   (React + Vite + UI)   │
                       └────────────┬────────────┘
                                    │ HTTP / REST
                       ┌────────────▼────────────┐
                       │     FastAPI Backend     │
                       └────────────┬────────────┘
                                    │
                       ┌────────────▼────────────┐
                       │   Krishi Orchestrator   │
                       │  (Multi-Agent Manager)  │
                       └─────┬───┬─────┬───┬─────┘
           ┌─────────────────┘   │     │   └────────────────┐
           ▼                     ▼     ▼                    ▼
┌────────────────────┐ ┌───────────┐ ┌─────────────┐ ┌──────────────┐
│ Weather Agent      │ │Crop Agent │ │Risk Agent   │ │Advisory Agent│
│ (Open-Meteo / IMD) │ │(Agronomics│ │(Deterministic││(Action Plans │
│                    │ │ Knowledge)│ │ Risk Engine)│ │  Hindi/Eng)  │
└────────────────────┘ └───────────┘ └─────────────┘ └──────────────┘
```

---

## 🛠️ Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React, Recharts, Axios, React Router
- **Backend**: Python 3.11+, FastAPI, Pydantic, Uvicorn, httpx, SQLite / SQLAlchemy
- **AI & Agents**: Strands Agents SDK & Amazon Bedrock foundation models
- **Weather Data**: Open-Meteo API & IMD (India Meteorological Department)
- **Testing**: Pytest, FastAPI TestClient, Vitest

---

## 📁 Repository Structure

```
KrishiSathi/
├── frontend/             # React + Vite + Tailwind UI
├── backend/              # FastAPI + Strands Multi-Agent system
│   ├── app/
│   │   ├── agents/       # Orchestrator & 4 Specialist Agents
│   │   ├── services/     # Deterministic Risk Engine & Weather Service
│   │   ├── knowledge/    # Crop profiles & Advisory rules
│   │   └── api/          # REST API Endpoints
│   └── tests/            # Pytest test suite
├── docs/                 # Architecture, Impact, and Progress documentation
├── reports/              # Sample agricultural advisories
├── README.md
├── LICENSE
└── .env.example
```

---

## 🚦 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/CyborgX-hash/AWS-builder-Project.git
cd AWS-builder-Project
```

### 2. Backend Setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```

Visit `http://localhost:5173` in your browser.

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).

