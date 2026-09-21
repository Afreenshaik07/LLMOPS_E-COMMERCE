import pandas as pd
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_model():
    """Load the embedding model."""

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Embedding model loaded.")

    return model


def create_product_text(df):
    """Combine important product fields into searchable text."""

    product_text = (
        "Product: " + df["product_name"].astype(str)
        + ". Category: " + df["category"].astype(str)
        + ". Brand: " + df["brand"].astype(str)
        + ". Description: " + df["description"].astype(str)
    )

    return product_text.tolist()


def create_embeddings(model, product_text):
    """Convert product text into vector embeddings."""

    print("Creating embeddings...")

    embeddings = model.encode(
        product_text,
        show_progress_bar=True
    )

    print(f"Created embeddings with shape: {embeddings.shape}")

    return embeddings


def main():

    print("=" * 50)
    print("PRODUCT EMBEDDING PIPELINE")
    print("=" * 50)

    df = pd.read_csv(
        "data/processed/products_clean.csv"
    )

    print(f"Loaded {len(df)} products.")

    product_text = create_product_text(df)

    model = load_model()

    embeddings = create_embeddings(
        model,
        product_text
    )

    print("\nFirst product:")
    print(product_text[0])

    print("\nEmbedding dimensions:")
    print(embeddings.shape[1])

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()