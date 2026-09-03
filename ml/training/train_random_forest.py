from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from ml.data.split import split_train_validation_test


RANDOM_STATE = 42

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
    "billing_shipping_mismatch",
    "country_changed",
    "minutes_since_previous_transaction",
    "device_customer_count",
    "ip_customer_count",
    "customer_device_count",
    "customer_ip_count",
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

    model_path = (
        project_root
        / "ml"
        / "models"
        / "random_forest_fraud_model.joblib"
    )

    df = pd.read_csv(data_path)

    target_column = "is_fraud"

    missing_columns = [
        column
        for column in FEATURE_COLUMNS + [target_column]
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    train_df, validation_df, test_df = split_train_validation_test(
        df=df,
        target_column=target_column,
        random_state=RANDOM_STATE,
    )

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df[target_column]

    X_validation = validation_df[FEATURE_COLUMNS]
    y_validation = validation_df[target_column]

    X_test = test_df[FEATURE_COLUMNS]
    y_test = test_df[target_column]

    print("Training Random Forest fraud model")
    print("----------------------------------------")
    print(f"Training samples:   {len(X_train)}")
    print(f"Validation samples: {len(X_validation)}")
    print(f"Test samples:       {len(X_test)}")
    print(f"Training frauds:    {y_train.sum()}")
    print(f"Validation frauds:  {y_validation.sum()}")
    print(f"Test frauds:        {y_test.sum()}")

    numeric_features = [
        column
        for column in FEATURE_COLUMNS
        if column not in [
            "currency",
            "status",
            "billing_country",
            "shipping_country",
            "merchant_id",
        ]
    ]

    categorical_features = [
        "currency",
        "status",
        "billing_country",
        "shipping_country",
        "merchant_id",
    ]

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median"),
            )
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                numeric_features,
            ),
            (
                "categorical",
                categorical_pipeline,
                categorical_features,
            ),
        ]
    )

    classifier = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=3,
        max_features="sqrt",
        class_weight="balanced_subsample",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    model = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "classifier",
                classifier,
            ),
        ]
    )

    model.fit(X_train, y_train)

    validation_probabilities = model.predict_proba(
        X_validation
    )[:, 1]

    test_probabilities = model.predict_proba(
        X_test
    )[:, 1]

    print("\nProbability ranges")
    print("----------------------------------------")
    print(
        f"Validation min: {validation_probabilities.min():.6f}"
    )
    print(
        f"Validation max: {validation_probabilities.max():.6f}"
    )
    print(
        f"Test min:       {test_probabilities.min():.6f}"
    )
    print(
        f"Test max:       {test_probabilities.max():.6f}"
    )

    model_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(model, model_path)

    print("\nModel saved")
    print("----------------------------------------")
    print(model_path)


if __name__ == "__main__":
    main()