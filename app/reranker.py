import pandas as pd
import numpy as np
import torch

from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"

PRODUCT_PATH = "data/processed/products_clean.csv"
EMBEDDING_PATH = "data/processed/product_embeddings.npy"


class AdvancedProductRetriever:

    def __init__(self):

        print("Loading embedding model...")

        self.embedding_model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        print("Loading reranker model...")

        self.reranker = CrossEncoder(
            RERANKER_MODEL,
            activation_fn=torch.nn.Sigmoid()
        )

        self.products = pd.read_csv(
            PRODUCT_PATH
        )

        self.product_embeddings = np.load(
            EMBEDDING_PATH
        )

        print("Models loaded successfully.")

        print(
            f"Products: {len(self.products)}"
        )

        print(
            f"Embeddings: "
            f"{self.product_embeddings.shape}"
        )

    def create_product_text(self, row):

        return (
            f"Product: {row['product_name']}. "
            f"Category: {row['category']}. "
            f"Brand: {row['brand']}. "
            f"Description: {row['description']}"
        )

    def retrieve(self, query, top_k=5):

        print("\nRunning semantic retrieval...")

        query_embedding = self.embedding_model.encode(
            query
        )

        # Normalize embeddings
        query_embedding = (
            query_embedding
            / np.linalg.norm(query_embedding)
        )

        product_embeddings = (
            self.product_embeddings
            / np.linalg.norm(
                self.product_embeddings,
                axis=1,
                keepdims=True
            )
        )

        # Cosine similarity
        scores = np.dot(
            product_embeddings,
            query_embedding
        )

        top_indices = np.argsort(
            scores
        )[::-1][:top_k]

        candidates = []

        for idx in top_indices:

            product = self.products.iloc[idx]

            candidates.append({
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "category": product["category"],
                "brand": product["brand"],
                "description": product["description"],
                "price": product["price"],
                "rating": product["rating"],
                "stock": product["stock"],
                "retrieval_score": float(
                    scores[idx]
                )
            })

        return candidates

    def rerank(self, query, candidates):

        print("Running Cross-Encoder reranking...")

        pairs = []

        for product in candidates:

            product_text = (
                f"Product: {product['product_name']}. "
                f"Category: {product['category']}. "
                f"Brand: {product['brand']}. "
                f"Description: {product['description']}"
            )

            pairs.append(
                [query, product_text]
            )

        scores = self.reranker.predict(
            pairs
        )

        results = []

        for product, score in zip(
            candidates,
            scores
        ):

            product = product.copy()

            product["rerank_score"] = float(
                score
            )

            results.append(product)

        results.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return results


def main():

    print("=" * 60)
    print("ADVANCED RAG RETRIEVAL + RERANKING")
    print("=" * 60)

    retriever = AdvancedProductRetriever()

    query = input(
        "\nEnter your product query: "
    )

    candidates = retriever.retrieve(
        query,
        top_k=5
    )

    print("\nInitial Retrieval:")
    print("-" * 60)

    for i, product in enumerate(
        candidates,
        start=1
    ):

        print(
            f"{i}. "
            f"{product['product_name']} "
            f"→ "
            f"{product['retrieval_score']:.4f}"
        )

    results = retriever.rerank(
        query,
        candidates
    )

    print("\nFinal Re-ranked Results:")
    print("-" * 60)

    for i, product in enumerate(
        results[:3],
        start=1
    ):

        print(
            f"\n{i}. "
            f"{product['product_name']}"
        )

        print(
            f"   Brand          : "
            f"{product['brand']}"
        )

        print(
            f"   Category       : "
            f"{product['category']}"
        )

        print(
            f"   Price          : "
            f"₹{product['price']}"
        )

        print(
            f"   Rating         : "
            f"{product['rating']}"
        )

        print(
            f"   Retrieval Score: "
            f"{product['retrieval_score']:.4f}"
        )

        print(
            f"   Rerank Score   : "
            f"{product['rerank_score']:.4f}"
        )


if __name__ == "__main__":
    main()