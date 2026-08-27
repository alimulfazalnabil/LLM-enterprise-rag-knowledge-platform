import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityContext:
    tenant_id: str
    user_id: str
    roles: frozenset[str]


def _encode(value: dict, secret: str) -> str:
    payload = base64.urlsafe_b64encode(json.dumps(value, separators=(",", ":")).encode()).decode().rstrip("=")
    signature = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{signature}"


def create_token(context: SecurityContext, secret: str, minutes: int = 30) -> str:
    return _encode({"tenant_id": context.tenant_id, "user_id": context.user_id, "roles": list(context.roles), "exp": int(time.time()) + minutes * 60}, secret)


def decode_token(token: str, secret: str) -> SecurityContext:
    try:
        payload, signature = token.split(".", 1)
        expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise ValueError("invalid signature")
        raw = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        data = json.loads(raw)
        if int(data["exp"]) < time.time():
            raise ValueError("expired token")
        return SecurityContext(data["tenant_id"], data["user_id"], frozenset(data["roles"]))
    except (KeyError, ValueError, json.JSONDecodeError, TypeError) as exc:
        raise ValueError("invalid token") from exc


def password_digest(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
