import json
from pathlib import Path

import pandas as pd
import requests
import streamlit as st


# ---------------------------------------------
# Page configuration
# ---------------------------------------------

st.set_page_config(
    page_title="RecoverIQ",
    page_icon="💳",
    layout="wide",
)


# ---------------------------------------------
# Configuration
# ---------------------------------------------

API_URL = "http://127.0.0.1:8000"


# ---------------------------------------------
# Header
# ---------------------------------------------

st.title("RecoverIQ")
st.caption(
    "AI-powered payment recovery orchestration engine"
)

st.divider()


# ---------------------------------------------
# Sidebar
# ---------------------------------------------

st.sidebar.header("Transaction")

amount = st.sidebar.number_input(
    "Amount (INR)",
    min_value=1.0,
    value=1500.0,
    step=100.0,
)

merchant_type = st.sidebar.selectbox(
    "Merchant Type",
    [
        "ecommerce",
        "food_delivery",
        "education",
        "saas",
    ],
)

payment_method = st.sidebar.selectbox(
    "Payment Method",
    [
        "upi",
        "card",
        "wallet",
        "netbanking",
    ],
)

failure_reason = st.sidebar.selectbox(
    "Failure Reason",
    [
        "insufficient_funds",
        "expired_card",
        "authentication_failed",
        "network_timeout",
        "technical_error",
        "bank_declined",
        "limit_exceeded",
    ],
)

attempt_number = st.sidebar.number_input(
    "Attempt Number",
    min_value=1,
    max_value=10,
    value=1,
)

customer_transaction_count = st.sidebar.number_input(
    "Customer Transaction Count",
    min_value=0,
    value=35,
)

predict_button = st.sidebar.button(
    "Analyze Recovery",
    type="primary",
)


# ---------------------------------------------
# Dashboard metrics
# ---------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Transaction Amount",
    f"₹{amount:,.2f}",
)

col2.metric(
    "Failure Reason",
    failure_reason.replace("_", " ").title(),
)

col3.metric(
    "Attempt",
    attempt_number,
)

col4.metric(
    "Customer Transactions",
    customer_transaction_count,
)


st.divider()


# ---------------------------------------------
# API prediction
# ---------------------------------------------

