#!/usr/bin/env python
"""Example demonstrating automatic decorators for CLI Builder.

This example shows how to use the auto_arguments, auto_options,
and auto_command decorators to create CLI commands with minimal code.
"""

import sys

from cli_builder import CLI


def main():
    """Run auto decorator examples."""
    cli = CLI(name="auto-example", description="Example of automatic decorators")
    cli.generate_help()  # Enable help command

    # Example 1: Using auto_arguments and auto_options separately
    @cli.command()  # Name will be "convert" from function name
    @cli.auto_arguments  # Will create args: value, from_unit, to_unit
    @cli.auto_options  # Will create option: precision (int, default=2)
    def convert(value: float, from_unit: str, to_unit: str, precision: int = 2):
        """Convert value between units.

        Args:
            value: The value to convert
            from_unit: Source unit
            to_unit: Target unit
            precision: Number of decimal places
        """
        # Simple conversion rates (for demonstration)
        rates = {
            "km": {"m": 1000, "mi": 0.621371},
            "m": {"km": 0.001, "mi": 0.000621371},
            "mi": {"km": 1.60934, "m": 1609.34},
            "kg": {"g": 1000, "lb": 2.20462},
            "g": {"kg": 0.001, "lb": 0.00220462},
            "lb": {"kg": 0.453592, "g": 453.592},
        }

        if from_unit not in rates or to_unit not in rates[from_unit]:
            print(f"Error: Cannot convert from {from_unit} to {to_unit}")
            return 1

        result = value * rates[from_unit][to_unit]
        result = round(result, precision)
        print(f"{value} {from_unit} = {result} {to_unit}")
        return 0

    # Example 2: Using auto_command for even simpler code
    @cli.auto_command()  # Combines command, auto_arguments, and auto_options
    def format_text(
        text: str, case: str = "unchanged", width: int = 0, align: str = "left", fill: bool = False
    ):
        """Format text according to specified options.

        Args:
            text: Text to format
            case: Text case (upper, lower, title, unchanged)
            width: Text width (0 for no width limit)
            align: Text alignment (left, center, right)
            fill: Fill with spaces to width
        """
        # Apply case transformation
        if case == "upper":
            text = text.upper()
        elif case == "lower":
            text = text.lower()
        elif case == "title":
            text = text.title()

        # Apply width and alignment
        if width > 0:
            if align == "center":
                text = text.center(width)
            elif align == "right":
                text = text.rjust(width)
            elif fill:
                text = text.ljust(width)

        print(f"Formatted text: {text}")
        return 0

    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
