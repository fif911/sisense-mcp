"""MCP tools for Dashboard operations."""

import base64
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
                        "description": "Name/title of the dashboard (e.g., 'Revenue over time')",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="export_dashboard_png",
            description=(
                "Export a Sisense dashboard as a PNG image. "
                "Returns the dashboard rendered as a PNG image file. "
                "The image is returned as a base64-encoded string that can be used to display or save the dashboard visualization."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "dashboard_id": {
                        "type": "string",
                        "description": "ID of the dashboard to export (required)",
                    },
                    "width": {
                        "type": "integer",
                        "description": "Image width in pixels (default: 1000)",
                        "default": 1000,
                    },
                    "layout": {
                        "type": "string",
                        "description": "Layout mode - 'asis' or other layout options (default: 'asis')",
                        "default": "asis",
                    },
                    "show_dashboard_title": {
                        "type": "boolean",
                        "description": "Whether to show dashboard title (default: true)",
                        "default": True,
                    },
                    "show_dashboard_filters": {
                        "type": "boolean",
                        "description": "Whether to show dashboard filters (default: true)",
                        "default": True,
                    },
                    "show_datasource_info": {
                        "type": "boolean",
                        "description": "Whether to show datasource info (default: true)",
                        "default": True,
                    },
                    "shared_mode": {
                        "type": "boolean",
                        "description": "If dashboard is in shared mode (optional)",
                    },
                    "tenant_id": {
                        "type": "string",
                        "description": "Tenant ID for x-tenant-id header (optional)",
                    },
                },
                "required": ["dashboard_id"],
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

        elif name == "export_dashboard_png":
            dashboard_id = arguments.get("dashboard_id")
            if not dashboard_id:
                raise ValueError("dashboard_id is required for export_dashboard_png")

            png_data = await service.export_dashboard_png(
                dashboard_id=dashboard_id,
                width=arguments.get("width", 1000),
                layout=arguments.get("layout", "asis"),
                show_dashboard_title=arguments.get("show_dashboard_title", True),
                show_dashboard_filters=arguments.get("show_dashboard_filters", True),
                show_datasource_info=arguments.get("show_datasource_info", True),
                shared_mode=arguments.get("shared_mode"),
                tenant_id=arguments.get("tenant_id"),
            )

            # Encode PNG as base64 for JSON transmission
            png_base64 = base64.b64encode(png_data).decode("utf-8")
            result = {
                "dashboard_id": dashboard_id,
                "image_format": "png",
                "image_data_base64": png_base64,
                "image_size_bytes": len(png_data),
            }
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
