from langchain.tools import tool
from tools._search_util import ddg_search


@tool
def search_result(query: str) -> str:
    """General web search for travel information — use for weather, local transport,
    food costs, sightseeing, visa, or anything not covered by other tools.
    Input: a clear, specific search query.
    """
    return ddg_search(query)