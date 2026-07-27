"""
KOS Core Application Facade
===========================
Provides a high-level facade coordinating Application Bus, Dependency Container, and Event Bus.
"""

from typing import Any
from src.kos.core.config_runtime import ConfigurationRuntime
from src.kos.core.di_container import DependencyInjectionContainer
from src.kos.core.event_bus import EventBus
from src.kos.core.application_bus import ApplicationBus, Command, Query


class KOSApplicationFacade:
    """Unified application entry point for KOS kernel services."""

    def __init__(self, config_path: str = None):
        self.config_runtime = ConfigurationRuntime(config_path)
        self.container = DependencyInjectionContainer.get_instance()
        self.event_bus = EventBus()
        self.application_bus = ApplicationBus()

        # Register core singletons
        self.container.register_singleton(ConfigurationRuntime, self.config_runtime)
        self.container.register_singleton(EventBus, self.event_bus)
        self.container.register_singleton(ApplicationBus, self.application_bus)

    def execute_command(self, command: Command) -> Any:
        return self.application_bus.execute_command(command)

    def execute_query(self, query: Query) -> Any:
        return self.application_bus.execute_query(query)
