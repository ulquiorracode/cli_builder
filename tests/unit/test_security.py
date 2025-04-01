"""Tests for security features."""

import pytest

from cli_builder.command import Command


def test_command_slots():
    """Test that Command uses slots."""
    command = Command(
        name="test", description="Test command", arguments=[], options=[], func=lambda: None
    )

    with pytest.raises(AttributeError):
        command.new_attribute = "test"


def test_command_mutability():
    """Test that Command instances are mutable before freezing."""
    command = Command(
        name="test", description="Test command", arguments=[], options=[], func=lambda: None
    )

    # Test that we can modify attributes
    command.add_argument({"name": "test_arg"})
    command.add_option({"name": "test_opt"})

    assert len(command.arguments) == 1
    assert len(command.options) == 1


def test_command_freeze():
    """Test that Command can be frozen."""
    command = Command(
        name="test", description="Test command", arguments=[], options=[], func=lambda: None
    )

    # Add some arguments and options
    command.add_argument({"name": "arg1", "help": "Test argument"})
    command.add_option({"name": "opt1", "help": "Test option"})

    # Freeze the command
    command.freeze()

    # Verify attributes are tuples
    assert isinstance(command.arguments, tuple)
    assert isinstance(command.options, tuple)

    # Try to modify frozen attributes
    with pytest.raises((AttributeError, TypeError)):
        command.arguments.append({"name": "test"})

    with pytest.raises((AttributeError, TypeError)):
        command.options.append({"name": "test"})
