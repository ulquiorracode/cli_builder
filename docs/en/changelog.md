# Changelog

All notable changes to the CLI Builder project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0-alpha] - 2025-04-02

### Added
- New `Library` decorator for creating non-executable library modules
- `CliLibrary` class to implement shared functionality
- Documentation structure using MkDocs
- New examples showcasing decorator usage
- Comprehensive integration tests for libraries
- Improved type checking with mypy

### Changed
- Reorganized project structure for better maintainability:
  - Split cli.py decorator into three files: cli.py, module.py, and library.py
  - Divided base.py class into four files: base.py, core.py, module.py, and library.py
  - Restructured tests into logical subdirectories: cli_base/, decorators/, and events/
- Improved code organization with focused, single-responsibility files
- Enhanced testing approach with more targeted test cases

### Improved
- Achieved 92% test coverage
- Cleaner API design with distinct component types
- Better code quality through smaller, more maintainable components

## [0.1.0] - 2025-04-02

### Added
- Initial project structure
- Basic documentation in English and Russian
- Development environment configuration
- Project metadata and build configuration
- License and contribution guidelines

### Changed
- None (initial release)

### Removed
- None (initial release)

### Fixed
- None (initial release)

### Security
- None (initial release)