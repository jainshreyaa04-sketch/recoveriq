from fastapi import FastAPI
from pydantic import BaseModel, Field

from backend.services.recovery_predictor import (
    RecoveryPredictor,
)

from backend.services.decision_engine import (
    decide_recovery_action,
)

from backend.services.ai_reasoner import AIReasoner

from backend.services.recovery_agent import RecoveryAgent

from backend.services.audit_logger import AuditLogger

app = FastAPI(
    title="RecoverIQ API",
    description=(
        "AI-powered revenue recovery "
        "orchestration engine"
    ),
    version="0.4.0",
)


# ---------------------------------------------
# Initialize services
# ---------------------------------------------

predictor = RecoveryPredictor()

ai_reasoner = AIReasoner()

recovery_agent = RecoveryAgent()

audit_logger = AuditLogger()
# ---------------------------------------------
# Request model
# ---------------------------------------------

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


# ---------------------------------------------
# Root endpoint
# ---------------------------------------------

@app.get("/")
def root():

    return {
        "project": "RecoverIQ",
        "status": "running",
        "version": "0.4.0",
    }


# ---------------------------------------------
# Health endpoint
# ---------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model": "loaded",
        "decision_engine": "loaded",
        "ai_reasoner": "loaded",
        "recovery_agent": "loaded",
    }


# ---------------------------------------------
# Recovery prediction endpoint
# ---------------------------------------------

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
    # STEP 4 — AI reasoning
    # ---------------------------------------------

    ai_analysis = ai_reasoner.analyze(
        amount=request.amount,
        merchant_type=request.merchant_type,
        payment_method=request.payment_method,
        failure_reason=request.failure_reason,
        attempt_number=request.attempt_number,
        customer_transaction_count=
            request.customer_transaction_count,
        recovery_probability=probability,
        recommended_action=decision["action"],
    )


    # ---------------------------------------------
    # STEP 5 — Recovery Agent
    # ---------------------------------------------

    agent_result = recovery_agent.execute(
        action=decision["action"],
        requires_human_approval=
            decision["requires_human_approval"],
        transaction_data={
            "amount": request.amount,
            "merchant_type": request.merchant_type,
            "payment_method": request.payment_method,
            "failure_reason": request.failure_reason,
            "attempt_number": request.attempt_number,
            "customer_transaction_count":
                request.customer_transaction_count,
        },
    )
       # ---------------------------------------------
    # STEP 6 — Audit logging
    # ---------------------------------------------

    audit_result = audit_logger.log(
        transaction_data={
            "amount": request.amount,
            "merchant_type": request.merchant_type,
            "payment_method": request.payment_method,
            "failure_reason": request.failure_reason,
            "attempt_number": request.attempt_number,
            "customer_transaction_count":
                request.customer_transaction_count,
        },
        recovery_probability=probability,
        decision=decision,
        ai_reasoning=ai_analysis,
        agent_execution=agent_result,
    )

        # ---------------------------------------------
    # STEP 7 — Final response
    # ---------------------------------------------

    return {
        "recovery_probability": round(
            probability,
            4,
        ),
        "priority": priority,
        "recommended_action":
            decision["action"],
        "reason":
            decision["reason"],
        "requires_human_approval":
            decision["requires_human_approval"],
        "decision_status":
            "decision_generated",
        "ai_reasoning":
            ai_analysis,
        "agent_execution":
            agent_result,
        "audit":
            audit_result,
    }