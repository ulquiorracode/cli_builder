#!/usr/bin/env python

"""Example demonstrating the use of standard commands.

Usage:
python standard_commands_example.py help                  # Help command
python standard_commands_example.py help --detailed       # Detailed help
python standard_commands_example.py version               # Show version
python standard_commands_example.py list                  # List commands
python standard_commands_example.py completion --shell bash  \
    # Generate bash completion
"""

from cli_builder import CLI


def main():
    """Run standard commands example."""
    # Create a CLI with all standard commands enabled
    cli = CLI(name="standard-cli", description="CLI with standard commands", version="1.5.0")

    # Enable all standard commands
    cli.enable_standard_commands(help=True, version=True, list=True, completion=True)

    # Add a custom command
    @cli.command(name="greet", description="Greet someone")
    @cli.argument("name", help="Name to greet")
    def greet(name):
        """Greet someone by name."""
        print(f"Hello, {name}!")
        return 0

    # Run the CLI
    return cli.run()


if __name__ == "__main__":
    import sys

    sys.exit(main())
