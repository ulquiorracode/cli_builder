# Event System

CLI Builder includes an event system that allows components to communicate with each other through events.

The `EventEmitter` class provides the foundation for the event system:

## EventEmitter

::: cli_builder.events.emitter.EventEmitter
    options:
      show_root_heading: true
      heading_level: 3

## Event Bubbling

Events emitted on a child component will bubble up to its parent component, allowing parent components to listen for events from any of their children.

### Example

```python
from cli_builder.decorators import Cli, Module

@Cli("app")
class App:
    def __init__(self):
        # Listen for 'command-executed' event on the app
        self.on("command-executed", self.on_command_executed)
    
    def on_command_executed(self, source, command):
        print(f"Command executed: {command} from {source.name}")

@Module("command", parent_name="app")
class Command:
    def run(self, command):
        # This event will bubble up to the parent
        self.emit("command-executed", self, command)
        return f"Executed: {command}"
```

In this example, when the `Command` module emits the `command-executed` event, it will bubble up to the `App` parent, which will handle it with its `on_command_executed` method. 