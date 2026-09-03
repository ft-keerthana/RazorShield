from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="RazorShield API",
    description="AI-powered risk intelligence platform for modern payments",
    version="0.2.0",
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "calibrated_behavior_aware_fraud_model.joblib"
)


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


model = None

if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)


class TransactionScoreRequest(BaseModel):
    transaction_id: str

    amount: float
    amount_log: float

    transaction_hour: int
    transaction_day_of_week: int
    is_weekend: int

    currency: str
    status: str
    billing_country: str
    shipping_country: str
    merchant_id: str

    customer_velocity_5m: float
    customer_velocity_1h: float
    customer_velocity_24h: float

    device_velocity_5m: float
    device_velocity_1h: float

    ip_velocity_5m: float
    ip_velocity_1h: float

    failed_attempts_1h: float

    customer_avg_amount: float
    customer_amount_deviation: float

    billing_shipping_mismatch: int
    country_changed: int

    minutes_since_previous_transaction: float

    device_customer_count: float
    ip_customer_count: float
    customer_device_count: float
    customer_ip_count: float

    rule_risk_score: float
    rule_risk_flag: int
    rule_signal_count: int


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


@app.get("/model/status", tags=["Model"])
def model_status():
    return {
        "model_loaded": model is not None,
        "model_path": str(MODEL_PATH),
        "model_name": "calibrated_behavior_aware_fraud_model",
    }


@app.post("/transactions/score", tags=["Transactions"])
def score_transaction(transaction: TransactionScoreRequest):
    if model is None:
        return {
            "error": "Fraud model is not available."
        }

    transaction_data = transaction.model_dump()

    transaction_id = transaction_data.pop("transaction_id")

    features = pd.DataFrame(
        [
            {
                feature: transaction_data[feature]
                for feature in MODEL_FEATURES
            }
        ]
    )

    fraud_probability = float(
        model.predict_proba(features)[0][1]
    )

    return {
        "transaction_id": transaction_id,
        "fraud_probability": round(fraud_probability, 6),
        "fraud_prediction": int(fraud_probability >= 0.050956),
        "threshold": 0.050956,
        "model": "calibrated_behavior_aware_fraud_model",
    }