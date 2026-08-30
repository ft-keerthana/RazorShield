from __future__ import annotations

import pandas as pd


def generate_transaction_features(
    df: pd.DataFrame,
    timestamp_column: str = "timestamp",
    amount_column: str = "amount",
) -> pd.DataFrame:
    """
    Generate baseline transaction-level features.

    Features are only created when the required source columns exist.
    """

    data = df.copy()

    # Convert timestamp to datetime if available
    if timestamp_column in data.columns:
        data[timestamp_column] = pd.to_datetime(
            data[timestamp_column],
            errors="coerce",
        )

        data["transaction_hour"] = data[timestamp_column].dt.hour
        data["transaction_day_of_week"] = (
            data[timestamp_column].dt.dayofweek
        )
        data["is_weekend"] = (
            data["transaction_day_of_week"] >= 5
        ).astype(int)

    # Amount-based features
    if amount_column in data.columns:
        data["amount_log"] = data[amount_column].apply(
            lambda value: __import__("math").log1p(value)
            if value >= 0
            else 0
        )

    return data