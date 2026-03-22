import logging
from functools import lru_cache
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from services.llm_service import get_llm
from tools.weather import weather
from tools.flights import get_flights
from tools.hotels import get_hotels
from tools.trains import get_trains
from tools.search import search_result

logger = logging.getLogger(__name__)

TOOLS = [get_flights, weather, get_hotels, get_trains, search_result]

SYSTEM_PROMPT = """You are an expert AI travel agent specializing in trips within and from India.

STRICT RULES — follow these exactly:
1. Call each tool AT MOST ONCE per user query. Never retry a tool with the same or similar input.
2. If a tool returns partial information, use what you have — do not call it again.
3. After collecting information from tools, ALWAYS provide a final answer to the user.
4. Never leave a query unanswered. If data is incomplete, give your best estimate and say so.

When planning trips always provide:
- Specific cost estimates in INR with a budget breakdown table
- Practical booking tips (best sites, timing)
- A day-by-day itinerary
- Total estimated cost vs the user's stated budget

Be concise, accurate, and helpful."""


@lru_cache(maxsize=1)
def get_agent_executor() -> AgentExecutor:
    """Build and cache the AgentExecutor — created once per process."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    llm = get_llm()

    agent = create_tool_calling_agent(
        llm=llm,
        tools=TOOLS,
        prompt=prompt,
    )

    return AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,
        max_iterations=8,
        max_execution_time=60,
        handle_parsing_errors=True,
        return_intermediate_steps=False,
    )


def run_agent(query: str) -> str:
    """Run the travel agent and return a plain-text response."""
    executor = get_agent_executor()
    try:
        result = executor.invoke({"input": query})
        return result.get("output", "I couldn't find an answer. Please try rephrasing.")
    except Exception as e:
        logger.exception("Agent execution failed for query: %s", query)
        return f"An error occurred while processing your request: {str(e)}"