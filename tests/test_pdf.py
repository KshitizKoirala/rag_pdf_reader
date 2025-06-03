from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app import create_app

base_url = "http://localhost:8000/api"
headers = {"x-api-key": "test-secret"}


@pytest.fixture
def mocked_app_with_api_key():
    with (
        patch("app.__init__.SentenceTransformer") as mocked_model,
        patch("app.database.config.qdrant_client") as mock_qdrant_client,
        patch("app.auth.auth_guard.get_email_from_api_key") as mock_get_email,
    ):
        mocked_model.return_value = MagicMock()
        mock_qdrant_client.get_collections.return_value.collections = []
        mock_qdrant_client.recreate_collection.return_value = None
        # ✅ Mock API key function to always succeed
        mock_get_email.return_value = "test@example.com"

        app = create_app()
        yield app


@pytest.mark.asyncio
async def test_pdf_upload(mocked_app_with_api_key):
    with patch("app.pdf.routes.pdf_service") as mock_service:
        mock_service.process_pdf_file = AsyncMock(return_value=True)

        transport = ASGITransport(app=mocked_app_with_api_key)
        async with AsyncClient(transport=transport, base_url=base_url) as client:
            files = {
                "file": ("test.pdf", b"%PDF-1.4 Fake PDF Content", "application/pdf")
            }
            headers = {"x-api-key": "valid-test-key"}
            response = await client.post("/pdf/upload", files=files, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Uploaded successfully"
