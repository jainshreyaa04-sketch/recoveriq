import pandas as pd


FILE_PATH = "data/raw/payment_transactions.csv"


def main():

    df = pd.read_csv(FILE_PATH)

    print("=" * 60)
    print("RecoverIQ Dataset Validation")
    print("=" * 60)

    # --------------------------------------------------
    # Basic information
    # --------------------------------------------------

    print("\n1. Dataset shape")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\n2. Columns")
    print(list(df.columns))

    # --------------------------------------------------
    # Missing values
    # --------------------------------------------------

    print("\n3. Missing values")
    print(df.isnull().sum())

    # --------------------------------------------------
    # Duplicate transactions
    # --------------------------------------------------

    print("\n4. Duplicate transaction IDs")
    duplicates = df["transaction_id"].duplicated().sum()
    print(duplicates)

    # --------------------------------------------------
    # Payment status
    # --------------------------------------------------

    print("\n5. Payment status")
    print(df["payment_status"].value_counts())

    # --------------------------------------------------
    # Failed payments
    # --------------------------------------------------

    failed = df[
        df["payment_status"] == "failed"
    ].copy()

    print("\n6. Failed payments")
    print(f"Failed transactions: {len(failed)}")

    # --------------------------------------------------
    # Failure reasons
    # --------------------------------------------------

    print("\n7. Failure reasons")
    print(
        failed["failure_reason"]
        .value_counts()
    )

    # --------------------------------------------------
    # Recovery actions
    # --------------------------------------------------

    print("\n8. Recovery actions")
    print(
        failed["recovery_action"]
        .value_counts()
    )

    # --------------------------------------------------
    # Recovery outcome
    # --------------------------------------------------

    print("\n9. Recovery outcome")
    print(
        failed["recovered"]
        .value_counts()
    )

    # --------------------------------------------------
    # Recovery rate
    # --------------------------------------------------

    recovery_rate = (
        failed["recovered"]
        .mean()
        * 100
    )

    print(
        f"\n10. Overall recovery rate: "
        f"{recovery_rate:.2f}%"
    )

    # --------------------------------------------------
    # Successful payment validation
    # --------------------------------------------------

    successful = df[
        df["payment_status"] == "successful"
    ]

    print(
        "\n11. Successful payments with "
        "failure reasons:"
    )

    print(
        successful["failure_reason"]
        .notna()
        .sum()
    )

    print(
        "\n12. Successful payments with "
        "recovery actions:"
    )

    print(
        (
            successful["recovery_action"]
            != "none"
        ).sum()
    )

    # --------------------------------------------------
    # Target distribution
    # --------------------------------------------------

    print("\n13. Target distribution")
    print(
        failed["recovered"]
        .value_counts(normalize=True)
        * 100
    )

    print("\n" + "=" * 60)
    print("Validation complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()