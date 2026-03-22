from langchain.tools import tool
from tools._search_util import ddg_search


@tool
def get_hotels(query: str) -> str:
    """Search for hotels in a city.
    Input: natural language query e.g. 'budget hotels in Goa under 1000 per night'
    Returns: hotel names, prices, and booking info.
    """
    return ddg_search(query)