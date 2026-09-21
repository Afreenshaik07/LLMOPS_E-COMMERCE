from app.advanced_rag import AdvancedRAG


class ProductSearchTool:
    """
    Tool for searching e-commerce products
    using the Advanced RAG pipeline.
    """

    def __init__(self):
        self.rag = AdvancedRAG()

    def search(self, query):
        """
        Search products using a natural-language query.
        """

        results = self.rag.search(query)

        return results


def main():

    print("=" * 70)
    print("PRODUCT SEARCH TOOL")
    print("=" * 70)

    tool = ProductSearchTool()

    query = "I need an Apple laptop under 90000"

    print(f"\nUser Query:")
    print(query)

    print("\nSearching products...")

    results = tool.search(query)

    print("\nSearch Results:")
    print("-" * 70)

    if not results:
        print("No products found.")
        return

    for i, product in enumerate(results, start=1):

        print(f"\n{i}. {product['product_name']}")
        print(f"   Brand    : {product['brand']}")
        print(f"   Category : {product['category']}")
        print(f"   Price    : ₹{product['price']}")
        print(f"   Rating   : {product['rating']}")
        print(f"   Stock    : {product['stock']}")


if __name__ == "__main__":
    main()