if predict_button:

    payload = {
        "amount": amount,
        "merchant_type": merchant_type,
        "payment_method": payment_method,
        "failure_reason": failure_reason,
        "attempt_number": attempt_number,
        "customer_transaction_count":
            customer_transaction_count,
    }

    try:

        with st.spinner(
            "Running RecoverIQ decision pipeline..."
        ):

            response = requests.post(
                f"{API_URL}/predict/recovery",
                json=payload,
                timeout=120,
            )

        if response.status_code != 200:

            st.error(
                f"API Error: {response.status_code}"
            )

        else:

            result = response.json()

            st.success(
                "Recovery decision generated successfully."
            )

            # -----------------------------------------
            # Main decision metrics
            # -----------------------------------------

            st.subheader("Recovery Decision")

            c1, c2, c3 = st.columns(3)

            probability = result.get(
                "recovery_probability",
                0,
            )

            c1.metric(
                "Recovery Probability",
                f"{probability * 100:.1f}%",
            )

            c2.metric(
                "Priority",
                result.get(
                    "priority",
                    "unknown",
                ).upper(),
            )

            c3.metric(
                "Recommended Action",
                result.get(
                    "recommended_action",
                    "unknown",
                ).replace("_", " ").title(),
            )


            # -----------------------------------------
            # Decision explanation
            # -----------------------------------------

            st.subheader("Decision Explanation")

            st.info(
                result.get(
                    "reason",
                    "No explanation available.",
                )
            )


            # -----------------------------------------
            # AI reasoning
            # -----------------------------------------

            st.subheader("AI Reasoning")

            ai_reasoning = result.get(
                "ai_reasoning",
                {},
            )

            if ai_reasoning:

                st.write(
                    "**Assessment**"
                )

                st.write(
                    ai_reasoning.get(
                        "assessment",
                        "Not available",
                    )
                )

                col_a, col_b = st.columns(2)

                with col_a:

                    st.write(
                        "**Key Signals**"
                    )

                    signals = ai_reasoning.get(
                        "key_signals",
                        [],
                    )

                    for signal in signals:
                        st.write(
                            f"• {signal}"
                        )

                with col_b:

                    st.write(
                        "**Risk Flags**"
                    )

                    risks = ai_reasoning.get(
                        "risk_flags",
                        [],
                    )

                    if risks:

                        for risk in risks:
                            st.warning(risk)

                    else:

                        st.success(
                            "No major risk flags."
                        )

                st.write(
                    "**Action Rationale**"
                )

                st.write(
                    ai_reasoning.get(
                        "action_rationale",
                        "Not available",
                    )
                )

                confidence = ai_reasoning.get(
                    "confidence",
                    0,
                )

                st.progress(
                    min(
                        max(float(confidence), 0),
                        1,
                    )
                )

                st.caption(
                    f"AI confidence: "
                    f"{float(confidence) * 100:.1f}%"
                )


            # -----------------------------------------
            # Agent execution
            # -----------------------------------------

            st.subheader(
                "Recovery Agent"
            )

            agent = result.get(
                "agent_execution",
                {},
            )

            agent_col1, agent_col2, agent_col3 = (
                st.columns(3)
            )

            agent_col1.metric(
                "Status",
                agent.get(
                    "status",
                    "unknown",
                ),
            )

            agent_col2.metric(
                "Executed",
                str(
                    agent.get(
                        "executed",
                        False,
                    )
                ),
            )

            verification = agent.get(
                "verification",
                {},
            )

            agent_col3.metric(
                "Verified",
                str(
                    verification.get(
                        "verified",
                        False,
                    )
                ),
            )

            st.write(
                agent.get(
                    "message",
                    "No agent message.",
                )
            )


            # -----------------------------------------
            # Audit information
            # -----------------------------------------

            st.subheader(
                "Audit Record"
            )

            audit = result.get(
                "audit",
                {},
            )

            if audit:

                st.write(
                    f"**Logged:** "
                    f"{audit.get('logged', False)}"
                )

                st.write(
                    f"**Timestamp:** "
                    f"{audit.get('timestamp', 'N/A')}"
                )

                st.write(
                    f"**Log File:** "
                    f"{audit.get('log_file', 'N/A')}"
                )

            with st.expander(
                "View Complete API Response"
            ):

                st.json(result)


    except requests.exceptions.ConnectionError:

        st.error(
            "RecoverIQ API is not running. "
            "Start FastAPI first."
        )

        st.code(
            "uvicorn backend.main:app --reload"
        )


    except requests.exceptions.Timeout:

        st.error(
            "The AI reasoning request timed out. "
            "Make sure Ollama is running."
        )


    except Exception as error:

        st.error(
            f"Unexpected error: {error}"
        )


else:

    st.info(
        "Configure the failed transaction in the "
        "sidebar and click **Analyze Recovery**."
    )


# ---------------------------------------------
# Audit log viewer
# ---------------------------------------------

st.divider()

st.subheader(
    "Recent Recovery Audit Logs"
)

log_file = Path(
    "logs/recovery_audit.jsonl"
)

if log_file.exists():

    records = []

    with open(
        log_file,
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:

            try:
                records.append(
                    json.loads(line)
                )

            except json.JSONDecodeError:
                continue

    if records:

        rows = []

        for record in records[-10:]:

            transaction = record.get(
                "transaction",
                {},
            )

            decision = record.get(
                "decision",
                {},
            )

            rows.append(
                {
                    "Timestamp":
                        record.get(
                            "timestamp",
                            "",
                        ),
                    "Amount":
                        transaction.get(
                            "amount",
                            0,
                        ),
                    "Failure":
                        transaction.get(
                            "failure_reason",
                            "",
                        ),
                    "Probability":
                        record.get(
                            "recovery_probability",
                            0,
                        ),
                    "Action":
                        decision.get(
                            "action",
                            "",
                        ),
                }
            )

        dataframe = pd.DataFrame(rows)

        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No audit records available yet."
        )

else:

    st.info(
        "No audit log found. Run a recovery prediction first."
    )