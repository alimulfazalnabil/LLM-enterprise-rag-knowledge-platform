from fastapi import APIRouter

router = APIRouter()

@router.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}

@router.get('/health/live')
def live() -> dict[str, str]:
    return {'status': 'live'}

@router.get('/health/ready')
def ready() -> dict[str, str]:
    return {'status': 'ready'}
