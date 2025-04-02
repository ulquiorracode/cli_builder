# CLI Builder

A modern, type-safe CLI framework for Python applications with event-driven architecture.

## Features

- Object-oriented CLI design
- Event-driven architecture with pre/post event listeners
- Type-safe command registration and argument handling
- Modular design with parent-child relationships
- Decorator-based API for easy CLI creation
- Library components for sharing functionality between modules

## Documentation

Full documentation is available in multiple languages:
- [English](docs/en/)
- [Русский](docs/ru/)

## Development Status

This project is currently in alpha stage with core functionality implemented. The latest 0.2.0-alpha release includes the Library decorator for creating non-executable library components.

## Development

1. Clone the repository:
```bash
git clone https://github.com/ulquiorracode/cli_builder.git
cd cli-builder
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On Unix or MacOS
source .venv/bin/activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
# Using the test script
bash run_tests.sh

# Or directly with pytest
pytest
```

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

