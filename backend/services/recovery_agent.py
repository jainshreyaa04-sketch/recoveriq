from typing import Dict


class RecoveryAgent:
    """
    RecoverIQ recovery orchestration agent.

    The agent coordinates recovery actions but does not
    override the deterministic decision engine.
    """

    def __init__(self):
        self.tools = {
            "retry_payment": self.retry_payment,
            "wait_and_retry": self.wait_and_retry,
            "send_payment_link": self.send_payment_link,
            "request_new_payment_method":
                self.request_new_payment_method,
            "no_action": self.no_action,
        }

    def execute(
        self,
        action: str,
        requires_human_approval: bool,
        transaction_data: Dict,
    ) -> Dict:

        # ---------------------------------------------
        # SAFETY GATE
        # ---------------------------------------------

        if requires_human_approval:
            return {
                "status": "pending_human_approval",
                "action": action,
                "executed": False,
                "message": (
                    "Human approval is required before "
                    "this recovery action can be executed."
                ),
            }

        # ---------------------------------------------
        # TOOL VALIDATION
        # ---------------------------------------------

        if action not in self.tools:
            return {
                "status": "failed",
                "action": action,
                "executed": False,
                "message": (
                    "Unknown recovery action. "
                    "No action was executed."
                ),
            }

        # ---------------------------------------------
        # TOOL EXECUTION
        # ---------------------------------------------

        result = self.tools[action](transaction_data)

        # ---------------------------------------------
        # VERIFICATION
        # ---------------------------------------------

        verification = self.verify_action(
            action=action,
            result=result,
        )

        return {
            "status": verification["status"],
            "action": action,
            "executed": result["executed"],
            "message": result["message"],
            "verification": verification,
        }

    # ---------------------------------------------
    # RECOVERY TOOLS
    # ---------------------------------------------

    def retry_payment(
        self,
        transaction_data: Dict,
    ) -> Dict:

        return {
            "executed": True,
            "tool": "retry_payment",
            "message": (
                "Simulated payment retry scheduled."
            ),
        }

    def wait_and_retry(
        self,
        transaction_data: Dict,
    ) -> Dict:

        return {
            "executed": True,
            "tool": "wait_and_retry",
            "message": (
                "Simulated delayed payment retry scheduled."
            ),
        }

    def send_payment_link(
        self,
        transaction_data: Dict,
    ) -> Dict:

        return {
            "executed": True,
            "tool": "send_payment_link",
            "message": (
                "Simulated payment link generated "
                "for the customer."
            ),
        }

    def request_new_payment_method(
        self,
        transaction_data: Dict,
    ) -> Dict:

        return {
            "executed": True,
            "tool": "request_new_payment_method",
            "message": (
                "Simulated request for a new payment "
                "method created."
            ),
        }

    def no_action(
        self,
        transaction_data: Dict,
    ) -> Dict:

        return {
            "executed": False,
            "tool": "no_action",
            "message": (
                "No recovery action was executed."
            ),
        }

    # ---------------------------------------------
    # VERIFICATION
    # ---------------------------------------------

    def verify_action(
        self,
        action: str,
        result: Dict,
    ) -> Dict:

        if action == "no_action":
            return {
                "status": "verified",
                "verified": True,
                "payment_status": "not_attempted",
                "reason": (
                    "No recovery action was expected."
                ),
            }

        if result.get("executed") is True:
            return {
                "status": "verified",
                "verified": True,
                "payment_status": "action_scheduled",
                "reason": (
                    "The recovery action was successfully "
                    "scheduled in the simulation environment. "
                    "Payment success is not assumed."
                ),
            }

        return {
            "status": "failed",
            "verified": False,
            "payment_status": "not_executed",
            "reason": (
                "The recovery action was not executed."
            ),
        }