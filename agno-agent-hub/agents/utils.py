"""Shared helper: run an Agno agent/team with automatic retry on transient
tool-call errors (a known occasional glitch with some Groq models where the
model emits a malformed tool call, e.g. wrong argument names)."""

import time


def run_with_retry(agent, *args, max_retries: int = 2, delay_seconds: float = 1.5, **kwargs):
    """Call agent.run(*args, **kwargs), retrying on failure.

    Returns the successful response object. If every attempt fails, returns
    a lightweight object with a friendly `.content` message instead of
    raising, so the Streamlit UI never crashes on a transient error.
    """
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return agent.run(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001 - we want to catch and retry any provider error
            last_error = exc
            if attempt < max_retries:
                time.sleep(delay_seconds)

    class _FallbackResponse:
        content = (
            "Sorry, I hit a temporary error talking to the model "
            f"(after {max_retries + 1} attempts): `{last_error}`.\n\n"
            "This is usually a brief hiccup - please try asking again."
        )

    return _FallbackResponse()
