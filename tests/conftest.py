"""Pytest configuration and fixtures."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.client import SisenseClient
from src.services import DashboardService, ElastiCubeService


@pytest.fixture
def mock_client():
    """Create a mock SisenseClient."""
    client = MagicMock(spec=SisenseClient)
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.encode_datasource_name = MagicMock(side_effect=lambda x: x.replace(" ", "%20"))
    return client


@pytest.fixture
def elasticube_service(mock_client):
    """Create an ElastiCubeService with a mock client."""
    return ElastiCubeService(mock_client)


@pytest.fixture
def dashboard_service(mock_client):
    """Create a DashboardService with a mock client."""
    return DashboardService(mock_client)
