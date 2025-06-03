
from fastapi import APIRouter, HTTPException, Query, Request, UploadFile

from .services import PdfService

router = APIRouter()
pdf_service = PdfService()


@router.post("/upload")
async def upload_pdf(file: UploadFile, request: Request):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400, detail="Only PDF files are supported")

    print("PDF Upload started")
    content = await file.read()
    await pdf_service.process_pdf_file(content, request)
    print("PDF Upload completed")
    return {"status": 200, "message": "Uploaded successfully"}


@router.get("/ask")
async def get_query_results(request: Request, question: str = Query(None, description="Ask Question")):
    return await pdf_service.query_from_db(request, question)
    # return current_user
