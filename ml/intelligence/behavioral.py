from __future__ import annotations

import pandas as pd


def add_behavioral_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate historical behavioral features.

    Features are calculated using transactions that occurred before
    the current transaction to avoid temporal leakage.
    """

    data = df.copy()

    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        errors="coerce",
    )

    data = data.sort_values("timestamp").reset_index(drop=True)

    # Previous activity timestamps for each entity.
    data["customer_velocity_5m"] = 0
    data["customer_velocity_1h"] = 0
    data["customer_velocity_24h"] = 0

    data["device_velocity_5m"] = 0
    data["device_velocity_1h"] = 0

    data["ip_velocity_5m"] = 0
    data["ip_velocity_1h"] = 0

    data["failed_attempts_1h"] = 0

    customer_history: dict[str, list[pd.Timestamp]] = {}
    device_history: dict[str, list[pd.Timestamp]] = {}
    ip_history: dict[str, list[pd.Timestamp]] = {}
    customer_failed_history: dict[str, list[pd.Timestamp]] = {}

    customer_amounts: dict[str, list[float]] = {}

    customer_velocity_5m = []
    customer_velocity_1h = []
    customer_velocity_24h = []

    device_velocity_5m = []
    device_velocity_1h = []

    ip_velocity_5m = []
    ip_velocity_1h = []

    failed_attempts_1h = []

    customer_avg_amount = []
    customer_amount_deviation = []

    for _, row in data.iterrows():

        timestamp = row["timestamp"]

        customer = str(row["customer_id"])
        device = str(row["device_id"])
        ip = str(row["ip_address"])

        # ----------------------------------------------------------
        # Customer velocity
        # ----------------------------------------------------------

        history = customer_history.setdefault(customer, [])

        customer_velocity_5m.append(
            sum(
                timestamp - previous <= pd.Timedelta(minutes=5)
                for previous in history
            )
        )

        customer_velocity_1h.append(
            sum(
                timestamp - previous <= pd.Timedelta(hours=1)
                for previous in history
            )
        )

        customer_velocity_24h.append(
            sum(
                timestamp - previous <= pd.Timedelta(hours=24)
                for previous in history
            )
        )

        history.append(timestamp)

        # ----------------------------------------------------------
        # Device velocity
        # ----------------------------------------------------------

        history = device_history.setdefault(device, [])

        device_velocity_5m.append(
            sum(
                timestamp - previous <= pd.Timedelta(minutes=5)
                for previous in history
            )
        )

        device_velocity_1h.append(
            sum(
                timestamp - previous <= pd.Timedelta(hours=1)
                for previous in history
            )
        )

        history.append(timestamp)

        # ----------------------------------------------------------
        # IP velocity
        # ----------------------------------------------------------

        history = ip_history.setdefault(ip, [])

        ip_velocity_5m.append(
            sum(
                timestamp - previous <= pd.Timedelta(minutes=5)
                for previous in history
            )
        )

        ip_velocity_1h.append(
            sum(
                timestamp - previous <= pd.Timedelta(hours=1)
                for previous in history
            )
        )

        history.append(timestamp)

        # ----------------------------------------------------------
        # Failed attempts
        # ----------------------------------------------------------

        failed_history = customer_failed_history.setdefault(
            customer,
            [],
        )

        recent_failures = sum(
            timestamp - previous <= pd.Timedelta(hours=1)
            for previous in failed_history
        )

        failed_attempts_1h.append(recent_failures)

        if str(row["status"]).lower() == "failed":
            failed_history.append(timestamp)

        # ----------------------------------------------------------
        # Amount behavior
        # ----------------------------------------------------------

        amounts = customer_amounts.setdefault(customer, [])

        if amounts:
            average_amount = sum(amounts) / len(amounts)
            deviation = (
                abs(float(row["amount"]) - average_amount)
                / max(average_amount, 1.0)
            )
        else:
            average_amount = float(row["amount"])
            deviation = 0.0

        customer_avg_amount.append(average_amount)
        customer_amount_deviation.append(deviation)

        amounts.append(float(row["amount"]))

    data["customer_velocity_5m"] = customer_velocity_5m
    data["customer_velocity_1h"] = customer_velocity_1h
    data["customer_velocity_24h"] = customer_velocity_24h

    data["device_velocity_5m"] = device_velocity_5m
    data["device_velocity_1h"] = device_velocity_1h

    data["ip_velocity_5m"] = ip_velocity_5m
    data["ip_velocity_1h"] = ip_velocity_1h

    data["failed_attempts_1h"] = failed_attempts_1h

    data["customer_avg_amount"] = customer_avg_amount
    data["customer_amount_deviation"] = customer_amount_deviation

    return data