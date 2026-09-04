from dataclasses import dataclass


@dataclass
class CostDecision:
    decision: str
    expected_cost: float
    allow_cost: float
    review_cost: float
    hold_cost: float


def optimize_decision(
    fraud_probability: float,
    transaction_amount: float,
    false_positive_cost_rate: float = 0.02,
    false_negative_cost_rate: float = 1.0,
    review_cost: float = 5.0,
) -> CostDecision:
    """
    Select the decision with the lowest expected business cost.

    Costs:
    - ALLOW: cost of missing fraud
    - REVIEW: manual review cost
    - HOLD: cost of blocking a legitimate transaction
    """

    legitimate_probability = 1 - fraud_probability

    false_positive_cost = (
        transaction_amount * false_positive_cost_rate
    )

    false_negative_cost = (
        transaction_amount * false_negative_cost_rate
    )

    allow_cost = (
        fraud_probability * false_negative_cost
    )

    review_cost_value = review_cost

    hold_cost = (
        legitimate_probability * false_positive_cost
    )

    costs = {
        "ALLOW": allow_cost,
        "REVIEW": review_cost_value,
        "HOLD": hold_cost,
    }

    decision = min(
        costs,
        key=costs.get,
    )

    return CostDecision(
        decision=decision,
        expected_cost=round(costs[decision], 2),
        allow_cost=round(allow_cost, 2),
        review_cost=round(review_cost_value, 2),
        hold_cost=round(hold_cost, 2),
    )