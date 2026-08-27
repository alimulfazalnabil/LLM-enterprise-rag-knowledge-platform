from fastapi import APIRouter

router = APIRouter()

@router.get('/metrics')
def metrics() -> dict[str, str]:
    return {'status': 'metrics endpoint scaffold'}
