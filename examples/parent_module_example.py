#!/usr/bin/env python3
"""
Example demonstrating the use of parent_name attribute.

This example shows how to organize CLI modules in separate files
using the parent_name attribute instead of nested classes.
"""

import sys
from typing import Any, Optional, cast

from cli_builder import Cli, Module
from cli_builder.cli.base import CliBase
from cli_builder.cli.core import CliCore
from cli_builder.cli.module import CliModule


# Main application
@Cli(name="advanced", description="An advanced CLI application with modules")
class AdvancedApp:
    """Advanced application showcasing module organization."""

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


# User management module
@Module("users", description="User management commands", parent_name="advanced")
class UserModule:
    """User management module."""

    def run(self) -> None:
        """Display available user commands."""
        # Get CliModule instance after applying the decorator
        self_module = cast(CliModule, self)
        print("Available user commands:")
        for child in self_module.list_children():
            print(f"  {child.name}: {child.description or 'No description'}")


# List users command - child of the users module
@Module("list", description="List all users", parent_name="users")
class ListUsers:
    """List users command."""

    def run(self) -> None:
        """List all users."""
        print("Listing all users:")
        print("  - admin")
        print("  - user1")
        print("  - user2")


# Add user command - child of the users module
@Module("add", description="Add a new user", parent_name="users")
class AddUser:
    """Add user command."""

    def run(self, username: Optional[str] = None) -> None:
        """
        Add a new user.

        Args:
            username: Username to add
        """
        if not username:
            print("Error: Username is required.")
            return

        print(f"Added user: {username}")


# Tools module
@Module(name="tools", parent_name="advanced")
class ToolsModule:
    def __init__(self) -> None:
        """Initialize tools module."""
        # Get CliModule instance after applying the decorator
        module_instance = cast(CliModule, self)
        # Register module in parent
        module_instance.register_in_parent()


if __name__ == "__main__":
    # Create the application
    app = AdvancedApp()  # This is actually a CliCore instance
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

    # Basic command parsing logic
    if len(args) == 1:
        # Single command
        command = app_core.get_child(args[0])
        if command:
            command_module = cast(CliModule, command)
            command_module.run()
        else:
            print(f"Unknown command: {args[0]}")
            sys.exit(1)
    elif len(args) == 2:
        # Command with subcommand
        command = app_core.get_child(args[0])
        if not command:
            print(f"Unknown command: {args[0]}")
            sys.exit(1)

        command_module = cast(CliModule, command)
        subcommand = command_module.get_child(args[1])
        if subcommand:
            subcommand_module = cast(CliModule, subcommand)
            subcommand_module.run()
        else:
            print(f"Unknown subcommand: {args[1]} for command {args[0]}")
            sys.exit(1)
    elif len(args) >= 3:
        # Command with subcommand and arguments
        command = app_core.get_child(args[0])
        if not command:
            print(f"Unknown command: {args[0]}")
            sys.exit(1)

        command_module = cast(CliModule, command)
        subcommand = command_module.get_child(args[1])
        if subcommand:
            subcommand_module = cast(CliModule, subcommand)
            subcommand_module.run(*args[2:])
        else:
            print(f"Unknown subcommand: {args[1]} for command {args[0]}")
            sys.exit(1)
