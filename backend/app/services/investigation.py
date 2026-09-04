from dataclasses import dataclass

import pandas as pd


@dataclass
class TransactionInvestigation:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: float
    currency: str
    status: str
    timestamp: str
    scenario: str
    is_fraud: bool
    rule_risk_score: float
    rule_risk_level: str
    risk_reasons: list[str]
    shared_device_flag: int
    shared_ip_flag: int
    customer_velocity_5m: float
    customer_velocity_1h: float
    device_velocity_5m: float
    ip_velocity_5m: float
    failed_attempts_1h: float


def get_transaction_investigation(
    transactions: pd.DataFrame,
    transaction_id: str,
) -> TransactionInvestigation:

    required_columns = {
        "transaction_id",
        "customer_id",
        "merchant_id",
        "amount",
        "currency",
        "status",
        "timestamp",
        "scenario",
        "is_fraud",
        "rule_risk_score",
        "rule_risk_level",
        "risk_reasons",
        "shared_device_flag",
        "shared_ip_flag",
        "customer_velocity_5m",
        "customer_velocity_1h",
        "device_velocity_5m",
        "ip_velocity_5m",
        "failed_attempts_1h",
    }

    missing_columns = required_columns - set(transactions.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    matches = transactions[
        transactions["transaction_id"] == transaction_id
    ]

    if matches.empty:
        raise KeyError(
            f"Transaction '{transaction_id}' was not found."
        )

    transaction = matches.iloc[0]

    risk_reasons = transaction["risk_reasons"]

    if pd.isna(risk_reasons) or risk_reasons == "[]":
        risk_reasons = []
    elif isinstance(risk_reasons, str):
        risk_reasons = risk_reasons.strip("[]").split(", ")
        risk_reasons = [
            reason.strip("'\"")
            for reason in risk_reasons
            if reason.strip("'\"")
        ]
    else:
        risk_reasons = list(risk_reasons)

    return TransactionInvestigation(
        transaction_id=str(transaction["transaction_id"]),
        customer_id=str(transaction["customer_id"]),
        merchant_id=str(transaction["merchant_id"]),
        amount=round(float(transaction["amount"]), 2),
        currency=str(transaction["currency"]),
        status=str(transaction["status"]),
        timestamp=str(transaction["timestamp"]),
        scenario=str(transaction["scenario"]),
        is_fraud=bool(transaction["is_fraud"]),
        rule_risk_score=round(float(transaction["rule_risk_score"]), 6),
        rule_risk_level=str(transaction["rule_risk_level"]),
        risk_reasons=risk_reasons,
        shared_device_flag=int(transaction["shared_device_flag"]),
        shared_ip_flag=int(transaction["shared_ip_flag"]),
        customer_velocity_5m=float(
            transaction["customer_velocity_5m"]
        ),
        customer_velocity_1h=float(
            transaction["customer_velocity_1h"]
        ),
        device_velocity_5m=float(
            transaction["device_velocity_5m"]
        ),
        ip_velocity_5m=float(
            transaction["ip_velocity_5m"]
        ),
        failed_attempts_1h=float(
            transaction["failed_attempts_1h"]
        ),
    )