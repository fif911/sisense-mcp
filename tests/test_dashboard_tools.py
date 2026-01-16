"""Tests for Dashboard MCP tools."""

import json
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from src.tools.dashboard_tools import get_dashboard_tools, handle_dashboard_tool


def test_get_dashboard_tools():
    """Test that all Dashboard tools are defined."""
    tools = get_dashboard_tools()

    assert len(tools) == 2
    tool_names = [tool.name for tool in tools]
    assert "list_dashboards" in tool_names
    assert "get_dashboard_info" in tool_names


@pytest.mark.asyncio
async def test_handle_list_dashboards(dashboard_service):
    """Test list_dashboards tool handler."""
    mock_result = [
        {
            "_id": "68c20e36b10aaf740421cf12",
            "title": "Telecom Services (1)",
            "desc": "",
            "source": "67d081cdea0fb30032897721",
            "type": "dashboard",
            "created": "2025-09-10T23:48:06.009Z",
            "lastUpdated": "2025-09-10T23:48:06.009Z",
            "owner": "67c6232ca2e4be002f89c338",
            "isPublic": None,
            "lastOpened": "2025-09-11T16:38:36.859Z",
            "parentFolder": None,
        }
    ]
    dashboard_service.list_dashboards = AsyncMock(return_value=mock_result)

    result = await handle_dashboard_tool("list_dashboards", {}, dashboard_service)

    assert len(result) == 1
    assert result[0].type == "text"
    data = json.loads(result[0].text)
    assert data == mock_result
    assert data[0]["_id"] == "68c20e36b10aaf740421cf12"
    assert data[0]["title"] == "Telecom Services (1)"


@pytest.mark.asyncio
async def test_handle_get_dashboard_info_by_id(dashboard_service):
    """Test get_dashboard_info tool handler with ID."""
    mock_dashboard = {
        "_id": "68c20e36b10aaf740421cf12",
        "title": "Telecom Services (1)",
        "desc": "",
        "source": "67d081cdea0fb30032897721",
        "type": "dashboard",
        "created": "2025-09-10T23:48:06.009Z",
        "lastUpdated": "2025-09-10T23:48:06.009Z",
        "owner": "67c6232ca2e4be002f89c338",
        "datasource": {
            "title": "SOC Data Model",
            "id": "live:SOC Data Model",
            "fullname": "live:SOC Data Model",
            "live": True,
        },
        "layout": {"instanceid": "test", "type": "grid"},
        "filters": [],
        "settings": {"autoUpdateOnFiltersChange": True},
    }
    dashboard_service.get_dashboard = AsyncMock(return_value=mock_dashboard)

    result = await handle_dashboard_tool(
        "get_dashboard_info", {"dashboard_id": "68c20e36b10aaf740421cf12"}, dashboard_service
    )

    assert len(result) == 1
    data = json.loads(result[0].text)
    assert data == mock_dashboard
    assert data["_id"] == "68c20e36b10aaf740421cf12"
    assert "datasource" in data
    assert "layout" in data
    dashboard_service.get_dashboard.assert_called_once_with(
        dashboard_id="68c20e36b10aaf740421cf12", dashboard_name=None
    )


@pytest.mark.asyncio
async def test_handle_get_dashboard_info_by_name(dashboard_service):
    """Test get_dashboard_info tool handler with name."""
    mock_dashboard = {
        "_id": "68c20e36b10aaf740421cf12",
        "title": "Telecom Services (1)",
        "desc": "",
        "source": "67d081cdea0fb30032897721",
        "type": "dashboard",
        "datasource": {
            "title": "SOC Data Model",
            "id": "live:SOC Data Model",
            "fullname": "live:SOC Data Model",
            "live": True,
        },
        "layout": {},
        "filters": [],
    }
    dashboard_service.get_dashboard = AsyncMock(return_value=mock_dashboard)

    result = await handle_dashboard_tool(
        "get_dashboard_info", {"dashboard_name": "Telecom Services (1)"}, dashboard_service
    )

    assert len(result) == 1
    data = json.loads(result[0].text)
    assert data == mock_dashboard
    assert data["title"] == "Telecom Services (1)"
    dashboard_service.get_dashboard.assert_called_once_with(
        dashboard_id=None, dashboard_name="Telecom Services (1)"
    )


@pytest.mark.asyncio
async def test_handle_get_dashboard_info_missing_args(dashboard_service):
    """Test get_dashboard_info with missing both ID and name."""
    with pytest.raises(ValueError, match="Either dashboard_id or dashboard_name must be provided"):
        await handle_dashboard_tool("get_dashboard_info", {}, dashboard_service)


@pytest.mark.asyncio
async def test_handle_dashboard_tool_http_error(dashboard_service):
    """Test tool handler with HTTP error."""
    dashboard_service.list_dashboards = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "500 Internal Server Error",
            request=MagicMock(url="https://test.com/api/v1/dashboards"),
            response=MagicMock(status_code=500, text="Internal Server Error"),
        )
    )

    with pytest.raises(Exception, match="API request failed"):
        await handle_dashboard_tool("list_dashboards", {}, dashboard_service)


@pytest.mark.asyncio
async def test_handle_dashboard_tool_timeout(dashboard_service):
    """Test tool handler with timeout error."""
    dashboard_service.get_dashboard = AsyncMock(side_effect=httpx.TimeoutException("Timeout"))

    with pytest.raises(Exception, match="Request timeout"):
        await handle_dashboard_tool(
            "get_dashboard_info", {"dashboard_id": "68c20e36b10aaf740421cf12"}, dashboard_service
        )


@pytest.mark.asyncio
async def test_handle_unknown_tool(dashboard_service):
    """Test tool handler with unknown tool name."""
    with pytest.raises(ValueError, match="Unknown Dashboard tool"):
        await handle_dashboard_tool("unknown_tool", {}, dashboard_service)
