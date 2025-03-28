"""Constants and utilities for CLI builder."""

from typing import Any, TypeVar

T = TypeVar("T")


class ConstantDescriptor:
    """Descriptor for constants that cannot be modified through instances."""

    def __init__(self, value: Any):
        """Initialize with a value.

        Args:
            value: The constant value
        """
        self._value = value

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        """Get constant value.

        Args:
            obj: Instance
            objtype: Class

        Returns:
            Constant value
        """
        return self._value

    def __set__(self, obj: Any, value: Any) -> None:
        """Prevent setting a new value via instance.

        Args:
            obj: Instance
            value: New value

        Raises:
            AttributeError: Always raised to prevent modification
        """
        raise AttributeError("Cannot modify a constant value")


# Apply metaclass to control class variable assignments
class ConstantMeta(type):
    """Metaclass for constant containers."""

    def __setattr__(cls, name, value):
        """Prevent changing class attributes after class definition."""
        if name in cls.__dict__:
            raise AttributeError(f"Cannot modify constant {name}")
        super().__setattr__(name, value)


class Constant:
    """Utility class to create constants."""

    @staticmethod
    def create(value: Any) -> ConstantDescriptor:
        """Create a constant descriptor.

        Args:
            value: The constant value

        Returns:
            A constant descriptor
        """
        return ConstantDescriptor(value)

    def __new__(cls, value: Any) -> ConstantDescriptor:
        """Constructor to create a constant descriptor.

        Args:
            value: The constant value

        Returns:
            A constant descriptor
        """
        return cls.create(value)


class CLIConstants(metaclass=ConstantMeta):
    """Constants used by the CLI class."""

    DEFAULT_CLI_DESCRIPTION = Constant("No description provided for this CLI")
    DEFAULT_COMMAND_DESCRIPTION = Constant("No description provided for this command")
    COMMAND_DEST = Constant("command")
    HELP_COMMAND_NAME = Constant("help")
