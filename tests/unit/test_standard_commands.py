"""Tests for standard commands functionality."""

import io
import sys

from cli_builder import CLI


def test_enable_standard_commands():
    """Test enabling standard commands."""
    cli = CLI(name="test-cli", version="1.2.3")
    cli.enable_standard_commands(help=True, version=True, list=True, completion=True)

    # Check that standard commands are registered
    assert "help" in cli.commands
    assert "version" in cli.commands
    assert "list" in cli.commands
    assert "completion" in cli.commands


def test_version_command():
    """Test version command."""
    cli = CLI(name="test-cli", version="1.2.3")
    cli._generate_version_command()

    # Capture stdout
    orig_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        cli.run(["version"])
        captured = sys.stdout.getvalue()
    finally:
        sys.stdout = orig_stdout

    # Check output
    assert "test-cli version 1.2.3" in captured


def test_list_command():
    """Test list command."""
    cli = CLI(name="test-cli")

    # Add some commands
    @cli.command(name="cmd1")
    def cmd1():
        pass

    @cli.command(name="cmd2")
    def cmd2():
        pass

    # Generate list command
    cli._generate_list_command()

    # Capture stdout
    orig_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        cli.run(["list"])
        captured = sys.stdout.getvalue()
    finally:
        sys.stdout = orig_stdout

    # Check output - should be sorted alphabetically
    expected_lines = ["cmd1", "cmd2", "list"]
    for line in expected_lines:
        assert line in captured


def test_completion_command_powershell():
    """Test completion command for PowerShell."""
    cli = CLI(name="test-cli")
    cli._generate_completion_command()

    # Capture stdout
    orig_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        cli.run(["completion", "--shell", "powershell"])
        captured = sys.stdout.getvalue()
    finally:
        sys.stdout = orig_stdout

    # Check output contains PowerShell completion script
    assert "Register-ArgumentCompleter" in captured
    assert "test-cli" in captured


def test_completion_command_bash():
    """Test completion command for Bash."""
    cli = CLI(name="test-cli")
    cli._generate_completion_command()

    # Capture stdout
    orig_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        cli.run(["completion", "--shell", "bash"])
        captured = sys.stdout.getvalue()
    finally:
        sys.stdout = orig_stdout

    # Check output contains bash completion script
    assert "_test-cli_completion()" in captured
    assert "complete -F _test-cli_completion test-cli" in captured


def test_standard_commands_not_overriding_user_commands():
    """Test that standard commands don't override user commands."""
    cli = CLI(name="test-cli")

    # User defines a custom version command
    @cli.command(name="version")
    def custom_version():
        return 42

    # Enable standard commands
    cli.enable_standard_commands(version=True)

    # Run the custom version command
    result = cli.run(["version"])

    # Should use the user-defined command
    assert result == 42


def test_help_command_not_registered_when_disabled():
    """Test that help command is not registered when disabled."""
    cli = CLI(name="test-cli")
    cli.enable_standard_commands(help=False)

    # Help command should not be registered
    assert "help" not in cli.commands
