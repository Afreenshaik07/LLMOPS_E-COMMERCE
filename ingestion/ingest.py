import pandas as pd

from configs.config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH
)


def load_data():
    """Load the raw product dataset."""

    print("Loading product data...")

    df = pd.read_csv(RAW_DATA_PATH)

    print(f"Loaded {len(df)} products.")

    return df


def inspect_data(df):
    """Display basic information about the dataset."""

    print("\nDataset shape:")
    print(df.shape)

    print("\nColumns:")
    print(list(df.columns))

    print("\nMissing values:")
    print(df.isnull().sum())


def clean_data(df):
    """Clean and validate product data."""

    print("\nCleaning data...")

    # Remove duplicate products
    df = df.drop_duplicates(subset=["product_id"])

    # Remove rows missing important information
    required_columns = [
        "product_id",
        "product_name",
        "category",
        "description",
        "price"
    ]

    df = df.dropna(subset=required_columns)

    # Make sure price is numeric
    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    # Make sure rating is numeric
    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

    # Remove invalid prices
    df = df[df["price"] > 0]

    # Keep valid ratings
    df = df[
        (df["rating"] >= 0) &
        (df["rating"] <= 5)
    ]

    return df


def save_data(df):
    """Save cleaned data."""

    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )

    print(
        f"\nSaved {len(df)} cleaned products to:"
        f"\n{PROCESSED_DATA_PATH}"
    )


def main():

    print("=" * 50)
    print("E-COMMERCE DATA INGESTION PIPELINE")
    print("=" * 50)

    df = load_data()

    inspect_data(df)

    df = clean_data(df)

    save_data(df)

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()