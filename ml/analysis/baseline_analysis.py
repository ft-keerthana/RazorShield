from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def load_data(path: Path) -> pd.DataFrame:
    """Load and prepare the transaction dataset for basic analysis."""

    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


def print_dataset_summary(df: pd.DataFrame) -> None:
    """Print basic dataset and fraud statistics."""

    total_transactions = len(df)
    fraud_count = int(df["is_fraud"].sum())
    fraud_rate = df["is_fraud"].mean() * 100

    print("=" * 50)
    print("RAZORSHIELD BASELINE FRAUD ANALYSIS")
    print("=" * 50)

    print(f"Total transactions: {total_transactions:,}")
    print(f"Fraud transactions: {fraud_count:,}")
    print(f"Legitimate transactions: {total_transactions - fraud_count:,}")
    print(f"Fraud rate: {fraud_rate:.2f}%")


def compare_amounts(df: pd.DataFrame) -> None:
    """Compare transaction amounts for fraud and legitimate events."""

    summary = (
        df.groupby("is_fraud")["amount"]
        .agg(["count", "mean", "median", "min", "max"])
        .rename(index={0: "Legitimate", 1: "Fraud"})
    )

    print("\nTransaction Amount Comparison:")
    print(summary.round(2))


def analyze_country_mismatch(df: pd.DataFrame) -> None:
    """Measure how frequently country mismatches occur."""

    df = df.copy()

    df["country_mismatch"] = (
        df["billing_country"] != df["shipping_country"]
    ).astype(int)

    mismatch_stats = (
        df.groupby("is_fraud")["country_mismatch"]
        .mean()
        .mul(100)
        .rename(index={0: "Legitimate", 1: "Fraud"})
    )

    print("\nCountry Mismatch Rate:")
    print(mismatch_stats.round(2).astype(str) + "%")


def analyze_device_reuse(df: pd.DataFrame) -> None:
    """Compare how many accounts share each device."""

    device_customer_counts = (
        df.groupby("device_id")["customer_id"]
        .nunique()
        .rename("unique_customers")
        .reset_index()
    )

    device_stats = df.merge(
        device_customer_counts,
        on="device_id",
        how="left",
    )

    summary = (
        device_stats.groupby("is_fraud")["unique_customers"]
        .mean()
        .rename(index={0: "Legitimate", 1: "Fraud"})
    )

    print("\nAverage Unique Customers per Device:")
    print(summary.round(2))


def create_fraud_distribution_plot(
    df: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Create and save a class distribution plot."""

    output_dir.mkdir(parents=True, exist_ok=True)

    counts = df["is_fraud"].value_counts().sort_index()

    plt.figure(figsize=(7, 5))
    plt.bar(
        ["Legitimate", "Fraud"],
        [counts.get(0, 0), counts.get(1, 0)],
    )
    plt.title("Transaction Class Distribution")
    plt.xlabel("Transaction Type")
    plt.ylabel("Number of Transactions")
    plt.tight_layout()

    output_path = output_dir / "class_distribution.png"
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"\nSaved plot: {output_path}")


def create_amount_plot(
    df: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Visualize transaction amount distributions."""

    output_dir.mkdir(parents=True, exist_ok=True)

    legitimate = df.loc[df["is_fraud"] == 0, "amount"]
    fraud = df.loc[df["is_fraud"] == 1, "amount"]

    plt.figure(figsize=(8, 5))
    plt.hist(
        legitimate,
        bins=50,
        alpha=0.7,
        label="Legitimate",
    )
    plt.hist(
        fraud,
        bins=50,
        alpha=0.7,
        label="Fraud",
    )

    plt.title("Transaction Amount Distribution")
    plt.xlabel("Amount")
    plt.ylabel("Number of Transactions")
    plt.legend()
    plt.tight_layout()

    output_path = output_dir / "amount_distribution.png"
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Saved plot: {output_path}")


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]

    data_path = (
        project_root
        / "data"
        / "raw"
        / "transactions.csv"
    )

    output_dir = (
        project_root
        / "docs"
        / "assets"
        / "analysis"
    )

    df = load_data(data_path)

    print_dataset_summary(df)
    compare_amounts(df)
    analyze_country_mismatch(df)
    analyze_device_reuse(df)

    create_fraud_distribution_plot(df, output_dir)
    create_amount_plot(df, output_dir)


if __name__ == "__main__":
    main()