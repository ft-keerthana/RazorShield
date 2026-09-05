from pathlib import Path

import joblib
import pandas as pd

from ml.evaluation.metrics import (
    calculate_classification_metrics,
    get_confusion_matrix,
)


MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "ml"
    / "models"
    / "calibrated_behavior_aware_fraud_model.joblib"
)

DATA_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "processed"
    / "transactions_processed.csv"
)

THRESHOLD = 0.050956

MODEL_FEATURES = [
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


def get_evaluation_metrics():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Calibrated behavior-aware fraud model is not available."
        )

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Processed transaction dataset is not available."
        )

    data = pd.read_csv(DATA_PATH)

    # Use the same chronological split used by the evaluation pipeline.
    data = data.sort_values("timestamp").reset_index(drop=True)

    test_start = int(len(data) * 0.80)
    test_data = data.iloc[test_start:].copy()

    missing_columns = [
        column
        for column in MODEL_FEATURES + ["is_fraud"]
        if column not in test_data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing evaluation columns: {missing_columns}"
        )

    model = joblib.load(MODEL_PATH)

    X_test = test_data[MODEL_FEATURES]
    y_test = test_data["is_fraud"]

    probabilities = model.predict_proba(X_test)[:, 1]

    predictions = (
        probabilities >= THRESHOLD
    ).astype(int)

    classification_metrics = calculate_classification_metrics(
        y_true=y_test,
        y_pred=predictions,
        y_score=probabilities,
    )

    confusion = get_confusion_matrix(
        y_true=y_test,
        y_pred=predictions,
    )

    return {
        "model": "calibrated_behavior_aware_fraud_model",
        "threshold": THRESHOLD,
        "evaluation_protocol": "chronological held-out test set",
        "test_samples": int(len(test_data)),
        "fraud_cases": int(y_test.sum()),
        "precision": round(classification_metrics["precision"], 4),
        "recall": round(classification_metrics["recall"], 4),
        "f1": round(classification_metrics["f1_score"], 4),
        "average_precision": round(
            classification_metrics["average_precision"],
            4,
        ),
        "roc_auc": round(
            classification_metrics["roc_auc"],
            4,
        ),
        **confusion,
    }
