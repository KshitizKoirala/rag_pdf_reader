from fastapi import Request

from app.utils.core.embedder import generate_embedings
from app.utils.core.extract_pdf import extract_text_from_pdf

from .repository import PdfRepository

pdf_repository = PdfRepository()


class PdfService:
    async def process_pdf_file(self, content: bytes, request: Request) -> bool:
        text = extract_text_from_pdf(content)
        chunks = text.split("\n")
        embeddings = generate_embedings(request, chunks)
        await pdf_repository.add_embeddings(embeddings, chunks)
        return True

    async def query_from_db(self, request, text):
        # chunks = text.split("\n")
        query_vector = generate_embedings(request, text)
        return pdf_repository.search_similar(query_vector)
