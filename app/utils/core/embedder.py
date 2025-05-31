from fastapi import Request

# model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')


# question = "What are the health benefits of green tea?"
# passages = [
#     "Green tea contains antioxidants that may help prevent heart disease.",
#     "Coffee contains more caffeine than green tea.",
#     "Vitamin D is essential for bone health."
# ]

# question_emb = model.encode(question, convert_to_tensor=True)
# passage_embs = model.encode(passages, convert_to_tensor=True)

# # Compute cosine similarities
# scores = util.dot_score(question_emb, passage_embs)
# best_idx = scores.argmax()
# print("Best answer:", passages[best_idx])


def generate_embedings(request: Request, chunks: list[str]):
    if not hasattr(request.app.state, "model"):
        raise RuntimeError(
            "Model not loaded. Did you forget to use FastAPI lifespan?")
    model = request.app.state.model
    return model.encode(chunks).tolist()
