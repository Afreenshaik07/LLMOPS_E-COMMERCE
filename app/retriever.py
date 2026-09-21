import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer, util


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

PRODUCT_PATH = "data/processed/products_clean.csv"

EMBEDDING_PATH = "data/processed/product_embeddings.npy"


class ProductRetriever:
    """Semantic product retriever."""

    def __init__(self):

        print("Loading product retriever...")

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        self.products = pd.read_csv(
            PRODUCT_PATH
        )

        self.embeddings = self.model.encode(
            self.products.apply(
                lambda row:
                (
                    f"Product: {row['product_name']}. "
                    f"Category: {row['category']}. "
                    f"Brand: {row['brand']}. "
                    f"Description: {row['description']}"
                ),
                axis=1
            ).tolist(),
            convert_to_tensor=True
        )

        print(
            f"Loaded {len(self.products)} products."
        )

        print(
            f"Product embeddings: "
            f"{self.embeddings.shape}"
        )

    def search(self, query, top_k=3):
        """Retrieve relevant products."""

        query_embedding = self.model.encode(
            query,
            convert_to_tensor=True
        )

        scores = util.cos_sim(
            query_embedding,
            self.embeddings
        )[0]

        top_results = scores.argsort(
            descending=True
        )[:top_k]

        results = []

        for idx in top_results:

            idx = idx.item()

            product = self.products.iloc[idx]

            results.append({
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "category": product["category"],
                "brand": product["brand"],
                "description": product["description"],
                "price": product["price"],
                "rating": product["rating"],
                "stock": product["stock"],
                "similarity": float(scores[idx])
            })

        return results


def main():

    print("=" * 60)
    print("PRODUCT RETRIEVER TEST")
    print("=" * 60)

    retriever = ProductRetriever()

    query = input(
        "\nEnter your product query: "
    )

    results = retriever.search(
        query,
        top_k=3
    )

    print("\nRetrieved Products:")
    print("-" * 60)

    for i, product in enumerate(
        results,
        start=1
    ):

        print(
            f"\n{i}. {product['product_name']}"
        )

        print(
            f"   Brand      : {product['brand']}"
        )

        print(
            f"   Category   : {product['category']}"
        )

        print(
            f"   Price      : ₹{product['price']}"
        )

        print(
            f"   Rating     : {product['rating']}"
        )

        print(
            f"   Similarity : "
            f"{product['similarity']:.4f}"
        )


if __name__ == "__main__":
    main()