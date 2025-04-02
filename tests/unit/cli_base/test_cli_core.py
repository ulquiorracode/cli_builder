"""
Tests for the CliCore class.
"""

from typing import Any, List, Tuple

from cli_builder.cli.base import CliBase
from cli_builder.cli.core import CliCore


class TestCliCore:
    """Tests for the CliCore class."""

    def test_core_initialization(self) -> None:
        """Test that CliCore initializes correctly."""
        core = CliCore(name="test-app", description="Test app", version="1.0.0")
        assert core.name == "test-app"
        assert core.description == "Test app"
        assert core.version == "1.0.0"

    def test_core_registry(self) -> None:
        """Test that CliCore is registered in the registry."""
        CliBase.clear_registry()
        core = CliCore(name="test-app")
        assert CliBase.get_component("test-app") is core

    def test_core_run_emits_events(self) -> None:
        """Test that CliCore.run() emits pre and post events."""
        core = CliCore(name="test-app")

        # Track events
        pre_called: List[Tuple[Any, tuple, dict]] = []
        post_called: List[Tuple[Any, Any, tuple, dict]] = []

        def pre_handler(core: CliCore, *args: Any, **kwargs: Any) -> None:
            pre_called.append((core, args, kwargs))

        def post_handler(core: CliCore, result: Any, *args: Any, **kwargs: Any) -> None:
            post_called.append((core, result, args, kwargs))

        # Register handlers
        core.on("before:run", pre_handler)
        core.on("after:run", post_handler)

        # Run and check events
        core.run("arg1", kwarg1="value1")

        # Check that both handlers were called
        assert len(pre_called) == 1
        assert pre_called[0][0] is core

        assert len(post_called) == 1
        assert post_called[0][0] is core
        assert post_called[0][1] is None  # Result is None
