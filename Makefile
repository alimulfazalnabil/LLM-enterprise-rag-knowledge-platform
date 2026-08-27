.PHONY: install dev test lint format typecheck security evaluate benchmark docker-build docker-up docker-down

install:
	pip install -e ./backend

dev:
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest backend/tests -q

lint:
	ruff check backend

format:
	ruff format backend

typecheck:
	mypy backend/app

security:
	bandit -r backend/app

evaluate:
	python scripts/evaluate.py

benchmark:
	python scripts/benchmark.py

docker-build:
	docker compose build

docker-up:
	docker compose up --build

docker-down:
	docker compose down
