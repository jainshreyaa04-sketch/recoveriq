import pandas as pd


FILE_PATH = "data/raw/payment_transactions.csv"


def main():

    df = pd.read_csv(FILE_PATH)

    failed = df[
        df["payment_status"] == "failed"
    ].copy()

    print("=" * 60)
    print("RecoverIQ — Exploratory Data Analysis")
    print("=" * 60)

    print("\n1. Dataset")
    print(f"Total transactions: {len(df)}")
    print(f"Failed payments: {len(failed)}")

    print("\n2. Recovery rate")
    recovery_rate = failed["recovered"].mean() * 100
    print(f"{recovery_rate:.2f}%")

    print("\n3. Recovery rate by failure reason")
    print(
        failed.groupby("failure_reason")["recovered"]
        .mean()
        .sort_values(ascending=False)
        .mul(100)
        .round(2)
    )

    print("\n4. Recovery rate by payment method")
    print(
        failed.groupby("payment_method")["recovered"]
        .mean()
        .sort_values(ascending=False)
        .mul(100)
        .round(2)
    )

    print("\n5. Recovery rate by recovery action")
    print(
        failed.groupby("recovery_action")["recovered"]
        .mean()
        .sort_values(ascending=False)
        .mul(100)
        .round(2)
    )

    print("\n6. Recovery rate by attempt number")
    print(
        failed.groupby("attempt_number")["recovered"]
        .mean()
        .sort_index()
        .mul(100)
        .round(2)
    )

    print("\n7. Average transaction amount")
    print(
        failed.groupby("recovered")["amount"]
        .mean()
        .round(2)
    )

    print("\n8. Average customer transaction count")
    print(
        failed.groupby("recovered")[
            "customer_transaction_count"
        ]
        .mean()
        .round(2)
    )

    print("\n" + "=" * 60)
    print("EDA complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()