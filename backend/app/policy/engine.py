from dataclasses import dataclass


@dataclass
class RiskDecision:
    decision: str
    risk_score: float
    reasons: list[str]


def make_decision(
    fraud_probability: float,
    rule_risk_score: float,
    rule_risk_flag: int,
    rule_signal_count: int,
) -> RiskDecision:
    """
    Convert model and rule signals into an operational risk decision.
    """

    risk_score = (
        0.70 * fraud_probability
        + 0.30 * rule_risk_score
    )

    reasons = []

    if fraud_probability >= 0.20:
        reasons.append("high_ml_fraud_probability")
    elif fraud_probability >= 0.05:
        reasons.append("elevated_ml_fraud_probability")

    if rule_risk_flag:
        reasons.append("rule_engine_flagged_transaction")

    if rule_signal_count >= 2:
        reasons.append("multiple_risk_signals")

    if risk_score >= 0.50:
        decision = "HOLD"
    elif risk_score >= 0.05 or rule_risk_flag:
        decision = "REVIEW"
    else:
        decision = "ALLOW"

    return RiskDecision(
        decision=decision,
        risk_score=round(risk_score, 6),
        reasons=reasons,
    )