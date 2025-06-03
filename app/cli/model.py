import typer

from qdrant_client.http.exceptions import ResponseHandlingException
from sentence_transformers import SentenceTransformer

from app.database.config import qdrant_client

app = typer.Typer()


@app.command("save-model")
def save_model():
    print("Downloading model from Hugging Face...")
    model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
    model.save("models/mpnet-dot")
    print("Model saved to models/mpnet-dot")


@app.command("reset-db")
def reset_db():
    try:
        """Delete the 'pdf_chunks' collection from Qdrant."""
        print("🔄 Resetting Qdrant collection: pdf_chunks")
        collections = qdrant_client.get_collections().collections
        for collection in collections:
            if collection.name == "pdf_chunks":
                qdrant_client.delete_collection("pdf_chunks")
                print("✅ Deleted 'pdf_chunks' collection")
                break
        else:
            print("ℹ️ 'pdf_chunks' collection not found. Nothing to delete.")  # noqa: RUF001
    except ResponseHandlingException as e:
        print("❌ Could not connect to Qdrant.")
        print(f"Error: {e}")


if __name__ == "__main__":
    app()
