from fastapi import Request


def generate_embedings(request: Request, chunks: list[str]):
    if not hasattr(request.app.state, "model"):
        raise RuntimeError(
            "Model not loaded. Did you forget to use FastAPI lifespan?")
    model = request.app.state.model
    return model.encode(chunks).tolist()
