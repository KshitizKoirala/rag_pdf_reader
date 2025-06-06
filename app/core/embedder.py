
import tiktoken

from fastapi import Request
from nltk.tokenize.punkt import PunktSentenceTokenizer

"""
cl100k_base => how transformer models like BERT, RoBERTa, and OpenAI models actually "see" and tokenize text.

 What is "cl100k_base" or "o200k_base" in tiktoken?

These are tokenizer encodings used to simulate how models convert text into tokens. Each base refers to a different tokenization strategy:

Encoding	    Used By	                Approx. Tokens per Word	        Notes

cl100k_base	    OpenAI's GPT-4 /        ~0.75/token per word        Fast, commonly used
                ChatGPT / 
                text-embedding-ada-002		

o200k_base	    Used in newer OpenAI     ~0.7/token per word	    More efficient, larger vocab
                models (like gpt-4o)	
                
These encodings define how text is split into subword tokens, not full words or characters.
"""


# Use tiktoken tokenizer for token counting (same as OpenAI)
tokenizer = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))


def smart_chunk(
    text: str,
    max_tokens: int = 256,
    overlap_tokens: int = 50
) -> list[str]:
    tokenizer = PunktSentenceTokenizer()
    sentences = tokenizer.tokenize(text)
    chunks = []
    current_chunk = []
    current_token_count = 0

    for sentence in sentences:
        token_len = count_tokens(sentence)
        if current_token_count + token_len > max_tokens:
            # Finalize current chunk
            chunk_text = " ".join(current_chunk).strip()
            if chunk_text:
                chunks.append(chunk_text)

            # Start new chunk, add overlap
            overlap = []
            while current_chunk and count_tokens(" ".join(overlap)) < overlap_tokens:
                overlap.insert(0, current_chunk.pop())
            current_chunk = [*overlap, sentence]
            current_token_count = count_tokens(" ".join(current_chunk))
        else:
            current_chunk.append(sentence)
            current_token_count += token_len

    # Add the final chunk
    if current_chunk:
        chunk_text = " ".join(current_chunk).strip()
        chunks.append(chunk_text)

    return chunks


def generate_embedings(request: Request, chunks: list[str]) -> list[list[float]]:
    if not hasattr(request.app.state, "model"):
        raise RuntimeError(
            "Model not loaded. Did you forget to use FastAPI lifespan?")
    model = request.app.state.model
    return model.encode(chunks).tolist()
