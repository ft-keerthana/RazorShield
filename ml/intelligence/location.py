from __future__ import annotations

import pandas as pd


def add_location_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate location-related transaction risk signals.

    The dataset contains country-level information, so these signals
    are intentionally coarse rather than pretending to provide
    precise geolocation.
    """

    data = df.copy()

    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        errors="coerce",
    )

    data = data.sort_values("timestamp").reset_index(drop=True)

    data["billing_shipping_mismatch"] = (
        data["billing_country"] != data["shipping_country"]
    ).astype(int)

    data["previous_country"] = (
        data.groupby("customer_id")["billing_country"]
        .shift(1)
    )

    data["country_changed"] = (
        data["previous_country"].notna()
        & (
            data["billing_country"]
            != data["previous_country"]
        )
    ).astype(int)

    data["previous_transaction_time"] = (
        data.groupby("customer_id")["timestamp"]
        .shift(1)
    )

    data["minutes_since_previous_transaction"] = (
        (
            data["timestamp"]
            - data["previous_transaction_time"]
        )
        .dt.total_seconds()
        .div(60)
    )

    data["minutes_since_previous_transaction"] = (
        data["minutes_since_previous_transaction"]
        .fillna(-1)
    )

    # Country-level data cannot provide precise travel distance.
    # This is deliberately a conservative coarse anomaly signal.


    return data