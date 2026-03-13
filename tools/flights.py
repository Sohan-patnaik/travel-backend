from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool

search = DuckDuckGoSearchRun()

class Flights:
    @tool
    def get_flights(query: str):
        """Search flights between cities"""
        return search.run(query + " flights price airlines")