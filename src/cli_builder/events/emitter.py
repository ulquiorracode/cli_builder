"""
Event emitter for CLI Builder.

This module provides a simple event emitter implementation
that supports pre- and post-event listeners.
"""

from collections import defaultdict
from typing import Any, Callable, Dict, List, Set, Tuple

# Type for event listeners
EventListener = Callable[..., Any]


class EventEmitter:
    """
    Implements a simple event emitter with pre- and post-event listeners.

    Events can have two types of listeners:
    - Pre-event listeners: Called before the event is processed
    - Post-event listeners: Called after the event is processed

    This allows for middleware-like patterns where listeners can modify
    the event data or perform actions before or after the event occurs.
    """

    def __init__(self) -> None:
        """Initialize the event emitter with empty listener dictionaries."""
        # Dictionary to store pre-event listeners
        self._pre_listeners: Dict[str, List[EventListener]] = defaultdict(list)

        # Dictionary to store post-event listeners
        self._post_listeners: Dict[str, List[EventListener]] = defaultdict(list)

        # Dictionary to store one-time listeners
        self._once_listeners: Dict[str, Set[EventListener]] = defaultdict(set)

    def on(self, event: str, listener: EventListener, *, is_pre: bool = False) -> None:
        """
        Register an event listener.

        Args:
            event: The event name
            listener: The listener function
            is_pre: Whether this is a pre-event listener
        """
        if is_pre:
            self._pre_listeners[event].append(listener)
        else:
            self._post_listeners[event].append(listener)

    def off(self, event: str, listener: EventListener, *, is_pre: bool = False) -> None:
        """
        Remove an event listener.

        Args:
            event: The event name
            listener: The listener to remove
            is_pre: Whether this is a pre-event listener
        """
        if is_pre:
            if event in self._pre_listeners:
                try:
                    self._pre_listeners[event].remove(listener)
                except ValueError:
                    pass
        else:
            if event in self._post_listeners:
                try:
                    self._post_listeners[event].remove(listener)
                except ValueError:
                    pass

        # Also check once listeners
        if event in self._once_listeners:
            self._once_listeners[event].discard(listener)

    def once(self, event: str, listener: EventListener, *, is_pre: bool = False) -> None:
        """
        Register a one-time event listener.

        Args:
            event: The event name
            listener: The listener function
            is_pre: Whether this is a pre-event listener
        """
        self.on(event, listener, is_pre=is_pre)
        self._once_listeners[event].add(listener)

    def emit(self, event: str, *args: Any, **kwargs: Any) -> bool:
        """
        Emit an event with the given arguments.

        Args:
            event: The event name
            *args: Positional arguments to pass to listeners
            **kwargs: Keyword arguments to pass to listeners

        Returns:
            True if the event had listeners, False otherwise
        """
        has_listeners = False

        # Call pre-event listeners
        if event in self._pre_listeners:
            has_listeners = True
            self._call_listeners(event, self._pre_listeners[event], args, kwargs)

        # Call post-event listeners
        if event in self._post_listeners:
            has_listeners = True
            self._call_listeners(event, self._post_listeners[event], args, kwargs)

        return has_listeners

    def _call_listeners(
        self,
        event: str,
        listeners: List[EventListener],
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
    ) -> None:
        """
        Call listeners for an event.

        Args:
            event: The event name
            listeners: The list of listeners to call
            args: Positional arguments to pass to listeners
            kwargs: Keyword arguments to pass to listeners
        """
        # Create a copy of the listeners list to avoid modification during iteration
        for listener in listeners.copy():
            listener(*args, **kwargs)

            # Remove one-time listeners after they've been called
            if event in self._once_listeners and listener in self._once_listeners[event]:
                self._once_listeners[event].discard(listener)
                try:
                    listeners.remove(listener)
                except ValueError:
                    pass

    def listeners(self, event: str, *, is_pre: bool = False) -> List[EventListener]:
        """
        Get all listeners for an event.

        Args:
            event: The event name
            is_pre: Whether to get pre-event listeners

        Returns:
            List of listener functions
        """
        if is_pre:
            return self._pre_listeners[event].copy()
        else:
            return self._post_listeners[event].copy()

    def event_names(self) -> Set[str]:
        """
        Get all event names that have listeners.

        Returns:
            Set of event names
        """
        # Combine keys from both pre and post listeners
        return set(self._pre_listeners.keys()) | set(self._post_listeners.keys())
