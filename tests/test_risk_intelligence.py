import pandas as pd
import pytest

from ml.intelligence.rules import apply_risk_rules


def test_rule_score_is_bounded():
    df = pd.DataFrame(
        {
            "customer_velocity_5m": [0, 3],
            "customer_velocity_1h": [0, 5],
            "device_velocity_1h": [0, 5],
            "ip_velocity_1h": [0, 5],
            "failed_attempts_1h": [0, 2],
            "billing_shipping_mismatch": [0, 1],
            "device_customer_count": [0, 5],
            "ip_customer_count": [0, 5],
        }
    )

    result = apply_risk_rules(df)

    assert result["rule_risk_score"].between(0, 1).all()


def test_high_signals_create_higher_risk():
    low_risk = pd.DataFrame(
        {
            "customer_velocity_5m": [0],
            "customer_velocity_1h": [0],
            "device_velocity_1h": [0],
            "ip_velocity_1h": [0],
            "failed_attempts_1h": [0],
            "billing_shipping_mismatch": [0],
            "device_customer_count": [0],
            "ip_customer_count": [0],
        }
    )

    high_risk = pd.DataFrame(
        {
            "customer_velocity_5m": [5],
            "customer_velocity_1h": [8],
            "device_velocity_1h": [8],
            "ip_velocity_1h": [8],
            "failed_attempts_1h": [4],
            "billing_shipping_mismatch": [1],
            "device_customer_count": [10],
            "ip_customer_count": [10],
        }
    )

    low_result = apply_risk_rules(low_risk)
    high_result = apply_risk_rules(high_risk)

    assert (
        high_result.loc[0, "rule_risk_score"]
        > low_result.loc[0, "rule_risk_score"]
    )


def test_missing_rule_feature_fails():
    df = pd.DataFrame(
        {
            "customer_velocity_5m": [1],
        }
    )

    with pytest.raises(ValueError):
        apply_risk_rules(df)