from __future__ import annotations

from collections import defaultdict

import pandas as pd


def add_device_entity_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate point-in-time device and IP intelligence features.

    Features are based only on relationships observed before the
    current transaction to avoid future-data leakage.
    """

    data = df.copy()

    required_columns = {
        "timestamp",
        "customer_id",
        "device_id",
        "ip_address",
    }

    missing = required_columns - set(data.columns)
    if missing:
        raise ValueError(
            f"Missing required columns for device intelligence: {sorted(missing)}"
        )

    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        errors="coerce",
    )

    data = data.sort_values("timestamp").reset_index(drop=True)

    # Historical customers seen on each device/IP.
    device_customers = defaultdict(set)
    ip_customers = defaultdict(set)

    # Historical devices/IPs used by each customer.
    customer_devices = defaultdict(set)
    customer_ips = defaultdict(set)

    device_customer_counts = []
    ip_customer_counts = []
    customer_device_counts = []
    customer_ip_counts = []

    for row in data.itertuples(index=False):
        customer_id = row.customer_id
        device_id = row.device_id
        ip_address = row.ip_address

        # IMPORTANT:
        # Calculate using history BEFORE adding the current transaction.
        device_customer_counts.append(
            len(device_customers[device_id])
        )

        ip_customer_counts.append(
            len(ip_customers[ip_address])
        )

        customer_device_counts.append(
            len(customer_devices[customer_id])
        )

        customer_ip_counts.append(
            len(customer_ips[customer_id])
        )

        # Update historical relationships.
        device_customers[device_id].add(customer_id)
        ip_customers[ip_address].add(customer_id)

        customer_devices[customer_id].add(device_id)
        customer_ips[customer_id].add(ip_address)

    data["device_customer_count"] = device_customer_counts
    data["ip_customer_count"] = ip_customer_counts
    data["customer_device_count"] = customer_device_counts
    data["customer_ip_count"] = customer_ip_counts

    # A device/IP previously associated with another customer
    # is a useful account-sharing / takeover signal.
    data["shared_device_flag"] = (
        data["device_customer_count"] > 0
    ).astype(int)

    data["shared_ip_flag"] = (
        data["ip_customer_count"] > 0
    ).astype(int)

    return data
