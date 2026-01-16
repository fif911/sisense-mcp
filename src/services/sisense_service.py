"""Core Sisense service - base service with common functionality."""

from ..client import SisenseClient


class SisenseService:
    """Base service for Sisense operations."""

    def __init__(self, client: SisenseClient):
        """Initialize the service with an HTTP client.

        Args:
            client: Sisense HTTP client instance
        """
        self.client = client
