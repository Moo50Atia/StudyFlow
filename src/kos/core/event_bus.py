"""
KOS Core Event Bus Subsystem
============================
Provides synchronous and asynchronous event publishing and subscription capabilities
for decoupling platform subsystems and auditing events.
"""

from typing import Dict, List, Callable, Any
from pydantic import BaseModel, Field
import time


class KOSEvent(BaseModel):
    event_id: str
    event_name: str
    timestamp: float = Field(default_factory=time.time)
    payload: Dict[str, Any] = Field(default_factory=dict)


EventHandler = Callable[[KOSEvent], None]


class EventBus:
    """Central Event Bus for handling system-wide event broadcasting."""

    def __init__(self):
        self._listeners: Dict[str, List[EventHandler]] = {}

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """Subscribes a callback handler to a specific event name."""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(handler)

    def publish(self, event: KOSEvent) -> int:
        """Publishes an event to all subscribed listeners. Returns number of listeners notified."""
        if event.event_name not in self._listeners:
            return 0
        notified_count = 0
        for handler in self._listeners[event.event_name]:
            handler(event)
            notified_count += 1
        return notified_count
