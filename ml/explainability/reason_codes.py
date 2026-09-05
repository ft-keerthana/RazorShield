def generate_reason_codes(
    transaction: dict,
    risk_score: float,
) -> list[str]:
    """
    Generate human-readable risk reason codes from
    observable transaction signals.
    """

    reasons = []

    if transaction.get("is_high_velocity"):
        reasons.append(
            "HIGH_TRANSACTION_VELOCITY"
        )

    if transaction.get("country_mismatch"):
        reasons.append(
            "BILLING_IP_COUNTRY_MISMATCH"
        )

    if transaction.get("new_device"):
        reasons.append(
            "NEW_OR_UNRECOGNIZED_DEVICE"
        )

    if transaction.get("unusual_amount"):
        reasons.append(
            "UNUSUAL_TRANSACTION_AMOUNT"
        )

    if risk_score >= 0.8:
        reasons.append(
            "HIGH_MODEL_FRAUD_RISK"
        )

    return reasons