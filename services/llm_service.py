import os
from functools import lru_cache
from dotenv import load_dotenv
from pathlib import Path
from langchain_nvidia_ai_endpoints import ChatNVIDIA

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


@lru_cache(maxsize=1)
def get_llm() -> ChatNVIDIA:
    """Singleton NVIDIA LLM instance — cached for process lifetime."""
    
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise EnvironmentError("NVIDIA_API_KEY is not set in environment.")

    return ChatNVIDIA(
        model="nvidia/nemotron-3-super-120b-a12b",
        api_key=api_key,
        temperature=0,             
        top_p=0.95,
        max_tokens=16384,
        reasoning_budget=16384,
        request_timeout=30,
        max_retries=3,
        chat_template_kwargs={"enable_thinking": True},
    )