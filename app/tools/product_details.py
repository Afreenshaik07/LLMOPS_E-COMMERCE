import pandas as pd


class ProductDetailsTool:
    """
    Tool for retrieving exact details
    about a specific product.
    """

    def __init__(self):
        self.data_path = "data/processed/products_clean.csv"
        self.products = pd.read_csv(self.data_path)

    def get_details(self, product_name):
        """
        Retrieve details for a product by name.
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


def main():

    print("=" * 70)
    print("PRODUCT DETAILS TOOL")
    print("=" * 70)

    tool = ProductDetailsTool()

    product_name = "MacBook Air M2"

    print(f"\nProduct requested:")
    print(product_name)

    product = tool.get_details(product_name)

    print("\nProduct Details:")
    print("-" * 70)

    if product is None:
        print("Product not found.")
        return

    print(f"Product ID : {product['product_id']}")
    print(f"Name       : {product['product_name']}")
    print(f"Brand      : {product['brand']}")
    print(f"Category   : {product['category']}")
    print(f"Description: {product['description']}")
    print(f"Price      : ₹{product['price']}")
    print(f"Rating     : {product['rating']}")
    print(f"Stock      : {product['stock']}")


if __name__ == "__main__":
    main()