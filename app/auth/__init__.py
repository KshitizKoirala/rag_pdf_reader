from fastapi import APIRouter

from . import routes


def auth_router():
    auth_router = APIRouter()
    auth_router.include_router(
        routes.router, prefix="/api/auth", tags=["auth"])
    return auth_router
