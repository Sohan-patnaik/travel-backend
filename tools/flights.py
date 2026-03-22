from langchain.tools import tool
from tools._search_util import ddg_search


@tool
def get_flights(query: str) -> str:
    """Search for flights between cities.
    Input: natural language query e.g. 'Bhubaneswar to Goa cheapest flight March 2026'
    Returns: flight prices, airlines, and availability info.
    """
    return ddg_search(query)