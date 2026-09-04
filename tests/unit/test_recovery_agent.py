from agents.core.recovery_agent import (
    RecoveryAgent,
)


def test_agent_processes_payment():

    agent = RecoveryAgent()

    result = agent.process_payment(
        transaction_id="txn_agent_001",
        amount=1500,
        merchant_type="ecommerce",
        payment_method="upi",
        failure_reason="insufficient_funds",
        attempt_number=1,
        customer_transaction_count=35,
    )

    assert "recovery_probability" in result
    assert "action" in result
    assert "reason" in result
    assert "status" in result


def test_agent_contains_transaction_id():

    agent = RecoveryAgent()

    result = agent.process_payment(
        transaction_id="txn_agent_002",
        amount=1200,
        merchant_type="food_delivery",
        payment_method="card",
        failure_reason="expired_card",
        attempt_number=1,
        customer_transaction_count=20,
    )

    assert result["transaction_id"] == "txn_agent_002"


def test_agent_handles_human_approval():

    agent = RecoveryAgent()

    result = agent.process_payment(
        transaction_id="txn_agent_003",
        amount=8000,
        merchant_type="ecommerce",
        payment_method="card",
        failure_reason="bank_declined",
        attempt_number=1,
        customer_transaction_count=30,
    )

    assert result["requires_human_approval"] is True
    assert result["status"] == "awaiting_human_approval"