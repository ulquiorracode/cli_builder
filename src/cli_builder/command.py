"""Command implementation."""

from typing import Any, Callable, Dict, List
import attrs


@attrs.define(frozen=False, slots=True, kw_only=True)
class Command:
    """Command class representing a CLI command."""

    name: str = attrs.field()
    description: str = attrs.field(default="")
    arguments: List[Dict[str, Any]] = attrs.field(factory=list)
    options: List[Dict[str, Any]] = attrs.field(factory=list)
    func: Callable = attrs.field()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Execute command function.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Command execution result
        """
        return self.func(*args, **kwargs)

    def add_argument(self, arg_data: Dict[str, Any]) -> None:
        """Add an argument to the command.

        Args:
            arg_data: Argument data
        """
        self.arguments.append(arg_data)

    def add_option(self, opt_data: Dict[str, Any]) -> None:
        """Add an option to the command.

        Args:
            opt_data: Option data
        """
        self.options.append(opt_data)

    def freeze(self) -> None:
        """Freeze command configuration."""
        object.__setattr__(self, "arguments", tuple(self.arguments))
        object.__setattr__(self, "options", tuple(self.options))
