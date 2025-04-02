"""
Tests for the CliLibrary class.
"""

from typing import Any, List, Tuple

from cli_builder.cli.base import CliBase
from cli_builder.cli.core import CliCore
from cli_builder.cli.library import CliLibrary


class TestCliLibrary:
    """Tests for the CliLibrary class."""

    def test_library_initialization(self) -> None:
        """Test that CliLibrary initializes correctly."""
        library = CliLibrary(name="test-lib", description="Test library", parent_name="parent")
        assert library.name == "test-lib"
        assert library.description == "Test library"
        assert library.parent_name == "parent"

    def test_library_registry(self) -> None:
        """Test that CliLibrary is registered in the registry."""
        CliBase.clear_registry()
        library = CliLibrary(name="test-lib")
        assert CliBase.get_component("test-lib") is library

    def test_library_parent_child_relationship(self) -> None:
        """Test that library with parent_name is added as child of parent."""
        CliBase.clear_registry()

        # Create parent first
        parent = CliCore(name="parent")

        # Create library with parent_name
        lib = CliLibrary(name="lib", parent_name="parent")

        # Check relationship
        assert lib.parent is parent
        assert parent.get_child("lib") is lib

    def test_library_run_does_nothing(self) -> None:
        """Test that CliLibrary.run() does nothing but emits events."""
        library = CliLibrary(name="test-lib")

        # Track events
        pre_called: List[Tuple[Any, tuple, dict]] = []
        post_called: List[Tuple[Any, Any, tuple, dict]] = []

        def pre_handler(lib: CliLibrary, *args: Any, **kwargs: Any) -> None:
            pre_called.append((lib, args, kwargs))

        def post_handler(lib: CliLibrary, result: Any, *args: Any, **kwargs: Any) -> None:
            post_called.append((lib, result, args, kwargs))

        # Register handlers
        library.on("before:run", pre_handler)
        library.on("after:run", post_handler)

        # Run and check events
        result = library.run("arg1", kwarg1="value1")

        # Check that both handlers were called
        assert len(pre_called) == 1
        assert pre_called[0][0] is library

        assert len(post_called) == 1
        assert post_called[0][0] is library
        assert post_called[0][1] is None  # Result should always be None

        # Result should be None
        assert result is None
