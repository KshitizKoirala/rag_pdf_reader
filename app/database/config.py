from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from app.config import qdrant_host, qdrant_port

# Initialize the Qdrant client and model
qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)

COLLECTION_NAME = "pdf_chunks"


# # # List all collections
# collections = qdrant_client.get_collections()
# # Accessing the list of collections
# # 'collections' is the correct key here
# collection_list = collections.collections

# # Now you can iterate or filter for your specific collection
# for collection in collection_list:
#     if collection.name == 'pdf_chunks':
#         # Do something with the 'pdf_chunks' collection
#         qdrant_client.delete_collection("pdf_chunks")
#         print(f"Found collection: {collection}")


def create_collection():
    if COLLECTION_NAME not in [c.name for c in qdrant_client.get_collections().collections]:
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        print(f"✅ Created collection: {COLLECTION_NAME}")


# create_collection()
