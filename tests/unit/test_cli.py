"""Tests for CLI implementation."""

from cli_builder import CLI
from cli_builder.command import Command


def test_cli_creation():
    """Test basic CLI creation."""
    cli = CLI(name="test", description="Test CLI")
    assert cli.name == "test"
    assert cli.description == "Test CLI"


def test_command_registration():
    """Test command registration."""
    cli = CLI(name="test", description="Test CLI")

    @cli.command(name="test", description="Test command")
    def test_command():
        return "test"

    assert "test" in cli.commands
    assert cli.commands["test"].name == "test"
    assert cli.commands["test"].description == "Test command"


def test_command_with_arguments():
    """Test command with arguments."""
    cli = CLI(name="test", description="Test CLI")

    @cli.command(name="test", description="Test command")
    @cli.argument("arg1", type=str)
    @cli.argument("arg2", type=int)
    def test_command(arg1: str, arg2: int):
        return f"{arg1} {arg2}"

    command = cli.commands["test"]
    assert len(command.arguments) == 2
    assert command.arguments[0]["name"] == "arg1"
    assert command.arguments[1]["name"] == "arg2"


def test_command_with_options():
    """Test command with options."""
    cli = CLI(name="test", description="Test CLI")

    @cli.command(name="test", description="Test command")
    @cli.option("opt1", short="o", type=str)
    @cli.option("opt2", type=bool)
    def test_command(opt1: str = None, opt2: bool = False):
        return f"{opt1} {opt2}"

    command = cli.commands["test"]
    assert len(command.options) == 2
    assert command.options[0]["name"] == "opt1"
    assert command.options[1]["name"] == "opt2"


def test_command_execution():
    """Test command execution."""
    cli = CLI(name="test", description="Test CLI")

    @cli.command(name="test", description="Test command")
    @cli.argument("arg1", type=str)
    @cli.option("opt1", short="o", type=str)
    def test_command(arg1: str, opt1: str = None):
        return f"{arg1} {opt1}"

    result = cli.run(["test", "value", "--opt1", "option"])
    assert result == 0


def test_unknown_command():
    """Test handling of unknown command."""
    cli = CLI(name="test", description="Test CLI")

    @cli.command(name="test", description="Test command")
    def test_command():
        return "test"

    result = cli.run(["unknown"])
    assert result == 1


def test_decorator_order():
    """Test different decorator orders."""
    cli = CLI(name="test", description="Test CLI")

    # Command first, then arguments and options
    @cli.command(name="test1", description="Test command 1")
    @cli.argument("arg1", type=str)
    @cli.option("opt1", short="o", type=str)
    def test_command1(arg1: str, opt1: str = None):
        return f"{arg1} {opt1}"

    # Arguments and options first, then command
    @cli.argument("arg1", type=str)
    @cli.option("opt1", short="o", type=str)
    @cli.command(name="test2", description="Test command 2")
    def test_command2(arg1: str, opt1: str = None):
        return f"{arg1} {opt1}"

    # Arguments first, then command, then options
    @cli.argument("arg1", type=str)
    @cli.command(name="test3", description="Test command 3")
    @cli.option("opt1", short="o", type=str)
    def test_command3(arg1: str, opt1: str = None):
        return f"{arg1} {opt1}"

    # Check all commands are registered
    assert "test1" in cli.commands
    assert "test2" in cli.commands
    assert "test3" in cli.commands

    # Check arguments and options are properly set
    for cmd_name in ["test1", "test2", "test3"]:
        command = cli.commands[cmd_name]
        assert len(command.arguments) == 1
        assert len(command.options) == 1
        assert command.arguments[0]["name"] == "arg1"
        assert command.options[0]["name"] == "opt1"


def test_command_direct_registration():
    """Test command registration without decorators."""
    cli = CLI(name="test", description="Test CLI")

    # Create command
    command = Command(
        name="test",
        description="Test command",
        arguments=[{"name": "arg1", "type": str, "help": "First argument"}],
        options=[{"name": "opt1", "short": "o", "type": str, "help": "First option"}],
        func=lambda arg1, opt1=None: 0,
    )

    # Register command
    cli.register_command(command)

    # Check command is registered
    assert "test" in cli.commands
    assert cli.commands["test"].name == "test"
    assert cli.commands["test"].description == "Test command"
    assert len(cli.commands["test"].arguments) == 1
    assert len(cli.commands["test"].options) == 1
