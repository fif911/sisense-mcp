"""MCP tools for ElastiCube operations."""

import json
from typing import Any

import httpx
from mcp.types import TextContent, Tool

from ..services import ElastiCubeService


def get_elasticube_tools() -> list[Tool]:
    """Get all ElastiCube-related MCP tools.

    Returns:
        List of Tool definitions for ElastiCube operations
    """
    return [
        Tool(
            name="list_elasticubes",
            description=(
                "List all available ElastiCubes/datamodels from Sisense. "
                "Use this first when you are not sure which cube name to work with, or you want to explore what data models exist. "
                "Returns a lightweight list per cube with: _id, title, type, server, lastUpdated (sufficient to pick a cube for further calls)."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_elasticube_schema",
            description=(
                "Get the schema (tables and columns) for a Sisense ElastiCube/Live Connection. "
                "Use this when you need to understand the data model (tables, columns, data types, and table-to-table relationships) "
                "for a specific cube before writing queries or debugging joins. "
                "Returns the full schema JSON including datasets, tables, columns, relations, and relationTables."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "elasticube_name": {
                        "type": "string",
                        "description": "Name of the ElastiCube (e.g., 'Sales Data Model')",
                    }
                },
                "required": ["elasticube_name"],
            },
        ),
        Tool(
            name="query_elasticube",
            description=(
                "Execute a SQL query to extract data from an ElastiCube. "
                "Use this when you already know which cube and tables/fields you want and need actual rows for analysis, debugging, or sampling. "
                "Returns the query result rows and basic metadata; use count/offset for pagination."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "datasource": {
                        "type": "string",
                        "description": "Name of the ElastiCube datasource (e.g., 'Sales Data Model')",
                    },
                    "sql_query": {
                        "type": "string",
                        "description": "SQL query string (must start with SELECT). Examples: 'SELECT * FROM TableName LIMIT 100', 'SELECT COUNT(*) FROM TableName', 'SELECT column1, column2 FROM TableName WHERE condition'",
                    },
                    "count": {
                        "type": "integer",
                        "description": "Maximum number of rows to return (default: 5000, max recommended: 10000 per request). Actual limit is 5000 rows per request for Live Connection and ~2M for Elastic Cubes.",
                        "default": 5000,
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset for pagination (default: 0). Use with count for large result sets.",
                        "default": 0,
                    },
                },
                "required": ["datasource", "sql_query"],
            },
        ),
    ]


async def handle_elasticube_tool(
    name: str, arguments: dict[str, Any], service: ElastiCubeService
) -> list[TextContent]:
    """Handle ElastiCube tool execution.

    Args:
        name: Tool name
        arguments: Tool arguments
        service: ElastiCube service instance

    Returns:
        List of TextContent with tool results

    Raises:
        ValueError: If tool name is unknown or required arguments are missing
        httpx.HTTPStatusError: If API request fails
        httpx.TimeoutException: If request times out
    """
    try:
        if name == "list_elasticubes":
            result = await service.list_elasticubes()

        elif name == "get_elasticube_schema":
            if "elasticube_name" not in arguments:
                raise ValueError("Missing required argument: elasticube_name")
            result = await service.get_schema(arguments["elasticube_name"])

        elif name == "query_elasticube":
            if "datasource" not in arguments or "sql_query" not in arguments:
                raise ValueError("Missing required arguments: datasource and sql_query")
            result = await service.query_sql(
                datasource=arguments["datasource"],
                sql_query=arguments["sql_query"],
                count=arguments.get("count", 5000),
                offset=arguments.get("offset", 0),
            )
        else:
            raise ValueError(f"Unknown ElastiCube tool: {name}")

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except httpx.HTTPStatusError as e:
        # Handle HTTP errors - include helpful context for common cases
        if e.response.status_code == 404:
            # For 404, provide more context about what endpoint was tried
            if "elasticubes" in str(e.request.url) if e.request else False:
                error_msg = (
                    "API endpoint not found (404). "
                    "The /api/v1/elasticubes/getElasticubes endpoint is not available in this Sisense instance. "
                    "Cube names must be known in advance. "
                    "Use get_elasticube_schema or query_elasticube with a specific cube name."
                )
            else:
                error_msg = f"API endpoint not found (404): {str(e.request.url) if e.request else 'unknown'}"
        else:
            error_details = {
                "error": f"API Error {e.response.status_code}",
                "message": e.response.text[:1000] if e.response.text else str(e),
                "url": str(e.request.url) if e.request else None,
            }
            error_msg = f"API request failed: {json.dumps(error_details, indent=2)}"

        raise Exception(error_msg) from e

    except httpx.TimeoutException as e:
        # Re-raise timeout errors with helpful message
        raise Exception(
            "Request timeout. The request took too long. "
            "Potential causes: The ElastiCube/Live Connection is misconfigured or the query is too complex (then set count to limit the number of rows returned)."
        ) from e
