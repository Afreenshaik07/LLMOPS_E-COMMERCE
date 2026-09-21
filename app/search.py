import pandas as pd
from sentence_transformers import SentenceTransformer, util


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_products():
    """Load processed product data."""

    return pd.read_csv(
        "data/processed/products_clean.csv"
    )


def create_product_text(df):
    """Create searchable text for each product."""

    return (
        "Product: " + df["product_name"].astype(str)
        + ". Category: " + df["category"].astype(str)
        + ". Brand: " + df["brand"].astype(str)
        + ". Description: " + df["description"].astype(str)
    ).tolist()


def semantic_search(query, top_k=3):
    """Find products semantically similar to the query."""

    print("\nLoading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    df = load_products()

    product_text = create_product_text(df)

    print(f"Searching {len(product_text)} products...")

    # Create embeddings for products
    product_embeddings = model.encode(
        product_text,
        convert_to_tensor=True
    )

    # Create embedding for user query
    query_embedding = model.encode(
        query,
        convert_to_tensor=True
    )

    # Calculate cosine similarity
    similarity_scores = util.cos_sim(
        query_embedding,
        product_embeddings
    )[0]

    # Get top results
    top_results = similarity_scores.argsort(
        descending=True
    )[:top_k]

    results = []

    for idx in top_results:

        idx = idx.item()

        results.append({
            "product_id": df.iloc[idx]["product_id"],
            "product_name": df.iloc[idx]["product_name"],
            "category": df.iloc[idx]["category"],
            "brand": df.iloc[idx]["brand"],
            "price": df.iloc[idx]["price"],
            "rating": df.iloc[idx]["rating"],
            "similarity": float(similarity_scores[idx])
        })

    return results


def main():

    print("=" * 60)
    print("SEMANTIC PRODUCT SEARCH")
    print("=" * 60)

    query = input(
        "\nEnter your product query: "
    )

    results = semantic_search(query)

    print("\nTop Results:")
    print("-" * 60)

    for i, product in enumerate(results, start=1):

        print(f"\n{i}. {product['product_name']}")
        print(f"   Product ID : {product['product_id']}")
        print(f"   Category   : {product['category']}")
        print(f"   Brand      : {product['brand']}")
        print(f"   Price      : ₹{product['price']}")
        print(f"   Rating     : {product['rating']}")
        print(
            f"   Similarity : "
            f"{product['similarity']:.4f}"
        )


if __name__ == "__main__":
    main()