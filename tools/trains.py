from langchain.tools import tool
from tools._search_util import ddg_search


@tool
def get_trains(query: str) -> str:
    """Search for trains between cities on Indian Railways / IRCTC.
    Input: natural language query e.g. 'Bhubaneswar to Goa train schedule fare'
    Returns: train names, schedules, and ticket prices.
    """
    return ddg_search(query)