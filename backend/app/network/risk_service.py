from dataclasses import dataclass

import pandas as pd

from app.network.entity_relationships import (
    analyze_entity_relationships,
)
from app.network.fraud_spike import detect_fraud_spike
from app.network.abuse_ring import detect_abuse_rings


@dataclass
class NetworkRiskResult:
    fraud_spike: bool
    shared_device_count: int
    shared_ip_count: int
    abuse_ring_detected: bool
    network_risk_score: float
    reasons: list[str]


def analyze_network_risk(
    transactions: pd.DataFrame,
) -> NetworkRiskResult:
    """
    Combine network-level detectors into a single network risk signal.
    """

    spike = detect_fraud_spike(transactions)

    relationships = analyze_entity_relationships(
        transactions
    )

    abuse_rings = detect_abuse_rings(
        transactions
    )

    reasons = []

    network_risk_score = 0.0

    if spike.fraud_spike:
        network_risk_score += 0.40
        reasons.append("fraud_spike_detected")

    if relationships.shared_device_count > 0:
        network_risk_score += 0.20
        reasons.append("shared_devices_detected")

    if relationships.shared_ip_count > 0:
        network_risk_score += 0.20
        reasons.append("shared_ips_detected")

    if abuse_rings.ring_count > 0:
        network_risk_score += 0.20
        reasons.append("candidate_abuse_network_detected")

    return NetworkRiskResult(
        fraud_spike=spike.fraud_spike,
        shared_device_count=relationships.shared_device_count,
        shared_ip_count=relationships.shared_ip_count,
        abuse_ring_detected=abuse_rings.ring_count > 0,
        network_risk_score=round(
            min(network_risk_score, 1.0),
            6,
        ),
        reasons=reasons,
    )