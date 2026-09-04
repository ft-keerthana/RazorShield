from dataclasses import dataclass

import pandas as pd


@dataclass
class EntityRelationshipResult:
    shared_device_count: int
    shared_ip_count: int
    high_risk_devices: list[str]
    high_risk_ips: list[str]


def analyze_entity_relationships(
    transactions: pd.DataFrame,
    min_customers: int = 2,
) -> EntityRelationshipResult:
    """
    Identify devices and IP addresses shared by multiple customers.

    A shared entity is useful as a network-risk signal because the same
    device or IP being associated with multiple customers can indicate
    coordinated or abusive activity.
    """

    required_columns = {
        "customer_id",
        "device_id",
        "ip_address",
    }

    missing_columns = required_columns - set(transactions.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    data = transactions[
        ["customer_id", "device_id", "ip_address"]
    ].copy()

    data = data.dropna(
        subset=["customer_id", "device_id", "ip_address"]
    )

    device_customer_counts = (
        data.groupby("device_id")["customer_id"]
        .nunique()
    )

    ip_customer_counts = (
        data.groupby("ip_address")["customer_id"]
        .nunique()
    )

    shared_devices = device_customer_counts[
        device_customer_counts >= min_customers
    ]

    shared_ips = ip_customer_counts[
        ip_customer_counts >= min_customers
    ]

    return EntityRelationshipResult(
        shared_device_count=int(len(shared_devices)),
        shared_ip_count=int(len(shared_ips)),
        high_risk_devices=shared_devices.index.astype(str).tolist(),
        high_risk_ips=shared_ips.index.astype(str).tolist(),
    )