import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DATA_PATH = "data/raw/payment_transactions.csv"
MODEL_PATH = "models/recovery_model.joblib"


def main():

    # --------------------------------------------------
    # Load data
    # --------------------------------------------------

    df = pd.read_csv(DATA_PATH)

    # Only failed payments are relevant
    df = df[
        df["payment_status"] == "failed"
    ].copy()

    # --------------------------------------------------
    # Features
    # --------------------------------------------------

    features = [
        "amount",
        "merchant_type",
        "payment_method",
        "failure_reason",
        "attempt_number",
        "customer_transaction_count",
    ]

    target = "recovered"

    X = df[features]
    y = df[target].astype(int)

    # --------------------------------------------------
    # Feature types
    # --------------------------------------------------

    numeric_features = [
        "amount",
        "attempt_number",
        "customer_transaction_count",
    ]

    categorical_features = [
        "merchant_type",
        "payment_method",
        "failure_reason",
    ]

    # --------------------------------------------------
    # Preprocessing
    # --------------------------------------------------

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_features,
            ),
        ],
        remainder="passthrough",
    )

    # --------------------------------------------------
    # Model
    # --------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_leaf=5,
        random_state=42,
        class_weight="balanced",
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                model,
            ),
        ]
    )

    # --------------------------------------------------
    # Train/test split
    # --------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # --------------------------------------------------
    # Train
    # --------------------------------------------------

    print("Training recovery prediction model...")

    pipeline.fit(
        X_train,
        y_train,
    )

    # --------------------------------------------------
    # Predictions
    # --------------------------------------------------

    predictions = pipeline.predict(X_test)

    probabilities = pipeline.predict_proba(
        X_test
    )[:, 1]

    # --------------------------------------------------
    # Evaluation
    # --------------------------------------------------

    print("\nClassification Report")
    print(
        classification_report(
            y_test,
            predictions,
        )
    )

    print("\nConfusion Matrix")
    print(
        confusion_matrix(
            y_test,
            predictions,
        )
    )

    auc = roc_auc_score(
        y_test,
        probabilities,
    )

    print(
        f"\nROC-AUC: {auc:.4f}"
    )

    # --------------------------------------------------
    # Save model
    # --------------------------------------------------

    joblib.dump(
        pipeline,
        MODEL_PATH,
    )

    print(
        f"\nModel saved to: {MODEL_PATH}"
    )


if __name__ == "__main__":
    main()