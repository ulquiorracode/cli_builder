# CLI Builder (deprecated, watch [rethink](https://github.com/ulquiorracode/cli_builder/edit/main) branch)

A modern, type-safe CLI framework for Python applications.

## Features

* Type hints and validation
* Immutable command configurations
* Private attributes protection
* Decorator-based command registration
* Flexible argument and option handling
* Built-in error handling
* Comprehensive test coverage

## Documentation

Full documentation is available in multiple languages:

* [English](docs/en/readme.md)
* [Русский](docs/ru/readme.md)

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

See the [examples](examples/) directory for usage examples.

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

## Roadmap

Future plans for the CLI Builder project:

* Add support for Fluent API
* Add interactive elements (menus, progress bars, find fields, etc.)
* Create Docker integration for containerized CLI apps
* Implement plugin system for extending functionality
* Add support for configuration files (.ini, .yaml, etc.)
* Improve error messages and debugging capabilities
* Implement localization

See [TODO list](docs/en/todo.md) for more details.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.
