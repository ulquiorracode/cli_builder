"""
Pytest configuration file.

This file contains fixtures and configuration for pytest.
"""

from typing import Any, Generator

import pytest

from cli_builder.cli.base import CliBase


@pytest.fixture(autouse=True)
def clear_registry_after_test() -> Generator[Any, Any, Any]:
    """
    Automatically clear the registry after each test.

    This ensures that tests don't interfere with each other
    through the global registry.
    """
    # Run the test
    yield

    # Clear the registry after the test
    CliBase.clear_registry()
