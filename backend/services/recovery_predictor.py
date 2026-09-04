import joblib
import pandas as pd


MODEL_PATH = "models/recovery_model.joblib"


class RecoveryPredictor:

    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict_probability(
        self,
        amount: float,
        merchant_type: str,
        payment_method: str,
        failure_reason: str,
        attempt_number: int,
        customer_transaction_count: int,
    ) -> float:

        data = pd.DataFrame(
            [
                {
                    "amount": amount,
                    "merchant_type": merchant_type,
                    "payment_method": payment_method,
                    "failure_reason": failure_reason,
                    "attempt_number": attempt_number,
                    "customer_transaction_count":
                        customer_transaction_count,
                }
            ]
        )

        probability = self.model.predict_proba(
            data
        )[0][1]

        return float(probability)