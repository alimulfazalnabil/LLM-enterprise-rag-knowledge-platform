from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoints() -> None:
    assert client.get('/api/v1/health').status_code == 200
    assert client.get('/api/v1/health/live').status_code == 200
    assert client.get('/api/v1/health/ready').status_code == 200
    assert client.get('/api/v1/metrics').status_code == 200
