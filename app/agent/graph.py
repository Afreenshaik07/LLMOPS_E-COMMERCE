from langgraph.graph import StateGraph, START, END

from app.agent.state import AgentState

from app.agent.nodes import (
    router_node,
    product_search_node,
    product_details_node,
    inventory_node,
    comparison_node,
    response_node,
)

from app.agent.entity_extractor import entity_extraction_node


def route_by_intent(state: AgentState):
    """
    Decide which tool node should execute
    based on the detected intent.
    """

    intent = state["intent"]

    if intent == "product_search":
        return "product_search"

    if intent == "product_details":
        return "product_details"

    if intent == "inventory":
        return "inventory"

    if intent == "comparison":
        return "comparison"

    # Default route
    return "product_search"


def build_graph():
    """
    Build the LangGraph agent workflow.
    """

    graph = StateGraph(AgentState)

    # ==================================================
    # ADD NODES
    # ==================================================

    graph.add_node(
        "router",
        router_node
    )

    graph.add_node(
        "entity_extraction",
        entity_extraction_node
    )

    graph.add_node(
        "product_search",
        product_search_node
    )

    graph.add_node(
        "product_details",
        product_details_node
    )

    graph.add_node(
        "inventory",
        inventory_node
    )

    graph.add_node(
        "comparison",
        comparison_node
    )

    graph.add_node(
        "response",
        response_node
    )

    # ==================================================
    # START → ROUTER
    # ==================================================

    graph.add_edge(
        START,
        "router"
    )

    # ==================================================
    # ROUTER → ENTITY EXTRACTION
    # ==================================================

    graph.add_edge(
        "router",
        "entity_extraction"
    )

    # ==================================================
    # ENTITY EXTRACTION → TOOL
    # ==================================================

    graph.add_conditional_edges(
        "entity_extraction",
        route_by_intent,
        {
            "product_search": "product_search",
            "product_details": "product_details",
            "inventory": "inventory",
            "comparison": "comparison",
        },
    )

    # ==================================================
    # TOOL → RESPONSE
    # ==================================================

    graph.add_edge(
        "product_search",
        "response"
    )

    graph.add_edge(
        "product_details",
        "response"
    )

    graph.add_edge(
        "inventory",
        "response"
    )

    graph.add_edge(
        "comparison",
        "response"
    )

    # ==================================================
    # RESPONSE → END
    # ==================================================

    graph.add_edge(
        "response",
        END
    )

    return graph.compile()


def main():

    print("=" * 70)
    print("LANGGRAPH AGENT - ALL ROUTES TEST")
    print("=" * 70)

    agent = build_graph()

    # ==================================================
    # TEST QUERIES
    # ==================================================

    test_queries = [

        "I need an Apple laptop under 90000",

        "Tell me the details of MacBook Air M2",

        "Is MacBook Air M2 in stock?",

        "Compare MacBook Air M2 and IdeaPad Slim 3",
    ]

    # ==================================================
    # RUN EACH QUERY
    # ==================================================

    for query in test_queries:

        print("\n" + "=" * 70)
        print("USER QUERY")
        print("=" * 70)

        print(query)

        print("\nRunning LangGraph...\n")

        result = agent.invoke(
            {
                "query": query
            }
        )

        print("\n" + "=" * 70)
        print("FINAL ANSWER")
        print("=" * 70)

        print(result["response"])

        print("\n" + "-" * 70)
        print("FINAL GRAPH STATE")
        print("-" * 70)

        print(result)


if __name__ == "__main__":
    main()