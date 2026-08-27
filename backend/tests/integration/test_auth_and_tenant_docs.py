from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _login(username: str, password: str) -> dict[str, str]:
    response = client.post('/api/v1/auth/login', json={'username': username, 'password': password})
    assert response.status_code == 200
    return response.json()


def test_login_and_refresh_flow() -> None:
    tokens = _login('admin_a', 'admin_a_password')
    assert 'access_token' in tokens
    assert 'refresh_token' in tokens

    refreshed = client.post('/api/v1/auth/refresh', json={'refresh_token': tokens['refresh_token']})
    assert refreshed.status_code == 200
    assert 'access_token' in refreshed.json()


def test_document_list_requires_auth() -> None:
    response = client.get('/api/v1/documents')
    assert response.status_code == 401


def test_tenant_isolation_on_document_list_and_get() -> None:
    token_a = _login('admin_a', 'admin_a_password')['access_token']
    token_b = _login('viewer_b', 'viewer_b_password')['access_token']

    docs_a = client.get('/api/v1/documents', headers={'Authorization': 'Bearer ' + token_a})
    docs_b = client.get('/api/v1/documents', headers={'Authorization': 'Bearer ' + token_b})

    assert docs_a.status_code == 200
    assert docs_b.status_code == 200
    assert all(doc['tenant_id'] == 'tenant_a' for doc in docs_a.json())
    assert all(doc['tenant_id'] == 'tenant_b' for doc in docs_b.json())

    forbidden_cross_tenant = client.get(
        '/api/v1/documents/doc_b_1',
        headers={'Authorization': 'Bearer ' + token_a},
    )
    assert forbidden_cross_tenant.status_code == 404
