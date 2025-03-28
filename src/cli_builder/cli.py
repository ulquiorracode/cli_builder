"""Base CLI implementation."""

import argparse
import inspect
import os
import platform
import sys
from typing import Any, Callable, Dict, List, Optional, Union, get_type_hints

import attrs

from .command import Command
from .constants import CLIConstants


@attrs.define(slots=True, frozen=True, kw_only=True)
class CLI:
    """Base CLI class."""

    # Constants from CLIConstants
    DEFAULT_CLI_DESCRIPTION = CLIConstants.DEFAULT_CLI_DESCRIPTION
    DEFAULT_COMMAND_DESCRIPTION = CLIConstants.DEFAULT_COMMAND_DESCRIPTION
    COMMAND_DEST = CLIConstants.COMMAND_DEST
    HELP_COMMAND_NAME = CLIConstants.HELP_COMMAND_NAME

    # Public attributes
    name: str = attrs.field()
    description: str = attrs.field(default="")
    auto_generate_help: bool = attrs.field(default=False)
    version: str = attrs.field(default="0.1.0")

    # Private attributes
    _CLI__commands: Dict[str, Command] = attrs.field(factory=dict, init=False)
    _CLI__parser: argparse.ArgumentParser = attrs.field(init=False)
    _CLI__subparsers: argparse._SubParsersAction = attrs.field(init=False)
    _CLI__parsers: Dict[str, argparse.ArgumentParser] = attrs.field(factory=dict, init=False)
    _CLI__temp_args: Dict[str, List[Dict[str, Any]]] = attrs.field(factory=dict, init=False)
    _CLI__temp_opts: Dict[str, List[Dict[str, Any]]] = attrs.field(factory=dict, init=False)
    _CLI__temp_cmd_names: Dict[str, str] = attrs.field(factory=dict, init=False)
    _CLI__help_string: str = attrs.field(default="", init=False)
    _CLI__detailed_help_string: str = attrs.field(default="", init=False)
    _CLI__list_string: str = attrs.field(default="", init=False)

    def __attrs_post_init__(self):
        """Initialize CLI after attrs initialization."""
        # Initialize parser
        object.__setattr__(
            self,
            "_CLI__parser",
            argparse.ArgumentParser(prog=self.name, description=self.description),
        )
        object.__setattr__(
            self,
            "_CLI__subparsers",
            self.__parser.add_subparsers(title="commands", dest=self.COMMAND_DEST, required=False),
        )

    @property
    def commands(self) -> Dict[str, Command]:
        """Get registered commands.

        Returns:
            Dictionary of registered commands
        """
        return dict(self.__commands)

    def register_command(self, command: Command) -> None:
        """Register a command.

        Args:
            command: Command to register
        """
        self.__commands[command.name] = command

        # Update help string if auto_generate_help is enabled
        if self.auto_generate_help:
            self.__update_help_string()

        # Update list string
        self.__update_list_string()

    def generate_help(self) -> "CLI":
        """Enable automatic help command generation.

        Returns:
            Self for method chaining
        """
        object.__setattr__(self, "auto_generate_help", True)
        self.__update_help_string()

        # Register help command immediately if not already registered
        if self.HELP_COMMAND_NAME not in self.__commands:

            @self.command(name=self.HELP_COMMAND_NAME, description="Show help information")
            @self.option(
                "detailed",
                short="d",
                is_flag=True,
                help="Show detailed help with arguments and options",
            )
            def help_cmd(detailed=False) -> int:
                if detailed:
                    print(self.__detailed_help_string)
                else:
                    print(self.__help_string)
                return 0

        return self

    def __update_help_string(self) -> None:
        """Update help strings with current commands."""
        if not self.auto_generate_help:
            return

        # Basic help
        help_text = [f"{self.name} - " f"{self.description or self.DEFAULT_CLI_DESCRIPTION}", ""]
        help_text.append("Available commands:")

        for name, cmd in sorted(self.__commands.items()):
            cmd_desc = cmd.description or self.DEFAULT_COMMAND_DESCRIPTION
            help_text.append(f"  {name:<15} - {cmd_desc}")

        help_text.append("")
        help_text.append(f"Use '{self.name} COMMAND --help' " f"for more information on a command.")
        help_text.append(
            f"Use '{self.name} help --detailed' " f"for detailed information on all commands."
        )

        object.__setattr__(self, "_CLI__help_string", "\n".join(help_text))

        # Detailed help
        detailed_text = [
            f"{self.name} - " f"{self.description or self.DEFAULT_CLI_DESCRIPTION}",
            "",
        ]
        detailed_text.append("COMMANDS:")
        detailed_text.append("")

        for name, cmd in sorted(self.__commands.items()):
            cmd_desc = cmd.description or self.DEFAULT_COMMAND_DESCRIPTION
            detailed_text.append(f"{name}")
            detailed_text.append(f"  Description: {cmd_desc}")

            if cmd.arguments:
                detailed_text.append("  Arguments:")
                for arg in cmd.arguments:
                    arg_name = arg["name"]
                    arg_type = arg.get("type", str).__name__
                    arg_help = arg.get("help", "")
                    detailed_text.append(f"    {arg_name}: ({arg_type}) {arg_help}")

            if cmd.options:
                detailed_text.append("  Options:")
                for opt in cmd.options:
                    opt_name = opt["name"]
                    opt_short = f"-{opt['short']}, " if opt.get("short") else ""
                    is_flag = opt.get("action") == "store_true" or opt.get("is_flag", False)
                    if is_flag:
                        opt_type = "flag"
                    else:
                        opt_type = opt.get("type", str).__name__
                    opt_help = opt.get("help", "")
                    detailed_text.append(f"    {opt_short}--{opt_name}: ({opt_type}) {opt_help}")

            detailed_text.append("")

        object.__setattr__(self, "_CLI__detailed_help_string", "\n".join(detailed_text))

    def __update_list_string(self) -> None:
        """Update the list string with current commands."""
        list_text = []
        for name, _ in sorted(self.__commands.items()):
            list_text.append(name)

        object.__setattr__(self, "_CLI__list_string", "\n".join(list_text))

    def _generate_version_command(self) -> None:
        """Generate version command if not already registered."""
        if "version" in self.__commands:
            return

        @self.command(name="version", description="Show version information")
        def version_cmd() -> int:
            print(f"{self.name} version {self.version}")
            return 0

    def _generate_list_command(self) -> None:
        """Generate list command if not already registered."""
        if "list" in self.__commands:
            return

        @self.command(name="list", description="List available commands")
        def list_cmd() -> int:
            print(self.__list_string)
            return 0

    def _generate_completion_command(self) -> None:
        """Generate command for shell completion scripts."""
        if "completion" in self.__commands:
            return

        @self.command(name="completion", description="Generate shell completion script")
        @self.option("shell", short="s", help="Shell type (bash, zsh, fish, powershell)")
        def completion_cmd(shell: Optional[str] = None) -> int:
            # Auto-detect shell if not specified
            if not shell:
                shell_env = os.environ.get("SHELL", "")
                if shell_env:
                    if "bash" in shell_env:
                        shell = "bash"
                    elif "zsh" in shell_env:
                        shell = "zsh"
                    elif "fish" in shell_env:
                        shell = "fish"
                elif platform.system() == "Windows":
                    shell = "powershell"

                if not shell:
                    print("Could not detect shell type. " "Please specify with --shell option.")
                    return 1

            shell = shell.lower()

            if shell == "bash":
                print(self.__generate_bash_completion())
            elif shell == "zsh":
                print(self.__generate_zsh_completion())
            elif shell == "fish":
                print(self.__generate_fish_completion())
            elif shell in ["powershell", "pwsh"]:
                print(self.__generate_powershell_completion())
            else:
                print(f"Unsupported shell: {shell}")
                print("Supported shells: bash, zsh, fish, powershell")
                return 1

            return 0

    def __generate_bash_completion(self) -> str:
        """Generate bash completion script."""
        cmd_list = " ".join(sorted(self.__commands.keys()))

        completion_script = f"""
# {self.name} bash completion script
_{self.name}_completion() {{
    local cur prev opts
    COMPREPLY=()
    cur="${{COMP_WORDS[COMP_CWORD]}}"
    prev="${{COMP_WORDS[COMP_CWORD-1]}}"

    # Main command completion
    if [ $COMP_CWORD -eq 1 ]; then
        opts="{cmd_list}"
        COMPREPLY=( $(compgen -W "${{opts}}" -- "${{cur}}") )
        return 0
    fi

    # Handle subcommand options
    case "${{prev}}" in
        {self.name})
            opts="{cmd_list}"
            COMPREPLY=( $(compgen -W "${{opts}}" -- "${{cur}}") )
            ;;
        *)
            COMPREPLY=()
            ;;
    esac

    return 0
}}

complete -F _{self.name}_completion {self.name}
"""
        return completion_script

    def __generate_zsh_completion(self) -> str:
        """Generate zsh completion script."""
        cmd_list = "\n        ".join([f"'{cmd}'" for cmd in sorted(self.__commands.keys())])

        completion_script = f"""
#compdef {self.name}

_commands() {{
    local -a commands
    commands=(
        {cmd_list}
    )
    _describe 'command' commands
}}

_arguments \\
    '1: :_commands' \\
    '*::args:->args'
"""
        return completion_script

    def __generate_fish_completion(self) -> str:
        """Generate fish completion script."""
        commands = "\n".join(
            [
                f"complete -c {self.name} -f -n '__fish_use_subcommand' -a {cmd}"
                for cmd in sorted(self.__commands.keys())
            ]
        )

        completion_script = f"""
# {self.name} fish completion script

{commands}
"""
        return completion_script

    def __generate_powershell_completion(self) -> str:
        """Generate PowerShell completion script."""
        cmd_list = ", ".join([f"'{cmd}'" for cmd in sorted(self.__commands.keys())])

        completion_script = f"""
Register-ArgumentCompleter -Native -CommandName {self.name} -ScriptBlock {{
    param($wordToComplete, $commandAst, $cursorPosition)

    $commands = @({cmd_list})

    # Handle command completion
    $cmdElements = $commandAst.CommandElements
    if ($cmdElements.Count -eq 2) {{
        $commands | Where-Object {{ $_ -like "$wordToComplete*" }} |
        ForEach-Object {{
            [System.Management.Automation.CompletionResult]::new(
                $_, $_, 'ParameterValue', $_
            )
        }}
    }}
}}
"""
        return completion_script

    def enable_standard_commands(
        self, help: bool = True, version: bool = False, list: bool = False, completion: bool = False
    ) -> None:
        """Enable standard CLI commands.

        Args:
            help: Enable help command
            version: Enable version command
            list: Enable list command
            completion: Enable shell completion command
        """
        if help:
            self.generate_help()

        if version:
            self._generate_version_command()

        if list:
            self._generate_list_command()

        if completion:
            self._generate_completion_command()

    def command(
        self,
        name: Optional[str] = None,
        description: str = "",
        arguments: Optional[List[Dict[str, Any]]] = None,
        options: Optional[List[Dict[str, Any]]] = None,
    ) -> Callable:
        """Register a command using decorator.

        Args:
            name: Command name (if None, function name will be used)
            description: Command description (if empty, function docstring will be used)
            arguments: List of argument definitions
            options: List of option definitions

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            # If name is not provided, use function name
            cmd_name = name if name is not None else func.__name__
            # If description is not provided, use function docstring
            cmd_desc = description or (func.__doc__ or "").strip()

            # Store command name mapping
            self.__temp_cmd_names[func.__name__] = cmd_name

            # Create command first
            command = Command(
                name=cmd_name, description=cmd_desc, arguments=[], options=[], func=func
            )

            # Add stored arguments and options
            if func.__name__ in self.__temp_args:
                args = list(reversed(self.__temp_args[func.__name__]))
                for arg_data in args:
                    command.add_argument(arg_data)
                del self.__temp_args[func.__name__]

            if func.__name__ in self.__temp_opts:
                opts = list(reversed(self.__temp_opts[func.__name__]))
                for opt_data in opts:
                    command.add_option(opt_data)
                del self.__temp_opts[func.__name__]

            # Add additional arguments and options if provided
            if arguments:
                for arg in arguments:
                    command.add_argument(arg)
            if options:
                for opt in options:
                    command.add_option(opt)

            self.register_command(command)

            # Update command if it was already registered with a different name
            if cmd_name in self.__commands and cmd_name != func.__name__:
                if func.__name__ in self.__temp_args:
                    for arg_data in reversed(self.__temp_args[func.__name__]):
                        self.__commands[cmd_name].add_argument(arg_data)
                if func.__name__ in self.__temp_opts:
                    for opt_data in reversed(self.__temp_opts[func.__name__]):
                        self.__commands[cmd_name].add_option(opt_data)

            return func

        return decorator

    def _extract_param_doc(self, func: Callable, param_name: str) -> str:
        """Extract parameter description from function docstring.

        Args:
            func: Function to extract docstring from
            param_name: Name of the parameter to find

        Returns:
            Parameter description or empty string
        """
        if not func.__doc__:
            return ""

        # Look for ":param param_name:" or "Args:" style docstrings
        doc_lines = func.__doc__.split("\n")

        # Check for reST style
        for i, line in enumerate(doc_lines):
            line = line.strip()
            if line.startswith(f":param {param_name}:"):
                return line.split(":", 2)[2].strip()

        # Check for Google style
        in_args_section = False
        for i, line in enumerate(doc_lines):
            line = line.strip()

            if line.lower() == "args:" or line.lower() == "arguments:":
                in_args_section = True
                continue

            if in_args_section:
                if line.startswith(f"{param_name}:"):
                    return line.split(":", 1)[1].strip()
                # Exit args section if we find an empty line or another section
                elif not line or line.endswith(":"):
                    break

        return ""

    def auto_arguments(self, func: Callable) -> Callable:
        """Automatically create arguments from function parameters without default values.

        Args:
            func: Function to extract parameters from

        Returns:
            Decorated function
        """
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)

        # Store arguments in list to preserve order
        arg_list = []

        # Process parameters without default values
        for name, param in sig.parameters.items():
            if param.default is param.empty:  # No default value
                # Get type from annotation
                param_type = type_hints.get(name, str)
                # Get help from docstring
                param_help = self._extract_param_doc(func, name)

                # Store argument data
                arg_list.append({"name": name, "type": param_type, "help": param_help})

        # Apply argument decorators in reverse order (last one first)
        for arg_data in reversed(arg_list):
            func = self.argument(
                name=arg_data["name"], type=arg_data["type"], help=arg_data["help"]
            )(func)

        return func

    def auto_options(self, func: Callable) -> Callable:
        """Automatically create options from function parameters with default values.

        Args:
            func: Function to extract parameters from

        Returns:
            Decorated function
        """
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)

        # Process parameters with default values
        for name, param in sig.parameters.items():
            if param.default is not param.empty:  # Has default value
                # Get type and value
                param_type = type_hints.get(name, type(param.default))
                is_flag = isinstance(param.default, bool)
                param_help = self._extract_param_doc(func, name)

                # Apply option decorator
                if is_flag:
                    func = self.option(
                        name=name,
                        short=name[0] if len(name) > 1 else None,
                        is_flag=True,
                        help=param_help,
                    )(func)
                else:
                    func = self.option(
                        name=name,
                        short=name[0] if len(name) > 1 else None,
                        type=param_type,
                        default=param.default,
                        help=param_help,
                    )(func)

        return func

    def auto_command(self, description: Optional[str] = None):
        """Automatically create a command with arguments and options.

        This is a convenience decorator that combines command, auto_arguments,
        and auto_options into a single decorator.

        Args:
            description: Command description (if None, function docstring will be used)

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            # Apply decorators in the correct order
            decorated = self.command(description=description)(func)
            decorated = self.auto_arguments(decorated)
            decorated = self.auto_options(decorated)
            return decorated

        return decorator

    def argument(
        self,
        name: str,
        type: Any = str,
        help: str = "",
        nargs: Union[int, str, None] = None,
        choices: Optional[List[Any]] = None,
        default: Any = None,
    ) -> Callable:
        """Add an argument to a command.

        Args:
            name: Argument name
            type: Argument type
            help: Argument help text
            nargs: Argument nargs
            choices: List of allowed choices
            default: Default value

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            cmd_name = func.__name__

            # Check if command name is mapped
            if cmd_name in self.__temp_cmd_names:
                cmd_name = self.__temp_cmd_names[cmd_name]

            # Store argument data temporarily
            if cmd_name not in self.__temp_args:
                self.__temp_args[cmd_name] = []

            arg_data = {
                "name": name,
                "type": type,
                "help": help,
                "nargs": nargs,
                "choices": choices,
                "default": default,
            }

            # If command already exists, add argument directly
            if cmd_name in self.__commands:
                self.__commands[cmd_name].add_argument(arg_data)
            else:
                self.__temp_args[cmd_name].append(arg_data)

            return func

        return decorator

    def option(
        self,
        name: str,
        short: Optional[str] = None,
        type: Any = str,
        help: str = "",
        choices: Optional[List[Any]] = None,
        default: Any = None,
        required: bool = False,
        is_flag: bool = False,
    ) -> Callable:
        """Add an option to a command.

        Args:
            name: Option name
            short: Short option name
            type: Option type
            help: Option help text
            choices: List of allowed choices
            default: Default value
            required: Whether the option is required
            is_flag: Whether the option is a flag

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            cmd_name = func.__name__

            # Check if command name is mapped
            if cmd_name in self.__temp_cmd_names:
                cmd_name = self.__temp_cmd_names[cmd_name]

            # Store option data temporarily
            if cmd_name not in self.__temp_opts:
                self.__temp_opts[cmd_name] = []

            opt_data = {"name": name, "short": short, "help": help, "required": required}

            if is_flag:
                opt_data["action"] = "store_true"
                opt_data["default"] = False
            else:
                opt_data["type"] = type
                opt_data["choices"] = choices
                opt_data["default"] = default

            # If command already exists, add option directly
            if cmd_name in self.__commands:
                self.__commands[cmd_name].add_option(opt_data)
            else:
                self.__temp_opts[cmd_name].append(opt_data)

            return func

        return decorator

    def __setup_command_parser(self, command: Command) -> None:
        """Set up parser for a command.

        Args:
            command: Command to setup parser for
        """
        name = command.name
        description = command.description

        if name not in self.__parsers:
            parser = self.__subparsers.add_parser(name, help=description)
            self.__parsers[name] = parser

            # Add arguments
            for arg in command.arguments:
                kwargs = {k: v for k, v in arg.items() if k not in ["name"] and v is not None}
                parser.add_argument(arg["name"], **kwargs)

            # Add options
            for opt in command.options:
                names = []
                if opt["short"]:
                    names.append(f"-{opt['short']}")
                names.append(f"--{opt['name']}")

                kwargs = {
                    k: v for k, v in opt.items() if k not in ["name", "short"] and v is not None
                }
                parser.add_argument(*names, **kwargs)

    def run(self, args: Optional[List[str]] = None) -> int:
        """Run CLI with arguments.

        Args:
            args: Command line arguments

        Returns:
            Exit code (0 on success)
        """
        if args is None:
            args = sys.argv[1:]

        try:
            # Set up command parsers
            for command in self.__commands.values():
                self.__setup_command_parser(command)

            # Parse arguments
            try:
                parsed_args = self.__parser.parse_args(args)
            except SystemExit:
                return 1

            # Get command
            command_name = getattr(parsed_args, self.COMMAND_DEST)
            if not command_name:
                self.__parser.print_help()
                return 1

            # Get command
            if command_name not in self.__commands:
                print(f"Unknown command: {command_name}", file=sys.stderr)
                return 1

            command = self.__commands[command_name]

            # Convert namespace to dict and remove command
            kwargs = vars(parsed_args)
            del kwargs[self.COMMAND_DEST]

            # Execute command
            result = command(**kwargs)
            return result if isinstance(result, int) else 0

        except Exception as e:
            print(str(e), file=sys.stderr)
            return 1
