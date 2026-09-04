from typing import Dict


def retry_payment(
    transaction_id: str,
) -> Dict:

    return {
        "success": True,
        "tool": "retry_payment",
        "transaction_id": transaction_id,
        "status": "retry_scheduled",
        "message": (
            "Payment retry has been scheduled."
        ),
    }


def send_payment_link(
    transaction_id: str,
) -> Dict:

    return {
        "success": True,
        "tool": "send_payment_link",
        "transaction_id": transaction_id,
        "status": "payment_link_generated",
        "message": (
            "A new payment link has been generated."
        ),
    }


def request_new_payment_method(
    transaction_id: str,
) -> Dict:

    return {
        "success": True,
        "tool": "request_new_payment_method",
        "transaction_id": transaction_id,
        "status": "customer_action_required",
        "message": (
            "Customer has been prompted to provide "
            "a new payment method."
        ),
    }


def wait_and_retry(
    transaction_id: str,
) -> Dict:

    return {
        "success": True,
        "tool": "wait_and_retry",
        "transaction_id": transaction_id,
        "status": "retry_scheduled_later",
        "message": (
            "Payment retry has been scheduled "
            "for a later time."
        ),
    }


def no_action(
    transaction_id: str,
) -> Dict:

    return {
        "success": True,
        "tool": "no_action",
        "transaction_id": transaction_id,
        "status": "no_action",
        "message": (
            "No automated recovery action was taken."
        ),
    }