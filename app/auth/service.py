from fastapi import HTTPException, status

from ..utils.helpers import (
    create_api_key,
    get_if_api_key_exists,
    verify_api_key,
)
from .serializer import LoginCredentials


class AuthService:
    async def create_or_get_api_key(self, login_credentials: LoginCredentials):
        api_key = get_if_api_key_exists(login_credentials.email)

        if not api_key:
            key = create_api_key(login_credentials.email,
                                 login_credentials.password)
            return {"API_KEY": key}

        if verify_api_key(api_key, login_credentials.password):
            return {"API_KEY": api_key}

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Password!"
        )
