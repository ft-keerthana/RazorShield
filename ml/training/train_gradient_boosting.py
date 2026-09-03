from pathlib import Path

import joblib
import pandas as pd

from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from ml.data.split import split_train_validation_test


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

    # Behavioral signals
    "customer_velocity_5m",
    "customer_velocity_1h",
    "customer_velocity_24h",
    "device_velocity_5m",
    "device_velocity_1h",
    "ip_velocity_5m",
    "ip_velocity_1h",
    "failed_attempts_1h",
    "customer_avg_amount",
    "customer_amount_deviation",

    # Location / entity signals
    "billing_shipping_mismatch",
    "country_changed",
    "minutes_since_previous_transaction",
    "device_customer_count",
    "ip_customer_count",
    "customer_device_count",
    "customer_ip_count",

    # Rule-engine signals
    "rule_risk_score",
    "rule_risk_flag",
    "rule_signal_count",
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
        column
        for column in FEATURE_COLUMNS
        if column not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing required feature columns: {missing_features}"
        )

    # Keep only explicitly approved model features + target
    model_df = df[FEATURE_COLUMNS + [target_column]].copy()

    # Create fixed train/validation/test split.
    #
    # 60% -> model training
    # 20% -> threshold selection
    # 20% -> final evaluation
    train_df, validation_df, test_df = (
        split_train_validation_test(
            df=model_df,
            target_column=target_column,
            random_state=42,
        )
    )

    # Prepare training data.
    # Validation and test sets remain completely untouched.
    X_train = train_df.drop(columns=[target_column])
    y_train = train_df[target_column]

    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(validation_df)}")
    print(f"Test samples: {len(test_df)}")
    print(f"Features used: {FEATURE_COLUMNS}")

    # Identify feature types
    numeric_features = X_train.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_features = X_train.select_dtypes(
        include=["object", "string", "category", "bool"]
    ).columns.tolist()

    # Numeric preprocessing
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
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
                    handle_unknown="ignore",
                    sparse_output=False,
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
        sparse_threshold=0,
    )

    # CPU-friendly gradient boosting model
    base_model = HistGradientBoostingClassifier(
        learning_rate=0.08,
        max_iter=75,
        max_leaf_nodes=15,
        min_samples_leaf=20,
        random_state=42,
    )

    # Calibrate predicted probabilities
    calibrated_model = CalibratedClassifierCV(
        estimator=base_model,
        method="sigmoid",
        cv=2,
    )

    # Complete pipeline
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", calibrated_model),
        ]
    )

    # Train only on the training partition.
    model.fit(X_train, y_train)

    # Save trained model
    model_path = (
        model_dir / "calibrated_gradient_boosting.joblib"
    )

    joblib.dump(model, model_path)

    print(
        "Calibrated gradient boosting training complete."
    )
    print(f"Model saved to: {model_path}")


if __name__ == "__main__":
    main()