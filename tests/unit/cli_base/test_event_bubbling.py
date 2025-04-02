"""
Tests for event bubbling between parent and child components.
"""

from typing import Any, List, Tuple

from cli_builder.cli.base import CliBase
from cli_builder.cli.core import CliCore
from cli_builder.cli.module import CliModule


class TestEventBubbling:
    """Tests for event bubbling between parent and child components."""

    def test_event_bubbles_to_parent(self) -> None:
        """Test that events emitted on a child bubble up to the parent."""
        CliBase.clear_registry()

        # Create parent and child
        parent = CliCore(name="parent")
        child = CliModule(name="child")
        parent.add_child(child)

        # Track events on parent
        parent_events: List[Tuple[Any, str]] = []

        def parent_handler(source: Any, data: str) -> None:
            parent_events.append((source, data))

        # Register handler on parent
        parent.on("test-event", parent_handler)

        # Emit event on child
        data = "test-data"
        child.emit("test-event", child, data)

        # Event should bubble to parent
        assert len(parent_events) == 1
        assert parent_events[0][0] is child
        assert parent_events[0][1] == data

    def test_parent_events_dont_bubble_to_child(self) -> None:
        """Test that events emitted on a parent don't bubble down to children."""
        CliBase.clear_registry()

        # Create parent and child
        parent = CliCore(name="parent")
        child = CliModule(name="child")
        parent.add_child(child)

        # Track events on child
        child_events: List[Tuple[Any, tuple, dict]] = []

        def child_handler(source: Any, *args: Any, **kwargs: Any) -> None:
            child_events.append((source, args, kwargs))

        # Register handler on child
        child.on("test-event", child_handler)

        # Emit event on parent
        parent.emit("test-event", parent, "test-data")

        # Event should NOT bubble to child
        assert len(child_events) == 0
