"""MCP tool definitions and handlers."""

from .dashboard_tools import get_dashboard_tools, handle_dashboard_tool
from .elasticube_tools import get_elasticube_tools, handle_elasticube_tool

__all__ = [
    "get_elasticube_tools",
    "handle_elasticube_tool",
    "get_dashboard_tools",
    "handle_dashboard_tool",
]
