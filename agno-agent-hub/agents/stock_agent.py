"""Investment Analyst Agent - stock prices, fundamentals, and analyst views."""

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools


def build_stock_agent() -> Agent:
    return Agent(
        name="Investment Analyst",
        model=Groq(id="openai/gpt-oss-120b"),
        tools=[YFinanceTools(), DuckDuckGoTools()],
        markdown=True,
        add_datetime_to_context=True,
        description=(
            "You are an investment analyst that researches stock prices, "
            "analyst recommendations, and stock fundamentals."
        ),
        instructions=[
            "Use the given tools whenever possible instead of relying on memory.",
            "Format your response using markdown and use tables to display data where possible.",
            "Clearly state the ticker, currency, and as-of date/time for any price you quote.",
        ],
    )
