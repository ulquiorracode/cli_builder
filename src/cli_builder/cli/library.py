"""
Library CLI class.

This module defines a library within a CLI application.
"""

from typing import Any, Optional

import attr

from .base import CliBase


@attr.define(slots=False)
class CliLibrary(CliBase):
    """
    CLI library module that provides shared functionality.

    This class represents a library that can be added to a CLI application
    or to a module to provide shared functionality. It is not meant
    to be executed directly as a command.
    """

    parent_name: Optional[str] = attr.field(default=None)

    def __attrs_post_init__(self) -> None:
        """Post-initialization hook."""
        # Call parent __attrs_post_init__ for registration
        super().__attrs_post_init__()

        # Try to find parent by name if parent_name is specified
        if self.parent_name and not self._parent:
            parent = CliBase.get(self.parent_name)
            if parent:
                parent.add_child(self)
            else:
                import warnings

                warnings.warn(f"Parent '{self.parent_name}' not found for library '{self.name}'.")

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """
        Libraries are not meant to be run directly.
        This method is implemented to satisfy the CliBase interface.
        """
        self.emit("before:run", self)

        # Libraries shouldn't be run directly, so return None
        result = None

        self.emit("after:run", self, result)
        return result
