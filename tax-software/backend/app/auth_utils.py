from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

def bearer_auth(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
) -> str:
    if not credentials or not credentials.scheme.lower() == "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    return credentials.credentials

def require_role(required_roles):
    def role_dependency(token: str = Depends(bearer_auth)):
        from .main import get_user_from_token
        user = get_user_from_token(token)
        if user.role not in required_roles and "*" not in required_roles:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user
    return role_dependency
