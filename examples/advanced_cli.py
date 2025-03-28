#!/usr/bin/env python
"""Advanced CLI example."""

from cli_builder import CLI


def main():
    """Run advanced CLI example."""
    cli = CLI(name="advanced-cli", description="Advanced CLI example")

    @cli.command(name="calc", description="Calculator")
    @cli.argument("operation", type=str, choices=["add", "sub", "mul", "div"])
    @cli.argument("a", type=float)
    @cli.argument("b", type=float)
    def calc(operation: str, a: float, b: float) -> float:
        """Calculate result of operation on two numbers."""
        if operation == "add":
            result = a + b
        elif operation == "sub":
            result = a - b
        elif operation == "mul":
            result = a * b
        elif operation == "div":
            if b == 0:
                raise ValueError("Division by zero")
            result = a / b

        print(f"{a} {operation} {b} = {result}")
        return result

    @cli.command(name="convert", description="Convert between units")
    @cli.argument("value", type=float)
    @cli.argument("from_unit", type=str)
    @cli.argument("to_unit", type=str)
    @cli.option("precision", short="p", type=int, default=2, help="Number of decimal places")
    def convert(value: float, from_unit: str, to_unit: str, precision: int = 2) -> float:
        """Convert value between units."""
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
            raise ValueError(f"Unsupported conversion from {from_unit} to {to_unit}")

        result = value * rates[from_unit][to_unit]
        result = round(result, precision)
        print(f"{value} {from_unit} = {result} {to_unit}")
        return result

    @cli.command(name="format", description="Format text")
    @cli.argument("text", type=str)
    @cli.option("case", short="c", type=str, choices=["upper", "lower", "title"], help="Text case")
    @cli.option("width", short="w", type=int, help="Minimum width")
    @cli.option(
        "align",
        short="a",
        type=str,
        choices=["left", "center", "right"],
        default="left",
        help="Text alignment",
    )
    def format_text(text: str, case: str = None, width: int = None, align: str = "left") -> str:
        """Format text according to options."""
        if case == "upper":
            text = text.upper()
        elif case == "lower":
            text = text.lower()
        elif case == "title":
            text = text.title()

        if width is not None:
            if align == "center":
                text = text.center(width)
            elif align == "right":
                text = text.rjust(width)
            else:  # left
                text = text.ljust(width)

        print(f"Formatted text: {text}")
        return text

    return cli.run()


if __name__ == "__main__":
    main()
