"""Tests for ElastiCube MCP tools."""

import json
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from src.tools.elasticube_tools import get_elasticube_tools, handle_elasticube_tool


def test_get_elasticube_tools():
    """Test that all ElastiCube tools are defined."""
    tools = get_elasticube_tools()

    assert len(tools) == 3
    tool_names = [tool.name for tool in tools]
    assert "list_elasticubes" in tool_names
    assert "get_elasticube_schema" in tool_names
    assert "query_elasticube" in tool_names


@pytest.mark.asyncio
async def test_handle_list_elasticubes(elasticube_service):
    """Test list_elasticubes tool handler."""
    mock_result = [
        {
            "_id": "507f1f77bcf86cd799439011",
            "title": "Sales Data Model",
            "type": "extract",
            "server": "LocalHost",
            "lastUpdated": "2024-08-02T16:50:14.417Z",
        }
    ]
    elasticube_service.list_elasticubes = AsyncMock(return_value=mock_result)

    result = await handle_elasticube_tool("list_elasticubes", {}, elasticube_service)

    assert len(result) == 1
    assert result[0].type == "text"
    data = json.loads(result[0].text)
    assert data == mock_result
    assert data[0]["_id"] == "507f1f77bcf86cd799439011"
    assert data[0]["title"] == "Sales Data Model"


@pytest.mark.asyncio
async def test_handle_get_elasticube_schema(elasticube_service):
    """Test get_elasticube_schema tool handler."""
    mock_schema = {
        "oid": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Sales Data Model",
        "server": "LocalHost",
        "datasets": [
            {
                "oid": "550e8400-e29b-41d4-a716-446655440001",
                "type": "elasticube",
                "name": "Dataset1",
                "fullname": "Dataset1",
            }
        ],
        "relations": [],
        "relationsTables": [],
    }
    elasticube_service.get_schema = AsyncMock(return_value=mock_schema)

    result = await handle_elasticube_tool(
        "get_elasticube_schema", {"elasticube_name": "Sales Data Model"}, elasticube_service
    )

    assert len(result) == 1
    data = json.loads(result[0].text)
    assert data == mock_schema
    assert "datasets" in data
    assert "relations" in data
    elasticube_service.get_schema.assert_called_once_with("Sales Data Model")


@pytest.mark.asyncio
async def test_handle_get_elasticube_schema_missing_arg(elasticube_service):
    """Test get_elasticube_schema with missing required argument."""
    with pytest.raises(ValueError, match="Missing required argument"):
        await handle_elasticube_tool("get_elasticube_schema", {}, elasticube_service)


@pytest.mark.asyncio
async def test_handle_query_elasticube(elasticube_service):
    """Test query_elasticube tool handler."""
    mock_result = {
        "rows": [
            {"BRAND_ID": 1, "BRAND_NAME": "Brand A"},
            {"BRAND_ID": 2, "BRAND_NAME": "Brand B"},
        ],
        "metadata": {
            "columns": [
                {"name": "BRAND_ID", "type": "numeric"},
                {"name": "BRAND_NAME", "type": "text"},
            ],
            "rowCount": 2,
        },
    }
    elasticube_service.query_sql = AsyncMock(return_value=mock_result)

    result = await handle_elasticube_tool(
        "query_elasticube",
        {
            "datasource": "Sales Data Model",
            "sql_query": "SELECT * FROM brands LIMIT 10",
        },
        elasticube_service,
    )

    assert len(result) == 1
    data = json.loads(result[0].text)
    assert data == mock_result
    assert "rows" in data
    assert "metadata" in data
    assert len(data["rows"]) == 2
    elasticube_service.query_sql.assert_called_once_with(
        datasource="Sales Data Model",
        sql_query="SELECT * FROM brands LIMIT 10",
        count=5000,
        offset=0,
    )


@pytest.mark.asyncio
async def test_handle_query_elasticube_with_pagination(elasticube_service):
    """Test query_elasticube with custom count and offset."""
    mock_result = {
        "rows": [{"BRAND_ID": 51, "BRAND_NAME": "Brand 51"}],
        "metadata": {"columns": [{"name": "BRAND_ID"}, {"name": "BRAND_NAME"}], "rowCount": 1},
    }
    elasticube_service.query_sql = AsyncMock(return_value=mock_result)

    await handle_elasticube_tool(
        "query_elasticube",
        {
            "datasource": "Sales Data Model",
            "sql_query": "SELECT * FROM brands",
            "count": 100,
            "offset": 50,
        },
        elasticube_service,
    )

    elasticube_service.query_sql.assert_called_once_with(
        datasource="Sales Data Model", sql_query="SELECT * FROM brands", count=100, offset=50
    )


@pytest.mark.asyncio
async def test_handle_query_elasticube_missing_args(elasticube_service):
    """Test query_elasticube with missing required arguments."""
    with pytest.raises(ValueError, match="Missing required arguments"):
        await handle_elasticube_tool(
            "query_elasticube", {"datasource": "Sales Data Model"}, elasticube_service
        )


@pytest.mark.asyncio
async def test_handle_elasticube_tool_http_error(elasticube_service):
    """Test tool handler with HTTP error."""
    elasticube_service.list_elasticubes = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "404 Not Found",
            request=MagicMock(url="https://test.com/api/v1/elasticubes/getElasticubes"),
            response=MagicMock(status_code=404, text="Not Found"),
        )
    )

    with pytest.raises(Exception, match="API endpoint not found"):
        await handle_elasticube_tool("list_elasticubes", {}, elasticube_service)


@pytest.mark.asyncio
async def test_handle_elasticube_tool_timeout(elasticube_service):
    """Test tool handler with timeout error."""
    elasticube_service.query_sql = AsyncMock(side_effect=httpx.TimeoutException("Timeout"))

    with pytest.raises(Exception, match="Request timeout"):
        await handle_elasticube_tool(
            "query_elasticube",
            {"datasource": "Sales Data Model", "sql_query": "SELECT * FROM brands"},
            elasticube_service,
        )


@pytest.mark.asyncio
async def test_handle_unknown_tool(elasticube_service):
    """Test tool handler with unknown tool name."""
    with pytest.raises(ValueError, match="Unknown ElastiCube tool"):
        await handle_elasticube_tool("unknown_tool", {}, elasticube_service)
