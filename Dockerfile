# ----------- Stage 1: Builder Layer -----------
FROM python:3.12-bookworm AS base

RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*


ENV POETRY_VERSION=1.8.2

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Configure Poetry and install dependencies (without virtualenvs)
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /app

COPY nltk_data /usr/local/nltk_data
ENV NLTK_DATA=/usr/local/nltk_data

RUN poetry run save-model && mkdir -p /app/logs


# ----------- Stage 2: Runtime Layer -----------
FROM base

COPY --from=base /app /app

EXPOSE 8000

CMD ["make", "dev"]