import pandas as pd
import numpy as np
import torch

from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)

from app.query_parser import parse_query


EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

RERANKER_MODEL = (
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)

PRODUCT_PATH = (
    "data/processed/products_clean.csv"
)

EMBEDDING_PATH = (
    "data/processed/product_embeddings.npy"
)


class AdvancedRAG:

    def __init__(self):

        print("Loading embedding model...")

        self.embedding_model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        print("Loading reranker...")

        self.reranker = CrossEncoder(
            RERANKER_MODEL,
            activation_fn=torch.nn.Sigmoid()
        )

        self.products = pd.read_csv(
            PRODUCT_PATH
        )

        self.embeddings = np.load(
            EMBEDDING_PATH
        )

        print("\nAdvanced RAG components loaded.")

    def filter_products(
        self,
        brand=None,
        category=None,
        max_price=None,
        min_price=None
    ):

        df = self.products.copy()

        if brand:

            df = df[
                df["brand"].str.lower()
                == brand.lower()
            ]

        if category:

            df = df[
                df["category"].str.lower()
                == category.lower()
            ]

        if max_price is not None:

            df = df[
                df["price"] <= max_price
            ]

        if min_price is not None:

            df = df[
                df["price"] >= min_price
            ]

        return df

    def retrieve(
        self,
        query,
        candidates,
        top_k=5
    ):

        if candidates.empty:
            return []

        candidate_indices = candidates.index.tolist()

        query_embedding = (
            self.embedding_model.encode(query)
        )

        query_embedding = (
            query_embedding
            / np.linalg.norm(query_embedding)
        )

        candidate_embeddings = (
            self.embeddings[candidate_indices]
        )

        candidate_embeddings = (
            candidate_embeddings
            / np.linalg.norm(
                candidate_embeddings,
                axis=1,
                keepdims=True
            )
        )

        scores = np.dot(
            candidate_embeddings,
            query_embedding
        )

        order = np.argsort(scores)[::-1]

        order = order[:top_k]

        results = []

        for position in order:

            original_index = (
                candidate_indices[position]
            )

            product = self.products.loc[
                original_index
            ]

            results.append({
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "category": product["category"],
                "brand": product["brand"],
                "description": product["description"],
                "price": product["price"],
                "rating": product["rating"],
                "stock": product["stock"],
                "retrieval_score": float(
                    scores[position]
                )
            })

        return results

    def rerank(self, query, products):

        if not products:
            return []

        pairs = []

        for product in products:

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
            products,
            scores
        ):

            item = product.copy()

            item["rerank_score"] = float(
                score
            )

            results.append(item)

        results.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return results

    def search(self, query):

        # -----------------------------
        # STEP 1: Query Understanding
        # -----------------------------

        parsed_query = parse_query(query)

        print("\nQuery Understanding:")
        print("-" * 60)

        for key, value in parsed_query.items():

            print(
                f"{key:12}: {value}"
            )

        # -----------------------------
        # STEP 2: Metadata Filtering
        # -----------------------------

        print("\n1. Applying metadata filters...")

        filtered = self.filter_products(
            brand=parsed_query["brand"],
            category=parsed_query["category"],
            max_price=parsed_query["max_price"],
            min_price=parsed_query["min_price"]
        )

        print(
            f"   Candidates after filtering: "
            f"{len(filtered)}"
        )

        # -----------------------------
        # STEP 3: Semantic Retrieval
        # -----------------------------

        print("\n2. Running semantic retrieval...")

        candidates = self.retrieve(
            query,
            filtered,
            top_k=5
        )

        print(
            f"   Retrieved candidates: "
            f"{len(candidates)}"
        )

        # -----------------------------
        # STEP 4: Reranking
        # -----------------------------

        print("\n3. Running reranking...")

        results = self.rerank(
            query,
            candidates
        )

        return results[:3]


def main():

    print("=" * 60)
    print("AUTOMATIC ADVANCED RAG")
    print("=" * 60)

    rag = AdvancedRAG()

    query = input(
        "\nEnter your product query: "
    )

    results = rag.search(query)

    print("\nFinal Results:")
    print("-" * 60)

    if not results:

        print("No matching products found.")

        return

    for i, product in enumerate(
        results,
        start=1
    ):

        print(
            f"\n{i}. {product['product_name']}"
        )

        print(
            f"   Brand    : "
            f"{product['brand']}"
        )

        print(
            f"   Category : "
            f"{product['category']}"
        )

        print(
            f"   Price    : "
            f"₹{product['price']}"
        )

        print(
            f"   Rating   : "
            f"{product['rating']}"
        )

        print(
            f"   Retrieval: "
            f"{product['retrieval_score']:.4f}"
        )

        print(
            f"   Rerank   : "
            f"{product['rerank_score']:.4f}"
        )


if __name__ == "__main__":
    main()