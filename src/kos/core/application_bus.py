"""
KOS Core Application Bus
========================
Implements Command/Query Responsibility Segregation (CQRS) Application Bus handlers.
"""

from typing import Dict, Any, Type, Callable
from pydantic import BaseModel


class Command(BaseModel):
    """Base class for all application commands."""
    pass


class Query(BaseModel):
    """Base class for all application queries."""
    pass


CommandHandler = Callable[[Command], Any]
QueryHandler = Callable[[Query], Any]


class ApplicationBus:
    """Dispatches Commands and Queries to their registered handlers."""

    def __init__(self):
        self._command_handlers: Dict[Type[Command], CommandHandler] = {}
        self._query_handlers: Dict[Type[Query], QueryHandler] = {}

    def register_command_handler(self, command_cls: Type[Command], handler: CommandHandler) -> None:
        self._command_handlers[command_cls] = handler

    def register_query_handler(self, query_cls: Type[Query], handler: QueryHandler) -> None:
        self._query_handlers[query_cls] = handler

    def execute_command(self, command: Command) -> Any:
        command_type = type(command)
        if command_type not in self._command_handlers:
            raise KeyError(f"No handler registered for command: {command_type.__name__}")
        return self._command_handlers[command_type](command)

    def execute_query(self, query: Query) -> Any:
        query_type = type(query)
        if query_type not in self._query_handlers:
            raise KeyError(f"No handler registered for query: {query_type.__name__}")
        return self._query_handlers[query_type](query)
