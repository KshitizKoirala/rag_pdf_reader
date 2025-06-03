from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from app.core.embedder import generate_embedings
from app.core.extract_pdf import extract_text_from_pdf


def test_generate_embedings_success():
    # Setup
    mock_model = MagicMock()
    mock_model.encode.return_value = np.array([[0.1, 0.2], [0.3, 0.4]])

    mock_app_state = MagicMock()
    mock_app_state.model = mock_model

    mock_request = MagicMock()
    mock_request.app.state = mock_app_state

    chunks = ["hello", "world"]

    # Call
    embeddings = generate_embedings(mock_request, chunks)

    # Assert
    assert embeddings == [[0.1, 0.2], [0.3, 0.4]]
    mock_model.encode.assert_called_once_with(chunks)


def test_generate_embedings_missing_model():
    request = MagicMock()
    request.app.state = MagicMock()

    del request.app.state.model  # simulate missing model

    with pytest.raises(RuntimeError, match="Model not loaded"):
        generate_embedings(request, ["sample"])


@patch("app.core.extract_pdf.fitz.open")
def test_extract_text_from_pdf(mock_fitz_open):
    # Setup mock page behavior
    mock_page1 = MagicMock()
    mock_page1.get_text.return_value = "Page 1 content."

    mock_page2 = MagicMock()
    mock_page2.get_text.return_value = "Page 2 content."

    mock_document = [mock_page1, mock_page2]
    mock_fitz_open.return_value = mock_document

    # Call the function
    text = extract_text_from_pdf(b"%PDF-1.4 fake bytes")

    # Assertions
    assert text == "Page 1 content.Page 2 content."
    mock_fitz_open.assert_called_once_with(
        stream=b"%PDF-1.4 fake bytes", filetype="pdf")
