import json
from datetime import datetime
from pathlib import Path
from typing import Dict


class AuditLogger:

    def __init__(self):
        self.log_directory = Path("logs")
        self.log_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.log_file = (
            self.log_directory / "recovery_audit.jsonl"
        )

    def log(
        self,
        transaction_data: Dict,
        recovery_probability: float,
        decision: Dict,
        ai_reasoning: Dict,
        agent_execution: Dict,
    ) -> Dict:

        audit_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "transaction": transaction_data,
            "recovery_probability":
                round(recovery_probability, 4),
            "decision": decision,
            "ai_reasoning": ai_reasoning,
            "agent_execution": agent_execution,
        }

        with open(
            self.log_file,
            "a",
            encoding="utf-8",
        ) as file:

            file.write(
                json.dumps(audit_record)
                + "\n"
            )

        return {
            "logged": True,
            "log_file": str(self.log_file),
            "timestamp":
                audit_record["timestamp"],
        }