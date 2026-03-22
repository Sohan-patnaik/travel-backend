import os
import requests
from langchain.tools import tool


@tool
def weather(city: str) -> str:
    """Get current weather for a city. Input should be a city name."""
    city = city.strip()
    if not city:
        return "Error: city name cannot be empty."

    api_key = os.getenv("WEATHERSTACK_API_KEY")
    if not api_key:
        return "Error: weather service is not configured."

    try:
        response = requests.get(
            "https://api.weatherstack.com/current",
            params={"access_key": api_key, "query": city},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            return f"Weather API error: {data['error'].get('info', 'Unknown error')}"

        current = data.get("current", {})
        location = data.get("location", {})
        return (
            f"Weather in {location.get('name', city)}: "
            f"{current.get('temperature')}°C, "
            f"{current.get('weather_descriptions', ['N/A'])[0]}, "
            f"Humidity: {current.get('humidity')}%, "
            f"Wind: {current.get('wind_speed')} km/h"
        )

    except requests.Timeout:
        return "Error: weather service timed out. Please try again."
    except requests.RequestException as e:
        return f"Error fetching weather: {str(e)}"