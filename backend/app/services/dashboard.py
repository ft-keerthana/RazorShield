from dataclasses import dataclass

import pandas as pd

from app.network.risk_service import analyze_network_risk


@dataclass
class DashboardSummary:
    total_transactions: int
    fraud_transactions: int
    legitimate_transactions: int
    fraud_rate: float
    total_amount: float
    average_transaction_amount: float
    network_risk_score: float
    fraud_spike: bool
    abuse_ring_detected: bool


def build_dashboard_summary(
    transactions: pd.DataFrame,
) -> DashboardSummary:
    if transactions.empty:
        raise ValueError("Transaction dataset is empty.")

    required_columns = {
        "amount",
        "is_fraud",
    }

    missing_columns = required_columns - set(transactions.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    total_transactions = len(transactions)

    fraud_transactions = int(
        transactions["is_fraud"].sum()
    )

    legitimate_transactions = (
        total_transactions - fraud_transactions
    )

    fraud_rate = (
        fraud_transactions / total_transactions
    )

    total_amount = float(
        transactions["amount"].sum()
    )

    average_transaction_amount = float(
        transactions["amount"].mean()
    )

    network = analyze_network_risk(transactions)

    return DashboardSummary(
        total_transactions=total_transactions,
        fraud_transactions=fraud_transactions,
        legitimate_transactions=legitimate_transactions,
        fraud_rate=round(fraud_rate, 6),
        total_amount=round(total_amount, 2),
        average_transaction_amount=round(
            average_transaction_amount,
            2,
        ),
        network_risk_score=network.network_risk_score,
        fraud_spike=network.fraud_spike,
        abuse_ring_detected=network.abuse_ring_detected,
    )