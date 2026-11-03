from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class LocationCoordinates(BaseModel):
    name: str
    latitude: float
    longitude: float
    state: Optional[str] = None
    country: Optional[str] = "India"


class CurrentWeather(BaseModel):
    temperature: float = Field(..., description="Current temperature in Celsius")
    humidity: float = Field(..., description="Relative humidity in percentage")
    rainfall: float = Field(default=0.0, description="Precipitation in mm for the current hour")
    wind_speed: float = Field(default=0.0, description="Wind speed in km/h")
    rainfall_probability: int = Field(default=0, description="Precipitation probability 0-100%")
    weather_code: int = Field(default=0, description="WMO weather interpretation code")
    weather_description: str = Field(default="Clear", description="Human-readable weather description")
    time: str = Field(..., description="ISO timestamp of observation")


class DailyForecastItem(BaseModel):
    date: str
    temp_max: float
    temp_min: float
    rainfall_sum: float
    precipitation_probability_max: int
    weather_code: int
    weather_description: str
    et0_fao_evapotranspiration: Optional[float] = None


class HourlyForecastItem(BaseModel):
    time: str
    temperature: float
    humidity: float
    precipitation: float
    precipitation_probability: int


class WeatherSummary(BaseModel):
    location: str
    latitude: float
    longitude: float
    current: CurrentWeather
    daily: List[DailyForecastItem]
    hourly_next_24h: List[HourlyForecastItem]
    source: str = "Open-Meteo & IMD Reference"
    retrieved_at: str

