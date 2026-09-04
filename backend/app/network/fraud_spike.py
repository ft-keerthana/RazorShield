from dataclasses import dataclass

import pandas as pd


@dataclass
class FraudSpikeResult:
    fraud_spike: bool
    recent_fraud_rate: float
    baseline_fraud_rate: float
    spike_ratio: float
    severity: str


def detect_fraud_spike(
    transactions: pd.DataFrame,
    recent_window: int = 100,
    baseline_window: int = 1000,
) -> FraudSpikeResult:
    """
    Detect an unusual increase in fraud rate using the most recent
    transactions compared with an earlier baseline window.
    """

    required_columns = {"timestamp", "is_fraud"}

    missing_columns = required_columns - set(transactions.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if len(transactions) < recent_window + baseline_window:
        raise ValueError(
            "Not enough transactions to calculate a fraud spike."
        )

    data = transactions.copy()

    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    data["is_fraud"] = pd.to_numeric(
        data["is_fraud"], errors="coerce"
    ).fillna(0)

    data = data.dropna(subset=["timestamp"])
    data = data.sort_values("timestamp")

    recent = data.tail(recent_window)
    baseline = data.iloc[-(recent_window + baseline_window):-recent_window]

    recent_fraud_rate = float(recent["is_fraud"].mean())
    baseline_fraud_rate = float(baseline["is_fraud"].mean())

    if baseline_fraud_rate == 0:
        spike_ratio = float("inf") if recent_fraud_rate > 0 else 1.0
    else:
        spike_ratio = recent_fraud_rate / baseline_fraud_rate

    fraud_spike = (
        recent_fraud_rate >= 0.05
        and spike_ratio >= 2.0
    )

    if not fraud_spike:
        severity = "none"
    elif spike_ratio >= 4.0:
        severity = "high"
    else:
        severity = "medium"

    return FraudSpikeResult(
        fraud_spike=fraud_spike,
        recent_fraud_rate=round(recent_fraud_rate, 6),
        baseline_fraud_rate=round(baseline_fraud_rate, 6),
        spike_ratio=round(spike_ratio, 6),
        severity=severity,
    )