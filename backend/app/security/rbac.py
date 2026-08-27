from enum import StrEnum
from dataclasses import dataclass

class Role(StrEnum):
    SUPER_ADMIN = 'SUPER_ADMIN'
    TENANT_ADMIN = 'TENANT_ADMIN'
    KNOWLEDGE_MANAGER = 'KNOWLEDGE_MANAGER'
    EMPLOYEE = 'EMPLOYEE'
    VIEWER = 'VIEWER'

class Permission(StrEnum):
    DOCUMENTS_READ = 'documents:read'
    DOCUMENTS_WRITE = 'documents:write'
    DOCUMENTS_DELETE = 'documents:delete'
    DOCUMENTS_MANAGE = 'documents:manage'
    DOCUMENTS_VERSION = 'documents:version'
    KNOWLEDGE_QUERY = 'knowledge:query'
    EVALUATION_READ = 'evaluation:read'
    EVALUATION_RUN = 'evaluation:run'
    ADMIN_MANAGE = 'admin:manage'

@dataclass(frozen=True)
class SecurityContext:
    user_id: str
    tenant_id: str
    roles: set[Role]
    permissions: set[Permission]
