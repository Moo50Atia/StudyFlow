"""
KOS Core Dependency Injection Container
======================================
Provides a thread-safe, decoupled service locator and dependency injection container for KOS.
"""

from typing import Dict, Any, Type, Callable, Optional


class DependencyInjectionContainer:
    """Singleton/Thread-safe Container managing component bindings and singletons."""

    _instance: Optional["DependencyInjectionContainer"] = None

    def __init__(self):
        self._singletons: Dict[Type[Any], Any] = {}
        self._factories: Dict[Type[Any], Callable[[], Any]] = {}

    @classmethod
    def get_instance(cls) -> "DependencyInjectionContainer":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register_singleton(self, interface_cls: Type[Any], instance: Any) -> None:
        """Binds a concrete singleton instance to an interface/type."""
        self._singletons[interface_cls] = instance

    def register_factory(self, interface_cls: Type[Any], factory: Callable[[], Any]) -> None:
        """Binds a factory closure to create fresh instances per resolve call."""
        self._factories[interface_cls] = factory

    def resolve(self, interface_cls: Type[Any]) -> Any:
        """Resolves a concrete instance for the requested interface class."""
        if interface_cls in self._singletons:
            return self._singletons[interface_cls]
        if interface_cls in self._factories:
            return self._factories[interface_cls]()
        raise KeyError(f"No binding found for interface: {interface_cls.__name__}")

    def clear(self) -> None:
        """Clears all registered bindings."""
        self._singletons.clear()
        self._factories.clear()
