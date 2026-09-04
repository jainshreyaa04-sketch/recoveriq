from typing import Dict

from backend.services.recovery_predictor import (
    RecoveryPredictor,
)

from backend.services.decision_engine import (
    decide_recovery_action,
)

from agents.tools.tool_router import (
    execute_tool,
)


class RecoveryAgent:

    def __init__(self):

        self.predictor = RecoveryPredictor()

    def process_payment(
        self,
        transaction_id: str,
        amount: float,
        merchant_type: str,
        payment_method: str,
        failure_reason: str,
        attempt_number: int,
        customer_transaction_count: int,
    ) -> Dict:

        # ---------------------------------------------
        # STEP 1 — Predict recovery probability
        # ---------------------------------------------

        probability = (
            self.predictor.predict_probability(
                amount=amount,
                merchant_type=merchant_type,
                payment_method=payment_method,
                failure_reason=failure_reason,
                attempt_number=attempt_number,
                customer_transaction_count=
                    customer_transaction_count,
            )
        )

        # ---------------------------------------------
        # STEP 2 — Decide recovery action
        # ---------------------------------------------

        decision = decide_recovery_action(
            recovery_probability=probability,
            failure_reason=failure_reason,
            attempt_number=attempt_number,
            amount=amount,
            customer_transaction_count=
                customer_transaction_count,
        )

        action = decision["action"]

        # ---------------------------------------------
        # STEP 3 — Human approval gate
        # ---------------------------------------------

        if decision["requires_human_approval"]:

            return {
                "transaction_id": transaction_id,
                "recovery_probability":
                    round(probability, 4),
                "action": action,
                "reason": decision["reason"],
                "requires_human_approval": True,
                "status": "awaiting_human_approval",
                "tool_result": None,
            }

        # ---------------------------------------------
        # STEP 4 — Execute controlled tool
        # ---------------------------------------------

        tool_result = execute_tool(
            action=action,
            transaction_id=transaction_id,
            requires_human_approval=False,
        )

        # ---------------------------------------------
        # STEP 5 — Verify tool result
        # ---------------------------------------------

        if tool_result.get("success"):

            status = "action_completed"

        else:

            status = "action_failed"

        # ---------------------------------------------
        # STEP 6 — Return complete agent result
        # ---------------------------------------------

        return {
            "transaction_id": transaction_id,
            "recovery_probability":
                round(probability, 4),
            "action": action,
            "reason": decision["reason"],
            "requires_human_approval":
                decision["requires_human_approval"],
            "status": status,
            "tool_result": tool_result,
        }