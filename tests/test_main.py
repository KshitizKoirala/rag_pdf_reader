from unittest.mock import MagicMock, patch

import pytest

from fastapi import FastAPI, status
from httpx import ASGITransport, AsyncClient

from app import create_app

base_url = "http://localhost:8000"
headers = {"x-api-key": "test-secret"}


@pytest.fixture
def mocked_app_without_api_key():
    with (
        patch("app.__init__.SentenceTransformer") as mocked_model,
        patch("app.database.config.qdrant_client") as mock_qdrant_client,

    ):
        mocked_model.return_value = MagicMock()
        mock_qdrant_client.get_collections.return_value.collections = []
        mock_qdrant_client.recreate_collection.return_value = None

        app = create_app()
        yield app


@pytest.fixture
def mocked_app():
    with (
        patch("app.__init__.SentenceTransformer") as mocked_model,
        patch("app.database.config.qdrant_client") as mock_qdrant_client,
        patch("app.auth.auth_guard.get_email_from_api_key") as mock_get_email,
    ):
        # Mock the model
        mocked_model.return_value = MagicMock()

        # Mock qdrant behavior
        mock_qdrant_client.get_collections.return_value.collections = []
        mock_qdrant_client.recreate_collection.return_value = None

        # ✅ Mock API key function to always succeed
        mock_get_email.return_value = "test@example.com"

        app: FastAPI = create_app()
        return app


@pytest.mark.asyncio
async def test_root_endpoint(mocked_app):
    transport = ASGITransport(app=mocked_app)
    async with AsyncClient(transport=transport, base_url=base_url) as client:
        response = await client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_rejects_bad_api_key(mocked_app_without_api_key):
    transport = ASGITransport(app=mocked_app_without_api_key)
    async with AsyncClient(transport=transport, base_url=base_url + "/api") as client:
        files = {"file": ("test.pdf", b"%PDF-1.4...", "application/pdf")}
        headers = {"x-api-key": "wrong-key"}
        response = await client.post("/pdf/upload", files=files, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
