FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends make \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .flake8 mypy.ini ./
COPY Makefile ./

RUN pip install --upgrade pip && \
    pip install build

COPY src ./src
COPY tests ./tests
COPY README.md LICENSE ./

RUN pip install -e ".[dev,docs]"

CMD ["make", "check"]
