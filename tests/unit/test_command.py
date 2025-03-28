"""Tests for Command class."""

from cli_builder.command import Command


def test_command_creation():
    """Test basic command creation."""

    def test_func():
        pass

    command = Command(
        name="test", func=test_func, description="Test command", arguments=[], options=[]
    )

    assert command.name == "test"
    assert command.func == test_func
    assert command.description == "Test command"
    assert command.arguments == []
    assert command.options == []


def test_command_with_arguments():
    """Test command with arguments."""

    def test_func(name: str, count: int):
        pass

    command = Command(
        name="test",
        func=test_func,
        description="Test command",
        arguments=[{"name": "name", "type": str}, {"name": "count", "type": int}],
        options=[],
    )

    assert len(command.arguments) == 2
    assert command.arguments[0]["name"] == "name"
    assert command.arguments[1]["name"] == "count"


def test_command_with_options():
    """Test command with options."""

    def test_func(name: str, count: int = 1):
        pass

    command = Command(
        name="test",
        func=test_func,
        description="Test command",
        arguments=[{"name": "name", "type": str}],
        options=[{"name": "count", "short": "c", "type": int, "default": 1}],
    )

    assert len(command.options) == 1
    assert command.options[0]["name"] == "count"
    assert command.options[0]["short"] == "c"
    assert command.options[0]["type"] == int
    assert command.options[0]["default"] == 1
