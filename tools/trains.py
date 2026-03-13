from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool

search = DuckDuckGoSearchRun()


class Trains:
    @tool
    def get_trains(query: str):
        """Search trains between cities"""
        return search.run(query + " trains IRCTC schedule")