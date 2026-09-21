import pandas as pd


PRODUCT_PATH = "data/processed/products_clean.csv"


class ProductFilter:
    """Filter products using structured metadata."""

    def __init__(self):

        self.products = pd.read_csv(
            PRODUCT_PATH
        )

    def filter(
        self,
        brand=None,
        category=None,
        max_price=None,
        min_price=None,
        min_rating=None,
        in_stock=None
    ):
        """Apply structured product filters."""

        df = self.products.copy()

        # Brand filter
        if brand:

            df = df[
                df["brand"].str.lower()
                == brand.lower()
            ]

        # Category filter
        if category:

            df = df[
                df["category"].str.lower()
                == category.lower()
            ]

        # Maximum price
        if max_price is not None:

            df = df[
                df["price"] <= max_price
            ]

        # Minimum price
        if min_price is not None:

            df = df[
                df["price"] >= min_price
            ]

        # Minimum rating
        if min_rating is not None:

            df = df[
                df["rating"] >= min_rating
            ]

        # Stock filter
        if in_stock:

            df = df[
                df["stock"] > 0
            ]

        return df


def main():

    print("=" * 60)
    print("PRODUCT METADATA FILTER")
    print("=" * 60)

    product_filter = ProductFilter()

    results = product_filter.filter(
        brand="Apple",
        category="Laptop",
        max_price=90000
    )

    print("\nFiltered Products:")
    print("-" * 60)

    if results.empty:

        print("No products found.")

    else:

        for _, product in results.iterrows():

            print(
                f"\n{product['product_name']}"
            )

            print(
                f"Brand    : {product['brand']}"
            )

            print(
                f"Category : {product['category']}"
            )

            print(
                f"Price    : ₹{product['price']}"
            )

            print(
                f"Rating   : {product['rating']}"
            )

            print(
                f"Stock    : {product['stock']}"
            )


if __name__ == "__main__":
    main()