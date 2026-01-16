"""MCP server for Sisense API integration."""

import asyncio
import logging
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

from .client import SisenseClient
from .config import settings
from .services import DashboardService, ElastiCubeService
from .tools import (
    get_dashboard_tools,
    get_elasticube_tools,
    handle_dashboard_tool,
    handle_elasticube_tool,
)

# Configure logging to stderr (not stdout) so it doesn't interfere with MCP protocol
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,  # Log to stderr, not stdout
)
logger = logging.getLogger(__name__)

app = Server("sisense-mcp")

# Initialize services
try:
    logger.debug("Initializing SisenseClient at module load...")
    client = SisenseClient(settings.sisense_base_url, settings.sisense_api_token)
    elasticube_service = ElastiCubeService(client)
    dashboard_service = DashboardService(client)
    logger.debug("Services initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize services during module import: {e}", exc_info=True)
    client = None
    elasticube_service = None
    dashboard_service = None


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available MCP tools."""
    tools = []
    tools.extend(get_elasticube_tools())
    tools.extend(get_dashboard_tools())
    return tools


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """Handle tool execution requests."""
    if elasticube_service is None or dashboard_service is None:
        raise RuntimeError("Services were not initialized. Check configuration and logs.")
        
    # Route to appropriate tool handler
    elasticube_tool_names = ["list_elasticubes", "get_elasticube_schema", "query_elasticube"]
    dashboard_tool_names = ["list_dashboards", "get_dashboard_info"]

    if name in elasticube_tool_names:
        return await handle_elasticube_tool(name, arguments, elasticube_service)
    elif name in dashboard_tool_names:
        return await handle_dashboard_tool(name, arguments, dashboard_service)
        else:
            raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point for the MCP server."""
    try:
        logger.info("Initializing Sisense MCP server...")
        logger.info(f"Base URL: {settings.sisense_base_url}")
        logger.info("Token configured: " + ("Yes" if settings.sisense_api_token else "No"))
        
        logger.info("Starting stdio_server...")
        async with stdio_server() as (read_stream, write_stream):
            logger.info("stdio_server started successfully")
            logger.info("Running MCP server...")
            await app.run(read_stream, write_stream, app.create_initialization_options())
            logger.info("MCP server finished")
    except Exception as e:
        logger.error(f"Server crashed: {e}", exc_info=True)
        raise


def cli():
    """Console script entry point (synchronous wrapper for async main)."""
    asyncio.run(main())


if __name__ == "__main__":
    cli()
