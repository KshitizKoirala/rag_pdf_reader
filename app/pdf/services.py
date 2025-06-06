import asyncio

from fastapi import Request
from openai import OpenAIError

from app.core.embedder import generate_embedings, smart_chunk
from app.core.extract_pdf import extract_text_from_pdf, filter_answers
from app.utils.generative_ai import openai_client

from .repository import PdfRepository

pdf_repository = PdfRepository()
MIN_QUERY_LENGTH = 10


class PdfService:
    async def process_pdf_file(self, content: bytes, request: Request) -> bool:
        text = extract_text_from_pdf(content)
        chunks = smart_chunk(text, max_tokens=256, overlap_tokens=40)
        embeddings = generate_embedings(request, chunks)
        await pdf_repository.add_embeddings(embeddings, chunks)
        return True

    async def augument_query_from_db(self, request: Request, text: str) -> str:
        try:
            if len(text.strip()) <= MIN_QUERY_LENGTH:
                text = f"Explain the concept of {text.strip().rstrip('.')}"
            query_vector = generate_embedings(request, text)
            results = pdf_repository.search_similar(query_vector)
            answer = filter_answers(results)
            context = "\n".join([text for text in answer])
            augument_answer = await generate_augumented_answer(context, text)
            return {"answer": augument_answer}

        except Exception:
            return {"status": 500, "detail": "Something unexpected occured. Please try again."}


async def generate_augumented_answer(context: str, user_question: str):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful, knowledgeable assistant. "
                "Answer the user's question using only the provided context. "
                "Be clear, structured, and concise. "
                "If the answer is not present in the context, respond with: "
                "\"I don't know based on the provided context.\""
            )
        },
        {
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Question: {user_question}"
            )
        }
    ]

    retries = 3
    for attempt in range(retries):
        try:
            # Optional: sleep to prevent hitting rate limits
            await asyncio.sleep(1.2)

            response = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.3
            )

            return response.choices[0].message.content

        except OpenAIError as e:
            if "429" in str(e) and attempt < retries - 1:
                wait = 2 ** attempt
                await asyncio.sleep(wait)
            else:
                return "I encountered an error while generating the answer."
