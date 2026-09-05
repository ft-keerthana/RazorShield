import pandas as pd


def build_fraud_trend(transactions: pd.DataFrame, days: int = 7):
    if days not in {7, 14, 30}:
        raise ValueError("days must be one of: 7, 14, 30")

    data = transactions.copy()

    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        errors="coerce",
    )

    data = data.dropna(subset=["timestamp"])

    if data.empty:
        return []

    latest_date = data["timestamp"].max().normalize()
    start_date = latest_date - pd.Timedelta(days=days - 1)

    data = data[
        (data["timestamp"] >= start_date)
        & (data["timestamp"] <= latest_date + pd.Timedelta(days=1))
    ].copy()

    data["date"] = data["timestamp"].dt.normalize()

    daily = (
        data.groupby("date")
        .agg(
            transactions=("transaction_id", "count"),
            fraudulent=("is_fraud", "sum"),
        )
        .reset_index()
    )

    date_range = pd.date_range(
        start=start_date,
        end=latest_date,
        freq="D",
    )

    daily = (
        daily.set_index("date")
        .reindex(date_range, fill_value=0)
        .rename_axis("date")
        .reset_index()
    )

    daily["fraud_rate"] = (
        daily["fraudulent"] / daily["transactions"].replace(0, pd.NA)
    ) * 100

    daily["fraud_rate"] = daily["fraud_rate"].fillna(0)

    return [
        {
            "date": row["date"].strftime("%Y-%m-%d"),
            "transactions": int(row["transactions"]),
            "fraudulent": int(row["fraudulent"]),
            "fraud_rate": round(float(row["fraud_rate"]), 2),
        }
        for _, row in daily.iterrows()
    ]