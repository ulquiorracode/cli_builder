# CLI Builder

A modern, type-safe CLI framework for Python applications.

## Features

* Type hints and validation
* Immutable command configurations
* Private attributes protection
* Decorator-based command registration
* Flexible argument and option handling
* Built-in error handling
* Comprehensive test coverage
* Multiple language support

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

## Automatic Decorators

CLI Builder provides automatic decorators to simplify command creation:

```python
@cli.auto_command()
def calculate(a: float, b: float, operation: str = "add"):
    """Perform a calculation.
    
    Args:
        a: First number
        b: Second number
        operation: Operation to perform (add, subtract, multiply, divide)
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            print("Error: Division by zero")
            return 1
        result = a / b
    else:
        print(f"Unknown operation: {operation}")
        return 1
        
    print(f"Result: {result}")
    return 0
```

## Standard Commands

CLI Builder provides a set of standard commands that can be enabled with a single method call:

```python
cli = CLI(
    name="my-cli", 
    description="My CLI application", 
    version="1.0.0"
)

# Enable all standard commands
cli.enable_standard_commands(
    help=True,         # Enable help command
    version=True,      # Enable version command
    list=True,         # Enable list command
    completion=True    # Enable completion command
)
```

## Examples

See the [examples](../examples/) directory for usage examples.

## Development

1. Clone the repository:

```bash
git clone https://github.com/ulquiorracode/cli_builder.git
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

## Roadmap

See the [TODO list](todo.md) for planned features and improvements.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](../../LICENSE) file for details. 