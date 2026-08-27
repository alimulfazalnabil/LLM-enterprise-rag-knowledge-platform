from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import DocumentChunk

client = TestClient(app)


def token(tenant: str = "demo") -> str:
    response = client.post("/api/v1/auth/login", json={"tenant_id": tenant, "user_id": "alice", "password": "demo-password"})
    return response.json()["access_token"]


def test_upload_creates_versioned_document():
    response = client.post(
        "/api/v1/documents",
        headers={"Authorization": f"Bearer {token()}"},
        files={"file": ("policy-v1.md", b"# Remote Work Policy\nEmployees may work remotely up to three days each week.")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "COMPLETED"
    assert body["document_id"]
    assert body["version_id"]


def test_second_upload_creates_new_version_for_same_document_name():
    first = client.post(
        "/api/v1/documents",
        headers={"Authorization": f"Bearer {token()}"},
        files={"file": ("versioned-policy.md", b"# First version\nRemote work is allowed with manager approval.")},
    )
    second = client.post(
        "/api/v1/documents",
        headers={"Authorization": f"Bearer {token()}"},
        files={"file": ("versioned-policy.md", b"# Second version\nRemote work is allowed up to three days per week.")},
    )
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["document_id"] == second.json()["document_id"]
    assert first.json()["version_id"] != second.json()["version_id"]


def test_upload_splits_large_document_into_multiple_chunks():
    payload = b" ".join([b"Remote work policy. " for _ in range(200)])
    response = client.post(
        "/api/v1/documents",
        headers={"Authorization": f"Bearer {token()}"},
        files={"file": ("chunked-policy.md", payload)},
    )
    assert response.status_code == 200
    version_id = response.json()["version_id"]
    with SessionLocal() as db:
        chunks = db.query(DocumentChunk).filter_by(version_id=version_id).all()
    assert len(chunks) > 1

    db_chunks = client.post(
        "/api/v1/search",
        headers={"Authorization": f"Bearer {token()}"},
        json={"query": "Remote work policy"},
    )
    assert db_chunks.status_code == 200
    assert any(item["version_id"] == version_id for item in db_chunks.json()["results"])
