"""MCP tools for Dashboard operations."""

import json
from typing import Any

import httpx
from mcp.types import TextContent, Tool

from ..services import DashboardService


def get_dashboard_tools() -> list[Tool]:
    """Get all Dashboard-related MCP tools.

    Returns:
        List of Tool definitions for Dashboard operations
    """
    return [
        Tool(
            name="list_dashboards",
            description=(
                "List all available dashboards from Sisense. "
                "Use this to discover which dashboards exist, then pick one to inspect further with get_dashboard_info. "
                "Returns a filtered list per dashboard with: _id, title, desc, source, type, created, lastUpdated, owner, isPublic, lastOpened, parentFolder."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_dashboard_info",
            description=(
                "Get information about a specific Sisense dashboard by ID or name. "
                "Use this when you want to inspect how a dashboard is built (widgets, filters, datasources, and configuration) "
                "or to discover which cubes and fields a dashboard uses. "
                "Returns the full dashboard object with all fields from the Sisense API."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "dashboard_id": {
                        "type": "string",
                        "description": "ID of the dashboard (e.g., '68c20e36b10aaf740421cf12')",
                    },
                    "dashboard_name": {
                        "type": "string",
                        "description": "Name/title of the dashboard (e.g., 'Telecom Services (1)')",
                    },
                },
                "required": [],
            },
        ),
    ]


async def handle_dashboard_tool(
    name: str, arguments: dict[str, Any], service: DashboardService
) -> list[TextContent]:
    """Handle Dashboard tool execution.

    Args:
        name: Tool name
        arguments: Tool arguments
        service: Dashboard service instance

    Returns:
        List of TextContent with tool results

    Raises:
        ValueError: If tool name is unknown or required arguments are missing
        httpx.HTTPStatusError: If API request fails
        httpx.TimeoutException: If request times out
    """
    try:
        if name == "list_dashboards":
            result = await service.list_dashboards()

        elif name == "get_dashboard_info":
            dashboard_id = arguments.get("dashboard_id")
            dashboard_name = arguments.get("dashboard_name")

            if not dashboard_id and not dashboard_name:
                raise ValueError("Either dashboard_id or dashboard_name must be provided")

            result = await service.get_dashboard(
                dashboard_id=dashboard_id, dashboard_name=dashboard_name
            )
        else:
            raise ValueError(f"Unknown Dashboard tool: {name}")

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except httpx.HTTPStatusError as e:
        # Handle HTTP errors
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
            "Potential causes: The Sisense instance is slow or unreachable."
        ) from e
