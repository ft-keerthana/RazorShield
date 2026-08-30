from __future__ import annotations

from typing import Any

from .config import DEFAULT_RISK_CONFIG, RiskConfig
from .rules import (
    check_country_mismatch,
    check_new_account_high_value,
    check_repeated_failures,
    check_velocity,
)


class RiskEngine:
    """Runs RazorShield's configurable fraud detection rules."""

    def __init__(
        self,
        config: RiskConfig = DEFAULT_RISK_CONFIG,
    ) -> None:
        self.config = config

    def evaluate(
        self,
        transaction: dict[str, Any],
        transaction_history: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:

        if transaction_history is None:
            transaction_history = []

        results = [
            check_velocity(
                transaction,
                transaction_history,
                self.config,
            ),
            check_country_mismatch(
                transaction,
                self.config,
            ),
            check_new_account_high_value(
                transaction,
                self.config,
            ),
            check_repeated_failures(
                transaction,
                transaction_history,
                self.config,
            ),
        ]

        triggered_signals = [
            result
            for result in results
            if result["triggered"]
        ]

        risk_score = min(
            sum(result["risk_points"] for result in results),
            100,
        )

        return {
            "risk_score": risk_score,
            "is_suspicious": risk_score > 0,
            "signals": triggered_signals,
            "all_rule_results": results,
        }