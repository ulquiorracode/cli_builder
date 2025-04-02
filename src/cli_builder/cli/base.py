"""
Base class for CLI Builder.

This module defines the abstract base class for all CLI components:
- CliBase: Abstract base class for all CLI components
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, ClassVar, Dict, List, Optional, TypeVar

import attr

from ..events.emitter import EventEmitter

# Type for CLI command handlers
CommandHandler = Callable[..., Any]

# Self type for return value annotations
S = TypeVar("S", bound="CliBase")


@attr.define(slots=False)
class CliBase(ABC):
    """
    Abstract base class for all CLI components.

    This class defines the common interface for all CLI components,
    including the core application and individual modules.

    All CLI components are event emitters and can have child components.
    """

    name: str = attr.field()
    description: Optional[str] = attr.field(default=None)

    # Private attributes
    _emitter: EventEmitter = attr.field(factory=EventEmitter)
    _commands: Dict[str, Any] = attr.field(factory=dict)
    _children: Dict[str, "CliBase"] = attr.field(factory=dict)
    _parent: Optional["CliBase"] = attr.field(default=None)

    # Registry for all CLI components - ClassVar for static class attribute
    _registry: ClassVar[Dict[str, "CliBase"]] = {}

    def __attrs_post_init__(self) -> None:
        """Register component after initialization."""
        # Register this component in the global registry
        CliBase.register(self)

    @classmethod
    def register(cls, instance: "CliBase") -> None:
        """Register a CLI component."""
        cls._registry[instance.name] = instance

        # Emit a registration event that can be used to establish parent-child relationships
        # This allows components created with parent_name to find their parent later
        instance.emit("component:registered", instance)

        # Try to find children that specified this component as parent
        for potential_child in cls._registry.values():
            if (
                hasattr(potential_child, "parent_name")
                and potential_child.parent_name == instance.name
                and potential_child.parent is None
            ):
                instance.add_child(potential_child)

    @classmethod
    def get(cls, name: str) -> Optional["CliBase"]:
        """Get a registered CLI component by name."""
        return cls._registry.get(name)

    @classmethod
    def get_component(cls, name: str) -> Optional["CliBase"]:
        """Get a registered CLI component by name (alias for get)."""
        return cls.get(name)

    @classmethod
    def clear_registry(cls) -> None:
        """Clear the CLI component registry."""
        cls._registry.clear()

    def add_command(self, name: str, command: Any) -> None:
        """Add a command to the CLI component."""
        self._commands[name] = command

    def get_command(self, name: str) -> Optional[Any]:
        """Get a command by name."""
        return self._commands.get(name)

    def add_child(self, child: "CliBase") -> None:
        """Add a child CLI component."""
        child._parent = self
        self._children[child.name] = child

        if hasattr(child, "parent_name"):
            child.parent_name = None

    def get_child(self, name: str) -> Optional["CliBase"]:
        """Get a child CLI component by name."""
        return self._children.get(name)

    def get_children(self) -> Dict[str, "CliBase"]:
        """Get all child CLI components."""
        return self._children

    def list_children(self) -> List["CliBase"]:
        """Get a list of all child CLI components."""
        return list(self._children.values())

    @property
    def parent(self) -> Optional["CliBase"]:
        """Get the parent component."""
        return self._parent

    def emit(self, event: str, *args: Any, **kwargs: Any) -> bool:
        """Emit an event."""
        result = self._emitter.emit(event, *args, **kwargs)

        if self._parent:
            self._parent.emit(event, *args, **kwargs)

        return result

    def on(self, event: str, listener: Callable, pre: bool = False) -> None:
        """Register an event listener."""
        self._emitter.on(event, listener, is_pre=pre)

    def off(self, event: str, listener: Callable) -> None:
        """Remove an event listener."""
        self._emitter.off(event, listener)

    def once(self, event: str, listener: Callable, pre: bool = False) -> None:
        """Register a one-time event listener."""
        self._emitter.once(event, listener, is_pre=pre)

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the CLI component."""
        pass
