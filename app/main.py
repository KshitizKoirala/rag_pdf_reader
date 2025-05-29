import uvicorn

from app import create_app

app = create_app()


# def start_dev():
#     """Launched with `poetry run start_dev` at root level"""
#     uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


@app.get("/")
async def root():
    """Function printing python version."""
    raise ValueError("OOPS! Another change made")
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=80)
