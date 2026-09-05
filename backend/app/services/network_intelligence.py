import pandas as pd


def build_network_overview(transactions: pd.DataFrame):
    data = transactions.copy()

    customers = int(data["customer_id"].nunique())
    devices = int(data["device_id"].nunique())
    ips = int(data["ip_address"].nunique())

    suspicious_devices = int(
        data.loc[
            data["shared_device_flag"] == 1,
            "device_id",
        ].nunique()
    )

    suspicious_ips = int(
        data.loc[
            data["shared_ip_flag"] == 1,
            "ip_address",
        ].nunique()
    )

    connected_fraud_transactions = int(
        data.loc[
            (
                (data["shared_device_flag"] == 1)
                | (data["shared_ip_flag"] == 1)
            )
            & (data["is_fraud"] == 1)
        ].shape[0]
    )

    return {
        "customers": customers,
        "devices": devices,
        "ips": ips,
        "suspicious_devices": suspicious_devices,
        "suspicious_ips": suspicious_ips,
        "connected_fraud_transactions": connected_fraud_transactions,
    }


def build_suspicious_devices(
    transactions: pd.DataFrame,
    limit: int = 10,
):
    data = transactions.copy()

    suspicious = (
        data[data["shared_device_flag"] == 1]
        .groupby("device_id")
        .agg(
            customers=("customer_id", "nunique"),
            transactions=("transaction_id", "count"),
            fraudulent=("is_fraud", "sum"),
            max_risk_score=("rule_risk_score", "max"),
        )
        .reset_index()
    )

    suspicious["fraud_rate"] = (
        suspicious["fraudulent"]
        / suspicious["transactions"]
        * 100
    )

    suspicious = suspicious.sort_values(
        ["fraudulent", "max_risk_score", "transactions"],
        ascending=False,
    ).head(limit)

    return [
        {
            "device_id": row["device_id"],
            "customers": int(row["customers"]),
            "transactions": int(row["transactions"]),
            "fraudulent": int(row["fraudulent"]),
            "fraud_rate": round(float(row["fraud_rate"]), 2),
            "max_risk_score": round(
                float(row["max_risk_score"]),
                2,
            ),
        }
        for _, row in suspicious.iterrows()
    ]


def build_suspicious_ips(
    transactions: pd.DataFrame,
    limit: int = 10,
):
    data = transactions.copy()

    suspicious = (
        data[data["shared_ip_flag"] == 1]
        .groupby("ip_address")
        .agg(
            customers=("customer_id", "nunique"),
            transactions=("transaction_id", "count"),
            fraudulent=("is_fraud", "sum"),
            max_risk_score=("rule_risk_score", "max"),
        )
        .reset_index()
    )

    suspicious["fraud_rate"] = (
        suspicious["fraudulent"]
        / suspicious["transactions"]
        * 100
    )

    suspicious = suspicious.sort_values(
        ["fraudulent", "max_risk_score", "transactions"],
        ascending=False,
    ).head(limit)

    return [
        {
            "ip_address": row["ip_address"],
            "customers": int(row["customers"]),
            "transactions": int(row["transactions"]),
            "fraudulent": int(row["fraudulent"]),
            "fraud_rate": round(float(row["fraud_rate"]), 2),
            "max_risk_score": round(
                float(row["max_risk_score"]),
                2,
            ),
        }
        for _, row in suspicious.iterrows()
    ]