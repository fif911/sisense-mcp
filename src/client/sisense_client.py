"""Pure HTTP client for Sisense API - no business logic."""

from typing import Any
from urllib.parse import quote

import httpx


class SisenseClient:
    """HTTP client for making requests to Sisense API.

    This is a pure HTTP client with no business logic. It handles:
    - HTTP request/response
    - Authentication headers
    - URL encoding
    - Error handling at HTTP level
    """

    def __init__(self, base_url: str, api_token: str):
        """Initialize the Sisense HTTP client.

        Args:
            base_url: Base URL of the Sisense instance (e.g., https://instance.sisense.com)
            api_token: Personal API token for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def get(
        self, endpoint: str, params: dict[str, Any] = None, timeout: float = 30.0
    ) -> dict[str, Any]:
        """Make a GET request to the Sisense API.

        Args:
            endpoint: API endpoint path (e.g., '/api/v1/elasticubes/getElasticubes')
            params: Query parameters
            timeout: Request timeout in seconds

        Returns:
            JSON response as dictionary

        Raises:
            httpx.HTTPStatusError: If the request fails
            httpx.TimeoutException: If the request times out
        """
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(
                f"{self.base_url}{endpoint}", headers=self.headers, params=params
            )
            response.raise_for_status()
            return response.json()

    async def post(
        self, endpoint: str, json_data: dict[str, Any] = None, timeout: float = 30.0
    ) -> dict[str, Any]:
        """Make a POST request to the Sisense API.

        Args:
            endpoint: API endpoint path
            json_data: JSON body data
            timeout: Request timeout in seconds

        Returns:
            JSON response as dictionary

        Raises:
            httpx.HTTPStatusError: If the request fails
            httpx.TimeoutException: If the request times out
        """
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{self.base_url}{endpoint}", headers=self.headers, json=json_data
            )
            response.raise_for_status()
            return response.json()

    async def post_binary(
        self,
        endpoint: str,
        json_data: dict[str, Any] = None,
        headers: dict[str, str] = None,
        params: dict[str, Any] = None,
        timeout: float = 60.0,
    ) -> bytes:
        """Make a POST request that returns binary data (e.g., PNG image).

        Args:
            endpoint: API endpoint path
            json_data: JSON body data
            headers: Additional headers to include (merged with default headers)
            params: Query parameters
            timeout: Request timeout in seconds (default 60 for image generation)

        Returns:
            Binary response data as bytes

        Raises:
            httpx.HTTPStatusError: If the request fails
            httpx.TimeoutException: If the request times out
        """
        # Merge additional headers with default headers
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)
        # Override Accept header for binary responses
        request_headers["Accept"] = "image/png"

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{self.base_url}{endpoint}",
                headers=request_headers,
                json=json_data,
                params=params,
            )
            response.raise_for_status()
            return response.content

    def encode_datasource_name(self, datasource: str) -> str:
        """URL encode a datasource name for use in API endpoints.

        Args:
            datasource: Datasource name (e.g., 'Sales Data Model')

        Returns:
            URL-encoded datasource name
        """
        return quote(datasource, safe="")
