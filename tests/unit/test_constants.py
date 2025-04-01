"""Tests for constants implementation."""

import pytest

from cli_builder import CLI, CLIConstants, Constant
from cli_builder.constants import ConstantMeta


def test_constant_descriptor():
    """Test that Constant descriptor works correctly."""

    # Create class with ConstantMeta
    class TestConstants(metaclass=ConstantMeta):
        MY_CONSTANT = Constant("test value")

    # Create instance
    test_instance = TestConstants()

    # Check constant access via class
    assert TestConstants.MY_CONSTANT == "test value"

    # Check constant access via instance
    assert test_instance.MY_CONSTANT == "test value"

    # Check that constants can't be changed via class
    with pytest.raises(AttributeError):
        TestConstants.MY_CONSTANT = "new value"

    # Check that constants can't be changed via instance
    with pytest.raises(AttributeError):
        test_instance.MY_CONSTANT = "new value"

    # Verify values haven't changed
    assert TestConstants.MY_CONSTANT == "test value"
    assert test_instance.MY_CONSTANT == "test value"


def test_cli_constants():
    """Test that CLI constants are properly defined."""
    # Check constant values
    assert CLIConstants.DEFAULT_CLI_DESCRIPTION == "No description provided for this CLI"
    assert CLIConstants.DEFAULT_COMMAND_DESCRIPTION == "No description provided for this command"
    assert CLIConstants.COMMAND_DEST == "command"
    assert CLIConstants.HELP_COMMAND_NAME == "help"

    # Check constants can't be changed
    with pytest.raises(AttributeError):
        CLIConstants.DEFAULT_CLI_DESCRIPTION = "New description"

    with pytest.raises(AttributeError):
        CLIConstants.COMMAND_DEST = "cmd"

    with pytest.raises(AttributeError):
        CLIConstants.HELP_COMMAND_NAME = "h"


def test_cli_constants_inheritance():
    """Test that CLI class correctly inherits constants."""
    # Check constants are accessible via CLI class
    assert CLI.DEFAULT_CLI_DESCRIPTION == "No description provided for this CLI"
    assert CLI.DEFAULT_COMMAND_DESCRIPTION == "No description provided for this command"
    assert CLI.COMMAND_DEST == "command"
    assert CLI.HELP_COMMAND_NAME == "help"

    # Create CLI instance
    cli = CLI(name="test-cli")

    # Check constants are accessible via instance
    assert cli.DEFAULT_CLI_DESCRIPTION == "No description provided for this CLI"
    assert cli.DEFAULT_COMMAND_DESCRIPTION == "No description provided for this command"
    assert cli.COMMAND_DEST == "command"
    assert cli.HELP_COMMAND_NAME == "help"

    # Check constants can't be changed via instance
    with pytest.raises(AttributeError):
        cli.DEFAULT_CLI_DESCRIPTION = "New description"

    # Verify values haven't changed
    assert CLI.DEFAULT_CLI_DESCRIPTION == "No description provided for this CLI"
    assert cli.DEFAULT_CLI_DESCRIPTION == "No description provided for this CLI"
