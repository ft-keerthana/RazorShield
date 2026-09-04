import joblib
import pandas as pd

from ml.evaluation.feedback import evaluate_predictions


MODEL_PATH = "ml/models/calibrated_behavior_aware_fraud_model.joblib"
DATA_PATH = "data/processed/transactions_processed.csv"

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


def main():
    data = pd.read_csv(DATA_PATH)

    # Reproduce the same chronological 60/20/20 split
    # used during model evaluation.
    data = data.sort_values("timestamp").reset_index(drop=True)

    test_start = int(len(data) * 0.80)
    test_data = data.iloc[test_start:].copy()

    model = joblib.load(MODEL_PATH)

    X_test = test_data[MODEL_FEATURES]
    y_test = test_data["is_fraud"]

    probabilities = model.predict_proba(X_test)[:, 1]

    result = evaluate_predictions(
        y_true=y_test,
        probabilities=probabilities,
        threshold=THRESHOLD,
    )

    print("RazorShield held-out evaluation")
    print("--------------------------------")
    print(f"Threshold: {result.threshold}")
    print(f"Test samples: {result.test_samples}")
    print(f"Confirmed fraud: {result.fraud_cases}")
    print(f"Precision: {result.precision}")
    print(f"Recall: {result.recall}")
    print(f"F1: {result.f1}")
    print(f"ROC-AUC: {result.roc_auc}")
    print(f"PR-AUC: {result.pr_auc}")


if __name__ == "__main__":
    main()