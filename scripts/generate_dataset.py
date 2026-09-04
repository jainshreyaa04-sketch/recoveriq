import os
import random
import uuid
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

NUM_TRANSACTIONS = 20000

OUTPUT_DIR = "data/raw"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "payment_transactions.csv"
)


# ---------------------------------------------------------
# Domain values
# ---------------------------------------------------------

MERCHANT_TYPES = [
    "ecommerce",
    "saas",
    "education",
    "travel",
    "food_delivery",
    "marketplace",
]

PAYMENT_METHODS = [
    "card",
    "upi",
    "netbanking",
    "wallet",
]

FAILURE_REASONS = [
    "insufficient_funds",
    "bank_declined",
    "technical_error",
    "authentication_failed",
    "network_timeout",
    "limit_exceeded",
    "expired_card",
]

RECOVERY_ACTIONS = [
    "retry_payment",
    "send_payment_link",
    "request_new_payment_method",
    "wait_and_retry",
    "no_action",
]


# ---------------------------------------------------------
# Base recovery probabilities
# ---------------------------------------------------------

BASE_RECOVERY_PROBABILITY = {
    "insufficient_funds": 0.62,
    "bank_declined": 0.35,
    "technical_error": 0.72,
    "authentication_failed": 0.30,
    "network_timeout": 0.76,
    "limit_exceeded": 0.25,
    "expired_card": 0.18,
}


# ---------------------------------------------------------
# Generate one transaction
# ---------------------------------------------------------

def generate_transaction():

    amount = round(
        float(
            np.random.lognormal(
                mean=7.0,
                sigma=0.8
            )
        ),
        2
    )

    merchant_type = random.choice(MERCHANT_TYPES)

    payment_method = random.choice(PAYMENT_METHODS)

    customer_transaction_count = random.randint(1, 100)

    attempt_number = random.randint(1, 4)

    payment_status = np.random.choice(
        ["successful", "failed"],
        p=[0.70, 0.30]
    )

    # -----------------------------------------------------
    # Successful payment
    # -----------------------------------------------------

    if payment_status == "successful":

        return {
            "transaction_id": str(uuid.uuid4()),
            "merchant_id": f"merchant_{random.randint(1, 500):04d}",
            "merchant_type": merchant_type,
            "amount": amount,
            "currency": "INR",
            "payment_method": payment_method,
            "payment_status": "successful",
            "failure_reason": None,
            "recovery_action": "none",
            "recovered": False,
            "attempt_number": attempt_number,
            "customer_transaction_count": customer_transaction_count,
            "created_at": (
                datetime.now()
                - timedelta(
                    days=random.randint(0, 180),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                )
            ).isoformat(),
        }

    # -----------------------------------------------------
    # Failed payment
    # -----------------------------------------------------

    failure_reason = random.choice(
        FAILURE_REASONS
    )

    # Base probability
    recovery_probability = BASE_RECOVERY_PROBABILITY[
        failure_reason
    ]

    # -----------------------------------------------------
    # Customer history effect
    # -----------------------------------------------------

    if customer_transaction_count >= 50:
        recovery_probability += 0.10

    elif customer_transaction_count >= 20:
        recovery_probability += 0.05

    elif customer_transaction_count <= 3:
        recovery_probability -= 0.08

    # -----------------------------------------------------
    # Attempt number effect
    # -----------------------------------------------------

    if attempt_number == 1:
        recovery_probability += 0.08

    elif attempt_number >= 3:
        recovery_probability -= 0.12

    # -----------------------------------------------------
    # Amount effect
    # -----------------------------------------------------

    if amount > 5000:
        recovery_probability -= 0.10

    elif amount < 500:
        recovery_probability += 0.04

    # -----------------------------------------------------
    # Payment method effect
    # -----------------------------------------------------

    if payment_method == "upi":
        recovery_probability += 0.04

    elif payment_method == "wallet":
        recovery_probability += 0.02

    # -----------------------------------------------------
    # Merchant effect
    # -----------------------------------------------------

    if merchant_type in ["ecommerce", "food_delivery"]:
        recovery_probability += 0.03

    elif merchant_type == "travel":
        recovery_probability -= 0.04

    # Keep probability within reasonable bounds
    recovery_probability = max(
        0.05,
        min(
            recovery_probability,
            0.95
        )
    )

    # -----------------------------------------------------
    # Choose recovery action based on failure reason
    # -----------------------------------------------------

    if failure_reason == "insufficient_funds":
        recovery_action = random.choice([
            "send_payment_link",
            "wait_and_retry",
            "retry_payment",
        ])

    elif failure_reason == "technical_error":
        recovery_action = random.choice([
            "retry_payment",
            "wait_and_retry",
        ])

    elif failure_reason == "network_timeout":
        recovery_action = random.choice([
            "retry_payment",
            "wait_and_retry",
        ])

    elif failure_reason in [
        "expired_card",
        "authentication_failed",
    ]:
        recovery_action = "request_new_payment_method"

    elif failure_reason == "limit_exceeded":
        recovery_action = random.choice([
            "request_new_payment_method",
            "send_payment_link",
            "no_action",
        ])

    else:
        recovery_action = random.choice(
            RECOVERY_ACTIONS[:-1]
        )

    # -----------------------------------------------------
    # Simulate recovery outcome
    # -----------------------------------------------------

    recovered = (
        np.random.random()
        < recovery_probability
    )

    return {
        "transaction_id": str(uuid.uuid4()),
        "merchant_id": f"merchant_{random.randint(1, 500):04d}",
        "merchant_type": merchant_type,
        "amount": amount,
        "currency": "INR",
        "payment_method": payment_method,
        "payment_status": "failed",
        "failure_reason": failure_reason,
        "recovery_action": recovery_action,
        "recovered": recovered,
        "attempt_number": attempt_number,
        "customer_transaction_count": customer_transaction_count,
        "created_at": (
            datetime.now()
            - timedelta(
                days=random.randint(0, 180),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )
        ).isoformat(),
    }


# ---------------------------------------------------------
# Main dataset generation
# ---------------------------------------------------------

def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    transactions = [
        generate_transaction()
        for _ in range(NUM_TRANSACTIONS)
    ]

    df = pd.DataFrame(
        transactions
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "Dataset generated successfully."
    )

    print(
        f"Records: {len(df)}"
    )

    print(
        f"File: {OUTPUT_FILE}"
    )

    print(
        "\nPayment status distribution:"
    )

    print(
        df["payment_status"]
        .value_counts()
    )

    failed_df = df[
        df["payment_status"] == "failed"
    ]

    print(
        "\nFailed payment recovery distribution:"
    )

    print(
        failed_df["recovered"]
        .value_counts()
    )

    print(
        "\nFailure reasons:"
    )

    print(
        failed_df["failure_reason"]
        .value_counts()
    )

    print(
        "\nRecovery actions:"
    )

    print(
        failed_df["recovery_action"]
        .value_counts()
    )


if __name__ == "__main__":
    main()