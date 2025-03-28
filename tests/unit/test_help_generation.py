"""Tests for help generation functionality."""

import io
import sys
from cli_builder import CLI


def test_auto_generate_help_flag():
    """Test that auto_generate_help flag works correctly."""
    cli = CLI(name="test-cli", description="Test CLI")
    assert cli.auto_generate_help is False

    cli.generate_help()
    assert cli.auto_generate_help is True


def test_help_string_updated_on_command_registration():
    """Test that help string is updated when commands are registered."""
    cli = CLI(name="test-cli", description="Test CLI")
    cli.generate_help()

    # Initially help string should contain basic info
    assert "test-cli - Test CLI" in cli._CLI__help_string
    assert "Available commands:" in cli._CLI__help_string

    # Register a command
    @cli.command(name="test", description="Test command")
    def test_cmd():
        pass

    # Check help string is updated
    assert "test-cli - Test CLI" in cli._CLI__help_string
    assert "Available commands:" in cli._CLI__help_string
    assert "test" in cli._CLI__help_string
    assert "Test command" in cli._CLI__help_string


def test_help_command_automatic_registration():
    """Test that help command is automatically registered."""
    cli = CLI(name="test-cli", description="Test CLI")
    cli.generate_help()  # Explicitly generate help - this registers help command

    # Register a command
    @cli.command(name="test", description="Test command")
    def test_cmd():
        pass

    # Help command should be registered now
    assert "help" in cli.commands

    # Run CLI with help command
    orig_stdout = sys.stdout
    sys.stdout = io.StringIO()  # Capture output
    try:
        cli.run(["help"])
        captured = sys.stdout.getvalue()
    finally:
        sys.stdout = orig_stdout

    # Output should contain help information
    assert "test-cli - Test CLI" in captured
    assert "Available commands:" in captured
    assert "test" in captured
    assert "Test command" in captured


def test_help_command_not_overwriting_user_command():
    """Test that auto-generated help command doesn't overwrite user command."""
    cli = CLI(name="test-cli", description="Test CLI")
    cli.generate_help()

    # User registers their own help command
    @cli.command(name="help", description="Custom help")
    def custom_help():
        return 42

    # Run CLI with help command
    orig_stdout = sys.stdout
    sys.stdout = io.StringIO()  # Capture output
    try:
        result = cli.run(["help"])
    finally:
        sys.stdout = orig_stdout

    # Check that it's the user's help command that ran
    assert result == 42


def test_help_command_shows_sorted_commands():
    """Test that help command shows commands in alphabetical order."""
    cli = CLI(name="test-cli", description="Test CLI")
    cli.generate_help()

    # Register commands in non-alphabetical order
    @cli.command(name="zebra", description="Z command")
    def z_cmd():
        pass

    @cli.command(name="alpha", description="A command")
    def a_cmd():
        pass

    @cli.command(name="middle", description="M command")
    def m_cmd():
        pass

    # Force generation of help
    cli.run(["--help"])

    # Get help content and find the command lines
    help_lines = cli._CLI__help_string.splitlines()
    cmd_lines = [line for line in help_lines if "  " in line]

    # Check commands are in alphabetical order
    # Note: help command is also included and sorted
    cmd_names = [line.split()[0] for line in cmd_lines]
    assert cmd_names == sorted(cmd_names)

    # Check specific commands exist
    assert any("alpha" in line for line in cmd_lines)
    assert any("help" in line for line in cmd_lines)
    assert any("middle" in line for line in cmd_lines)
    assert any("zebra" in line for line in cmd_lines)


def test_detailed_help_option():
    """Test that detailed help option works correctly."""
    cli = CLI(name="test-cli", description="Test CLI")
    cli.generate_help()

    # Register a command with argument and option
    @cli.command(name="greet", description="Greet someone")
    @cli.argument("name", type=str, help="Name to greet")
    @cli.option("count", short="c", type=int, default=1, help="Number of times to greet")
    def greet(name, count=1):
        pass

    # Run CLI with help command
    orig_stdout = sys.stdout
    sys.stdout = io.StringIO()  # Capture output
    try:
        cli.run(["help", "--detailed"])
        detailed_output = sys.stdout.getvalue()
    finally:
        sys.stdout = orig_stdout

    # Check detailed output
    assert "COMMANDS:" in detailed_output
    assert "greet" in detailed_output
    assert "Description: Greet someone" in detailed_output

    # Check arguments section
    assert "Arguments:" in detailed_output
    assert "name: (str) Name to greet" in detailed_output

    # Check options section
    assert "Options:" in detailed_output
    assert "-c, --count: (int) Number of times to greet" in detailed_output

    # Check detailed help shows information about help command itself
    assert "help" in detailed_output
    assert "detailed: (flag) Show detailed help" in detailed_output


def test_help_string_additional_instruction():
    """Test that help string contains instruction for detailed help."""
    cli = CLI(name="test-cli", description="Test CLI")
    cli.generate_help()

    assert (
        "Use 'test-cli help --detailed' for detailed information on all commands."
        in cli._CLI__help_string
    )
