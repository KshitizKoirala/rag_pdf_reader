from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

# Initialize the Qdrant client and model
qdrant_client = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "pdf_chunks"


def create_collection():
    if COLLECTION_NAME not in [c.name for c in qdrant_client.get_collections().collections]:
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        print(f"✅ Created collection: {COLLECTION_NAME}")


create_collection()
