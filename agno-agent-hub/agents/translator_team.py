"""Answer & Translation Team — three language-specialist agents answer together."""

from agno.agent import Agent
from agno.models.groq import Groq
from agno.team import Team


def build_translator_team() -> Team:
    eng_agent = Agent(name="English Agent", role="You answer questions in English")
    chi_agent = Agent(name="Chinese Agent", role="You answer questions in Chinese")
    hindi_agent = Agent(name="Hindi Agent", role="You answer questions in Hindi")

    return Team(
        name="Answer & Translation Team",
        members=[eng_agent, chi_agent, hindi_agent],
        model=Groq(id="qwen/qwen3-32b"),
        markdown=True,
        show_members_responses=True,
        instructions=(
            "All member agents must respond to answer the query in their specific "
            "language. Do not route to just one agent. Output the response of all agents."
        ),
    )
