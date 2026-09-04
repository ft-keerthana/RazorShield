from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.app.policy.engine import make_decision
from backend.app.policy.cost_optimizer import optimize_decision
from backend.app.network.fraud_spike import detect_fraud_spike
from backend.app.services.dashboard import build_dashboard_summary
from backend.app.services.investigation import (
    get_transaction_investigation,
)

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


@app.get("/network/fraud-spike", tags=["Network Intelligence"])
def fraud_spike_status():
    dataset_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "transactions_processed.csv"
    )

    if not dataset_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Processed transaction dataset is not available.",
        )

    transactions = pd.read_csv(dataset_path)

    result = detect_fraud_spike(transactions)

    return {
        "fraud_spike": result.fraud_spike,
        "recent_fraud_rate": result.recent_fraud_rate,
        "baseline_fraud_rate": result.baseline_fraud_rate,
        "spike_ratio": result.spike_ratio,
        "severity": result.severity,
    }


@app.get("/dashboard/summary", tags=["Dashboard"])
def dashboard_summary():
    dataset_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "transactions_processed.csv"
    )

    if not dataset_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Processed transaction dataset is not available.",
        )

    transactions = pd.read_csv(dataset_path)

    summary = build_dashboard_summary(transactions)

    return {
        "total_transactions": summary.total_transactions,
        "fraud_transactions": summary.fraud_transactions,
        "legitimate_transactions": summary.legitimate_transactions,
        "fraud_rate": summary.fraud_rate,
        "total_amount": summary.total_amount,
        "average_transaction_amount": (
            summary.average_transaction_amount
        ),
        "network_risk_score": summary.network_risk_score,
        "fraud_spike": summary.fraud_spike,
        "abuse_ring_detected": summary.abuse_ring_detected,
    }
@app.get(
    "/transactions/{transaction_id}",
    tags=["Transactions"],
)
def transaction_investigation(transaction_id: str):
    dataset_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "transactions_processed.csv"
    )

    if not dataset_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Processed transaction dataset is not available.",
        )

    transactions = pd.read_csv(dataset_path)

    try:
        investigation = get_transaction_investigation(
            transactions,
            transaction_id,
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return {
        "transaction_id": investigation.transaction_id,
        "customer_id": investigation.customer_id,
        "merchant_id": investigation.merchant_id,
        "amount": investigation.amount,
        "currency": investigation.currency,
        "status": investigation.status,
        "timestamp": investigation.timestamp,
        "scenario": investigation.scenario,
        "is_fraud": investigation.is_fraud,
        "rule_risk_score": investigation.rule_risk_score,
        "rule_risk_level": investigation.rule_risk_level,
        "risk_reasons": investigation.risk_reasons,
        "shared_device_flag": investigation.shared_device_flag,
        "shared_ip_flag": investigation.shared_ip_flag,
        "customer_velocity_5m": investigation.customer_velocity_5m,
        "customer_velocity_1h": investigation.customer_velocity_1h,
        "device_velocity_5m": investigation.device_velocity_5m,
        "ip_velocity_5m": investigation.ip_velocity_5m,
        "failed_attempts_1h": investigation.failed_attempts_1h,
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

    # Existing ML + rule-based policy decision
    decision = make_decision(
        fraud_probability=fraud_probability,
        rule_risk_score=transaction.rule_risk_score,
        rule_risk_flag=transaction.rule_risk_flag,
        rule_signal_count=transaction.rule_signal_count,
    )

    # Business-aware cost optimization
    business_decision = optimize_decision(
        fraud_probability=fraud_probability,
        transaction_amount=transaction.amount,
    )

    return {
        "transaction_id": transaction_id,
        "fraud_probability": round(fraud_probability, 6),

        # Existing risk policy
        "risk_score": decision.risk_score,
        "decision": decision.decision,
        "reasons": decision.reasons,

        # Business-aware recommendation
        "business_decision": business_decision.decision,
        "expected_cost": business_decision.expected_cost,
        "allow_cost": business_decision.allow_cost,
        "review_cost": business_decision.review_cost,
        "hold_cost": business_decision.hold_cost,

        "threshold": 0.050956,
        "model": "calibrated_behavior_aware_fraud_model",
    }