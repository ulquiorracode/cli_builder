"""
Module CLI class.

This module defines a module within a CLI application.
"""

from typing import Any, Optional

import attr

from .base import CliBase


@attr.define(slots=False)
class CliModule(CliBase):
    """
    A module within a CLI application.

    This class represents a module that can be added to a CLI application
    or to another module to create a hierarchical command structure.
    """

    is_command: bool = attr.field(default=True)
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

                warnings.warn(f"Parent '{self.parent_name}' not found for module '{self.name}'.")

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the CLI module."""
        self.emit("before:run", self)

        # Run implementation goes here
        result = None

        self.emit("after:run", self, result)
        return result
