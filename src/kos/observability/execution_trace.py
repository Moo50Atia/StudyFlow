"""
Full Execution Trace & Telemetry Subsystem
===========================================
Emits exportable end-to-end Execution Trace payloads (TRACE-V1) and tracks query token costs.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
import time
import uuid


class ExecutionTraceStep(BaseModel):
    step_name: str
    status: str = "SUCCESS"
    latency_ms: int
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExecutionTrace(BaseModel):
    trace_id: str = Field(default_factory=lambda: f"trace_{uuid.uuid4().hex[:8]}")
    timestamp: float = Field(default_factory=time.time)
    total_latency_ms: int = 0
    steps: List[ExecutionTraceStep] = Field(default_factory=list)

    def add_step(self, step_name: str, latency_ms: int, metadata: Dict[str, Any] = None) -> None:
        self.steps.append(
            ExecutionTraceStep(step_name=step_name, latency_ms=latency_ms, metadata=metadata or {})
        )
        self.total_latency_ms += latency_ms


class CostTracker:
    """Tracks token consumption and USD expenditure per query."""

    @staticmethod
    def calculate_cost(input_tokens: int, output_tokens: int) -> float:
        input_cost = (input_tokens / 1000) * 0.00125
        output_cost = (output_tokens / 1000) * 0.00500
        return round(input_cost + output_cost, 6)
