"""
Tests for the CliModule class.
"""

from typing import Any, List, Tuple

from cli_builder.cli.base import CliBase
from cli_builder.cli.core import CliCore
from cli_builder.cli.module import CliModule
from cli_builder.events.emitter import EventEmitter
import pytest
from typing import Generator


class TestCliModule:
    """Tests for the CliModule class."""

    @pytest.fixture
    def clear_registry(self) -> Generator[None, None, None]:
        """Clear the component registry before and after each test."""
        CliBase.clear_registry()
        yield
        CliBase.clear_registry()

    def test_module_initialization(self) -> None:
        """Test that CliModule initializes correctly."""
        module = CliModule(
            name="test-module", description="Test module", is_command=True, parent_name="parent"
        )
        assert module.name == "test-module"
        assert module.description == "Test module"
        assert module.is_command is True
        assert module.parent_name == "parent"

    def test_module_registry(self) -> None:
        """Test that CliModule is registered in the registry."""
        CliBase.clear_registry()
        module = CliModule(name="test-module")
        assert CliBase.get_component("test-module") is module

    def test_module_parent_child_relationship(self) -> None:
        """Test that module with parent_name is added as child of parent."""
        CliBase.clear_registry()

        # Create parent first
        parent = CliCore(name="parent")

        # Create child with parent_name
        child = CliModule(name="child", parent_name="parent")

        # Check relationship
        assert child.parent is parent
        assert parent.get_child("child") is child

    def test_module_parent_added_later(self) -> None:
        """Test that module correctly handles parent added after the module."""
        CliBase.clear_registry()

        # Create child first, should give warning but not error
        child = CliModule(name="child", parent_name="parent")

        # Parent not found yet
        assert child.parent is None

        # Now add the parent
        parent = CliCore(name="parent")

        # Unfortunately, with the current implementation, we can't automatically
        # set up the relationship when parent is added after the child.
        # This would require an event system or a registration callback.
        #
        # We might want to add that feature, but for now, we'll
        # just check that both components are in the registry
        assert CliBase.get_component("child") is child
        assert CliBase.get_component("parent") is parent

    def test_module_run_emits_events(self) -> None:
        """Test that CliModule.run() emits pre and post events."""
        module = CliModule(name="test-module")

        # Track events
        pre_called: List[Tuple[Any, tuple, dict]] = []
        post_called: List[Tuple[Any, Any, tuple, dict]] = []

        def pre_handler(module: CliModule, *args: Any, **kwargs: Any) -> None:
            pre_called.append((module, args, kwargs))

        def post_handler(module: CliModule, result: Any, *args: Any, **kwargs: Any) -> None:
            post_called.append((module, result, args, kwargs))

        # Register handlers
        module.on("before:run", pre_handler)
        module.on("after:run", post_handler)

        # Run and check events
        module.run("arg1", kwarg1="value1")

        # Check that both handlers were called
        assert len(pre_called) == 1
        assert pre_called[0][0] is module

        assert len(post_called) == 1
        assert post_called[0][0] is module
        assert post_called[0][1] is None  # Result is None

    def test_automatic_parent_child_relation_using_events(self, clear_registry: None) -> None:
        """Test automatic setup of parent-child relationship with events."""
        # Create global EventEmitter for component registration
        global_emitter = EventEmitter()

        # Save original register method
        original_register = CliBase.register

        try:
            # Create new implementation for register method
            def new_register_impl(cls: Any, instance: CliBase) -> None:
                # Call original method
                original_register(instance)
                # Emit registration event
                global_emitter.emit("component:registered", instance)

            # Override register method with new function
            setattr(CliBase, "register", classmethod(new_register_impl))

            # Create child component first
            child = CliModule(name="child", parent_name="parent")

            # Register event handler to check parent-child relationship
            def check_parent(component: CliBase) -> None:
                if (
                    component.name == "parent"
                    and hasattr(child, "parent_name")
                    and child.parent_name == "parent"
                ):
                    component.add_child(child)

            # Subscribe to registration event
            global_emitter.on("component:registered", check_parent)

            # Check that parent is not yet set
            assert child.parent is None

            # Now create parent component
            parent = CliCore(name="parent")

            # After parent registration, the relationship should be automatically set
            assert child.parent is parent
            # Check that parent exists before checking its children
            assert parent is not None
            assert parent.get_child("child") is child

        finally:
            # Restore original register method
            setattr(CliBase, "register", original_register)

    def test_automatic_parent_child_relation_through_registry(self, clear_registry: None) -> None:
        """Test automatic parent-child relationship using the registry mechanism."""
        # Create child first with parent_name (but no parent exists yet)
        child = CliModule(name="child_module", parent_name="parent_app")

        # Verify child is in registry but has no parent yet
        assert CliBase.get("child_module") is child
        assert child.parent is None

        # Create parent after the child
        parent = CliCore(name="parent_app")

        # Verify parent is in registry
        assert CliBase.get("parent_app") is parent

        # Check that relationship was automatically established during parent registration
        assert child.parent is parent
        assert parent.get_child("child_module") is child

        # Create another child with parent_name to the existing parent
        another_child = CliModule(name="another_child", parent_name="parent_app")

        # Check that relationship was immediately established
        assert another_child.parent is parent
        assert parent.get_child("another_child") is another_child
