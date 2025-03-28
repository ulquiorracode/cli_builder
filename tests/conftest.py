"""Common test fixtures."""

import pytest
from cli_builder import CLI


@pytest.fixture
def cli():
    """Create a basic CLI instance."""
    return CLI("test", "Test CLI")
