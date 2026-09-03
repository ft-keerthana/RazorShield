from __future__ import annotations

import pandas as pd


DEFAULT_RULES = {
    "customer_velocity_5m": {
        "moderate_threshold": 2,
        "high_threshold": 3,
        "weight": 0.20,
        "reason": "High customer transaction velocity",
    },
    "customer_velocity_1h": {
        "moderate_threshold": 3,
        "high_threshold": 5,
        "weight": 0.15,
        "reason": "Elevated customer transaction velocity",
    },
    "device_velocity_1h": {
        "moderate_threshold": 3,
        "high_threshold": 5,
        "weight": 0.15,
        "reason": "High device transaction velocity",
    },
    "ip_velocity_1h": {
        "moderate_threshold": 3,
        "high_threshold": 5,
        "weight": 0.15,
        "reason": "High IP transaction velocity",
    },
    "failed_attempts_1h": {
        "moderate_threshold": 1,
        "high_threshold": 2,
        "weight": 0.15,
        "reason": "Multiple failed attempts",
    },
    "billing_shipping_mismatch": {
        "moderate_threshold": 1,
        "high_threshold": 1,
        "weight": 0.05,
        "reason": "Billing and shipping country mismatch",
    },
    "device_customer_count": {
        "moderate_threshold": 3,
        "high_threshold": 5,
        "weight": 0.05,
        "reason": "Device associated with many customers",
    },
    "ip_customer_count": {
        "moderate_threshold": 3,
        "high_threshold": 5,
        "weight": 0.10,
        "reason": "IP associated with many customers",
    },
}


def apply_risk_rules(
    df: pd.DataFrame,
    rules: dict | None = None,
) -> pd.DataFrame:
    """
    Apply configurable risk rules and generate a unified rule-based risk score.

    Each rule contributes:
        0.0              -> below moderate threshold
        0.5 * weight     -> moderate signal
        1.0 * weight     -> high signal
    """

    data = df.copy()
    active_rules = rules or DEFAULT_RULES

    missing_columns = [
        column for column in active_rules
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required rule features: {missing_columns}"
        )

    scores = []
    flags = []
    levels = []
    reasons = []
    signal_counts = []

    for _, row in data.iterrows():
        score = 0.0
        row_reasons = []
        signals = 0

        for feature, config in active_rules.items():
            value = row[feature]

            moderate_threshold = config["moderate_threshold"]
            high_threshold = config["high_threshold"]
            weight = config["weight"]

            if value >= high_threshold:
                score += weight
                signals += 1
                row_reasons.append(config["reason"])

            elif value >= moderate_threshold:
                score += weight * 0.5
                signals += 1
                row_reasons.append(
                    f"Moderate: {config['reason']}"
                )

        score = min(score, 1.0)

        if score >= 0.50:
            level = "high"
        elif score >= 0.20:
            level = "medium"
        else:
            level = "low"

        # Only escalate to a rule flag when multiple/strong
        # risk signals produce a meaningful combined score.
        flag = int(score >= 0.50)

        scores.append(score)
        flags.append(flag)
        levels.append(level)
        reasons.append(row_reasons)
        signal_counts.append(signals)

    data["rule_risk_score"] = scores
    data["rule_risk_flag"] = flags
    data["rule_risk_level"] = levels
    data["risk_reasons"] = reasons
    data["rule_signal_count"] = signal_counts

    return data