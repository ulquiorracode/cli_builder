# CLI Builder

Современный, типобезопасный фреймворк для создания CLI приложений на Python.

## Возможности

- Поддержка типизации и валидация
- Неизменяемые конфигурации команд
- Защита приватных атрибутов
- Регистрация команд через декораторы
- Гибкая обработка аргументов и опций
- Встроенная обработка ошибок
- Полное тестовое покрытие
- Поддержка нескольких языков

## Установка

```bash
pip install cli-builder
```

## Быстрый старт

### Использование декораторов

```python
from cli_builder.app import CLI

cli = CLI(name="my-cli", description="Мое CLI приложение")

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

## Автоматические декораторы

CLI Builder предоставляет автоматические декораторы для упрощения создания команд, автоматически определяя аргументы и опции из параметров функции.

### Auto Arguments

Декоратор `@cli.auto_arguments` автоматически создает аргументы из параметров функции без значений по умолчанию.

```python
@cli.command()
@cli.auto_arguments
def greet(name: str, title: str):
    """Приветствует человека.
    
    Args:
        name: Имя человека
        title: Обращение
    """
    print(f"Здравствуйте, {title} {name}!")
    return 0
```

Это создает два аргумента: `name` и `title`. Описания извлекаются из документации функции.

### Auto Options

Декоратор `@cli.auto_options` автоматически создает опции из параметров функции со значениями по умолчанию.

```python
@cli.command()
@cli.auto_options
def format_text(text: str, upper: bool = False, width: int = 10):
    """Форматирует текст.
    
    Args:
        text: Текст для форматирования
        upper: Преобразовать в верхний регистр
        width: Ширина вывода
    """
    result = text.upper() if upper else text
    result = result.center(width)
    print(f"[{result}]")
    return 0
```

Это создает две опции: `--upper` и `--width`.

### Auto Command

Декоратор `@cli.auto_command()` объединяет функциональность `@cli.command()`, `@cli.auto_arguments` и `@cli.auto_options`:

```python
@cli.auto_command()
def calculate(a: float, b: float, operation: str = "add"):
    """Выполняет вычисление.
    
    Args:
        a: Первое число
        b: Второе число
        operation: Операция (add, subtract, multiply, divide)
    """
    # Реализация команды
```

Это создает команду с именем "calculate" с двумя аргументами (`a` и `b`) и одной опцией (`--operation`).

## Использование Command и CommandConfig

```python
from cli_builder.app import CLI
from cli_builder.app.command import Command
from cli_builder.app.config import CommandConfig

cli = CLI(name="my-cli", description="Мое CLI приложение")

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

## Примеры

В директории [examples](examples/) находятся примеры использования библиотеки:

### Базовые примеры

#### basic_cli.py
Простой пример, демонстрирующий базовое использование библиотеки:
- Создание CLI приложения
- Регистрация простых команд
- Использование аргументов и опций

```bash
# Запуск команды hello
python basic_cli.py hello

# Запуск команды greet с аргументами
python basic_cli.py greet John --count 3
```

### Продвинутые примеры

#### advanced_cli.py
Более сложный пример, показывающий расширенные возможности:
- Множественные аргументы (nargs="+")
- Валидация и преобразование типов
- Флаги и опциональные параметры
- Возвращаемые значения и обработка ошибок

```bash
# Калькулятор
python advanced_cli.py calc add 1 2 3 4 --precision 2
python advanced_cli.py calc mul 2 3 4 --precision 0

# Конвертер единиц
python advanced_cli.py convert 5 km m
python advanced_cli.py convert 1000 g kg --system metric

# Форматирование текста
python advanced_cli.py format "hello world" --upper
python advanced_cli.py format "hello world" --title --width 5
```

## Разработка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/cli-builder.git
cd cli-builder
```

2. Установите зависимости для разработки:
```bash
pip install -e ".[dev]"
```

3. Запустите тесты:
```bash
pytest
```

## Лицензия

Этот проект распространяется под лицензией GPL-3.0 - подробности в файле [LICENSE](LICENSE). 