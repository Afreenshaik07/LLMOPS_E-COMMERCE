from app.agent_router import AgentRouter


class AgentExecutor:
    """
    Executes the tool selected by the AgentRouter.
    """

    def __init__(self):

        self.router = AgentRouter()

    def execute(self, query):

        intent = self.router.detect_intent(query)

        print("\nDetected Intent:")
        print("-" * 50)
        print(intent)

        # --------------------------------------------------
        # Product Search
        # --------------------------------------------------

        if intent == "product_search":

            print("\nExecuting Product Search Tool...")

            results = self.router.search_tool.search(query)

            return results

        # --------------------------------------------------
        # Product Details
        # --------------------------------------------------

        elif intent == "product_details":

            print("\nExecuting Product Details Tool...")

            # Temporary product extraction
            product_name = self.extract_product_name(query)

            return self.router.details_tool.get_details(
                product_name
            )

        # --------------------------------------------------
        # Inventory
        # --------------------------------------------------

        elif intent == "inventory":

            print("\nExecuting Inventory Tool...")

            product_name = self.extract_product_name(query)

            return self.router.inventory_tool.check_stock(
                product_name
            )

        # --------------------------------------------------
        # Comparison
        # --------------------------------------------------

        elif intent == "comparison":

            print("\nExecuting Comparison Tool...")

            product1 = "MacBook Air M2"
            product2 = "IdeaPad Slim 3"

            return self.router.comparison_tool.compare(
                product1,
                product2
            )

        return None

    def extract_product_name(self, query):

        products = [
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
            "PowerCore 20K"
        ]

        query_lower = query.lower()

        for product in products:

            if product.lower() in query_lower:
                return product

        return query


def main():

    print("=" * 70)
    print("AGENT EXECUTOR")
    print("=" * 70)

    executor = AgentExecutor()

    queries = [
        "I need an Apple laptop under 90000",
        "Tell me the details of MacBook Air M2",
        "Is MacBook Air M2 in stock?",
        "Compare MacBook Air M2 and IdeaPad Slim 3"
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print("USER:")
        print(query)

        result = executor.execute(query)

        print("\nTOOL RESULT:")
        print("-" * 70)

        print(result)


if __name__ == "__main__":
    main()