from __future__ import annotations

from pathlib import Path

import pandas as pd

from ml.data.features import generate_transaction_features
from ml.data.preprocessing import (
    clean_transactions,
    handle_missing_values,
)
from ml.data.split import split_train_test


def main():
    project_root = Path(__file__).resolve().parents[2]

    raw_path = project_root / "data" / "raw" / "transactions.csv"
    processed_dir = project_root / "data" / "processed"

    processed_dir.mkdir(parents=True, exist_ok=True)

    # Load
    df = pd.read_csv(raw_path)

    print(f"Raw dataset shape: {df.shape}")

    # Clean
    df = clean_transactions(df)

    # Handle missing values
    df = handle_missing_values(df)

    # Generate features
    df = generate_transaction_features(df)

    # Save processed dataset
    processed_path = processed_dir / "transactions_processed.csv"
    df.to_csv(processed_path, index=False)

    print(f"Processed dataset shape: {df.shape}")
    print(f"Saved processed data to: {processed_path}")

    # Split only if target exists
    target_column = "is_fraud"

    if target_column in df.columns:
        X_train, X_test, y_train, y_test = split_train_test(
            df=df,
            target_column=target_column,
        )

        print(f"Training samples: {len(X_train)}")
        print(f"Test samples: {len(X_test)}")


if __name__ == "__main__":
    print("Starting RazorShield dataset pipeline...")
    main()