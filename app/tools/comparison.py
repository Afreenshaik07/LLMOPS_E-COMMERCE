import pandas as pd


class ProductComparisonTool:
    """
    Tool for comparing two e-commerce products.
    """

    def __init__(self):
        self.data_path = "data/processed/products_clean.csv"
        self.products = pd.read_csv(self.data_path)

    def get_product(self, product_name):
        """
        Find a product by name.
        """

        product_name = product_name.strip().lower()

        matches = self.products[
            self.products["product_name"]
            .str.lower()
            .str.contains(product_name, na=False)
        ]

        if matches.empty:
            return None

        return matches.iloc[0].to_dict()

    def compare(self, product1_name, product2_name):
        """
        Compare two products.
        """

        product1 = self.get_product(product1_name)
        product2 = self.get_product(product2_name)

        if product1 is None or product2 is None:
            return None

        return {
            "product1": product1,
            "product2": product2
        }


def main():

    print("=" * 70)
    print("PRODUCT COMPARISON TOOL")
    print("=" * 70)

    tool = ProductComparisonTool()

    product1_name = "MacBook Air M2"
    product2_name = "IdeaPad Slim 3"

    print("\nProducts:")
    print(f"1. {product1_name}")
    print(f"2. {product2_name}")

    result = tool.compare(
        product1_name,
        product2_name
    )

    if result is None:
        print("\nOne or both products were not found.")
        return

    product1 = result["product1"]
    product2 = result["product2"]

    print("\nComparison:")
    print("-" * 70)

    print(f"\n{'Feature':<20}{product1['product_name']:<25}{product2['product_name']}")

    print("-" * 70)

    print(
        f"{'Brand':<20}"
        f"{product1['brand']:<25}"
        f"{product2['brand']}"
    )

    print(
        f"{'Category':<20}"
        f"{product1['category']:<25}"
        f"{product2['category']}"
    )

    print(
        f"{'Price':<20}"
        f"₹{product1['price']:<24}"
        f"₹{product2['price']}"
    )

    print(
        f"{'Rating':<20}"
        f"{product1['rating']:<25}"
        f"{product2['rating']}"
    )

    print(
        f"{'Stock':<20}"
        f"{product1['stock']:<25}"
        f"{product2['stock']}"
    )


if __name__ == "__main__":
    main()