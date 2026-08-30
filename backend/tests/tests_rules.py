from datetime import datetime, timedelta

from backend.app.risk.config import DEFAULT_RISK_CONFIG
from backend.app.risk.engine import RiskEngine


def make_transaction(
    customer_id: str = "cust_1",
    timestamp: datetime | None = None,
    amount: float = 100.0,
    billing_country: str = "IN",
    shipping_country: str = "IN",
    account_created_at: datetime | None = None,
    status: str = "success",
) -> dict:

    now = timestamp or datetime.now()

    return {
        "transaction_id": "txn_test",
        "customer_id": customer_id,
        "amount": amount,
        "timestamp": now.isoformat(),
        "billing_country": billing_country,
        "shipping_country": shipping_country,
        "account_created_at": (
            account_created_at or now - timedelta(days=30)
        ).isoformat(),
        "status": status,
    }


def test_country_mismatch():
    engine = RiskEngine()

    transaction = make_transaction(
        billing_country="IN",
        shipping_country="US",
    )

    result = engine.evaluate(transaction)

    assert result["risk_score"] == (
        DEFAULT_RISK_CONFIG.country_mismatch_risk_points
    )


def test_new_account_high_value():
    now = datetime.now()

    transaction = make_transaction(
        amount=1000.0,
        timestamp=now,
        account_created_at=now - timedelta(days=2),
    )

    result = RiskEngine().evaluate(transaction)

    assert any(
        signal["rule"] == "new_account_high_value"
        for signal in result["signals"]
    )


def test_velocity():
    now = datetime.now()

    transaction = make_transaction(timestamp=now)

    history = [
        make_transaction(
            customer_id="cust_1",
            timestamp=now - timedelta(minutes=i),
        )
        for i in range(1, 6)
    ]

    result = RiskEngine().evaluate(
        transaction,
        transaction_history=history,
    )

    assert any(
        signal["rule"] == "velocity"
        for signal in result["signals"]
    )


def test_repeated_failures():
    now = datetime.now()

    transaction = make_transaction(
        timestamp=now,
        status="failed",
    )

    history = [
        make_transaction(
            customer_id="cust_1",
            timestamp=now - timedelta(minutes=i),
            status="failed",
        )
        for i in range(1, 3)
    ]

    result = RiskEngine().evaluate(
        transaction,
        transaction_history=history,
    )

    assert any(
        signal["rule"] == "repeated_failures"
        for signal in result["signals"]
    )


def test_normal_transaction_has_zero_risk():
    transaction = make_transaction()

    result = RiskEngine().evaluate(transaction)

    assert result["risk_score"] == 0
    assert result["signals"] == []