"""Tests for SisenseClient."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.client import SisenseClient


@pytest.mark.asyncio
async def test_client_init():
    """Test client initialization."""
    client = SisenseClient("https://test.sisense.com", "test_token")
    assert client.base_url == "https://test.sisense.com"
    assert "Bearer test_token" in client.headers["Authorization"]


@pytest.mark.asyncio
async def test_client_get_success():
    """Test successful GET request."""
    client = SisenseClient("https://test.sisense.com", "test_token")

    mock_response = {"data": "test"}
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response_obj = MagicMock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response_obj

        result = await client.get("/api/test")
        assert result == mock_response
        mock_client.get.assert_called_once()


@pytest.mark.asyncio
async def test_client_get_error():
    """Test GET request with HTTP error."""
    client = SisenseClient("https://test.sisense.com", "test_token")

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response_obj = MagicMock()
        mock_response_obj.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock()
        )
        mock_client.get.return_value = mock_response_obj

        with pytest.raises(httpx.HTTPStatusError):
            await client.get("/api/test")


@pytest.mark.asyncio
async def test_client_post_success():
    """Test successful POST request."""
    client = SisenseClient("https://test.sisense.com", "test_token")

    mock_response = {"result": "success"}
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response_obj = MagicMock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_response_obj

        result = await client.post("/api/test", json_data={"key": "value"})
        assert result == mock_response


def test_encode_datasource_name():
    """Test datasource name encoding."""
    client = SisenseClient("https://test.sisense.com", "test_token")

    # Test basic encoding
    encoded = client.encode_datasource_name("Sales Data Model")
    assert "%20" in encoded or " " not in encoded

    # Test already safe characters
    encoded = client.encode_datasource_name("SimpleName")
    assert encoded == "SimpleName"
