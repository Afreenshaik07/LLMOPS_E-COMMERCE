from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    """
    Shared state used by the LangGraph agent.
    """

    query: str

    intent: str

    product_name: str

    product_name_2: str

    tool_result: Any

    response: str