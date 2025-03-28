#!/usr/bin/env python
"""Example demonstrating default descriptions when none are provided."""

from cli_builder import CLI


def main():
    """Run example with missing descriptions."""
    # Create CLI without description
    cli = CLI(name="no-desc-example")
    cli.generate_help()

    # Command without explicit description
    @cli.command()
    def hello():
        """This docstring will be used as description."""
        print("Hello from docstring description!")
        return 0

    # Command with no description at all
    @cli.command(name="no_desc")
    def no_description():
        # No docstring, so default description will be used
        print("No description provided!")
        return 0

    # Command with empty description
    @cli.command(name="empty_desc", description="")
    def empty_description():
        # Empty description, so default will be used
        print("Empty description provided!")
        return 0

    # Run the CLI
    return cli.run()


if __name__ == "__main__":
    import sys

    sys.exit(main())
