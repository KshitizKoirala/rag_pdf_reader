from typing import Any

import fitz


def de_duplicate_response(filtered_answers: list[dict[str, Any]]):
    seen = set()
    filtered_texts = []
    for answer in filtered_answers:
        text = answer["text"].strip()
        if text not in seen:
            filtered_texts.append(text)
            seen.add(text)
    return " ".join(filtered_texts)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    document = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in document:
        text += page.get_text()
    return text
