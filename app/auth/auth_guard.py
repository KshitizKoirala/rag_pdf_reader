from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

from app.utils.helpers import get_email_from_api_key

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def validate_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = get_email_from_api_key(api_key)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return email
