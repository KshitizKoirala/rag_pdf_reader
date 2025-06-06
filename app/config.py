import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = os.getenv('SECRET_KEY').encode()
qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
OPENAI_API_KEY = os.getenv("OPEN_AI_KEY")
