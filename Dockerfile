# ----------- Stage 1: Builder Layer -----------
FROM python:3.12-bookworm AS base

RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.8.2

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Configure Poetry and install dependencies (without virtualenvs)
RUN poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi

COPY . /app


# ----------- Stage 2: Runtime Layer -----------
FROM base

COPY --from=base /app /app

RUN mkdir -p /app/logs

EXPOSE 8000

CMD ["make", "dev"]