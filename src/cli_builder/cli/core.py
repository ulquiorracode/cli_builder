"""
Core CLI class.

This module defines the main entry point for a CLI application.
"""

from typing import Any

import attr

from .base import CliBase


@attr.define(slots=False)
class CliCore(CliBase):
    """
    Main entry point for a CLI application.

    This class represents the core of a CLI application and serves
    as the main entry point for executing commands.
    """

    version: str = attr.field(default="0.1.0")

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the CLI application."""
        self.emit("before:run", self)

        result = None

        self.emit("after:run", self, result)
        return result
