from typing import Dict


def decide_recovery_action(
    recovery_probability: float,
    failure_reason: str,
    attempt_number: int,
    amount: float,
    customer_transaction_count: int,
) -> Dict:

    # ---------------------------------------------
    # Safety rule: very low recovery probability
    # ---------------------------------------------

    if recovery_probability < 0.30:
        return {
            "action": "no_action",
            "priority": "low",
            "reason": (
                "Low predicted recovery probability. "
                "Automated recovery is not recommended."
            ),
            "requires_human_approval": False,
        }

    # ---------------------------------------------
    # Expired card
    # ---------------------------------------------

    if failure_reason == "expired_card":
        return {
            "action": "request_new_payment_method",
            "priority": "medium",
            "reason": (
                "The payment method appears expired. "
                "Requesting a new payment method is more "
                "appropriate than repeatedly retrying."
            ),
            "requires_human_approval": False,
        }

    # ---------------------------------------------
    # Authentication failure
    # ---------------------------------------------

    if failure_reason == "authentication_failed":
        return {
            "action": "request_new_payment_method",
            "priority": "medium",
            "reason": (
                "Authentication failed. A different "
                "payment method may provide a safer "
                "recovery path."
            ),
            "requires_human_approval": False,
        }

    # ---------------------------------------------
    # Insufficient funds
    # ---------------------------------------------

    if failure_reason == "insufficient_funds":

        if attempt_number >= 3:
            return {
                "action": "send_payment_link",
                "priority": "high",
                "reason": (
                    "Multiple attempts have already failed. "
                    "A payment link avoids repeated automatic "
                    "retries."
                ),
                "requires_human_approval": False,
            }

        return {
            "action": "wait_and_retry",
            "priority": "high",
            "reason": (
                "Insufficient funds may be temporary. "
                "Waiting before another attempt reduces "
                "unnecessary retries."
            ),
            "requires_human_approval": False,
        }

    # ---------------------------------------------
    # Technical / network problems
    # ---------------------------------------------

    if failure_reason in [
        "technical_error",
        "network_timeout",
    ]:

        if attempt_number >= 3:
            return {
                "action": "send_payment_link",
                "priority": "medium",
                "reason": (
                    "Repeated technical failures detected. "
                    "Avoid additional automatic retries."
                ),
                "requires_human_approval": False,
            }

        return {
            "action": "retry_payment",
            "priority": "high",
            "reason": (
                "The failure appears temporary and the "
                "payment has not exceeded the retry threshold."
            ),
            "requires_human_approval": False,
        }

    # ---------------------------------------------
    # Bank decline / limit exceeded
    # ---------------------------------------------

    if failure_reason in [
        "bank_declined",
        "limit_exceeded",
    ]:

        if amount >= 5000:
            return {
                "action": "send_payment_link",
                "priority": "high",
                "reason": (
                    "Higher-value payment combined with "
                    "bank/limit failure should avoid repeated "
                    "automatic retries."
                ),
                "requires_human_approval": True,
            }

        return {
            "action": "request_new_payment_method",
            "priority": "medium",
            "reason": (
                "Changing the payment method is preferable "
                "to repeatedly retrying the same failed attempt."
            ),
            "requires_human_approval": False,
        }

    # ---------------------------------------------
    # Default fallback
    # ---------------------------------------------

    return {
        "action": "send_payment_link",
        "priority": "medium",
        "reason": (
            "Fallback recovery strategy selected because "
            "no specialized rule matched the failure."
        ),
        "requires_human_approval": False,
    }