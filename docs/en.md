# CLI Builder Documentation

## Introduction

CLI Builder is a modern, type-safe CLI framework for Python applications. It provides a simple and intuitive API for creating command-line interfaces with robust argument and option handling.

## Features

- Type hints and validation
- Immutable command configurations
- Private attributes protection
- Decorator-based command registration
- Flexible argument and option handling
- Built-in error handling
- Comprehensive test coverage
- Multiple language support

## Installation

```bash
pip install cli-builder
```

## Quick Start

### Using Decorators

```python
from cli_builder.app import CLI

cli = CLI(name="my-cli", description="My CLI application")

@cli.option("count", short="c", type=int, default=1, help="Number of times to greet")
@cli.argument("name", help="Name to greet")
@cli.command(description="Say hello")
def hello(name: str, count: int = 1) -> None:
    """Simple hello command."""
    for _ in range(count):
        print(f"Hello, {name}!")

if __name__ == "__main__":
    cli.run()
```

### Using Command and CommandConfig

```python
from cli_builder.app import CLI
from cli_builder.app.command import Command
from cli_builder.app.config import CommandConfig

cli = CLI(name="my-cli", description="My CLI application")

# Create command configuration
config = CommandConfig(
    name="hello",
    description="Say hello",
    arguments=[
        {
            "name": "name",
            "type": str,
            "help": "Name to greet",
            "required": True
        }
    ],
    options=[
        {
            "name": "count",
            "short": "c",
            "type": int,
            "help": "Number of times to greet",
            "default": 1
        }
    ]
)

# Create command function
def hello(name: str, count: int = 1) -> None:
    """Simple hello command."""
    for _ in range(count):
        print(f"Hello, {name}!")

# Create and register command
command = Command(config=config, func=hello)
cli.register_command(command)

if __name__ == "__main__":
    cli.run()
```

## Core Concepts

### CLI Instance

The `CLI` class is the main entry point for creating CLI applications.

```python
from cli_builder.app import CLI

cli = CLI(
    name="my-cli",           # Required: The name of the CLI
    description="My CLI",    # Optional: Description of the CLI
    version="1.0.0"          # Optional: Version of the CLI
)
```

### Commands

Commands are registered using the `@cli.command()` decorator.

```python
@cli.command(name="greet", description="Greet someone")
def greet():
    print("Hello, World!")
```

If `name` is not provided, the function name will be used as the command name. If `description` is not provided, the function's docstring will be used if available.

### Arguments

Arguments are registered using the `@cli.argument()` decorator.

```python
@cli.argument("name", type=str, help="Name to greet")
@cli.command(name="greet")
def greet(name: str):
    print(f"Hello, {name}!")
```

### Options

Options are registered using the `@cli.option()` decorator.

```python
@cli.option("count", short="c", type=int, default=1, help="Number of times to greet")
@cli.argument("name", type=str, help="Name to greet")
@cli.command(name="greet")
def greet(name: str, count: int = 1):
    for _ in range(count):
        print(f"Hello, {name}!")
```

## Standard Commands

CLI Builder provides a set of standard commands that can be enabled with a single method call. This makes it easy to include common functionality without having to implement it yourself.

```python
cli = CLI(
    name="my-cli", 
    description="My CLI application", 
    version="1.0.0"
)

# Enable all standard commands
cli.enable_standard_commands(
    help=True,         # Enable help command (default: True)
    version=True,      # Enable version command (default: False)
    list=True,         # Enable list command (default: False)
    completion=True    # Enable completion command (default: False)
)
```

### Help Command

The help command shows a list of available commands and general usage information.

```
$ my-cli help
my-cli - My CLI application

Available commands:
  command1        - Description of command1
  command2        - Description of command2
  help            - Show help information

Use 'my-cli COMMAND --help' for more information on a command.
Use 'my-cli help --detailed' for detailed information on all commands.
```

With the `--detailed` flag, it shows more detailed information about each command, including its arguments and options:

```
$ my-cli help --detailed
my-cli - My CLI application

COMMANDS:

command1
  Description: Description of command1
  Arguments:
    arg1: (str) Help text for arg1
  Options:
    -o, --option1: (int) Help text for option1

command2
  Description: Description of command2
  Arguments:
    arg1: (str) Help text for arg1
    arg2: (int) Help text for arg2
```

### Version Command

The version command shows the version of the CLI application.

```
$ my-cli version
my-cli version 1.0.0
```

### List Command

The list command shows a simple list of available commands, one per line.

```
$ my-cli list
command1
command2
help
list
version
```

### Completion Command

The completion command generates shell completion scripts for various shells.

```
$ my-cli completion --shell bash
# Output: Bash completion script for my-cli

$ my-cli completion --shell zsh
# Output: Zsh completion script for my-cli

$ my-cli completion --shell fish
# Output: Fish completion script for my-cli

$ my-cli completion --shell powershell
# Output: PowerShell completion script for my-cli
```

If no shell is specified, it will attempt to detect the current shell and generate the appropriate script.

## Constants

CLI Builder uses a system of immutable constants for default values and other configuration.

