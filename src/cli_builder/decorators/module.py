"""
Module decorator.

This module provides the Module decorator for creating CLI module components.
"""

from typing import Any, Callable, Optional, Type, TypeVar, Union, overload

from ..cli.module import CliModule
from .utils import _create_component_decorator

T = TypeVar("T", bound=Type)


@overload
def Module(name_or_class: T) -> CliModule: ...


@overload
def Module(
    name_or_class: Optional[Union[str, None]] = None, **kwargs: Any
) -> Callable[[T], CliModule]: ...


def Module(
    name_or_class: Optional[Union[str, T]] = None, **kwargs: Any
) -> Union[CliModule, Callable[[T], CliModule]]:
    """Decorator for creating CLI module components (command modules).

    This decorator transforms a class into a CLI module.

    Examples:
        With arguments:
        ```python
        @Module("my-module", description="My module")
        class MyModule:
            def run(self):
                return "Running my module"
        ```

        Without arguments:
        ```python
        @Module
        class MyModule:
            def run(self):
                return "Running my module"
        ```
    """
    result = _create_component_decorator(name_or_class, CliModule, **kwargs)
    return result
