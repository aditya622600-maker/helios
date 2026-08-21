.PHONY: install run test lint db-up db-down

install:
	python -m pip install -e ".[dev]"

run:
	uvicorn apps.api.main:app --reload

test:
	pytest

lint:
	ruff check .

db-up:
	docker compose up -d db

db-down:
	docker compose down
