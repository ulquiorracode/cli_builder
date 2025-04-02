"""
Tests for the Library decorator.
"""

from typing import Generator

import pytest

from cli_builder.cli.base import CliBase
from cli_builder.cli.library import CliLibrary
from cli_builder.decorators.cli import Cli
from cli_builder.decorators.library import Library


@pytest.fixture
def clear_registry() -> Generator[None, None, None]:
    """Clear the component registry before and after each test."""
    CliBase.clear_registry()
    yield
    CliBase.clear_registry()


class TestLibraryDecorator:
    """Tests for the Library decorator."""

    def test_library_decorator_with_arguments(self, clear_registry: None) -> None:
        """Test that Library decorator works with arguments."""

        @Library("test-lib", description="Test library")
        class TestLibrary:
            def get_value(self) -> str:
                return "value"

        # Should be transformed into a CliLibrary instance
        assert isinstance(TestLibrary, CliLibrary)
        assert TestLibrary.name == "test-lib"
        assert TestLibrary.description == "Test library"
        assert hasattr(TestLibrary, "get_value")
        assert TestLibrary.get_value() == "value"

    def test_library_decorator_without_arguments(self, clear_registry: None) -> None:
        """Test that Library decorator works without arguments."""

        @Library
        class TestLibrary:
            def get_value(self) -> str:
                return "value"

        # Should be transformed into a CliLibrary instance
        assert isinstance(TestLibrary, CliLibrary)
        assert TestLibrary.name == "TestLibrary"
        assert TestLibrary.description is None
        assert hasattr(TestLibrary, "get_value")
        assert TestLibrary.get_value() == "value"

    def test_library_with_parent_name(self, clear_registry: None) -> None:
        """Test that Library with parent_name is added as child of parent."""

        # Create parent first
        @Cli("parent")
        class Parent:
            pass

        # Create library with parent_name
        @Library("util", parent_name="parent")
        class Util:
            def helper(self) -> str:
                return "helper"

        # Check relationship
        assert Util.parent is Parent
        assert Parent.get_child("util") is Util
        assert Util.helper() == "helper"

    def test_library_and_module_siblings(self, clear_registry: None) -> None:
        """Test that Library and Module can be siblings under the same parent."""

        from cli_builder.decorators.module import Module

        @Cli("app")
        class App:
            pass

        @Module("command", parent_name="app")
        class Command:
            def run(self) -> str:
                # Use library helper
                lib = self.parent.get_child("util")
                return lib.helper()

        @Library("util", parent_name="app")
        class Util:
            def helper(self) -> str:
                return "helper result"

        # Check hierarchy
        assert Command.parent is App
        assert Util.parent is App
        assert App.get_child("command") is Command
        assert App.get_child("util") is Util

        # Test interaction
        assert Command.run() == "helper result"
