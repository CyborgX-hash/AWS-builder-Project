# KrishiSathi Data Sources & Agronomic References

KrishiSathi integrates official meteorological observations, global numerical weather predictions, and validated Indian agricultural research guidelines.

---

## 1. Meteorological Data Sources

### Open-Meteo Weather API
- **Endpoint**: `https://api.open-meteo.com/v1/forecast`
- **Geocoding Endpoint**: `https://geocoding-api.open-meteo.com/v1/search`
- **Data Provided**:
  - Real-time 2m temperature (°C)
  - 2m relative humidity (%)
  - Hourly precipitation (mm) and precipitation probability (%)
  - Wind speed at 10m (km/h)
  - 7-day daily maximum / minimum temperatures
  - Daily precipitation accumulations
  - WMO 4677 weather interpretation codes
  - FAO-56 Reference Crop Evapotranspiration ($ET_0$, mm/day)
- **License**: Non-commercial & open-access with attribution under CC BY 4.0.

### India Meteorological Department (IMD)
- **Portal**: `https://mausam.imd.gov.in/` & `https://agromet.imd.gov.in/`
- **Agricultural Agromet Advisories**: National Agromet Advisory Services (AAS) bulletins under Gramin Krishi Mausam Sewa (GKMS).
- **Advisory Role**: Used to calibrate rainfall classification thresholds (Light, Moderate, Heavy, Very Heavy rain) and frost/heatwave warnings according to IMD meteorological standards.

---

## 2. Crop Knowledge Base & Agronomic Sourcing

All crop thresholds, optimal temperature windows, daily water requirements, and stage-specific sensitivities are derived from published research institutes:

### 1. Soybean (*Glycine max*)
- **Primary Source**: ICAR - Indian Institute of Soybean Research (IISR), Indore, Madhya Pradesh.
- **Reference**: IISR Technical Bulletins on *Package of Practices for Soybean in Central India*.
- **Vulnerabilities**: Water stagnation (>24h causes seed rot/chlorosis), Flower drop at ambient temp >35°C during anthesis, Pod filling moisture deficit.

### 2. Rice / Paddy (*Oryza sativa*)
- **Primary Source**: ICAR - National Rice Research Institute (NRRI), Cuttack, Odisha & ICAR - Indian Institute of Rice Research (IIRR), Hyderabad.
- **Reference**: *Rice Knowledge Management Portal (RKMP)* & NRRI Agricultural Climate Bulletins.
- **Vulnerabilities**: Submergence (>48h seedling damage), High temp sterility (>35°C during morning anthesis), Lodging with wind speeds >25 km/h.

### 3. Wheat (*Triticum aestivum*)
- **Primary Source**: ICAR - Indian Institute of Wheat and Barley Research (IIWBR), Karnal, Haryana & CIMMYT Global Wheat Program.
- **Reference**: *Crop Protection & Agronomy Bulletins for Timely and Late Sown Wheat in North-Western and Central Plains*.
- **Vulnerabilities**: Terminal heat stress (>32°C in grain filling/milking stage), Water stress at Crown Root Initiation (CRI) cutting yield by 25%, Hailstorm and lodging.

### 4. Maize (*Zea mays*)
- **Primary Source**: ICAR - Indian Institute of Maize Research (IIMR), Ludhiana, Punjab.
- **Reference**: *Production Technology of Kharif and Rabi Maize in India*.
- **Vulnerabilities**: Intolerance to water stagnation (>48h reduces yield by 35%), Silking desiccation at temperatures >35°C resulting in barren cobs.

### 5. Cotton (*Gossypium hirsutum*)
- **Primary Source**: ICAR - Central Institute for Cotton Research (CICR), Nagpur, Maharashtra.
- **Reference**: *CICR Technical Protocols on Climate Resilience and Boll Development*.
- **Vulnerabilities**: Asphyxiation of roots under waterlogging, Square and boll shedding under prolonged overcast/high humidity, Lint staining from unseasonal rain at boll bursting.

---

## 3. FAO Standard Reference
- **FAO-56 Irrigation and Drainage Paper No. 56**: *Crop Evapotranspiration - Guidelines for computing crop water requirements*.
- Used for calculating crop water stress and water balance: $ET_c = K_c \times ET_0$.
