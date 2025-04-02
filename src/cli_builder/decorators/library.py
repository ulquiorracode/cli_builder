"""
Library decorator.

This module provides the Library decorator for creating CLI library components.
"""

from typing import Any, Callable, Optional, Type, TypeVar, Union, overload

from ..cli.library import CliLibrary
from .utils import _create_component_decorator

T = TypeVar("T", bound=Type)


@overload
def Library(name_or_class: T) -> CliLibrary: ...


@overload
def Library(
    name_or_class: Optional[Union[str, None]] = None, **kwargs: Any
) -> Callable[[T], CliLibrary]: ...


def Library(
    name_or_class: Optional[Union[str, T]] = None, **kwargs: Any
) -> Union[CliLibrary, Callable[[T], CliLibrary]]:
    """Decorator for creating CLI library components (non-executable modules).

    This decorator transforms a class into a CLI library.

    Examples:
        With arguments:
        ```python
        @Library("my-lib", description="My library")
        class MyLibrary:
            def get_value(self):
                return "value"
        ```

        Without arguments:
        ```python
        @Library
        class MyLibrary:
            def get_value(self):
                return "value"
        ```
    """
    result = _create_component_decorator(name_or_class, CliLibrary, **kwargs)
    return result
