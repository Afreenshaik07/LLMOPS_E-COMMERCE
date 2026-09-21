import pandas as pd


class InventoryTool:
    """
    Tool for checking product inventory.
    """

    def __init__(self):
        self.data_path = "data/processed/products_clean.csv"
        self.products = pd.read_csv(self.data_path)

    def check_stock(self, product_name):
        """
        Check the stock of a specific product.
        """

        product_name = product_name.strip().lower()

        matches = self.products[
            self.products["product_name"]
            .str.lower()
            .str.contains(product_name, na=False)
        ]

        if matches.empty:
            return None

        product = matches.iloc[0]

        return {
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "stock": int(product["stock"])
        }


def main():

    print("=" * 70)
    print("INVENTORY TOOL")
    print("=" * 70)

    tool = InventoryTool()

    product_name = "MacBook Air M2"

    print("\nProduct requested:")
    print(product_name)

    inventory = tool.check_stock(product_name)

    print("\nInventory Information:")
    print("-" * 70)

    if inventory is None:
        print("Product not found.")
        return

    print(f"Product ID : {inventory['product_id']}")
    print(f"Product    : {inventory['product_name']}")
    print(f"Stock      : {inventory['stock']}")

    if inventory["stock"] > 0:
        print("Status     : In Stock")
    else:
        print("Status     : Out of Stock")


if __name__ == "__main__":
    main()