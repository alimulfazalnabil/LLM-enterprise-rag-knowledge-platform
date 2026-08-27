from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.security.rbac import Permission, Role, SecurityContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@dataclass(frozen=True)
class UserRecord:
    username: str
    password_hash: str
    tenant_id: str
    roles: set[Role]
    permissions: set[Permission]
    is_active: bool = True


_USERS: dict[str, UserRecord] = {
    'admin_a': UserRecord(
        username='admin_a',
        password_hash=pwd_context.hash('admin_a_password'),
        tenant_id='tenant_a',
        roles={Role.TENANT_ADMIN},
        permissions={
            Permission.DOCUMENTS_READ,
            Permission.DOCUMENTS_WRITE,
            Permission.DOCUMENTS_DELETE,
            Permission.DOCUMENTS_VERSION,
            Permission.KNOWLEDGE_QUERY,
            Permission.EVALUATION_READ,
            Permission.EVALUATION_RUN,
        },
    ),
    'viewer_b': UserRecord(
        username='viewer_b',
        password_hash=pwd_context.hash('viewer_b_password'),
        tenant_id='tenant_b',
        roles={Role.VIEWER},
        permissions={Permission.DOCUMENTS_READ, Permission.KNOWLEDGE_QUERY},
    ),
}


def authenticate_user(username: str, password: str) -> UserRecord | None:
    user = _USERS.get(username)
    if not user or not user.is_active:
        return None
    if not pwd_context.verify(password, user.password_hash):
        return None
    return user


def get_user(username: str) -> UserRecord | None:
    user = _USERS.get(username)
    if not user or not user.is_active:
        return None
    return user


def _encode_token(user: UserRecord, token_type: str, lifetime_minutes: int) -> str:
    now = datetime.now(UTC)
    payload = {
        'sub': user.username,
        'tenant_id': user.tenant_id,
        'roles': [r.value for r in user.roles],
        'permissions': [p.value for p in user.permissions],
        'token_type': token_type,
        'iat': now,
        'exp': now + timedelta(minutes=lifetime_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm='HS256')


def issue_access_token(user: UserRecord) -> str:
    return _encode_token(user=user, token_type='access', lifetime_minutes=30)


def issue_refresh_token(user: UserRecord) -> str:
    return _encode_token(user=user, token_type='refresh', lifetime_minutes=60 * 24 * 7)


def decode_token(token: str, expected_type: str | None = None) -> dict:
    payload = jwt.decode(token, settings.jwt_secret, algorithms=['HS256'])
    if expected_type and payload.get('token_type') != expected_type:
        raise jwt.InvalidTokenError('Invalid token type')
    return payload


def payload_to_context(payload: dict) -> SecurityContext:
    return SecurityContext(
        user_id=str(payload['sub']),
        tenant_id=str(payload['tenant_id']),
        roles={Role(r) for r in payload.get('roles', [])},
        permissions={Permission(p) for p in payload.get('permissions', [])},
    )
