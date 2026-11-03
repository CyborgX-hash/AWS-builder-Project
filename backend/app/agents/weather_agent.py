from strands import Agent
from app.tools.weather_tool import get_current_weather, get_weather_forecast
from app.tools.location_tool import get_location_coordinates
from app.agents.model_factory import get_bedrock_model

WEATHER_AGENT_SYSTEM_PROMPT = """You are the Weather Intelligence Specialist Agent for KrishiSathi.
Your primary responsibility is to analyze meteorological patterns for Indian agricultural regions.

Capabilities & Tools:
1. get_location_coordinates: Resolves any village, town, or district in India to its latitude and longitude.
2. get_current_weather: Retrieves real-time temperature, humidity, rainfall, wind speed, and observation time.
3. get_weather_forecast: Retrieves 7-day daily forecasts, precipitation accumulations, and hourly trends.

Guidelines:
- Never fabricate or guess weather data.
- Always use the tools to retrieve actual data for the farmer's location.
- Provide objective meteorological summaries focusing on agricultural impacts (e.g., rainfall amounts, precipitation probability, peak daytime temperatures, dry spells).
- Distinguish clearly between current observations and future forecasts.
- If data retrieval fails, state clearly that the weather data is currently unavailable.
"""


def create_weather_agent() -> Agent:
    """Instantiate the Strands Weather Intelligence Agent."""
    return Agent(
        model=get_bedrock_model(),
        name="WeatherIntelligenceAgent",
        description="Retrieves and interprets real-time and 7-day numerical weather forecasts, rainfall probabilities, and temperature trends.",
        tools=[get_location_coordinates, get_current_weather, get_weather_forecast],
        system_prompt=WEATHER_AGENT_SYSTEM_PROMPT
    )

