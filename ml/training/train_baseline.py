from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml.data.split import split_train_test


# Explicit baseline feature set.
# Raw identifiers and synthetic scenario labels are intentionally excluded.
FEATURE_COLUMNS = [
    "amount",
    "amount_log",
    "transaction_hour",
    "transaction_day_of_week",
    "is_weekend",
    "currency",
    "status",
    "billing_country",
    "shipping_country",
    "merchant_id",
]


def main():
    project_root = Path(__file__).resolve().parents[2]

    data_path = (
        project_root
        / "data"
        / "processed"
        / "transactions_processed.csv"
    )

    model_dir = project_root / "ml" / "models"
    model_dir.mkdir(parents=True, exist_ok=True)

    # Load processed data
    df = pd.read_csv(data_path)

    target_column = "is_fraud"

    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' was not found."
        )

    # Validate required features
    missing_features = [
        column for column in FEATURE_COLUMNS
        if column not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing required feature columns: {missing_features}"
        )

    # Keep only explicitly approved model features + target
    model_df = df[FEATURE_COLUMNS + [target_column]].copy()

    # Split
    X_train, X_test, y_train, y_test = split_train_test(
        df=model_df,
        target_column=target_column,
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Features used: {FEATURE_COLUMNS}")

    # Identify feature types
    numeric_features = X_train.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_features = X_train.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    # Numeric preprocessing
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    # Categorical preprocessing
    categorical_transformer = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
            ),
        ]
    )

    # Combine transformations
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_transformer,
                numeric_features,
            ),
            (
                "categorical",
                categorical_transformer,
                categorical_features,
            ),
        ],
        remainder="drop",
    )

    # Logistic regression baseline
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )

    # Train
    model.fit(X_train, y_train)

    # Save
    model_path = model_dir / "baseline_fraud_model.joblib"
    joblib.dump(model, model_path)

    print("Baseline model training complete.")
    print(f"Model saved to: {model_path}")


if __name__ == "__main__":
    main()