from fastapi import APIRouter

from .serializer import LoginCredentials, LoginResponse
from .service import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/login", response_model=LoginResponse)
async def login(login_credentials: LoginCredentials):
    return await auth_service.create_or_get_api_key(login_credentials)
