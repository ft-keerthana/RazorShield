from dataclasses import dataclass
from itertools import combinations

import pandas as pd


@dataclass
class AbuseRingResult:
    ring_count: int
    high_risk_customers: list[str]
    ring_sizes: list[int]
    top_rings: list[dict]


def detect_abuse_rings(
    transactions: pd.DataFrame,
    min_shared_entities: int = 2,
    min_ring_size: int = 3,
    max_rings: int = 20,
) -> AbuseRingResult:
    """
    Detect and rank potential abuse rings using shared infrastructure.

    Relationship strength is based on:
        - shared devices
        - shared IP addresses
        - repeated shared devices
        - repeated shared IP addresses

    The detector returns ranked local ring candidates rather than
    treating the entire connected network as one ring.
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
    ].dropna().copy()

    data["customer_id"] = data["customer_id"].astype(str)
    data["device_id"] = data["device_id"].astype(str)
    data["ip_address"] = data["ip_address"].astype(str)

    # Map each entity to the customers using it.
    device_customers = (
        data.groupby("device_id")["customer_id"]
        .unique()
        .to_dict()
    )

    ip_customers = (
        data.groupby("ip_address")["customer_id"]
        .unique()
        .to_dict()
    )

    # Count shared devices and IPs for every customer pair.
    pair_stats: dict[tuple[str, str], dict[str, int]] = {}

    for customers in device_customers.values():
        customers = sorted(customers)

        for customer_a, customer_b in combinations(customers, 2):
            pair = (customer_a, customer_b)

            stats = pair_stats.setdefault(
                pair,
                {
                    "shared_devices": 0,
                    "shared_ips": 0,
                },
            )

            stats["shared_devices"] += 1

    for customers in ip_customers.values():
        customers = sorted(customers)

        for customer_a, customer_b in combinations(customers, 2):
            pair = (customer_a, customer_b)

            stats = pair_stats.setdefault(
                pair,
                {
                    "shared_devices": 0,
                    "shared_ips": 0,
                },
            )

            stats["shared_ips"] += 1

    # Score relationships.
    scored_pairs = []

    for pair, stats in pair_stats.items():
        shared_devices = stats["shared_devices"]
        shared_ips = stats["shared_ips"]

        shared_entity_types = int(shared_devices > 0) + int(shared_ips > 0)

        if shared_entity_types < min_shared_entities:
            continue

        score = (
            2 * int(shared_devices > 0)
            + 2 * int(shared_ips > 0)
            + 2 * int(shared_devices >= 2)
            + 2 * int(shared_ips >= 2)
        )

        scored_pairs.append(
            {
                "customers": pair,
                "score": score,
                "shared_devices": shared_devices,
                "shared_ips": shared_ips,
            }
        )

    scored_pairs.sort(
        key=lambda item: (
            item["score"],
            item["shared_devices"] + item["shared_ips"],
        ),
        reverse=True,
    )

    # Keep only the strongest relationships for ring construction.
    strong_pairs = scored_pairs[: max_rings * 10]

    graph: dict[str, set[str]] = {}

    for relationship in strong_pairs:
        customer_a, customer_b = relationship["customers"]

        graph.setdefault(customer_a, set()).add(customer_b)
        graph.setdefault(customer_b, set()).add(customer_a)

    # Find local candidate groups.
    candidate_groups: list[set[str]] = []

    for customer in graph:
        neighbors = graph[customer]

        if len(neighbors) < min_ring_size - 1:
            continue

        group = {customer}
        group.update(neighbors)

        if len(group) >= min_ring_size:
            candidate_groups.append(group)

    # Deduplicate groups.
    unique_groups = {
        tuple(sorted(group))
        for group in candidate_groups
    }

    top_rings = []

    for group in unique_groups:
        members = list(group)

        relationships = []

        for customer_a, customer_b in combinations(members, 2):
            pair = (customer_a, customer_b)

            for relationship in strong_pairs:
                if relationship["customers"] == pair:
                    relationships.append(relationship)
                    break

        if not relationships:
            continue

        total_score = sum(
            relationship["score"]
            for relationship in relationships
        )

        top_rings.append(
            {
                "customers": sorted(members),
                "ring_size": len(members),
                "relationship_count": len(relationships),
                "total_score": total_score,
            }
        )

    top_rings.sort(
        key=lambda ring: (
            ring["total_score"],
            ring["relationship_count"],
        ),
        reverse=True,
    )

    top_rings = top_rings[:max_rings]

    high_risk_customers = sorted(
        {
            customer
            for ring in top_rings
            for customer in ring["customers"]
        }
    )

    ring_sizes = [
        ring["ring_size"]
        for ring in top_rings
    ]

    return AbuseRingResult(
        ring_count=len(top_rings),
        high_risk_customers=high_risk_customers,
        ring_sizes=ring_sizes,
        top_rings=top_rings,
    )