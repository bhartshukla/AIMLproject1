"""Memory Chat Agent - remembers facts about each user across turns via SQLite."""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.groq import Groq

DB_FILE = "agno_memory.db"


def build_memory_agent(db_file: str = DB_FILE) -> Agent:
    db = SqliteDb(db_file=db_file)
    return Agent(
        name="Memory Chat Agent",
        db=db,
        model=Groq(id="openai/gpt-oss-120b"),
        markdown=True,
        add_history_to_context=True,
        enable_user_memories=True,
        instructions=(
            "You are a friendly chat companion who remembers what the user tells you. "
            "Reply like a normal chat message - a few short sentences, no headers, no "
            "markdown tables, no bullet-point essays - unless the user specifically asks "
            "for a list or a detailed breakdown."
        ),
    )


def get_memories(agent: Agent, user_id: str):
    """Return the list of stored memories for a given user_id."""
    return agent.get_user_memories(user_id=user_id)
