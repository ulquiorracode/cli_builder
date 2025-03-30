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

## Documentation

Full documentation is available in multiple languages:

* English
* Русский

## Quick Start

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

## Installation

```
pip install cli-builder
```

## Examples

See the examples directory for usage examples.

## Development

1. Clone the repository:

```
git clone https://github.com/ulquiorracode/cli_builder.git
cd cli-builder
```

2. Install development dependencies:

```
pip install -e ".[dev]"
```

3. Run tests:

```
pytest
```

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details. 