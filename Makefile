.PHONY: dev prod logs format lint

PYTHON=python3
LOG_CONFIG=config/log_config.yml
APP_PATH=app.main:app

dev:
	poetry run uvicorn $(APP_PATH) --host 0.0.0.0 --port 8000 --reload --log-config $(LOG_CONFIG)

prod:
	poetry run uvicorn $(APP_PATH) --host 0.0.0.0 --port 8000 --log-config $(LOG_CONFIG)

logs:
	tail -f logs/app.log

format:
	poetry run ruff format .

lint:
	poetry run ruff check .

lint-fix:
	poetry run ruff check --fix