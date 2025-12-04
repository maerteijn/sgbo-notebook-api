.PHONY: install lint format test coverage dev

default: install

install:
	uv sync --extra dev

lint:
	uv run zmypy src
	uv run ruff check

format:
	uv run ruff check --fix
	uv run ruff format

test:
	uv run pytest tests src/sgbo_notebook_api

coverage:
	uv run pytest --cov=sgbo_notebook_api tests src/sgbo_notebook_api --cov-report=term

migrate: install
	uv run manage.py migrate

superuser: migrate
	uv run manage.py createsuperuser

dev: migrate
	uv run manage.py runserver 0.0.0.0:8000
