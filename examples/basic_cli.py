#!/usr/bin/env python
"""Basic CLI example demonstrating core features."""

import sys

from cli_builder import CLI


def main(args: list[str] | None = None) -> int:
    """Run the basic CLI example.

    Args:
        args: Command line arguments (without program name).
             If None, sys.argv[1:] will be used.

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    cli = CLI(name="basic-cli", description="Basic CLI example")

    @cli.command(name="hello", description="Say hello")
    def hello() -> None:
        """Simple hello command without arguments."""
        print("Hello, World!")

    @cli.argument("name", type=str, help="Name to greet")
    @cli.option("count", short="c", type=int, default=1, help="Number of times to greet")
    @cli.command(name="greet", description="Greet someone")
    def greet(name: str, count: int = 1) -> None:
        """Greet someone multiple times."""
        for _ in range(count):
            print(f"Hello, {name}!")

    @cli.argument("b", type=int, help="Second number")
    @cli.argument("a", type=int, help="First number")
    @cli.command(name="add", description="Add two numbers")
    def add(a: int, b: int) -> int:
        """Add two numbers and print the result."""
        result = a + b
        print(f"{a} + {b} = {result}")
        return result

    return cli.run(args if args is not None else sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
