"""
CLI Core decorator.

This module provides the main Cli decorator for creating CLI applications.
"""

from typing import Any, Callable, Optional, Type, TypeVar, Union, overload

from ..cli.core import CliCore
from .utils import _process_nested_classes, _transfer_methods

T = TypeVar("T", bound=Type)


@overload
def Cli(name_or_class: T) -> CliCore: ...


@overload
def Cli(
    name_or_class: Optional[Union[str, None]] = None, **kwargs: Any
) -> Callable[[T], CliCore]: ...


def Cli(
    name_or_class: Optional[Union[str, T]] = None, **kwargs: Any
) -> Union[CliCore, Callable[[T], CliCore]]:
    """Decorator for creating CLI core components.

    This decorator transforms a class into a CLI application.

    Examples:
        With arguments:
        ```python
        @Cli("my-cli", description="My CLI")
        class MyCli:
            def run(self):
                return "Running my CLI"
        ```

        Without arguments:
        ```python
        @Cli
        class MyCli:
            def run(self):
                return "Running my CLI"
        ```
    """

    def _process_class(cls: Type) -> CliCore:
        # Create CLI instance
        name = kwargs.get("name", getattr(cls, "name", cls.__name__))
        cli_instance = CliCore(name=name, **{k: v for k, v in kwargs.items() if k != "name"})

        # Store original class for reference
        cls._cli_original_class = cls  # type: ignore

        # Transfer methods to CLI instance
        _transfer_methods(cls, cli_instance)

        # Process nested classes
        _process_nested_classes(cls, cli_instance)

        # Call the original class init if it exists
        if hasattr(cls, "__init__") and cls.__init__ is not object.__init__:
            # Get the init method
            init_method = cls.__init__.__get__(cli_instance, cli_instance.__class__)
            # Call it without passing self (already bound)
            init_method()

        # Return the CLI instance directly instead of a factory
        return cli_instance

    # Decorator called with arguments: @Cli(name="my-cli")
    if not isinstance(name_or_class, type) and name_or_class is not None:
        kwargs["name"] = name_or_class
        return lambda cls: _process_class(cls)

    # Decorator called without arguments: @Cli
    if isinstance(name_or_class, type):
        return _process_class(name_or_class)

    # Decorator called without arguments but with parentheses: @Cli()
    return lambda cls: _process_class(cls)
