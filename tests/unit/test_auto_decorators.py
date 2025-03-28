"""Tests for automatic decorator functions."""

from typing import List

from cli_builder import CLI


def test_auto_arguments():
    """Test automatic argument generation from function parameters."""
    cli = CLI(name="test-cli", description="Test CLI")

    @cli.command()
    @cli.auto_arguments
    def test_func(name: str, count: int, items: List[str]):
        """Test function with arguments.

        Args:
            name: User name
            count: Number of items
            items: List of items
        """
        return 0

    # Check that arguments were created correctly
    command = cli.commands["test_func"]
    assert len(command.arguments) == 3

    # Check arguments are present (order may vary based on implementation)
    arg_names = [arg["name"] for arg in command.arguments]
    assert "name" in arg_names
    assert "count" in arg_names
    assert "items" in arg_names

    # Create a dictionary for easier access
    args_dict = {arg["name"]: arg for arg in command.arguments}

    # Check types
    assert args_dict["items"]["type"] == List[str]
    assert args_dict["count"]["type"] == int
    assert args_dict["name"]["type"] == str

    # Check help text from docstring
    assert args_dict["items"]["help"] == "List of items"
    assert args_dict["count"]["help"] == "Number of items"
    assert args_dict["name"]["help"] == "User name"


def test_auto_options():
    """Test automatic option generation from function parameters with defaults."""
    cli = CLI(name="test-cli", description="Test CLI")

    @cli.command()
    @cli.auto_options
    def test_func(required_arg, verbose: bool = False, count: int = 10, name: str = "test"):
        """Test function with options.

        Args:
            required_arg: Required argument (not turned into an option)
            verbose: Enable verbose output
            count: Number of items
            name: User name
        """
        return 0

    # Check that options were created correctly
    command = cli.commands["test_func"]
    assert len(command.options) == 3

    # Get options by name
    options_dict = {opt["name"]: opt for opt in command.options}

    # Check verbose option
    assert "verbose" in options_dict
    assert (
        options_dict["verbose"].get("is_flag", False)
        or options_dict["verbose"].get("action") == "store_true"
    )
    assert options_dict["verbose"]["help"] == "Enable verbose output"

    # Check count option
    assert "count" in options_dict
    assert options_dict["count"]["type"] == int
    assert options_dict["count"]["default"] == 10
    assert options_dict["count"]["help"] == "Number of items"

    # Check name option
    assert "name" in options_dict
    assert options_dict["name"]["type"] == str
    assert options_dict["name"]["default"] == "test"
    assert options_dict["name"]["help"] == "User name"

    # Check short options
    assert options_dict["verbose"].get("short") == "v"
    assert options_dict["count"].get("short") == "c"
    assert options_dict["name"].get("short") == "n"


def test_auto_command():
    """Test auto_command decorator that combines command, auto_arguments, and auto_options."""
    cli = CLI(name="test-cli", description="Test CLI")

    @cli.auto_command()
    def convert(value: float, from_unit: str, to_unit: str, precision: int = 2):
        """Convert values between units.

        Args:
            value: The value to convert
            from_unit: Source unit
            to_unit: Target unit
            precision: Number of decimal places
        """
        return 0

    # Check that command was created with the function name
    assert "convert" in cli.commands
    command = cli.commands["convert"]

    # Check that description was taken from first line of docstring
    assert command.description.startswith("Convert values between units.")

    # Check arguments
    assert len(command.arguments) == 3
    arg_names = [arg["name"] for arg in command.arguments]
    assert "value" in arg_names
    assert "from_unit" in arg_names
    assert "to_unit" in arg_names

    # Check option
    assert len(command.options) == 1
    assert command.options[0]["name"] == "precision"
    assert command.options[0]["default"] == 2


def test_command_name_inference():
    """Test that command name is inferred from function name when not provided."""
    cli = CLI(name="test-cli", description="Test CLI")

    @cli.command()  # No name provided
    def hello_world():
        """Say hello."""
        return 0

    assert "hello_world" in cli.commands
    assert cli.commands["hello_world"].description == "Say hello."


def test_docstring_extraction():
    """Test that parameter descriptions are extracted from different docstring formats."""
    cli = CLI(name="test-cli", description="Test CLI")

    # Test reST style docstring
    @cli.command()
    @cli.auto_arguments
    def rest_style(name: str, count: int):
        """Test function with reST style docstring.

        :param name: User name in reST style
        :param count: Count in reST style
        :return: Always zero
        """
        return 0

    # Test Google style docstring
    @cli.command()
    @cli.auto_arguments
    def google_style(name: str, count: int):
        """Test function with Google style docstring.

        Args:
            name: User name in Google style
            count: Count in Google style

        Returns:
            Always zero
        """
        return 0

    # Check reST style extraction
    rest_cmd = cli.commands["rest_style"]
    rest_args = {arg["name"]: arg for arg in rest_cmd.arguments}
    assert rest_args["name"]["help"] == "User name in reST style"
    assert rest_args["count"]["help"] == "Count in reST style"

    # Check Google style extraction
    google_cmd = cli.commands["google_style"]
    google_args = {arg["name"]: arg for arg in google_cmd.arguments}
    assert google_args["name"]["help"] == "User name in Google style"
    assert google_args["count"]["help"] == "Count in Google style"
