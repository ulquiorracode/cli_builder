#!/usr/bin/env python
"""Example demonstrating help generation with detailed option.

Usage:
python help_example.py help                 # Basic help
python help_example.py help --detailed      # Detailed help with arguments and options
python help_example.py greet John           # Run greet command
python help_example.py add 5 3              # Run add command
python help_example.py subtract 10 4        # Run subtract command
"""

from cli_builder import CLI


def main():
    """Run help generation example."""
    # Create CLI with automatic help generation
    cli = CLI(name="help-example", description="Example CLI with auto-generated help")
    cli.generate_help()  # Enable help generation with detailed option

    @cli.command(name="greet", description="Greet someone")
    @cli.argument("name", help="Name to greet")
    @cli.option("count", short="c", type=int, default=1, help="Number of times to greet")
    @cli.option("uppercase", short="u", is_flag=True, help="Convert greeting to uppercase")
    def greet(name, count=1, uppercase=False):
        """Greet someone multiple times."""
        message = f"Hello, {name}!"
        if uppercase:
            message = message.upper()

        for _ in range(count):
            print(message)
        return 0

    @cli.command(name="add", description="Add two numbers")
    @cli.argument("a", type=int, help="First number")
    @cli.argument("b", type=int, help="Second number")
    def add(a, b):
        """Add two numbers and print the result."""
        result = a + b
        print(f"{a} + {b} = {result}")
        return 0

    @cli.command(name="subtract", description="Subtract two numbers")
    @cli.argument("a", type=int, help="First number")
    @cli.argument("b", type=int, help="Second number")
    @cli.option("absolute", short="a", is_flag=True, help="Return absolute result")
    def subtract(a, b, absolute=False):
        """Subtract second number from first and print the result."""
        result = a - b
        if absolute:
            result = abs(result)
        print(f"{a} - {b} = {result}")
        return 0

    # Run the CLI - help command will be automatically registered
    return cli.run()


if __name__ == "__main__":
    import sys

    sys.exit(main())
