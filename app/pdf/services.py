from fastapi import Request

from app.core.embedder import generate_embedings
from app.core.extract_pdf import extract_text_from_pdf

from .repository import PdfRepository

pdf_repository = PdfRepository()


class PdfService:
    async def process_pdf_file(self, content: bytes, request: Request) -> bool:
        text = extract_text_from_pdf(content)
        chunks = text.split("\n")
        embeddings = generate_embedings(request, chunks)
        await pdf_repository.add_embeddings(embeddings, chunks)
        return True

    async def query_from_db(self, request: Request, text: str) -> str:
        query_vector = generate_embedings(request, text)
        results = pdf_repository.search_similar(query_vector)
        # Extract the text and score from the results
        answer_list = [{"score": r["score"], "text": r["text"].strip()}
                       for r in results]
        sorted_answers = sorted(
            answer_list, key=lambda x: x["score"], reverse=True)

        threshold = 0.6
        filtered_answers = [
            answer for answer in sorted_answers if answer["score"] > threshold]

        # Filter out the most relevant answers and combine them
        combined_answer = ""
        for answer in filtered_answers:
            combined_answer += answer["text"] + " "
        combined_answer = combined_answer.strip()
        return combined_answer
