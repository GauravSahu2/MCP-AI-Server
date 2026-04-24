# apps/model-control-plane/auth/jwt.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
import os
from fastapi import HTTPException

SECRET_KEY  = os.getenv("JWT_SECRET_KEY", "aegis-super-secret-key-change-me")
ALGORITHM   = "HS256" # Using HS256 for now, can upgrade to RS256 with Vault in Phase 6
ACCESS_TTL  = timedelta(minutes=15)

class TokenPayload(BaseModel):
    sub: str         # user_id
    tenant_id: str
    role: str
    permissions: list[str]
    exp: datetime

def create_access_token(user_id: str, tenant_id: str, role: str, permissions: list[str]) -> str:
    payload = {
        "sub":         user_id,
        "tenant_id":   tenant_id,
        "role":        role,
        "permissions": permissions,
        "exp":         datetime.utcnow() + ACCESS_TTL,
        "iat":         datetime.utcnow(),
        "type":        "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
