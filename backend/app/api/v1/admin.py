from fastapi import APIRouter

router = APIRouter()

@router.get('/admin/health')
def admin_health() -> dict[str, str]:
    return {'status': 'admin-ok'}
