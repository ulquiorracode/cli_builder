"""
Tests for the EventEmitter class.
"""

from typing import Any, List

from cli_builder.events.emitter import EventEmitter


def test_emitter_initialization() -> None:
    """Test that EventEmitter initializes correctly."""
    emitter = EventEmitter()
    assert emitter is not None
    assert not emitter.event_names()


def test_add_listener() -> None:
    """Test that listeners can be added."""
    emitter = EventEmitter()

    # Define a simple listener
    def listener(data: Any) -> None:
        pass

    # Add the listener for a test event
    emitter.on("test", listener)

    # Check that the event was registered
    assert "test" in emitter.event_names()
    assert listener in emitter.listeners("test")

    # Check that pre-listeners work too
    emitter.on("pre-test", listener, is_pre=True)
    assert "pre-test" in emitter.event_names()
    assert listener in emitter.listeners("pre-test", is_pre=True)


def test_remove_listener() -> None:
    """Test that listeners can be removed."""
    emitter = EventEmitter()

    # Define a simple listener
    def listener(data: Any) -> None:
        pass

    # Add and then remove the listener
    emitter.on("test", listener)
    assert listener in emitter.listeners("test")

    emitter.off("test", listener)
    assert listener not in emitter.listeners("test")

    # Test removing a non-existent listener doesn't raise
    emitter.off("test", listener)  # Should not raise

    # Test removing from a non-existent event doesn't raise
    emitter.off("non-existent", listener)  # Should not raise


def test_once_listener() -> None:
    """Test that once listeners are called only once."""
    emitter = EventEmitter()

    # Use a list to track call count
    call_count: List[str] = []

    def listener(data: str) -> None:
        call_count.append(data)

    # Register as a one-time listener
    emitter.once("test", listener)

    # Emit twice
    emitter.emit("test", "first")
    emitter.emit("test", "second")

    # Should only be called once
    assert len(call_count) == 1
    assert call_count[0] == "first"

    # Listener should be removed after being called
    assert listener not in emitter.listeners("test")


def test_emit_calls_listeners() -> None:
    """Test that emit calls all registered listeners."""
    emitter = EventEmitter()

    # Track calls from different listeners
    pre_calls: List[str] = []
    post_calls: List[str] = []

    def pre_listener(data: str) -> None:
        pre_calls.append(data)

    def post_listener(data: str) -> None:
        post_calls.append(data)

    # Register listeners
    emitter.on("test", pre_listener, is_pre=True)
    emitter.on("test", post_listener)

    # Emit the event
    emitter.emit("test", "data")

    # Check that both listeners were called
    assert len(pre_calls) == 1
    assert pre_calls[0] == "data"
    assert len(post_calls) == 1
    assert post_calls[0] == "data"


def test_emit_returns_boolean() -> None:
    """Test that emit returns a boolean indicating if listeners were called."""
    emitter = EventEmitter()

    # Define a simple listener
    def listener(data: Any) -> None:
        pass

    # No listeners for this event yet
    assert not emitter.emit("test", "data")

    # Add a listener
    emitter.on("test", listener)

    # Now emit should return True
    assert emitter.emit("test", "data")


def test_multiple_listeners() -> None:
    """Test that multiple listeners can be registered for the same event."""
    emitter = EventEmitter()

    # Track calls from different listeners
    calls_1: List[str] = []
    calls_2: List[str] = []

    def listener_1(data: str) -> None:
        calls_1.append(data)

    def listener_2(data: str) -> None:
        calls_2.append(data)

    # Register multiple listeners
    emitter.on("test", listener_1)
    emitter.on("test", listener_2)

    # Emit the event
    emitter.emit("test", "data")

    # Both listeners should have been called
    assert len(calls_1) == 1
    assert calls_1[0] == "data"
    assert len(calls_2) == 1
    assert calls_2[0] == "data"
