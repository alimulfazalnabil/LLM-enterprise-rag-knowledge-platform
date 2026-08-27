install:
	python -m pip install -e './backend[test]'
dev:
	uvicorn backend.app.main:app --reload --port 8000
test:
	pytest -q backend/tests
lint:
	python -m compileall backend/app
format:
	python -m compileall backend/app
typecheck:
	python -m compileall backend/app
security:
	pytest -q backend/tests/test_security.py
docker-up:
	docker compose up --build
docker-down:
	docker compose down
