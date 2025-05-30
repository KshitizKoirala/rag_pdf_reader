from fastapi import APIRouter, Depends

from app.auth.auth_guard import validate_api_key

from . import routes


def pdf_router(curent_user: str = Depends(validate_api_key)):
    pdf_router = APIRouter()
    pdf_router.include_router(
        routes.router, prefix="/api/pdf", tags=["Upload Pdf"], dependencies=[curent_user])
    return pdf_router
