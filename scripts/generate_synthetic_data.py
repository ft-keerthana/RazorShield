from __future__ import annotations

import random
import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker


SEED = 42

fake = Faker()
Faker.seed(SEED)
random.seed(SEED)


COUNTRIES = ["US", "CA", "GB", "DE", "IN", "FR", "AU", "JP"]
CURRENCY = "USD"


def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def random_timestamp(
    start_time: datetime,
    end_time: datetime,
) -> datetime:
    """Generate a random timestamp within the given window."""
    total_seconds = int((end_time - start_time).total_seconds())

    return start_time + timedelta(
        seconds=random.randint(0, total_seconds)
    )


def generate_razorshield_dataset(
    num_records: int = 10_000,
    fraud_ratio: float = 0.03,
) -> pd.DataFrame:
    """
    Generate a synthetic transaction dataset for RazorShield.

    Fraud scenarios:
    - fraud_ring: shared devices/IPs across multiple customers
    - account_takeover: unusual device/location + higher value transaction
    - velocity_attack: multiple transactions from an account in a short period
    - high_risk_transaction: suspicious combination of signals

    Legitimate scenarios include normal transactions and legitimate-but-unusual
    behaviour to prevent perfect separation between classes.
    """

    if not 0 < fraud_ratio < 1:
        raise ValueError("fraud_ratio must be between 0 and 1")

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    num_fraud = int(num_records * fraud_ratio)
    num_legitimate = num_records - num_fraud

    num_customers = max(500, num_records // 5)
    num_devices = max(200, num_records // 8)
    num_ips = max(200, num_records // 8)

    customers = [generate_id("cust") for _ in range(num_customers)]
    devices = [generate_id("dev") for _ in range(num_devices)]
    ips = [fake.ipv4() for _ in range(num_ips)]

    # Small pool deliberately used by fraud-ring transactions.
    suspicious_devices = devices[:10]
    suspicious_ips = ips[:10]

    # Each customer gets a "home" country and a primary device.
    customer_country = {
        customer_id: random.choice(COUNTRIES)
        for customer_id in customers
    }

    customer_primary_device = {
        customer_id: random.choice(devices)
        for customer_id in customers
    }

    customer_primary_ip = {
        customer_id: random.choice(ips)
        for customer_id in customers
    }

    # Track historical activity while generating data.
    customer_transactions = defaultdict(list)

    now = datetime.now()
    start_time = now - timedelta(days=30)

    records = []

    # ------------------------------------------------------------------
    # Helper functions
    # ------------------------------------------------------------------

    def create_base_transaction(
        customer_id: str,
        timestamp: datetime,
        scenario: str,
        is_fraud: int,
    ) -> dict:
        """Create a common transaction structure."""

        return {
            "transaction_id": generate_id("txn"),
            "customer_id": customer_id,
            "merchant_id": f"merch_{random.randint(1, 50)}",
            "currency": CURRENCY,
            "status": "success",
            "timestamp": timestamp.isoformat(),
            "billing_country": customer_country[customer_id],
            "scenario": scenario,
            "is_fraud": is_fraud,
        }

    # ------------------------------------------------------------------
    # LEGITIMATE TRANSACTIONS
    # ------------------------------------------------------------------

    for _ in range(num_legitimate):
        customer_id = random.choice(customers)
        timestamp = random_timestamp(start_time, now)

        # Most legitimate customers use their normal device/IP.
        if random.random() < 0.85:
            device_id = customer_primary_device[customer_id]
            ip_address = customer_primary_ip[customer_id]
        else:
            # New device / travel happens legitimately too.
            device_id = random.choice(devices)
            ip_address = random.choice(ips)

        billing_country = customer_country[customer_id]

        # Some legitimate customers purchase internationally.
        if random.random() < 0.08:
            shipping_country = random.choice(COUNTRIES)
        else:
            shipping_country = billing_country

        # Most amounts are small, but some legitimate purchases are expensive.
        if random.random() < 0.10:
            amount = round(random.uniform(200, 1_200), 2)
            scenario = "legitimate_unusual"
        else:
            amount = round(random.uniform(5, 350), 2)
            scenario = "legitimate"

        transaction = create_base_transaction(
            customer_id=customer_id,
            timestamp=timestamp,
            scenario=scenario,
            is_fraud=0,
        )

        transaction.update(
            {
                "amount": amount,
                "shipping_country": shipping_country,
                "device_id": device_id,
                "ip_address": ip_address,
            }
        )

        records.append(transaction)
        customer_transactions[customer_id].append(timestamp)

    # ------------------------------------------------------------------
    # FRAUD TRANSACTIONS
    # ------------------------------------------------------------------

    fraud_scenarios = [
        "fraud_ring",
        "account_takeover",
        "velocity_attack",
        "high_risk_transaction",
    ]

    for _ in range(num_fraud):
        scenario = random.choice(fraud_scenarios)
        customer_id = random.choice(customers)
        billing_country = customer_country[customer_id]

        timestamp = random_timestamp(start_time, now)

        transaction = create_base_transaction(
            customer_id=customer_id,
            timestamp=timestamp,
            scenario=scenario,
            is_fraud=1,
        )

        # --------------------------------------------------------------
        # Scenario 1: FRAUD RING
        # Multiple accounts reuse the same suspicious devices/IPs.
        # --------------------------------------------------------------

        if scenario == "fraud_ring":
            device_id = random.choice(suspicious_devices)
            ip_address = random.choice(suspicious_ips)

            amount = round(random.uniform(30, 1_000), 2)

            # Often, but not always, there is a location mismatch.
            if random.random() < 0.65:
                shipping_country = random.choice(
                    [
                        country
                        for country in COUNTRIES
                        if country != billing_country
                    ]
                )
            else:
                shipping_country = billing_country

        # --------------------------------------------------------------
        # Scenario 2: ACCOUNT TAKEOVER
        # New device + new location + unusual transaction amount.
        # --------------------------------------------------------------

        elif scenario == "account_takeover":
            device_id = random.choice(devices)
            ip_address = random.choice(ips)

            amount = round(random.uniform(100, 1_500), 2)

            shipping_country = random.choice(
                [
                    country
                    for country in COUNTRIES
                    if country != billing_country
                ]
            )

            # More likely during unusual hours, but not guaranteed.
            timestamp = timestamp.replace(
                hour=random.choice([0, 1, 2, 3, 4, 22, 23])
            )

            transaction["timestamp"] = timestamp.isoformat()

        # --------------------------------------------------------------
        # Scenario 3: VELOCITY ATTACK
        # Many transactions are concentrated in a short time window.
        # --------------------------------------------------------------

        elif scenario == "velocity_attack":
            if customer_transactions[customer_id]:
                recent_base = random.choice(
                    customer_transactions[customer_id]
                )

                timestamp = recent_base + timedelta(
                    minutes=random.randint(1, 10)
                )

                # Keep timestamp inside our overall window.
                timestamp = min(timestamp, now)

            device_id = customer_primary_device[customer_id]
            ip_address = customer_primary_ip[customer_id]

            amount = round(random.uniform(20, 800), 2)

            shipping_country = (
                billing_country
                if random.random() < 0.70
                else random.choice(COUNTRIES)
            )

            transaction["timestamp"] = timestamp.isoformat()

        # --------------------------------------------------------------
        # Scenario 4: HIGH-RISK TRANSACTION
        # Combination of moderately suspicious signals.
        # --------------------------------------------------------------

        else:
            amount = round(random.uniform(250, 2_000), 2)

            device_id = (
                random.choice(suspicious_devices)
                if random.random() < 0.50
                else random.choice(devices)
            )

            ip_address = (
                random.choice(suspicious_ips)
                if random.random() < 0.50
                else random.choice(ips)
            )

            shipping_country = (
                random.choice(
                    [
                        country
                        for country in COUNTRIES
                        if country != billing_country
                    ]
                )
                if random.random() < 0.60
                else billing_country
            )

        transaction.update(
            {
                "amount": amount,
                "shipping_country": shipping_country,
                "device_id": device_id,
                "ip_address": ip_address,
            }
        )

        records.append(transaction)
        customer_transactions[customer_id].append(timestamp)

    # ------------------------------------------------------------------
    # Finalize dataset
    # ------------------------------------------------------------------

    df = pd.DataFrame(records)

    # Shuffle so fraud isn't grouped together.
    df = (
        df.sample(frac=1, random_state=SEED)
        .reset_index(drop=True)
    )

    return df


def main() -> None:
    df = generate_razorshield_dataset(
        num_records=10_000,
        fraud_ratio=0.03,
    )

    project_root = Path(__file__).resolve().parents[1]

    output_dir = project_root / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "transactions.csv"

    df.to_csv(output_path, index=False)

    print("=" * 50)
    print("RazorShield Synthetic Dataset Generated")
    print("=" * 50)
    print(f"Total transactions: {len(df):,}")
    print(f"Fraud transactions: {df['is_fraud'].sum():,}")
    print(f"Fraud rate: {df['is_fraud'].mean() * 100:.2f}%")

    print("\nScenario distribution:")
    print(df["scenario"].value_counts())

    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()