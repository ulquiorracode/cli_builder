# Quick Start

This guide will help you get started with CLI Builder quickly by creating a simple command-line application.

## Installation

First, install CLI Builder using pip:

```bash
pip install cli-builder
```

## Creating a Basic CLI Application

Here's a simple example of a CLI application using CLI Builder:

```python
from cli_builder.decorators import Cli, Module, Library

# Create the main application
@Cli("hello-app", description="A simple greeting application", version="1.0.0")
class HelloApp:
    def __init__(self):
        # Initialize with a formatter library and a greeter module
        self.add_child(TextFormatter)
        self.add_child(Greeter)
    
    def run(self):
        """Main entry point for the application"""
        greeter = self.get_child("greeter")
        return greeter.run("World")

# Create a utility library
@Library("formatter")
class TextFormatter:
    def format_greeting(self, name):
        """Format a greeting message"""
        return f"Hello, {name}!"
    
    def format_farewell(self, name):
        """Format a farewell message"""
        return f"Goodbye, {name}!"

# Create a module
@Module("greeter", parent_name="hello-app")
class Greeter:
    def run(self, name):
        """Greet someone by name"""
        formatter = self.parent.get_child("formatter")
        greeting = formatter.format_greeting(name)
        return greeting

# Run the application
if __name__ == "__main__":
    result = HelloApp.run()
    print(result)  # Output: Hello, World!
```

## Explanation

1. **Main Application**: The `@Cli` decorator transforms the `HelloApp` class into a CLI application. It automatically becomes an instance of `CliCore`.

2. **Utility Library**: The `@Library` decorator transforms the `TextFormatter` class into a utility library. It automatically becomes an instance of `CliLibrary` which provides helper methods but isn't directly executable.

3. **Command Module**: The `@Module` decorator transforms the `Greeter` class into a command module. It automatically becomes an instance of `CliModule` which can be executed.

4. **Component Relationships**: Components can reference each other through the parent-child relationship. 
   - The main app adds children during initialization
   - The module can access other components through `self.parent`
   - The parent can access children through `get_child(name)`

5. **Running the Application**: Simply call the `run()` method on the application instance.

## Next Steps

Now that you've seen a basic example, you can:

- Learn more about [Creating a CLI App](creating-cli-app.md)
- Explore [Working with Modules](working-with-modules.md)
- Discover how to leverage [Using Libraries](using-libraries.md)
- Understand the [Event System](events.md)

For a more complex example, check out the [Building a Todo App](../tutorials/todo-app.md) tutorial. 