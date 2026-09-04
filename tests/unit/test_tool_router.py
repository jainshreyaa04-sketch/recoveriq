from agents.tools.tool_router import execute_tool


def test_retry_payment():

    result = execute_tool(
        action="retry_payment",
        transaction_id="txn_test_001",
    )

    assert result["success"] is True
    assert result["status"] == "retry_scheduled"


def test_payment_link():

    result = execute_tool(
        action="send_payment_link",
        transaction_id="txn_test_002",
    )

    assert result["success"] is True
    assert result["status"] == "payment_link_generated"


def test_human_approval():

    result = execute_tool(
        action="send_payment_link",
        transaction_id="txn_test_003",
        requires_human_approval=True,
    )

    assert result["success"] is False
    assert (
        result["status"]
        == "human_approval_required"
    )


def test_unknown_action():

    result = execute_tool(
        action="invalid_action",
        transaction_id="txn_test_004",
    )

    assert result["success"] is False
    assert result["status"] == "unknown_action"