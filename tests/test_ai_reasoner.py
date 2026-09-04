from backend.services.ai_reasoner import AIReasoner


def main():

    reasoner = AIReasoner()

    result = reasoner.analyze(
        amount=1500,
        merchant_type="ecommerce",
        payment_method="upi",
        failure_reason="insufficient_funds",
        attempt_number=1,
        customer_transaction_count=35,
        recovery_probability=0.826,
        recommended_action="wait_and_retry",
    )

    print("\nAI REASONING RESULT:")
    print(result)


if __name__ == "__main__":
    main()