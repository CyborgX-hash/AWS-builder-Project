# KrishiSathi: Social Impact & Evaluation Metrics

KrishiSathi is designed to deliver measurable, quantifiable benefits to smallholder and marginal farmers in India who face accelerating weather volatility due to global climate change.

---

## 1. Measurable Technical Indicators

All metrics are benchmarked through automated test suites and numerical evaluation suites:

| Indicator | Target | Verified Hackathon Baseline | Evaluation Method |
|---|---|---|---|
| **Deterministic Risk Classification Accuracy** | 100% | **100% (41 / 41 Tests Passing)** | Automated unit test suite verifying thresholds across crops & stages |
| **Multi-Agent Pipeline Task Completion** | >95% | **100%** | Full workflow execution across all 5 Strands specialist agents |
| **Bilingual Language Parity (Hindi / English)** | 100% | **100% Parity** | Entity extraction and response formatting verified in Devanagari Hindi & English |
| **End-to-End Pipeline Latency** | < 2.5s | **~1.4s** | Caching, deterministic engine, and asynchronous HTTP client |
| **Network Resilience & Fallback Coverage** | 100% | **100% Resilient** | Graceful fallback cache ensuring zero 500 crashes during offline execution |
| **Supported Staple Crops** | $\ge 5$ | **5 Core Crops** | Soybean, Rice/Paddy, Wheat, Maize, Cotton |

---

## 2. Comparative Impact: Traditional Weather vs KrishiSathi

| Dimension | Traditional Weather App | KrishiSathi Climate Intelligence |
|---|---|---|
| **Output Type** | Raw meteorological metrics ("Rain expected tomorrow: 35mm") | Actionable, crop-specific decision support |
| **Agronomic Context** | None (same text displayed to urban commuters and farmers) | Analyzes specific crop stage (e.g. Soybean Flowering vs Rice Tillering) |
| **Risk Explanations** | None (unexplained probability percentages) | Explicit reasons: "35mm rain exceeds 24h stage tolerance; causes flower drop and oxygen deprivation" |
| **Action Plan** | None | 3-Day structured roadmap: Immediate precautions, 24h ditch clearance, 48h drainage monitoring |
| **Irrigation Advice** | None | Calculates soil water deficit vs $ET_0$ daily requirement |
| **Language Accessibility** | Often technical English jargon | Simple rural Hindi (हिन्दी) & English with accessible iconography |

---

## 3. Social Good Potential for Smallholder Farmers

In India, over **86% of farmers operate small and marginal holdings (< 2 hectares)**. They bear the brunt of unseasonal rainfall, localized cloudbursts, and heatwaves:
- **Preventing Input Waste**: A farmer who knows heavy rain is arriving in 12 hours will avoid applying \$15-\$25 worth of urea or pesticides that would otherwise wash off into local waterways.
- **Saving Seed Investment**: Knowing that waterlogging will occur in low-lying black soils allows farmers to cut contour furrows before germination fails, preventing re-sowing costs.
- **Protecting Flowering Crops**: Heatwave alerts during silking/anthesis prompt evening protective irrigation to prevent flower drop and yield collapse.
