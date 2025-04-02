"""
CLI Builder - A modern, type-safe CLI framework for Python applications.
"""

from .cli import CliBase, CliCore, CliLibrary, CliModule
from .decorators import Cli, Library, Module
from .events.emitter import EventEmitter

__version__ = "0.1.0"

__all__ = [
    # Core CLI classes
    "CliBase",
    "CliCore",
    "CliModule",
    "CliLibrary",
    # Decorators
    "Cli",
    "Module",
    "Library",
    # Event system
    "EventEmitter",
    # Package metadata
    "__version__",
]
