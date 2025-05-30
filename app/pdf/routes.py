from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def upload_pdf():
    return True
