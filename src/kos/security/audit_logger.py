"""
KOS Security Audit Logger
=========================
Records append-only security logs for privileged store mutations and authorization checks.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
import time


class SecurityAuditEvent(BaseModel):
    event_id: str
    user_id: str
    action: str
    resource_id: str
    status: str = Field(default="SUCCESS")
    timestamp: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SecurityAuditLogger:
    """Manages append-only security audit events."""

    def __init__(self):
        self._audit_events: list = []

    def log_event(self, event: SecurityAuditEvent) -> None:
        self._audit_events.append(event)

    def get_events(self) -> list:
        return list(self._audit_events)
