# Decorators

CLI Builder provides decorators to easily transform Python classes into CLI components:

- `@Cli`: Creates a `CliCore` instance (main application)
- `@Module`: Creates a `CliModule` instance (command module)
- `@Library`: Creates a `CliLibrary` instance (utility library)

## CLI Decorator

::: cli_builder.decorators.cli.Cli
    options:
      show_root_heading: true
      heading_level: 3

## Module Decorator

::: cli_builder.decorators.module.Module
    options:
      show_root_heading: true
      heading_level: 3

## Library Decorator

::: cli_builder.decorators.library.Library
    options:
      show_root_heading: true
      heading_level: 3 