# KrishiSathi: Problem Statement

## The Agricultural Climate Dilemma in Rural India

Smallholder and marginal farmers constitute more than **86% of India's total farming households**. These farmers operate on thin profit margins, often with limited formal education, and face escalating climate risks:
1. **Unseasonal & Extreme Rainfall Events**: Sudden downpours during flowering or harvest destroy entire crop seasons.
2. **Prolonged Dry Spells within Monsoons**: Crops experience water stress during crucial physiological phases like pod filling or crown root initiation.
3. **Heat Spikes & Terminal Heat Stress**: Unseasonal March temperatures desiccate wheat florets, causing forced maturity and shriveled grain.
4. **Waterlogging & Poor Drainage**: Heavy clay soils (Vertisols) retain water, leading to root rot and collar rot in legumes like soybean.

---

## Why Conventional Weather Apps Fail Farmers

1. **Meteorological Data is Not Agricultural Advice**:
   - Standard weather apps display: `"Rain 30 mm, Humidity 85%, Temperature 28°C"`.
   - A farmer needs to know:
     - *Will this rain damage my soybean flowers?*
     - *Will water accumulate in my low-lying plot for more than 24 hours?*
     - *Should I postpone my urea top-dressing?*
     - *Should I irrigate today or wait for rainfall?*

2. **Crop Sensitivity Varies Drastically by Stage**:
   - 30 mm of rain is a blessing for Rice at Tillering stage, but catastrophic for Wheat at Harvest stage or Cotton at Boll Bursting.
   - Conventional weather apps make no distinction between crops or growth stages.

3. **Language and Technical Jargon Barriers**:
   - Meteorological terms like "precipitation probability", "relative humidity index", and "dew point" are rarely understood by rural smallholders who communicate in local languages like Hindi.

4. **Hallucination Risk of Generic LLMs**:
   - Asking a generic commercial LLM chatbot often leads to invented weather forecasts, fabricated pesticide prescriptions, and unreliable advice that can ruin a farmer's crop.

---

## The KrishiSathi Solution

KrishiSathi bridges this gap through a **hierarchical multi-agent AI architecture** powered by the **AWS Strands Agents SDK**:
- Integrates live meteorological radar from Open-Meteo and IMD.
- Leverages structured agronomic databases from ICAR (Indian Council of Agricultural Research) and FAO.
- Employs a **deterministic Python risk engine** where numerical risk scores (0-100) are computed mathematically without LLM hallucination.
- Formulates practical, preventive 3-day action plans in clear, rural-friendly Hindi and English.

