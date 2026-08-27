from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def token(tenant: str = "demo") -> str:
    response = client.post("/api/v1/auth/login", json={"tenant_id": tenant, "user_id": "alice", "password": "demo-password"})
    return response.json()["access_token"]


def test_search_is_tenant_scoped():
    response = client.post("/api/v1/search", headers={"Authorization": f"Bearer {token()}"}, json={"query": "confidential information"})
    assert response.status_code == 200
    assert all(item["document_id"] != "secret" for item in response.json()["results"])


def test_chat_returns_verified_citations():
    response = client.post("/api/v1/chat", headers={"Authorization": f"Bearer {token()}"}, json={"question": "How many days can employees work remotely?"})
    body = response.json()
    assert body["grounded"] is True
    assert body["citations"]
    assert all(item["verified"] for item in body["citations"])


def test_invalid_token_rejected():
    response = client.post("/api/v1/search", headers={"Authorization": "Bearer forged"}, json={"query": "policy"})
    assert response.status_code == 401
