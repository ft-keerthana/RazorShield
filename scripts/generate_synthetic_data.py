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

    Fraud scenarios describe behavioral patterns rather than directly
    determining the fraud label.

    Scenarios:
    - fraud_ring
    - account_takeover
    - velocity_attack
    - high_risk_transaction
    - repeated_failures
    - legitimate
    - legitimate_unusual

    The fraud label is sampled probabilistically from the generated
    transaction signals. This prevents scenario -> label leakage.
    """

    if not 0 < fraud_ratio < 1:
        raise ValueError("fraud_ratio must be between 0 and 1")

    num_records = int(num_records)

    num_customers = max(500, num_records // 5)
    num_devices = max(200, num_records // 8)
    num_ips = max(200, num_records // 8)

    customers = [
        generate_id("cust")
        for _ in range(num_customers)
    ]

    devices = [
        generate_id("dev")
        for _ in range(num_devices)
    ]

    ips = [
        fake.ipv4()
        for _ in range(num_ips)
    ]

    # A small subset of devices/IPs will appear more frequently in
    # suspicious activity, but they are NOT automatically fraudulent.
    suspicious_devices = devices[:10]
    suspicious_ips = ips[:10]

    now = datetime.now()
    start_time = now - timedelta(days=30)

    # --------------------------------------------------------------
    # Customer profiles
    # --------------------------------------------------------------

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

    # Account creation dates.
    customer_created_at = {}

    for customer_id in customers:
        if random.random() < 0.10:
            # New account: 0-7 days old
            created_at = now - timedelta(
                days=random.randint(0, 7),
                hours=random.randint(0, 23),
            )
        else:
            # Established account: 8-365 days old
            created_at = now - timedelta(
                days=random.randint(8, 365),
                hours=random.randint(0, 23),
            )

        customer_created_at[customer_id] = created_at

    # Track activity while generating transactions.
    customer_transactions = defaultdict(list)

    records = []

    # --------------------------------------------------------------
    # Helper functions
    # --------------------------------------------------------------

    def create_base_transaction(
        customer_id: str,
        timestamp: datetime,
        scenario: str,
        is_fraud: int,
        status: str = "success",
    ) -> dict:
        return {
            "transaction_id": generate_id("txn"),
            "customer_id": customer_id,
            "merchant_id": f"merch_{random.randint(1, 50)}",
            "currency": CURRENCY,
            "status": status,
            "timestamp": timestamp.isoformat(),
            "account_created_at": customer_created_at[
                customer_id
            ].isoformat(),
            "billing_country": customer_country[customer_id],
            "scenario": scenario,
            "is_fraud": is_fraud,
        }

    def sample_fraud_label(
        signal_score: float,
        target_rate: float = fraud_ratio,
    ) -> int:
        """
        Convert behavioral signals into a probabilistic fraud label.

        The score influences the probability but does not guarantee
        the label. This intentionally creates overlap between
        legitimate and fraudulent transactions.
        """

        # Center the probability around the requested dataset
        # fraud rate while allowing strong signals to increase risk.
        probability = target_rate * (
            0.2 + 6 * signal_score
        )

        probability = max(
            0.002,
            min(0.85, probability),
        )

        return int(random.random() < probability)

    # --------------------------------------------------------------
    # LEGITIMATE / MIXED TRANSACTIONS
    # --------------------------------------------------------------

    for _ in range(num_records):
        customer_id = random.choice(customers)

        valid_start = max(
            start_time,
            customer_created_at[customer_id],
        )

        timestamp = random_timestamp(
            valid_start,
            now,
        )

        # Start with normal customer behavior.
        device_id = customer_primary_device[customer_id]
        ip_address = customer_primary_ip[customer_id]

        billing_country = customer_country[customer_id]

        shipping_country = billing_country

        amount = round(
            random.uniform(5, 350),
            2,
        )

        status = "success"

        signal_score = 0.0
        scenario = "legitimate"

        # ----------------------------------------------------------
        # Normal behavioral variation
        # ----------------------------------------------------------

        # 15% chance of a different device.
        if random.random() < 0.15:
            device_id = random.choice(devices)
            signal_score += 0.10

        # 10% chance of a different IP.
        if random.random() < 0.10:
            ip_address = random.choice(ips)
            signal_score += 0.08

        # 8% location mismatch.
        if random.random() < 0.08:
            shipping_country = random.choice(
                [
                    country
                    for country in COUNTRIES
                    if country != billing_country
                ]
            )

            signal_score += 0.10

        # 10% unusually large legitimate purchase.
        if random.random() < 0.10:
            amount = round(
                random.uniform(200, 1_200),
                2,
            )

            scenario = "legitimate_unusual"
            signal_score += 0.10

        # Legitimate payment failures.
        if random.random() < 0.03:
            status = "failed"
            signal_score += 0.04

        # Occasionally create suspicious-looking but legitimate events.
        # These are important false-positive examples.
        if random.random() < 0.025:
            device_id = random.choice(devices)
            ip_address = random.choice(ips)

            shipping_country = random.choice(
                [
                    country
                    for country in COUNTRIES
                    if country != billing_country
                ]
            )

            amount = round(
                random.uniform(250, 1_000),
                2,
            )

            scenario = "legitimate_unusual"
            signal_score += 0.12

        # Weak probability of fraud based on signals.
        is_fraud = sample_fraud_label(
            signal_score
        )

        transaction = create_base_transaction(
            customer_id=customer_id,
            timestamp=timestamp,
            scenario=scenario,
            is_fraud=is_fraud,
            status=status,
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

        customer_transactions[
            customer_id
        ].append(timestamp)

    # --------------------------------------------------------------
    # BEHAVIORAL FRAUD-PATTERN TRANSACTIONS
    # --------------------------------------------------------------

    fraud_scenarios = [
        "fraud_ring",
        "account_takeover",
        "velocity_attack",
        "high_risk_transaction",
        "repeated_failures",
    ]

    # Generate additional transactions containing strong suspicious
    # patterns. Their labels are still probabilistic.
    num_pattern_events = max(
        1,
        int(
            num_records
            * fraud_ratio
            * 4.0
        ),
    )

    for _ in range(num_pattern_events):
        scenario = random.choice(
            fraud_scenarios
        )

        customer_id = random.choice(
            customers
        )

        billing_country = customer_country[
            customer_id
        ]

        valid_start = max(
            start_time,
            customer_created_at[
                customer_id
            ],
        )

        timestamp = random_timestamp(
            valid_start,
            now,
        )

        signal_score = 0.0

        # ----------------------------------------------------------
        # FRAUD RING
        # ----------------------------------------------------------

        if scenario == "fraud_ring":

            device_id = random.choice(
                suspicious_devices
            )

            ip_address = random.choice(
                suspicious_ips
            )

            amount = round(
                random.uniform(30, 1_000),
                2,
            )

            signal_score += 0.30

            if random.random() < 0.70:
                shipping_country = random.choice(
                    [
                        country
                        for country in COUNTRIES
                        if country != billing_country
                    ]
                )

                signal_score += 0.20

            else:
                shipping_country = billing_country

            status = "success"

        # ----------------------------------------------------------
        # ACCOUNT TAKEOVER
        # ----------------------------------------------------------

        elif scenario == "account_takeover":

            device_id = random.choice(devices)
            ip_address = random.choice(ips)

            amount = round(
                random.uniform(100, 1_500),
                2,
            )

            signal_score += 0.20

            # New device/IP is suspicious, but not always present.
            if random.random() < 0.85:

                device_id = random.choice(
                    [
                        device
                        for device in devices
                        if device
                        != customer_primary_device[
                            customer_id
                        ]
                    ]
                )

                signal_score += 0.20

            if random.random() < 0.75:

                ip_address = random.choice(
                    [
                        ip
                        for ip in ips
                        if ip
                        != customer_primary_ip[
                            customer_id
                        ]
                    ]
                )

                signal_score += 0.15

            if random.random() < 0.70:

                shipping_country = random.choice(
                    [
                        country
                        for country in COUNTRIES
                        if country != billing_country
                    ]
                )

                signal_score += 0.15

            else:
                shipping_country = billing_country

            if random.random() < 0.75:

                timestamp = timestamp.replace(
                    hour=random.choice(
                        [
                            0,
                            1,
                            2,
                            3,
                            4,
                            22,
                            23,
                        ]
                    )
                )

                signal_score += 0.15

            status = "success"

        # ----------------------------------------------------------
        # VELOCITY ATTACK
        # ----------------------------------------------------------

        elif scenario == "velocity_attack":

            if customer_transactions[
                customer_id
            ]:

                recent_base = max(
                    customer_transactions[
                        customer_id
                    ]
                )

                timestamp = (
                    recent_base
                    + timedelta(
                        minutes=random.randint(
                            1,
                            10,
                        )
                    )
                )

                timestamp = min(
                    timestamp,
                    now,
                )

            device_id = customer_primary_device[
                customer_id
            ]

            ip_address = customer_primary_ip[
                customer_id
            ]

            amount = round(
                random.uniform(20, 800),
                2,
            )

            shipping_country = billing_country

            status = "success"

            signal_score += 0.40

        # ----------------------------------------------------------
        # REPEATED FAILURES
        # ----------------------------------------------------------

        elif scenario == "repeated_failures":

            device_id = random.choice(
                suspicious_devices
            )

            ip_address = random.choice(
                suspicious_ips
            )

            amount = round(
                random.uniform(5, 500),
                2,
            )

            shipping_country = billing_country

            status = "failed"

            signal_score += 0.35

            # Generate a smaller burst of related attempts.
            burst_size = random.randint(
                2,
                4,
            )

            for attempt in range(
                burst_size
            ):

                attempt_time = (
                    timestamp
                    + timedelta(
                        minutes=attempt + 1
                    )
                )

                attempt_transaction = (
                    create_base_transaction(
                        customer_id=customer_id,
                        timestamp=attempt_time,
                        scenario=scenario,
                        is_fraud=sample_fraud_label(
                            signal_score
                        ),
                        status="failed",
                    )
                )

                attempt_transaction.update(
                    {
                        "amount": amount,
                        "shipping_country": shipping_country,
                        "device_id": device_id,
                        "ip_address": ip_address,
                    }
                )

                records.append(
                    attempt_transaction
                )

                customer_transactions[
                    customer_id
                ].append(attempt_time)

            continue

        # ----------------------------------------------------------
        # HIGH-RISK TRANSACTION
        # ----------------------------------------------------------

        else:

            amount = round(
                random.uniform(
                    250,
                    2_000,
                ),
                2,
            )

            signal_score += 0.20

            if random.random() < 0.50:

                device_id = random.choice(
                    suspicious_devices
                )

                signal_score += 0.15

            else:

                device_id = random.choice(
                    devices
                )

            if random.random() < 0.50:

                ip_address = random.choice(
                    suspicious_ips
                )

                signal_score += 0.15

            else:

                ip_address = random.choice(
                    ips
                )

            if random.random() < 0.60:

                shipping_country = random.choice(
                    [
                        country
                        for country in COUNTRIES
                        if country != billing_country
                    ]
                )

                signal_score += 0.15

            else:

                shipping_country = billing_country

            status = "success"

        # ----------------------------------------------------------
        # Label from signals, not scenario
        # ----------------------------------------------------------

        is_fraud = sample_fraud_label(
            signal_score
        )

        transaction = create_base_transaction(
            customer_id=customer_id,
            timestamp=timestamp,
            scenario=scenario,
            is_fraud=is_fraud,
            status=status,
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

        customer_transactions[
            customer_id
        ].append(timestamp)

    # --------------------------------------------------------------
    # Finalize
    # --------------------------------------------------------------

    df = pd.DataFrame(records)

    desired_fraud_count = int(
        num_records * fraud_ratio
    )

    fraud_df = df[
        df["is_fraud"] == 1
    ].copy()

    legitimate_df = df[
        df["is_fraud"] == 0
    ].copy()

    # --------------------------------------------------------------
    # Preserve representation of the main fraud mechanisms.
    # This prevents random downsampling from removing rare scenarios.
    # --------------------------------------------------------------

    fraud_scenarios = [
        "fraud_ring",
        "account_takeover",
        "velocity_attack",
        "high_risk_transaction",
        "repeated_failures",
    ]

    minimum_per_scenario = 25

    selected_indices = []

    for scenario_name in fraud_scenarios:

        scenario_indices = fraud_df.index[
            fraud_df["scenario"]
            == scenario_name
        ]

        sample_size = min(
            minimum_per_scenario,
            len(scenario_indices),
        )

        if sample_size > 0:

            selected = fraud_df.loc[
                scenario_indices
            ].sample(
                n=sample_size,
                random_state=SEED,
            )

            selected_indices.extend(
                selected.index.tolist()
            )

    selected_fraud = fraud_df.loc[
        selected_indices
    ].copy()

    # Fill the remaining fraud quota from fraud rows
    # that were not already selected.
    remaining_fraud_count = (
        desired_fraud_count
        - len(selected_fraud)
    )

    remaining_fraud_pool = fraud_df.drop(
        index=selected_indices,
        errors="ignore",
    )

    if remaining_fraud_count > 0:

        remaining_fraud = (
            remaining_fraud_pool.sample(
                n=min(
                    remaining_fraud_count,
                    len(remaining_fraud_pool),
                ),
                random_state=SEED,
            )
        )

        fraud_df = pd.concat(
            [
                selected_fraud,
                remaining_fraud,
            ],
            ignore_index=True,
        )

    else:

        fraud_df = selected_fraud.sample(
            n=desired_fraud_count,
            random_state=SEED,
        ).reset_index(drop=True)

    # Fill the remaining dataset with legitimate transactions.
    remaining = (
        num_records
        - len(fraud_df)
    )

    if len(legitimate_df) > remaining:

        legitimate_df = (
            legitimate_df.sample(
                n=remaining,
                random_state=SEED,
            )
        )

    df = pd.concat(
        [
            legitimate_df,
            fraud_df,
        ],
        ignore_index=True,
    )

    df = (
        df.sample(
            frac=1,
            random_state=SEED,
        )
        .reset_index(drop=True)
    )

    return df


def main() -> None:

    df = generate_razorshield_dataset(
        num_records=10_000,
        fraud_ratio=0.03,
    )

    project_root = (
        Path(__file__).resolve().parents[1]
    )

    output_dir = (
        project_root
        / "data"
        / "raw"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir
        / "transactions.csv"
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print("=" * 50)
    print(
        "RazorShield Synthetic Dataset Generated"
    )
    print("=" * 50)

    print(
        f"Total events: {len(df):,}"
    )

    print(
        f"Fraud events: "
        f"{df['is_fraud'].sum():,}"
    )

    print(
        f"Fraud rate: "
        f"{df['is_fraud'].mean() * 100:.2f}%"
    )

    print("\nScenario distribution:")

    print(
        df["scenario"].value_counts()
    )

    print("\nFraud rate by scenario:")

    print(
        df.groupby("scenario")["is_fraud"]
        .agg(["count", "mean"])
        .sort_values(
            "mean",
            ascending=False,
        )
        .round(3)
    )

    print("\nStatus distribution:")

    print(
        df["status"].value_counts()
    )

    print(
        f"\nSaved to: {output_path}"
    )


if __name__ == "__main__":
    main()