```python
from cli_builder.app import CLI, CLIConstants

# Access constants directly
print(CLIConstants.DEFAULT_CLI_DESCRIPTION)  # "No description provided for this CLI"
print(CLIConstants.DEFAULT_COMMAND_DESCRIPTION)  # "No description provided for this command"
```

These constants are also inherited by the CLI class:

```python
cli = CLI(name="my-cli")
print(cli.DEFAULT_CLI_DESCRIPTION)  # "No description provided for this CLI"
```

## Advanced Usage

For more advanced usage, see the [examples](../examples) directory.

## Automatic Decorators

CLI Builder provides automatic decorators to simplify command creation by inferring arguments and options from function parameters.

### Auto Arguments

The `@cli.auto_arguments` decorator automatically creates arguments from function parameters without default values.

```python
@cli.command()
@cli.auto_arguments
def greet(name: str, title: str):
    """Greet a person.
    
    Args:
        name: Person's name
        title: Person's title
    """
    print(f"Hello, {title} {name}!")
    return 0
```

This creates two arguments: `name` and `title`. The descriptions are extracted from the function's docstring.

### Auto Options

The `@cli.auto_options` decorator automatically creates options from function parameters with default values.

```python
@cli.command()
@cli.auto_options
def format_text(text: str, upper: bool = False, width: int = 10):
    """Format text.
    
    Args:
        text: Text to format
        upper: Convert to uppercase
        width: Output width
    """
    result = text.upper() if upper else text
    result = result.center(width)
    print(f"[{result}]")
    return 0
```

This creates two options: `--upper` and `--width`.

### Auto Command

The `@cli.auto_command()` decorator combines the functionality of `@cli.command()`, `@cli.auto_arguments`, and `@cli.auto_options`:

```python
@cli.auto_command()
def calculate(a: float, b: float, operation: str = "add"):
    """Perform a calculation.
    
    Args:
        a: First number
        b: Second number
        operation: Operation to perform (add, subtract, multiply, divide)
    """
    # Command implementation
```

This creates a command named "calculate" with two arguments (`a` and `b`) and one option (`--operation`).

## API Reference

### CLI Class

```python
class CLI:
    """Base CLI class."""
    
    def __init__(
        self, 
        name: str, 
        description: str = "", 
        version: str = "0.1.0"
    ):
        """Initialize CLI.
        
        Args:
            name: CLI name
            description: CLI description
            version: CLI version
        """
        
    def command(
        self,
        name: Optional[str] = None,
        description: str = "",
        arguments: Optional[List[Dict[str, Any]]] = None,
        options: Optional[List[Dict[str, Any]]] = None
    ) -> Callable:
        """Register a command using decorator."""
        
    def argument(
        self,
        name: str,
        type: Any = str,
        help: str = "",
        nargs: Union[int, str, None] = None,
        choices: Optional[List[Any]] = None,
        default: Any = None
    ) -> Callable:
        """Add an argument to a command."""
        
    def option(
        self,
        name: str,
        short: Optional[str] = None,
        type: Any = str,
        help: str = "",
        choices: Optional[List[Any]] = None,
        default: Any = None,
        required: bool = False,
        is_flag: bool = False
    ) -> Callable:
        """Add an option to a command."""
        
    def run(self, args: Optional[List[str]] = None) -> int:
        """Run CLI with arguments."""
        
    def generate_help(self) -> 'CLI':
        """Enable automatic help command generation."""
        
    def enable_standard_commands(
        self, 
        help: bool = True, 
        version: bool = False, 
        list: bool = False, 
        completion: bool = False
    ) -> None:
        """Enable standard CLI commands."""
```

### Command Class

```python
class Command:
    """Command class representing a CLI command."""
    
    def __init__(
        self,
        name: str,
        description: str = "",
        arguments: List[Dict[str, Any]] = None,
        options: List[Dict[str, Any]] = None,
        func: Callable = None
    ):
        """Initialize command."""
        
    def add_argument(self, arg_data: Dict[str, Any]) -> None:
        """Add an argument to the command."""
        
    def add_option(self, opt_data: Dict[str, Any]) -> None:
        """Add an option to the command."""
        
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Execute command function."""
```

## Compatibility

CLI Builder is compatible with Python 3.8 and above.

## Examples

The [examples](examples/) directory contains usage examples:

### Basic Examples

#### basic_cli.py
A simple example demonstrating basic library usage:
- Creating a CLI application
- Registering simple commands
- Using arguments and options

```bash
# Run hello command
python basic_cli.py hello

# Run greet command with arguments
python basic_cli.py greet John --count 3
```

### Advanced Examples

#### advanced_cli.py
A more complex example showing advanced features:
- Multiple arguments (nargs="+")
- Type validation and conversion
- Flags and optional parameters
- Return values and error handling

```bash
# Calculator
python advanced_cli.py calc add 1 2 3 4 --precision 2
python advanced_cli.py calc mul 2 3 4 --precision 0

# Unit converter
python advanced_cli.py convert 5 km m
python advanced_cli.py convert 1000 g kg --system metric

# Text formatter
python advanced_cli.py format "hello world" --upper
python advanced_cli.py format "hello world" --title --width 5
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cli-builder.git
cd cli-builder
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details. 