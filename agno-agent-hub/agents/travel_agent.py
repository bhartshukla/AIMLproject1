"""Travel Safety Agent — answers travel/safety questions using live web search."""

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools


def build_travel_agent() -> Agent:
    return Agent(
        name="Travel Safety Agent",
        model=Groq(id="qwen/qwen3-32b"),
        tools=[DuckDuckGoTools()],
        markdown=True,
        instructions=(
            "You are a helpful and expert travel agent. Use web search to check "
            "current safety advisories, weather, visa rules, and local conditions "
            "before answering. Always mention the recency of your information."
        ),
        add_datetime_to_context=True,
    )
