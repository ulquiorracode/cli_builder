"""
Utility functions for CLI decorators.

This module contains internal utility functions used by the decorators.
"""

import inspect
from typing import Any, Callable, Optional, Type, TypeVar, Union

from ..cli.base import CliBase

T = TypeVar("T", bound=Type)
R = TypeVar("R", bound=CliBase)


def _create_component_decorator(
    name_or_class: Optional[Union[str, T]], component_class: Type[R], **kwargs: Any
) -> Union[R, Callable[[T], R]]:
    """
    Create a component decorator for either Module or Library.

    Args:
        name_or_class: Either the name or the class to decorate
        component_class: The class to instantiate (CliModule or CliLibrary)
        **kwargs: Additional arguments for the component

    Returns:
        Either the decorated component or a decorator function
    """

    def _process_class(cls: Type) -> R:
        # Create component instance
        name = kwargs.get("name", getattr(cls, "name", cls.__name__))
        component = component_class(name=name, **{k: v for k, v in kwargs.items() if k != "name"})

        # Store original class for reference
        cls._cli_original_class = cls  # type: ignore

        # Transfer methods to component instance
        _transfer_methods(cls, component)

        # Process nested classes
        _process_nested_classes(cls, component)

        # Call the original class init if it exists
        if hasattr(cls, "__init__") and cls.__init__ is not object.__init__:
            # Get the init method
            init_method = cls.__init__.__get__(component, component.__class__)
            # Call it without passing self (already bound)
            init_method()

        # Return the component instance directly
        return component

    # Decorator called with arguments: @Decorator(name="name")
    if not isinstance(name_or_class, type) and name_or_class is not None:
        kwargs["name"] = name_or_class
        return lambda cls: _process_class(cls)  # type: ignore

    # Decorator called without arguments: @Decorator
    if isinstance(name_or_class, type):
        return _process_class(name_or_class)

    # Decorator called without arguments but with parentheses: @Decorator()
    return lambda cls: _process_class(cls)  # type: ignore


def _transfer_methods(cls: Type, instance: CliBase) -> None:
    """Transfer methods from class to CLI instance."""
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        # Skip private methods and special methods
        if name.startswith("_"):
            continue

        # Check if method already exists on instance
        if hasattr(instance, name) and callable(getattr(instance, name)):
            # If method exists and is not a default implementation, skip
            attr_method = getattr(instance.__class__, name, None)

            # Skip if the method is defined in CliBase/CliCore/CliModule/CliLibrary
            # and overridden in the decorated class
            base_classes = ("CliBase", "CliCore", "CliModule", "CliLibrary")
            if attr_method is not None and attr_method.__qualname__.split(".")[0] in base_classes:
                # Replace with the class method
                setattr(instance, name, method.__get__(instance, instance.__class__))
        else:
            # Add method to instance
            setattr(instance, name, method.__get__(instance, instance.__class__))


def _process_nested_classes(cls: Type, instance: CliBase) -> None:
    """Process nested classes in the decorated class."""
    # Avoid circular imports
    from .module import Module

    for name, nested_cls in cls.__dict__.items():
        if not isinstance(nested_cls, type):
            continue

        # Skip private classes
        if name.startswith("_"):
            continue

        # Check if this class has Module, Library or Cli decorator
        if hasattr(nested_cls, "_cli_original_class"):
            # Create instance using the decorator
            if isinstance(nested_cls, CliBase):
                # It's already a CLI component instance, use it directly
                child = nested_cls
            else:
                # Probably a class that needs to be instantiated
                # Use Module decorator to create a module
                child = Module(name)(nested_cls)  # type: ignore

            # Add as child to parent instance
            instance.add_child(child)
