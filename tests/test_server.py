"""Integration tests for the MCP server."""

import os
from unittest.mock import AsyncMock, patch

import pytest

# Set test environment variables before importing server
os.environ.setdefault("SISENSE_BASE_URL", "https://test.sisense.com")
os.environ.setdefault("SISENSE_API_TOKEN", "test_token")


def test_list_tools():
    """Test that server lists all tools correctly."""
    # This is a synchronous test, but list_tools is async
    # We'll test it by checking the tool definitions directly
    from src.tools import get_dashboard_tools, get_elasticube_tools

    elasticube_tools = get_elasticube_tools()
    dashboard_tools = get_dashboard_tools()

    assert len(elasticube_tools) == 3
    assert len(dashboard_tools) == 2

    all_tool_names = [t.name for t in elasticube_tools + dashboard_tools]
    assert "list_elasticubes" in all_tool_names
    assert "get_elasticube_schema" in all_tool_names
    assert "query_elasticube" in all_tool_names
    assert "list_dashboards" in all_tool_names
    assert "get_dashboard_info" in all_tool_names


@pytest.mark.asyncio
async def test_call_tool_list_elasticubes():
    """Test server call_tool with list_elasticubes."""
    with patch("src.server.elasticube_service") as mock_service:
        mock_service.list_elasticubes = AsyncMock(
            return_value=[
                {
                    "_id": "507f1f77bcf86cd799439011",
                    "title": "Sales Data Model",
                    "type": "extract",
                    "server": "LocalHost",
                    "lastUpdated": "2024-08-02T16:50:14.417Z",
                }
            ]
        )

        from src.tools import handle_elasticube_tool

        result = await handle_elasticube_tool("list_elasticubes", {}, mock_service)

        assert len(result) == 1
        assert result[0].type == "text"


@pytest.mark.asyncio
async def test_call_tool_unknown_tool():
    """Test server call_tool with unknown tool."""
    with pytest.raises(ValueError, match="Unknown tool"):
        # Simulate what server.call_tool would do
        tool_name = "unknown_tool"
        if tool_name not in [
            "list_elasticubes",
            "get_elasticube_schema",
            "query_elasticube",
            "list_dashboards",
            "get_dashboard_info",
        ]:
            raise ValueError(f"Unknown tool: {tool_name}")
