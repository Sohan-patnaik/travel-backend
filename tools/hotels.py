from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool

search = DuckDuckGoSearchRun()

class Hotels:
    @tool
    def get_hotels(query: str):
        """Search hotels in a city"""
        return search.run(query + " best hotels price per night")