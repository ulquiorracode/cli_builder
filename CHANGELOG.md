# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-03-29 (UTC 10:00)

### Added
- Added `auto_arguments` decorator to automatically generate arguments from function parameters
- Added `auto_options` decorator to automatically generate options from function parameters with defaults
- Added `auto_command` convenience decorator that combines command, auto_arguments, and auto_options
- Added support for automatic parameter help text extraction from function docstrings
- New example file demonstrating usage of automatic decorators

### Changed
- Made `name` parameter optional in `command` decorator - now uses function name by default
- Improved docstring processing to extract parameter descriptions for help text

## [0.4.1] - 2025-03-29 (UTC 06:30)

### Changed
- Simplified project structure by removing the `app` subdirectory
- Improved code formatting according to PEP 8 standards
- Added shebang lines to all example scripts
- Moved `conftest.py` from `tests/unit/` to `tests/` root directory

### Fixed
- Fixed string formatting in tests to avoid multiline string comparison issues
- Fixed imports to reference relocated modules correctly
- Corrected decorator formatting for better readability

### Removed
- Removed obsolete `command_config_example.py` that used deprecated API
- Removed unused `shlex` import

## [0.4.0] - 2025-03-29 (UTC 01:30)

### Added
- Standard command system with `enable_standard_commands()` method
- Automatic help command with detailed view option (`help --detailed`)
- Version command for displaying CLI version information
- List command for simple command listing
- Shell completion command for generating auto-completion scripts (bash, zsh, fish, PowerShell)
- New examples demonstrating standard commands usage
- True constants implementation using descriptors and metaclasses
- Semantic constants with specific context (CLI vs command)

### Changed
- Improved command help text generation with better contextual defaults
- Enhanced help output with more detailed instructions
- Reorganized internal code structure for better maintainability
- New testing structure for the standard command system

### Fixed
- Proper handling of missing or empty descriptions
- Command sorting in help display for better readability

## [0.3.1] - 2025-03-29 (UTC 00:30)

### Fixed
- Corrected argument order in basic example
- Fixed tests to match actual CLI behavior with error handling
- Consolidated duplicate examples into a single file

## [0.3.0] - 2025-03-28 (UTC 23:00)

### Added
- Enhanced encapsulation with private attributes in CLI class
- Improved command configuration validation
- Additional constructor for Command class to reduce code duplication
- Comprehensive test suite for private attributes and command handling
- Full documentation in multiple languages (English and Russian)

### Changed
- Refactored CLI implementation for better encapsulation
- Improved command recognition system
- Enhanced argument handling and validation
- Updated test coverage for all major components
- Reorganized documentation structure for better clarity and maintainability
- Moved detailed documentation to dedicated docs directory

### Fixed
- Command recognition issues in advanced CLI examples
- Argument parsing and validation bugs
- Test failures related to command handling

## [0.2.0] - 2025-03-28 (UTC 17:00)

### Added
- Advanced CLI example with multiple commands
- Support for multiple arguments (nargs="+")
- Type validation and conversion
- Flags and optional parameters
- Return values and error handling

### Changed
- Improved command registration with decorators
- Enhanced argument and option handling
- Better error messages and validation
- Updated documentation with examples

### Fixed
- Command argument parsing issues
- Option handling with flags
- Return value handling in commands

### Security
- Added private attributes with double underscores
- Improved immutability of command configurations
- Enhanced validation of command arguments

## [0.1.0] - 2025-03-28 (UTC 15:00)

### Added
- Basic CLI framework implementation
- Command registration system
- Argument and option handling
- Basic documentation
- Initial test suite 
# Version 0.2.0
# Version 0.3.0
# Version 0.3.1
# Version 0.4.0
# Version 0.4.1
