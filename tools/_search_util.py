import re
import hashlib
from functools import lru_cache
from langchain_community.tools import DuckDuckGoSearchRun

_ddg = DuckDuckGoSearchRun()

# How many characters of DDG output to pass to the LLM — enough signal, not noise
_MAX_CHARS = 800


def _clean(text: str) -> str:
    """Remove repeated whitespace, strip ad-like fragments, truncate."""
    text = re.sub(r"\s+", " ", text).strip()
    # Remove promo-code noise
    text = re.sub(r"(promo code\s+\w+[\w\d]*)", "", text, flags=re.IGNORECASE)
    return text[:_MAX_CHARS]


@lru_cache(maxsize=64)
def _cached_search(query: str) -> str:
    """LRU-cached DDG search — identical queries within a process hit DDG only once."""
    try:
        raw = _ddg.invoke(query)
        return _clean(raw)
    except Exception as e:
        return f"Search error: {str(e)}"


def ddg_search(query: str) -> str:
    query = query.strip()
    if not query:
        return "Error: search query cannot be empty."
    return _cached_search(query)