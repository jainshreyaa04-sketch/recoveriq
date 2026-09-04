from typing import Dict

from agents.tools.payment_tools import (
    retry_payment,
    send_payment_link,
    request_new_payment_method,
    wait_and_retry,
    no_action,
)


TOOLS = {
    "retry_payment": retry_payment,
    "send_payment_link": send_payment_link,
    "request_new_payment_method":
        request_new_payment_method,
    "wait_and_retry": wait_and_retry,
    "no_action": no_action,
}


def execute_tool(
    action: str,
    transaction_id: str,
    requires_human_approval: bool = False,
) -> Dict:

    # ------------------------------------------------
    # Safety guardrail
    # ------------------------------------------------

    if requires_human_approval:

        return {
            "success": False,
            "status": "human_approval_required",
            "action": action,
            "transaction_id": transaction_id,
            "message": (
                "Action blocked until human approval "
                "is provided."
            ),
        }

    # ------------------------------------------------
    # Check whether tool exists
    # ------------------------------------------------

    if action not in TOOLS:

        return {
            "success": False,
            "status": "unknown_action",
            "action": action,
            "transaction_id": transaction_id,
        }

    # ------------------------------------------------
    # Execute tool
    # ------------------------------------------------

    tool = TOOLS[action]

    result = tool(
        transaction_id
    )

    return result