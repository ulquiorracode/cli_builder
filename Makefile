.PHONY: test lint type check clean docs

test:
	PYTHONPATH=. pytest --cov=cli_builder tests/ -v --cov-report=term-missing

lint:
	flake8

type:
	mypy --ignore-missing-imports .

check: lint type test

clean:
	rm -rf .coverage .pytest_cache .mypy_cache __pycache__ */__pycache__ */*/__pycache__
	rm -rf build/ dist/ *.egg-info/

docs:
	mkdocs serve

build-docs:
	mkdocs build

install-dev:
	pip install -e ".[dev,docs]" 