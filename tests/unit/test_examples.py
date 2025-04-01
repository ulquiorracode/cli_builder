"""Tests for CLI examples."""

import pytest

from cli_builder import CLI
from examples.basic_cli import main


def test_advanced_cli_calc():
    """Test calculator command."""
    cli = CLI(name="test-cli", description="Test CLI")

    @cli.option("precision", short="p", type=int, default=2, help="Decimal precision")
    @cli.argument("numbers", type=float, nargs="+", help="Numbers to calculate")
    @cli.command(description="Calculate operations on numbers")
    def calc(numbers: list[float], precision: int = 2) -> int:
        """Calculate sum of numbers."""
        result = sum(numbers)
        print(f"Result: {result:.{precision}f}")
        return 0

    # Test with default precision
    assert cli.run(["calc", "1", "2", "3"]) == 0

    # Test with custom precision
    assert cli.run(["calc", "1", "2", "3", "--precision", "1"]) == 0


def test_advanced_cli_convert():
    """Test unit converter command."""
    cli = CLI(name="test-cli", description="Test CLI")

    @cli.argument("to_unit", help="Target unit")
    @cli.argument("from_unit", help="Source unit")
    @cli.argument("value", type=float, help="Value to convert")
    @cli.command(description="Convert units")
    def convert(value: float, from_unit: str, to_unit: str) -> int:
        """Convert between units."""
        conversions = {
            ("km", "m"): lambda x: x * 1000,
            ("m", "km"): lambda x: x / 1000,
            ("kg", "g"): lambda x: x * 1000,
            ("g", "kg"): lambda x: x / 1000,
        }

        key = (from_unit, to_unit)
        if key in conversions:
            result = conversions[key](value)
            print(f"{value} {from_unit} = {result} {to_unit}")
            return 0
        else:
            print(f"Conversion from {from_unit} to {to_unit} not supported")
            return 1

    # Test supported conversion
    assert cli.run(["convert", "5", "km", "m"]) == 0

    # Test unsupported conversion
    assert cli.run(["convert", "5", "km", "kg"]) == 1


def test_advanced_cli_format():
    """Test text formatter command."""
    cli = CLI(name="test-cli", description="Test CLI")

    @cli.option("title", short="t", is_flag=True, help="Convert to title case")
    @cli.option("lower", short="l", is_flag=True, help="Convert to lowercase")
    @cli.option("upper", short="u", is_flag=True, help="Convert to uppercase")
    @cli.argument("text", help="Text to format")
    @cli.command(description="Format text")
    def format(text: str, upper: bool = False, lower: bool = False, title: bool = False) -> int:
        """Format text according to specified options."""
        if upper:
            result = text.upper()
        elif lower:
            result = text.lower()
        elif title:
            result = text.title()
        else:
            result = text
        print(f"Formatted text: {result}")
        return 0

    # Test uppercase formatting
    assert cli.run(["format", "hello world", "--upper"]) == 0

    # Test lowercase formatting
    assert cli.run(["format", "HELLO WORLD", "--lower"]) == 0

    # Test title case formatting
    assert cli.run(["format", "hello world", "--title"]) == 0


def test_hello_command(capsys):
    """Test hello command without arguments."""
    # Arrange
    sys_args = ["hello"]

    # Act
    main(sys_args)
    captured = capsys.readouterr()

    # Assert
    assert captured.out == "Hello, World!\n"
    assert captured.err == ""


@pytest.mark.parametrize("name", ["John", "Alice", "Bob"])
def test_greet_command_with_different_names(capsys, name):
    """Test greet command with different names."""
    # Arrange
    sys_args = ["greet", name]

    # Act
    main(sys_args)
    captured = capsys.readouterr()

    # Assert
    assert captured.out == f"Hello, {name}!\n"
    assert captured.err == ""


@pytest.mark.parametrize("count", [1, 2, 3])
def test_greet_command_with_count(capsys, count):
    """Test greet command with different count values."""
    # Arrange
    sys_args = ["greet", "John", "-c", str(count)]

    # Act
    main(sys_args)
    captured = capsys.readouterr()

    # Assert
    assert captured.out == "Hello, John!\n" * count
    assert captured.err == ""


@pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (0, 0, 0), (-1, 1, 0), (100, 200, 300)])
def test_add_command_with_different_numbers(capsys, a, b, expected):
    """Test add command with different number combinations."""
    # Arrange
    sys_args = ["add", str(a), str(b)]

    # Act
    result = main(sys_args)
    captured = capsys.readouterr()

    # Assert
    assert captured.out == f"{a} + {b} = {expected}\n"
    assert captured.err == ""
    assert result == expected


def test_invalid_command(capsys):
    """Test behavior with invalid command."""
    # Arrange
    sys_args = ["invalid"]

    # Act
    result = main(sys_args)
    captured = capsys.readouterr()

    # Assert
    assert result != 0  # Should return non-zero exit code
    assert "error: argument command: invalid choice" in captured.err


@pytest.mark.parametrize(
    "command,args,error_pattern",
    [
        ("greet", [], "error: the following arguments are required: name"),
        ("add", ["1"], "error: the following arguments are required"),
        ("add", ["a", "b"], "error: argument"),
    ],
)
def test_invalid_arguments(capsys, command, args, error_pattern):
    """Test behavior with invalid arguments."""
    # Arrange
    sys_args = [command] + args

    # Act
    result = main(sys_args)
    captured = capsys.readouterr()

    # Assert
    assert result != 0  # Should return non-zero exit code
    assert error_pattern in captured.err
