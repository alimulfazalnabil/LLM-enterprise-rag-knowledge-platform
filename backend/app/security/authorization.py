from fastapi import HTTPException, status

from app.security.rbac import Permission, SecurityContext


def require_permission(context: SecurityContext, permission: Permission) -> None:
    if permission not in context.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Missing required permission: {permission.value}',
        )
