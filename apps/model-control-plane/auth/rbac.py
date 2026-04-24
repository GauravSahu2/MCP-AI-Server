# apps/model-control-plane/auth/rbac.py
from functools import wraps
from fastapi import Depends, HTTPException
from .jwt import TokenPayload, verify_token
from fastapi.security import HTTPBearer

bearer = HTTPBearer()

def require_permission(permission: str):
    """Decorator factory — use as: @require_permission('model:promote')"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, token=Depends(bearer), **kwargs):
            payload = verify_token(token.credentials)
            if permission not in payload.permissions:
                raise HTTPException(
                    status_code=403,
                    detail=f"Permission denied: requires '{permission}'"
                )
            # Inject context into kwargs
            kwargs["tenant_id"] = payload.tenant_id
            kwargs["user_id"]   = payload.sub
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def get_current_tenant(token=Depends(bearer)) -> str:
    payload = verify_token(token.credentials)
    return payload.tenant_id
