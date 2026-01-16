# Sisense MCP Server

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Test Status](https://img.shields.io/badge/tests-passing-brightgreen)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for interacting with the Sisense API. This server enables AI assistants to query ElastiCubes, fetch schemas, and retrieve dashboard information from Sisense instances.

## Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites & Required Inputs](#prerequisites--required-inputs)
- [Functionality Overview](#functionality-overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Functionality Details](#functionality-details)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Quick Start

### Single Command (No Installation Required)

Run directly from GitHub using `uvx` (like `npx` for Python):

```bash
uvx --from git+https://github.com/fif911/sisense-mcp.git sisense-mcp
```

Then configure your MCP client (see [Configuration](#configuration) section).

### Or Install First

1. **Install from GitHub:**
   ```bash
   uv pip install git+https://github.com/fif911/sisense-mcp.git
   ```

2. **Configure your MCP client** (see [Configuration](#configuration) section)

3. **Start using the tools!** Your AI assistant can now interact with Sisense.

## Prerequisites & Required Inputs

Before you can use this MCP server, you need two pieces of information from your Sisense instance:

### 1. Sisense Instance URL

**What it is:** The base URL of your Sisense instance (e.g., `https://your-company.sisense.com` or `https://oxio-dev.sisense.com`).

**How to get it:**
- Open your Sisense instance in a web browser
- Copy the URL from the address bar (without any path after `.com`)
- Example: If you see `https://oxio-dev.sisense.com/app/main#/dashboards`, your base URL is `https://oxio-dev.sisense.com`

### 2. Personal API Token

**What it is:** A personal authentication token that allows the MCP server to make API requests on your behalf.

**How to get it:**
1. Log in to your Sisense instance
2. Click on your **user profile icon** (usually in the top-right corner)
3. Select **"My Profile"** from the dropdown menu
4. Navigate to the **"API Token"** section
5. If you don't have a token yet:
   - Click **"Generate Token"** or **"Create Token"**
   - A token will be generated and displayed
6. **Copy the token immediately** - you won't be able to see it again after closing the dialog
7. Save it securely (you'll need it for configuration)

**Important Notes:**
- Personal API tokens don't expire unless manually regenerated
- Each user has their own token
- Tokens are tied to your user permissions - the MCP server will have the same access as your user account
- If you lose your token, you'll need to generate a new one

## Functionality Overview

The Sisense MCP server provides **5 tools** that enable AI assistants to interact with your Sisense instance:

1. **`list_elasticubes`** - Discover available ElastiCubes/datamodels
2. **`get_elasticube_schema`** - Understand data structure (tables, columns, relationships)
3. **`query_elasticube`** - Execute SQL queries to extract data
4. **`list_dashboards`** - Discover available dashboards
5. **`get_dashboard_info`** - Inspect dashboard configuration and components

These tools allow AI assistants to:
- Explore your data models and understand their structure
- Query data directly from ElastiCubes
- Discover and analyze dashboard configurations
- Answer questions about your Sisense data

## Installation

### Prerequisites

- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`
- Sisense instance URL and personal API token (see [Prerequisites & Required Inputs](#prerequisites--required-inputs))

### Option 1: Run Directly from GitHub (Recommended - No Local Clone Required)

You can run the server directly from GitHub without cloning or installing, similar to how Node.js tools work with `npx`. This is the simplest approach!

**Using `uvx` (like `npx` for Python) - RECOMMENDED:**

```bash
uvx --from git+https://github.com/fif911/sisense-mcp.git sisense-mcp
```

This single command will:
1. Download the package from GitHub (if not already cached)
2. Install dependencies in an isolated environment
3. Run the `sisense-mcp` command

**Install a specific branch or tag:**

```bash
# Run from a specific branch
uvx --from git+https://github.com/fif911/sisense-mcp.git@main sisense-mcp

# Run from a specific tag/version
uvx --from git+https://github.com/fif911/sisense-mcp.git@v0.1.0 sisense-mcp
```

**Alternative: Install First, Then Run**

If you prefer to install the package first (useful for frequent use):

**Using uv:**

```bash
uv pip install git+https://github.com/fif911/sisense-mcp.git
sisense-mcp
```

**Using pip:**

```bash
pip install git+https://github.com/fif911/sisense-mcp.git
sisense-mcp
```

**Updating the package:**

To update to the latest version from GitHub:

```bash
uv pip install --upgrade git+https://github.com/fif911/sisense-mcp.git
# or with pip:
pip install --upgrade git+https://github.com/fif911/sisense-mcp.git
```

### Option 2: Clone and Install Locally

If you prefer to clone the repository locally:

**Step 1: Clone the Repository**

```bash
git clone https://github.com/fif911/sisense-mcp.git
cd sisense-mcp
```

**Step 2: Install Dependencies**

**Using uv (recommended):**

```bash
uv sync
```

**Using pip:**

```bash
pip install -e .
```

## Configuration

The MCP server needs to be configured in your MCP client. The configuration varies depending on which client you're using.

### Environment Variables

The server requires two environment variables:

- `SISENSE_BASE_URL` - Your Sisense instance URL (e.g., `https://your-instance.sisense.com`)
- `SISENSE_API_TOKEN` - Your personal API token

### Configuration Examples

#### Option A: Using `uvx` (Run Directly from GitHub - Recommended)

The simplest approach - runs directly from GitHub without installation, like `npx`:

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "sisense": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/fif911/sisense-mcp.git",
        "sisense-mcp"
      ],
      "env": {
        "SISENSE_BASE_URL": "https://your-instance.sisense.com",
        "SISENSE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json` on macOS/Linux):

```json
{
  "mcpServers": {
    "sisense": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/fif911/sisense-mcp.git",
        "sisense-mcp"
      ],
      "env": {
        "SISENSE_BASE_URL": "https://your-instance.sisense.com",
        "SISENSE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Run a specific version:**

```json
{
  "mcpServers": {
    "sisense": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/fif911/sisense-mcp.git@v0.1.0",
        "sisense-mcp"
      ],
      "env": {
        "SISENSE_BASE_URL": "https://your-instance.sisense.com",
        "SISENSE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Option B: Install First, Then Run

If you prefer to install the package first (useful for frequent use or production):

**After installing with `uv pip install git+https://...` or `pip install git+https://...`:**

```json
{
  "mcpServers": {
    "sisense": {
      "command": "sisense-mcp",
      "env": {
        "SISENSE_BASE_URL": "https://your-instance.sisense.com",
        "SISENSE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Or using Python module:**

```json
{
  "mcpServers": {
    "sisense": {
      "command": "python",
      "args": ["-m", "src.server"],
      "env": {
        "SISENSE_BASE_URL": "https://your-instance.sisense.com",
        "SISENSE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Option B: Using Local Clone

If you cloned the repository locally, use the directory-based approach:

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "sisense": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/sisense-mcp",
        "run",
        "python",
        "-m",
        "src.server"
      ],
      "env": {
        "SISENSE_BASE_URL": "https://your-instance.sisense.com",
        "SISENSE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json` on macOS/Linux):

```json
{
  "mcpServers": {
    "sisense": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/sisense-mcp",
        "run",
        "python",
        "-m",
        "src.server"
      ],
      "env": {
        "SISENSE_BASE_URL": "https://your-instance.sisense.com",
        "SISENSE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Using pip (Alternative):**

```json
{
  "mcpServers": {
    "sisense": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/sisense-mcp",
      "env": {
        "SISENSE_BASE_URL": "https://your-instance.sisense.com",
        "SISENSE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

**Important:** After updating your MCP client configuration, **restart the client** for changes to take effect.

## Functionality Details

### Tool: `list_elasticubes`

**Purpose:** Discover all available ElastiCubes/datamodels in your Sisense instance.

**When to use:** Use this first when you're not sure which cube name to work with, or when you want to explore what data models exist.

**Parameters:** None

**Returns:** A filtered list of ElastiCubes with essential fields:
- `_id` - Unique identifier
- `title` - Name of the ElastiCube (e.g., "[REPORT] M2M Summary")
- `type` - Type of ElastiCube (e.g., "extract", "live")
- `server` - Server where the cube is hosted
- `lastUpdated` - Timestamp of last update

**Example:**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "title": "[REPORT] M2M Summary",
    "type": "extract",
    "server": "LocalHost",
    "lastUpdated": "2024-01-15T10:30:00Z"
      }
]
```

**Note:** If the `/api/v1/elasticubes/getElasticubes` endpoint is not available in your Sisense instance, this tool will return a 404 error. In that case, you'll need to know cube names in advance and use `get_elasticube_schema` or `query_elasticube` directly.

### Tool: `get_elasticube_schema`

**Purpose:** Get the complete schema (tables, columns, data types, and relationships) for a specific ElastiCube.

**When to use:** Use this when you need to understand the data model structure before writing queries, or when debugging joins and relationships.

**Parameters:**
- `elasticube_name` (required, string) - Name of the ElastiCube (e.g., "[REPORT] M2M Summary")

**Returns:** Full schema JSON including:
- `datasets` - Dataset definitions
- `tables` - Table definitions with columns
- `columns` - Column details with data types
- `relations` - Column-level relationships
- `relationTables` - Table-level relationships

**Example:**
```json
{
  "datasets": [...],
  "tables": [
    {
      "name": "brands",
      "columns": [
        {"name": "BRAND_ID", "type": "numeric"},
        {"name": "BRAND_NAME", "type": "text"}
      ]
    }
  ],
  "relations": [...],
  "relationTables": [...]
}
```

### Tool: `query_elasticube`

**Purpose:** Execute SQL queries to extract data from an ElastiCube.

**When to use:** Use this when you already know which cube and tables/fields you want, and need actual data rows for analysis, debugging, or sampling.

**Parameters:**
- `datasource` (required, string) - Name of the ElastiCube datasource (e.g., "[REPORT] M2M Summary")
- `sql_query` (required, string) - SQL query string (must start with SELECT)
- `count` (optional, integer) - Maximum number of rows to return (default: 5000, max recommended: 10000)
- `offset` (optional, integer) - Offset for pagination (default: 0)

**Returns:** Query result with:
- `rows` - Array of result rows
- `metadata` - Query metadata (if `includeMetadata=true`)

**Limits:**
- Live Connections: ~5000 rows per request
- ElastiCubes: ~2M rows per request
- Use `count` and `offset` for pagination with large result sets

**Example:**
```json
{
  "rows": [
    {"BRAND_ID": 1, "BRAND_NAME": "Brand A"},
    {"BRAND_ID": 2, "BRAND_NAME": "Brand B"}
  ],
  "metadata": {...}
}
```

**SQL Query Examples:**
- `SELECT * FROM brands LIMIT 100`
- `SELECT COUNT(*) FROM brands`
- `SELECT column1, column2 FROM table1 WHERE condition`

### Tool: `list_dashboards`

**Purpose:** Discover all available dashboards in your Sisense instance.

**When to use:** Use this to explore which dashboards exist, then pick one to inspect further with `get_dashboard_info`.

**Parameters:** None

**Returns:** A filtered list of dashboards with essential fields:
- `_id` - Unique identifier
- `title` - Dashboard name
- `desc` - Description
- `source` - Source identifier
- `type` - Type (typically "dashboard")
- `created` - Creation timestamp
- `lastUpdated` - Last update timestamp
- `owner` - Owner user ID
- `isPublic` - Public visibility flag
- `lastOpened` - Last opened timestamp
- `parentFolder` - Parent folder identifier

**Example:**
```json
[
{
    "_id": "68c20e36b10aaf740421cf12",
    "title": "Telecom Services (1)",
    "desc": "Telecom services dashboard",
    "type": "dashboard",
    "created": "2024-01-01T00:00:00Z",
    "lastUpdated": "2024-01-15T10:30:00Z"
  }
]
```

### Tool: `get_dashboard_info`

**Purpose:** Get complete information about a specific dashboard, including widgets, filters, datasources, and configuration.

**When to use:** Use this when you want to inspect how a dashboard is built, or to discover which cubes and fields a dashboard uses.

**Parameters:**
- `dashboard_id` (optional, string) - ID of the dashboard (e.g., "68c20e36b10aaf740421cf12")
- `dashboard_name` (optional, string) - Name/title of the dashboard (e.g., "Telecom Services (1)")

**Note:** Either `dashboard_id` or `dashboard_name` must be provided.

**Returns:** Full dashboard object with all fields from the Sisense API, including:
- `widgets` - Dashboard widgets and their configurations
- `filters` - Filter definitions
- `datasource` - Datasource information
- `layout` - Layout configuration
- `settings` - Dashboard settings
- All other dashboard metadata

**Example:**
```json
{
  "_id": "68c20e36b10aaf740421cf12",
  "title": "Telecom Services (1)",
  "widgets": [...],
  "filters": [...],
  "datasource": {...},
  "layout": {...}
}
```

## API Reference

The server uses the following Sisense API endpoints:

- `GET /api/v1/elasticubes/getElasticubes` - List all ElastiCubes
- `GET /api/v2/datamodels/schema?title={name}` - Get ElastiCube schema
- `GET /api/v1/dashboards` - List all dashboards
- `GET /api/v1/dashboards/{id}` - Get specific dashboard by ID
- `GET /api/datasources/{encoded_name}/sql` - Execute SQL query

## Troubleshooting

### Server Won't Start

**Check Python and dependencies:**
```bash
python --version  # Should be 3.10+
uv sync  # Or: pip install -e .
```

**Check configuration:**
- Verify environment variables are set correctly in your MCP client configuration
- Ensure `SISENSE_BASE_URL` doesn't have a trailing slash
- Ensure `SISENSE_API_TOKEN` is valid and not expired

### Authentication Errors (401/403)

- Verify your API token is valid (regenerate if needed from Sisense user profile)
- Check that the token hasn't been revoked
- Ensure token is correctly set in environment variables (no extra spaces or quotes)

### 404 Errors

- Verify your Sisense base URL is correct (no trailing slash)
- Check that the API endpoints are available for your Sisense version
- For `list_elasticubes`, if you get 404, the endpoint may not be available in your instance

### Timeout Errors

- Default timeout is 30s for metadata, 60s for queries
- Increase timeout values if needed for slow queries
- Refresh the ElastiCube in Sisense console if it's misconfigured
- Check network connectivity to your Sisense instance

### Query Errors

- Verify ElastiCube name matches exactly (including brackets, case, and special characters)
- Example: `[REPORT] M2M Summary` (with brackets and exact spacing)
- Check SQL syntax is valid for Sisense
- Ensure table names match the schema (use `get_elasticube_schema` to verify)

### Debug Mode

If you need to see what's happening, check your MCP client's logs or run the server manually:

```bash
cd sisense-mcp
python -m src.server
```

The server logs to stderr, which won't break the MCP protocol.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Code style and formatting
- Testing requirements
- Submitting pull requests
- Reporting issues

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
