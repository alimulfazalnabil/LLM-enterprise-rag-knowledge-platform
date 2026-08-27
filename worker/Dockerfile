FROM python:3.12-slim
WORKDIR /app
COPY backend/pyproject.toml .
RUN pip install --no-cache-dir .
COPY worker ./worker
CMD ["python", "-m", "worker.ingestion_worker"]
