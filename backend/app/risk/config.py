from dataclasses import dataclass


@dataclass(frozen=True)
class RiskConfig:
    """Configuration for RazorShield fraud detection rules."""

    # Velocity rule
    velocity_window_minutes: int = 10
    max_transactions_in_window: int = 5
    velocity_risk_points: int = 30

    # Country mismatch rule
    country_mismatch_risk_points: int = 20

    # New account + high-value rule
    new_account_max_age_days: int = 7
    high_value_threshold: float = 500.0
    new_account_high_value_risk_points: int = 30

    # Repeated failures rule
    failure_window_minutes: int = 15
    max_failures_in_window: int = 3
    repeated_failures_risk_points: int = 25


DEFAULT_RISK_CONFIG = RiskConfig()