from qdrant_client.http.models import PointStruct

from ..database.config import COLLECTION_NAME, qdrant_client


class PdfRepository:

    async def add_embeddings(self, embeddings: list[str], texts: list[str]):
        points = [
            PointStruct(id=i, vector=vector, payload={"text": text})
            for i, (vector, text) in enumerate(zip(embeddings, texts, strict=False))
        ]

        # Insert points in batches
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i+batch_size]
            qdrant_client.upsert(collection_name=COLLECTION_NAME, points=batch)

        print(f"✅ Inserted {len(points)} points into '{COLLECTION_NAME}'")
        return True

    def search_similar(self, query_vector: list[float], top_k: int = 10):
        results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k,
        )
        return [{"score": r.score, "text": r.payload["text"]} for r in results]
