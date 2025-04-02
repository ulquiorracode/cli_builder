"""
Tests for the Cli decorator.
"""

from typing import Generator, List

import pytest

from cli_builder.cli.base import CliBase
from cli_builder.cli.core import CliCore
from cli_builder.decorators.cli import Cli


@pytest.fixture
def clear_registry() -> Generator[None, None, None]:
    """Clear the component registry before and after each test."""
    CliBase.clear_registry()
    yield
    CliBase.clear_registry()


class TestCliDecorator:
    """Tests for the Cli decorator."""

    def test_cli_decorator_with_arguments(self, clear_registry: None) -> None:
        """Test that Cli decorator works with arguments."""

        @Cli("test-app", description="Test app", version="1.0.0")
        class TestApp:
            def run_custom(self) -> str:
                return "custom"

        # Should be transformed into a CliCore instance
        assert isinstance(TestApp, CliCore)
        assert TestApp.name == "test-app"
        assert TestApp.description == "Test app"
        assert TestApp.version == "1.0.0"

        # Methods should be transferred
        assert hasattr(TestApp, "run_custom")
        assert TestApp.run_custom() == "custom"

        # Should be in the registry
        assert CliBase.get_component("test-app") is TestApp

    def test_cli_decorator_without_arguments(self, clear_registry: None) -> None:
        """Test that Cli decorator works without arguments."""

        @Cli
        class TestApp:
            def run_custom(self) -> str:
                return "custom"

        # Should be transformed into a CliCore instance
        assert isinstance(TestApp, CliCore)
        assert TestApp.name == "TestApp"  # Name from class name
        assert TestApp.description is None
        assert TestApp.version == "0.1.0"  # Default version

        # Methods should be transferred
        assert hasattr(TestApp, "run_custom")
        assert TestApp.run_custom() == "custom"

        # Should be in the registry
        assert CliBase.get_component("TestApp") is TestApp

    def test_cli_decorator_preserves_init(self, clear_registry: None) -> None:
        """Test that Cli decorator preserves __init__ method."""

        init_called: List[bool] = []

        @Cli("test-app")
        class TestApp:
            def __init__(self) -> None:
                init_called.append(True)

        # Should be transformed into a CliCore instance
        assert isinstance(TestApp, CliCore)
        assert TestApp.name == "test-app"

        # Check that __init__ was called
        assert len(init_called) == 1
