"""
Tests for the Module decorator.
"""

from typing import Generator

import pytest

from cli_builder.cli.base import CliBase
from cli_builder.cli.module import CliModule
from cli_builder.decorators.cli import Cli
from cli_builder.decorators.module import Module


@pytest.fixture
def clear_registry() -> Generator[None, None, None]:
    """Clear the component registry before and after each test."""
    CliBase.clear_registry()
    yield
    CliBase.clear_registry()


class TestModuleDecorator:
    """Tests for the Module decorator."""

    def test_module_decorator_with_arguments(self, clear_registry: None) -> None:
        """Test that Module decorator works with arguments."""

        @Module("test-module", description="Test module", is_command=True)
        class TestModule:
            def run_custom(self) -> str:
                return "custom"

        # Should be transformed into a CliModule instance
        assert isinstance(TestModule, CliModule)
        assert TestModule.name == "test-module"
        assert TestModule.description == "Test module"
        assert TestModule.is_command is True

        # Methods should be transferred
        assert hasattr(TestModule, "run_custom")
        assert TestModule.run_custom() == "custom"

        # Should be in the registry
        assert CliBase.get_component("test-module") is TestModule

    def test_module_decorator_without_arguments(self, clear_registry: None) -> None:
        """Test that Module decorator works without arguments."""

        @Module
        class TestModule:
            def run_custom(self) -> str:
                return "custom"

        # Should be transformed into a CliModule instance
        assert isinstance(TestModule, CliModule)
        assert TestModule.name == "TestModule"  # Name from class name
        assert TestModule.description is None
        assert TestModule.is_command is True  # Default is_command

        # Methods should be transferred
        assert hasattr(TestModule, "run_custom")
        assert TestModule.run_custom() == "custom"

        # Should be in the registry
        assert CliBase.get_component("TestModule") is TestModule

    def test_module_with_parent_name(self, clear_registry: None) -> None:
        """Test that Module with parent_name is added as child of parent."""

        # Create parent first
        @Cli("parent")
        class Parent:
            pass

        # Create child with parent_name
        @Module("child", parent_name="parent")
        class Child:
            pass

        # Check relationship
        assert Child.parent is Parent
        assert Parent.get_child("child") is Child

    def test_module_with_parent_name_added_later(self, clear_registry: None) -> None:
        """Test that Module correctly handles parent added after the module."""

        # Create child first
        @Module("child", parent_name="parent")
        class Child:
            pass

        # Parent not found yet (shows warning)
        assert Child.parent is None

        # Create parent later
        @Cli("parent")
        class Parent:
            pass

        # With our new implementation, the relationship IS automatically established
        # when the parent is registered after the child
        assert Child.parent is Parent
        assert Parent.get_child("child") is Child
