import json
import ollama


class AIReasoner:

    def __init__(self):
        self.model = "llama3.2"

    def analyze(
        self,
        amount,
        merchant_type,
        payment_method,
        failure_reason,
        attempt_number,
        customer_transaction_count,
        recovery_probability=None,
        recommended_action=None
    ):
        transaction_data = {
            "amount": amount,
            "merchant_type": merchant_type,
            "payment_method": payment_method,
            "failure_reason": failure_reason,
            "attempt_number": attempt_number,
            "customer_transaction_count": customer_transaction_count
        }

        prompt = f"""
You are the AI reasoning layer of RecoverIQ,
a fintech payment recovery system.

Analyze this failed payment.

Transaction:
{json.dumps(transaction_data, indent=2)}

Recovery probability:
{recovery_probability}

Recommended action:
{recommended_action}

Return ONLY valid JSON:

{{
    "assessment": "short assessment",
    "key_signals": ["signal 1", "signal 2"],
    "action_rationale": "why this action makes sense",
    "risk_flags": ["risk 1"],
    "confidence": 0.0
}}

Rules:
- Do not invent transaction data.
- Do not claim access to Razorpay systems.
- Do not execute payments.
- Do not change the recommended action.
- Confidence must be between 0 and 1.
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response["message"]["content"]

        try:
            return json.loads(content)

        except json.JSONDecodeError:
            return {
                "assessment": content,
                "key_signals": [],
                "action_rationale": "AI response was not returned as structured JSON.",
                "risk_flags": ["unstructured_ai_response"],
                "confidence": 0.0
            }