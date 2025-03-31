# CLI Builder

Современный, типобезопасный фреймворк для создания CLI-приложений на Python.

## Возможности

* Типизация и валидация
* Неизменяемые конфигурации команд
* Защита приватных атрибутов
* Регистрация команд через декораторы
* Гибкая обработка аргументов и опций
* Встроенная обработка ошибок
* Полное тестовое покрытие
* Поддержка нескольких языков

## Установка

```bash
pip install cli-builder
```

## Быстрый старт

### Использование декораторов

```python
from cli_builder.app import CLI

cli = CLI(name="my-cli", description="Мое CLI-приложение")

@cli.option("count", short="c", type=int, default=1, help="Количество приветствий")
@cli.argument("name", help="Имя для приветствия")
@cli.command(description="Поздороваться")
def hello(name: str, count: int = 1) -> None:
    """Простая команда приветствия."""
    for _ in range(count):
        print(f"Привет, {name}!")

if __name__ == "__main__":
    cli.run()
```

### Использование Command и CommandConfig

```python
from cli_builder.app import CLI
from cli_builder.app.command import Command
from cli_builder.app.config import CommandConfig

cli = CLI(name="my-cli", description="Мое CLI-приложение")

# Создание конфигурации команды
config = CommandConfig(
    name="hello",
    description="Поздороваться",
    arguments=[
        {
            "name": "name",
            "type": str,
            "help": "Имя для приветствия",
            "required": True
        }
    ],
    options=[
        {
            "name": "count",
            "short": "c",
            "type": int,
            "help": "Количество приветствий",
            "default": 1
        }
    ]
)

# Создание функции команды
def hello(name: str, count: int = 1) -> None:
    """Простая команда приветствия."""
    for _ in range(count):
        print(f"Привет, {name}!")

# Создание и регистрация команды
command = Command(config=config, func=hello)
cli.register_command(command)

if __name__ == "__main__":
    cli.run()
```

## Автоматические декораторы

CLI Builder предоставляет автоматические декораторы для упрощения создания команд:

```python
@cli.auto_command()
def calculate(a: float, b: float, operation: str = "add"):
    """Выполняет вычисление.
    
    Args:
        a: Первое число
        b: Второе число
        operation: Операция (add, subtract, multiply, divide)
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            print("Ошибка: Деление на ноль")
            return 1
        result = a / b
    else:
        print(f"Неизвестная операция: {operation}")
        return 1
        
    print(f"Результат: {result}")
    return 0
```

## Стандартные команды

CLI Builder предоставляет набор стандартных команд, которые можно включить одним вызовом метода:

```python
cli = CLI(
    name="my-cli", 
    description="Мое CLI-приложение", 
    version="1.0.0"
)

# Включение всех стандартных команд
cli.enable_standard_commands(
    help=True,         # Включить команду help
    version=True,      # Включить команду version
    list=True,         # Включить команду list
    completion=True    # Включить команду completion
)
```

## Примеры

См. директорию [examples](../examples/) для примеров использования.

## Разработка

1. Клонировать репозиторий:

```bash
git clone https://github.com/ulquiorracode/cli_builder.git
cd cli-builder
```

2. Установить зависимости для разработки:

```bash
pip install -e ".[dev]"
```

3. Запустить тесты:

```bash
pytest
```

## Дорожная карта

См. [список задач](todo.md) для планируемых функций и улучшений.

## Лицензия

Этот проект распространяется под лицензией GPL-3.0 - см. файл [LICENSE](../../LICENSE) для подробностей. 