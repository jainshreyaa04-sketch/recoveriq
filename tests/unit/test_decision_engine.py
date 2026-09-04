from backend.services.decision_engine import (
    decide_recovery_action,
)


def test_insufficient_funds_first_attempt():

    result = decide_recovery_action(
        recovery_probability=0.75,
        failure_reason="insufficient_funds",
        attempt_number=1,
        amount=1500,
        customer_transaction_count=30,
    )

    assert result["action"] == "wait_and_retry"


def test_insufficient_funds_multiple_attempts():

    result = decide_recovery_action(
        recovery_probability=0.75,
        failure_reason="insufficient_funds",
        attempt_number=3,
        amount=1500,
        customer_transaction_count=30,
    )

    assert result["action"] == "send_payment_link"


def test_expired_card():

    result = decide_recovery_action(
        recovery_probability=0.60,
        failure_reason="expired_card",
        attempt_number=1,
        amount=1000,
        customer_transaction_count=20,
    )

    assert result["action"] == "request_new_payment_method"


def test_low_probability():

    result = decide_recovery_action(
        recovery_probability=0.20,
        failure_reason="technical_error",
        attempt_number=1,
        amount=1000,
        customer_transaction_count=10,
    )

    assert result["action"] == "no_action"