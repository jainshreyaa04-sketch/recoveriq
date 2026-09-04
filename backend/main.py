from fastapi import FastAPI
from pydantic import BaseModel, Field

from backend.services.recovery_predictor import (
    RecoveryPredictor,
)

from backend.services.decision_engine import (
    decide_recovery_action,
)


app = FastAPI(
    title="RecoverIQ API",
    description=(
        "AI-powered revenue recovery "
        "orchestration engine"
    ),
    version="0.3.0",
)


predictor = RecoveryPredictor()


class RecoveryRequest(BaseModel):

    amount: float = Field(
        gt=0,
        description="Failed payment amount in INR",
    )

    merchant_type: str

    payment_method: str

    failure_reason: str

    attempt_number: int = Field(
        ge=1,
        le=10,
    )

    customer_transaction_count: int = Field(
        ge=0,
    )


@app.get("/")
def root():

    return {
        "project": "RecoverIQ",
        "status": "running",
        "version": "0.3.0",
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model": "loaded",
        "decision_engine": "loaded",
    }


@app.post("/predict/recovery")
def predict_recovery(
    request: RecoveryRequest,
):

    # ---------------------------------------------
    # STEP 1 — ML prediction
    # ---------------------------------------------

    probability = predictor.predict_probability(
        amount=request.amount,
        merchant_type=request.merchant_type,
        payment_method=request.payment_method,
        failure_reason=request.failure_reason,
        attempt_number=request.attempt_number,
        customer_transaction_count=
            request.customer_transaction_count,
    )

    # ---------------------------------------------
    # STEP 2 — Determine priority
    # ---------------------------------------------

    if probability >= 0.70:
        priority = "high"

    elif probability >= 0.40:
        priority = "medium"

    else:
        priority = "low"

    # ---------------------------------------------
    # STEP 3 — Decision engine
    # ---------------------------------------------

    decision = decide_recovery_action(
        recovery_probability=probability,
        failure_reason=request.failure_reason,
        attempt_number=request.attempt_number,
        amount=request.amount,
        customer_transaction_count=
            request.customer_transaction_count,
    )

    # ---------------------------------------------
    # STEP 4 — Return complete decision
    # ---------------------------------------------

    return {
        "recovery_probability": round(
            probability,
            4,
        ),
        "priority": priority,
        "recommended_action": decision["action"],
        "reason": decision["reason"],
        "requires_human_approval":
            decision["requires_human_approval"],
        "decision_status": "decision_generated",
    }