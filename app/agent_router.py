from app.tools.product_search import ProductSearchTool
from app.tools.product_details import ProductDetailsTool
from app.tools.inventory import InventoryTool
from app.tools.comparison import ProductComparisonTool


class AgentRouter:
    """
    Routes user queries to the appropriate
    e-commerce tool.
    """

    def __init__(self):

        self.search_tool = ProductSearchTool()
        self.details_tool = ProductDetailsTool()
        self.inventory_tool = InventoryTool()
        self.comparison_tool = ProductComparisonTool()

    def detect_intent(self, query):
        """
        Detect the user's intent using simple rules.
        """

        query_lower = query.lower()

        # Comparison intent
        if (
            "compare" in query_lower
            or "comparison" in query_lower
            or "difference between" in query_lower
        ):
            return "comparison"

        # Inventory intent
        if (
            "in stock" in query_lower
            or "stock" in query_lower
            or "available" in query_lower
            or "availability" in query_lower
        ):
            return "inventory"

        # Product details intent
        if (
            "details" in query_lower
            or "specifications" in query_lower
            or "specs" in query_lower
            or "tell me about" in query_lower
        ):
            return "product_details"

        # Default → product search
        return "product_search"

    def route(self, query):
        """
        Route the query to the appropriate tool.
        """

        intent = self.detect_intent(query)

        print("\nDetected Intent:")
        print("-" * 50)
        print(intent)

        return intent


def main():

    print("=" * 70)
    print("AGENT ROUTER")
    print("=" * 70)

    router = AgentRouter()

    test_queries = [
        "I need an Apple laptop under 90000",
        "Tell me the details of MacBook Air M2",
        "Is MacBook Air M2 in stock?",
        "Compare MacBook Air M2 and IdeaPad Slim 3"
    ]

    for query in test_queries:

        print("\n" + "=" * 70)
        print("User Query:")
        print(query)

        router.route(query)


if __name__ == "__main__":
    main()