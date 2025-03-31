# Contributing to CLI Builder

Thank you for your interest in contributing to the CLI Builder project! This document provides information on how to contribute to the project's development.

## Reporting Issues

If you've found a bug or have a suggestion for improvement:

1. Check if the issue has already been reported in the GitHub Issues.
2. If not, create a new issue with a detailed description of the problem or suggestion.
3. Include information about your environment (Python version, operating system).
4. If possible, provide a minimal reproducible example.

## Making Changes

1. Fork the repository and clone it to your local machine.
2. Create a new branch for your changes:
   ```
   git checkout -b feature/feature-name
   ```
   or
   ```
   git checkout -b fix/fix-name
   ```
3. Install development dependencies:
   ```
   pip install -e ".[dev]"
   ```
4. Make your changes.
5. Ensure your code follows the project's style guidelines:
   ```
   black src tests examples
   isort src tests examples
   flake8 src tests examples
   ```
6. Make sure all tests pass:
   ```
   pytest
   ```
7. Add new tests for your functionality.
8. Commit your changes and push to your fork:
   ```
   git push origin feature/feature-name
   ```
9. Create a Pull Request to the main repository.

## Code Style

- Follow PEP 8 and use Black for code formatting.
- Add type hints for all new functions.
- Write docstrings for new classes and methods.
- Comment complex parts of code.

## Documentation

- If you add new functionality, update the corresponding documentation.
- For complex features, consider adding usage examples.

## Testing

- New functionality should be covered by tests.
- Aim for at least 90% test coverage for new code.
- Use fixtures and mocking where appropriate.

## Review Process

1. Your code will be automatically checked by CI/CD for style conformance and test passing.
2. Project maintainers will review your code and may request changes.
3. Once approved, your PR will be merged into the main branch.

## License

By contributing to the project, you agree that your code will be distributed under the GPL-3.0 license.

Thank you for contributing to CLI Builder! 