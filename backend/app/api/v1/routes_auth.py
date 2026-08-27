from fastapi import APIRouter
from pydantic import BaseModel

from app.auth.service import (
    authenticate_user,
    decode_token,
    get_user,
    issue_access_token,
    issue_refresh_token,
    payload_to_context,
)

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post('/login')
def login(payload: LoginRequest) -> TokenResponse:
    user = authenticate_user(payload.username, payload.password)
    if not user:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    return TokenResponse(
        access_token=issue_access_token(user),
        refresh_token=issue_refresh_token(user),
    )


@router.post('/refresh')
def refresh(payload: RefreshRequest) -> dict[str, str]:
    from fastapi import HTTPException, status

    try:
        token_payload = decode_token(payload.refresh_token, expected_type='refresh')
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token') from exc
    context = payload_to_context(token_payload)
    user = get_user(context.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is inactive or missing')
    return {
        'access_token': issue_access_token(user),
        'token_type': 'bearer',
    }
