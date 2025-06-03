
from app import create_app
from app.database.config import create_collection

app = create_app()


if __name__ == "__main__":
    create_collection()
    # uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
