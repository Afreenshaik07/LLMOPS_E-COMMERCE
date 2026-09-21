import re


SUPPORTED_BRANDS = [
    "Apple",
    "Samsung",
    "Sony",
    "Lenovo",
    "ASUS",
    "Dell",
    "Logitech",
    "Xiaomi",
    "Anker"
]


SUPPORTED_CATEGORIES = [
    "Laptop",
    "Headphones",
    "Mouse",
    "Keyboard",
    "Tablet",
    "Power Bank"
]


def extract_brand(query):
    """Extract brand from query."""

    query_lower = query.lower()

    for brand in SUPPORTED_BRANDS:

        if brand.lower() in query_lower:

            return brand

    return None


def extract_category(query):
    """Extract product category."""

    query_lower = query.lower()

    for category in SUPPORTED_CATEGORIES:

        if category.lower() in query_lower:

            return category

    return None


def extract_max_price(query):
    """Extract maximum price."""

    query_lower = query.lower()

    patterns = [
        r"under\s*₹?\s*([\d,]+)",
        r"below\s*₹?\s*([\d,]+)",
        r"less than\s*₹?\s*([\d,]+)",
        r"upto\s*₹?\s*([\d,]+)",
        r"up to\s*₹?\s*([\d,]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            query_lower
        )

        if match:

            price = match.group(1)

            price = price.replace(
                ",",
                ""
            )

            return float(price)

    return None


def extract_min_price(query):
    """Extract minimum price."""

    query_lower = query.lower()

    patterns = [
        r"above\s*₹?\s*([\d,]+)",
        r"over\s*₹?\s*([\d,]+)",
        r"more than\s*₹?\s*([\d,]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            query_lower
        )

        if match:

            price = match.group(1)

            price = price.replace(
                ",",
                ""
            )

            return float(price)

    return None


def parse_query(query):
    """Convert natural language into structured filters."""

    return {
        "brand": extract_brand(query),
        "category": extract_category(query),
        "max_price": extract_max_price(query),
        "min_price": extract_min_price(query)
    }


def main():

    print("=" * 60)
    print("QUERY UNDERSTANDING")
    print("=" * 60)

    query = input(
        "\nEnter your product query: "
    )

    filters = parse_query(query)

    print("\nExtracted Query Information:")
    print("-" * 60)

    for key, value in filters.items():

        print(
            f"{key:12}: {value}"
        )


if __name__ == "__main__":
    main()