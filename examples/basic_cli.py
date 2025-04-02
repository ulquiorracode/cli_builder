#!/usr/bin/env python3
"""
Basic CLI example using CLI Builder.

This example demonstrates how to create a simple CLI application
with commands using the new event-driven architecture.
"""

import sys
from typing import Any, Optional, cast

from cli_builder import Cli, Module
from cli_builder.cli.base import CliBase
from cli_builder.cli.core import CliCore
from cli_builder.cli.module import CliModule


@Cli(name="hello", description="A simple hello world CLI application")
class HelloApp:
    """Hello application with basic commands."""

    def __init__(self) -> None:
        """Initialize the application."""
        # Get CliCore instance after applying the decorator
        app_instance = cast(CliCore, self)

        # Add version command
        version_module = CliModule(name="version", parent=app_instance)

        # Get the correctly typed version
        self.version_module = cast(CliModule, version_module)

    def _setup(self, cli: CliBase, *args: Any, **kwargs: Any) -> None:
        """Setup the application before running."""
        # Get version with the correct type
        version = getattr(cli, "version", "unknown")
        print(f"Setting up {cli.name} v{version}...")

    @Module("hello", description="Say hello to someone")
    class Hello:
        """Hello command module."""

        def run(self, name: Optional[str] = None) -> None:
            """
            Say hello to someone.

            Args:
                name: Name to greet (optional)
            """
            if name:
                print(f"Hello, {name}!")
            else:
                print("Hello, World!")

    @Module("goodbye", description="Say goodbye to someone")
    class Goodbye:
        """Goodbye command module."""

        def run(self, name: Optional[str] = None) -> None:
            """
            Say goodbye to someone.

            Args:
                name: Name to say goodbye to (optional)
            """
            if name:
                print(f"Goodbye, {name}!")
            else:
                print("Goodbye, World!")


if __name__ == "__main__":
    # Create the application
    app = HelloApp()  # This is actually a CliCore instance
    app_core = cast(CliCore, app)

    # Parse command line arguments
    args = sys.argv[1:]

    if not args:
        # No arguments, show help
        print(f"{app_core.name} v{app_core.version}")
        print(f"Description: {app_core.description}")
        print("Available commands:")
        for child in app_core.list_children():
            print(f"  {child.name}: {child.description or 'No description'}")
        sys.exit(0)

    # Get the command
    command_name = args[0]
    command = app_core.get_child(command_name)

    if not command:
        print(f"Unknown command: {command_name}")
        sys.exit(1)

    # Run the command with remaining arguments
    command_module = cast(CliModule, command)
    command_module.run(*args[1:])
