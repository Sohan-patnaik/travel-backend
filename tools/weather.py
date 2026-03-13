from langchain_community.tools import tool
import requests

class Weather:

    @tool
    def weather(city: str):
        """Get weather of the city"""
        url = f"https://api.weatherstack.com/current?access_key=21a1c74f5a0fa5380bc2f9b783b3e798&query={city}"
        r = requests.get(url)
        return str(r.json())