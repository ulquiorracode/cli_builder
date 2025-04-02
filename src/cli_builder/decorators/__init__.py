"""
Decorators package.

This package provides decorators for creating CLI components:
- Cli: Creates CliCore instances (main CLI applications)
- Module: Creates CliModule instances (executable modules)
- Library: Creates CliLibrary instances (utility libraries)
"""

from .cli import Cli
from .library import Library
from .module import Module

__all__ = ["Cli", "Module", "Library"]
