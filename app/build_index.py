import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

PRODUCT_PATH = "data/processed/products_clean.csv"

EMBEDDING_PATH = "data/processed/product_embeddings.npy"


def create_product_text(df):
    """Create searchable text for each product."""

    return (
        "Product: " + df["product_name"].astype(str)
        + ". Category: " + df["category"].astype(str)
        + ". Brand: " + df["brand"].astype(str)
        + ". Description: " + df["description"].astype(str)
    ).tolist()


def main():

    print("=" * 60)
    print("BUILDING PRODUCT VECTOR INDEX")
    print("=" * 60)

    # Load products
    df = pd.read_csv(PRODUCT_PATH)

    print(f"Loaded {len(df)} products.")

    # Create searchable text
    product_text = create_product_text(df)

    # Load embedding model
    print("\nLoading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Embedding model loaded.")

    # Generate embeddings
    print("\nCreating product embeddings...")

    embeddings = model.encode(
        product_text,
        show_progress_bar=True
    )

    # Convert to NumPy
    embeddings = np.asarray(embeddings)

    # Save embeddings
    np.save(
        EMBEDDING_PATH,
        embeddings
    )

    print("\nVector index saved successfully!")

    print(f"Embedding shape: {embeddings.shape}")

    print(f"Saved to: {EMBEDDING_PATH}")


if __name__ == "__main__":
    main()