from app.agent.state import AgentState


PRODUCTS = [
    "MacBook Air M2",
    "IdeaPad Slim 3",
    "Vivobook 15",
    "Inspiron 15",
    "Galaxy Book4",
    "WH-CH520",
    "AirPods 4",
    "Galaxy Buds FE",
    "MX Master 3S",
    "Magic Mouse",
    "K380 Keyboard",
    "Galaxy Tab S9",
    "iPad 10th Gen",
    "Redmi Pad Pro",
    "PowerCore 20K",
]


def entity_extraction_node(state: AgentState):
    """
    Extract product names mentioned in the user query.
    """

    query = state["query"].lower()

    found_products = []

    for product in PRODUCTS:

        if product.lower() in query:
            found_products.append(product)

    print("\n[ENTITY EXTRACTION NODE]")

    print(f"Products found: {found_products}")

    result = {}

    if len(found_products) >= 1:
        result["product_name"] = found_products[0]

    if len(found_products) >= 2:
        result["product_name_2"] = found_products[1]

    return result


def main():

    test_queries = [
        "Tell me the details of MacBook Air M2",
        "Is MacBook Air M2 in stock?",
        "Compare MacBook Air M2 and IdeaPad Slim 3",
    ]

    for query in test_queries:

        print("\n" + "=" * 60)
        print("Query:")
        print(query)

        state = {
            "query": query
        }

        result = entity_extraction_node(state)

        print("Extracted:")
        print(result)


if __name__ == "__main__":
    main()