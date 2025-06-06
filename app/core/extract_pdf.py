from typing import Any

import fitz


def de_duplicate_response(filtered_answers: list[dict[str, Any]]) -> list[str]:
    seen = set()
    filtered_texts = []
    for answer in filtered_answers:
        text = answer["text"].strip()
        if text not in seen:
            filtered_texts.append(text)
            seen.add(text)
    return filtered_texts


def extract_text_from_pdf(file_bytes: bytes) -> str:
    document = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in document:
        text += page.get_text()
    return text


def filter_answers(results: list[dict[str, Any]]):
    # Extract the text and score from the results
    answer_list = [{"score": r["score"], "text": r["text"].strip()}
                   for r in results]
    sorted_answers = sorted(
        answer_list, key=lambda x: x["score"], reverse=True)
    threshold = 0.6
    filtered_answers = [
        answer for answer in sorted_answers if answer["score"] > threshold]

    # Filter out the most relevant answers and combine them
    return de_duplicate_response(filtered_answers)
