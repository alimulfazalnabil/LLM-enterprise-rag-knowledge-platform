from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post('/login')
def login(_: LoginRequest) -> dict[str, str]:
    return {'access_token': 'dev-token', 'refresh_token': 'dev-refresh'}

@router.post('/refresh')
def refresh() -> dict[str, str]:
    return {'access_token': 'dev-token'}
