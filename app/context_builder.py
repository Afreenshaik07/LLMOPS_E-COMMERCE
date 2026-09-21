def build_context(products):
    """Convert retrieved products into clean LLM context."""

    if not products:
        return "No relevant products were found."

    context_parts = []

    for i, product in enumerate(
        products,
        start=1
    ):

        product_context = f"""
Product {i}:

Product ID: {product['product_id']}
Name: {product['product_name']}
Brand: {product['brand']}
Category: {product['category']}
Description: {product['description']}
Price: ₹{product['price']}
Rating: {product['rating']}
Stock: {product['stock']}
"""

        context_parts.append(
            product_context.strip()
        )

    return "\n\n".join(
        context_parts
    )


def main():

    print("=" * 60)
    print("RAG CONTEXT BUILDER TEST")
    print("=" * 60)

    sample_products = [
        {
            "product_id": "P005",
            "product_name": "MacBook Air M2",
            "brand": "Apple",
            "category": "Laptop",
            "description": (
                "Lightweight laptop with "
                "Apple M2 chip, 8GB RAM "
                "and 256GB SSD"
            ),
            "price": 84999,
            "rating": 4.7,
            "stock": 8
        }
    ]

    context = build_context(
        sample_products
    )

    print("\nGenerated Context:")
    print("-" * 60)
    print(context)


if __name__ == "__main__":
    main()