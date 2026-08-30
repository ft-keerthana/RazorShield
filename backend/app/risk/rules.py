from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from .config import RiskConfig


def _parse_datetime(value: str | datetime) -> datetime:
    """Convert an ISO datetime string or datetime object into datetime."""
    if isinstance(value, datetime):
        return value

    return datetime.fromisoformat(value)


def check_velocity(
    transaction: dict[str, Any],
    transaction_history: list[dict[str, Any]],
    config: RiskConfig,
) -> dict[str, Any]:
    """Detect too many transactions from the same customer in a time window."""

    current_time = _parse_datetime(transaction["timestamp"])
    customer_id = transaction["customer_id"]

    window_start = current_time - timedelta(
        minutes=config.velocity_window_minutes
    )

    recent_transactions = [
        event
        for event in transaction_history
        if event["customer_id"] == customer_id
        and window_start <= _parse_datetime(event["timestamp"]) <= current_time
    ]

    transaction_count = len(recent_transactions) + 1

    triggered = transaction_count > config.max_transactions_in_window

    return {
        "rule": "velocity",
        "triggered": triggered,
        "risk_points": (
            config.velocity_risk_points if triggered else 0
        ),
        "reason": (
            f"{transaction_count} transactions detected within "
            f"{config.velocity_window_minutes} minutes"
            if triggered
            else None
        ),
    }


def check_country_mismatch(
    transaction: dict[str, Any],
    config: RiskConfig,
) -> dict[str, Any]:
    """Detect billing and shipping country mismatches."""

    triggered = (
        transaction["billing_country"]
        != transaction["shipping_country"]
    )

    return {
        "rule": "country_mismatch",
        "triggered": triggered,
        "risk_points": (
            config.country_mismatch_risk_points if triggered else 0
        ),
        "reason": (
            "Billing and shipping countries do not match"
            if triggered
            else None
        ),
    }


def check_new_account_high_value(
    transaction: dict[str, Any],
    config: RiskConfig,
) -> dict[str, Any]:
    """Detect high-value transactions from newly created accounts."""

    transaction_time = _parse_datetime(transaction["timestamp"])
    account_created_at = _parse_datetime(
        transaction["account_created_at"]
    )

    account_age_days = (
        transaction_time - account_created_at
    ).total_seconds() / 86_400

    amount = float(transaction["amount"])

    is_new_account = (
        account_age_days <= config.new_account_max_age_days
    )

    is_high_value = (
        amount >= config.high_value_threshold
    )

    triggered = is_new_account and is_high_value

    return {
        "rule": "new_account_high_value",
        "triggered": triggered,
        "risk_points": (
            config.new_account_high_value_risk_points
            if triggered
            else 0
        ),
        "reason": (
            f"New account ({account_age_days:.1f} days old) "
            f"made a high-value transaction of {amount:.2f}"
            if triggered
            else None
        ),
    }


def check_repeated_failures(
    transaction: dict[str, Any],
    transaction_history: list[dict[str, Any]],
    config: RiskConfig,
) -> dict[str, Any]:
    """Detect repeated failed payment attempts."""

    current_time = _parse_datetime(transaction["timestamp"])
    customer_id = transaction["customer_id"]

    window_start = current_time - timedelta(
        minutes=config.failure_window_minutes
    )

    failed_attempts = [
        event
        for event in transaction_history
        if event["customer_id"] == customer_id
        and event.get("status") in {"failed", "declined"}
        and window_start <= _parse_datetime(event["timestamp"]) <= current_time
    ]

    # Include the current transaction if it is a failed attempt.
    if transaction.get("status") in {"failed", "declined"}:
        failed_attempts.append(transaction)

    failure_count = len(failed_attempts)

    triggered = (
        failure_count >= config.max_failures_in_window
    )

    return {
        "rule": "repeated_failures",
        "triggered": triggered,
        "risk_points": (
            config.repeated_failures_risk_points
            if triggered
            else 0
        ),
        "reason": (
            f"{failure_count} failed payment attempts detected within "
            f"{config.failure_window_minutes} minutes"
            if triggered
            else None
        ),
    }