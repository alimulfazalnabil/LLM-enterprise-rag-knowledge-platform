from __future__ import annotations

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.service import decode_token, payload_to_context
from app.security.authorization import require_permission
from app.security.rbac import Permission, SecurityContext

bearer = HTTPBearer(auto_error=True)


def get_current_security_context(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> SecurityContext:
    try:
        payload = decode_token(credentials.credentials, expected_type='access')
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired access token',
        ) from exc
    return payload_to_context(payload)


def require_documents_read(context: SecurityContext = Depends(get_current_security_context)) -> SecurityContext:
    require_permission(context, Permission.DOCUMENTS_READ)
    return context


def require_documents_write(context: SecurityContext = Depends(get_current_security_context)) -> SecurityContext:
    require_permission(context, Permission.DOCUMENTS_WRITE)
    return context


def require_documents_delete(context: SecurityContext = Depends(get_current_security_context)) -> SecurityContext:
    require_permission(context, Permission.DOCUMENTS_DELETE)
    return context
