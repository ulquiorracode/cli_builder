"""
CLI package.

This package defines the core classes for building CLI applications:
- CliBase: Abstract base class for all CLI components
- CliCore: Main entry point for a CLI application
- CliModule: A module within a CLI application
- CliLibrary: A library module providing shared functionality
"""

from .base import CliBase
from .core import CliCore
from .library import CliLibrary
from .module import CliModule

__all__ = ["CliBase", "CliCore", "CliModule", "CliLibrary"]
