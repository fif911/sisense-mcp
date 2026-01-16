# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX

### Added

- Initial release of Sisense MCP Server
- **ElastiCube Tools:**
  - `list_elasticubes` - List all available ElastiCubes/datamodels
  - `get_elasticube_schema` - Get schema (tables, columns, relationships) for an ElastiCube
  - `query_elasticube` - Execute SQL queries against ElastiCubes
- **Dashboard Tools:**
  - `list_dashboards` - List all available dashboards
  - `get_dashboard_info` - Get complete dashboard information by ID or name
- Comprehensive test suite with >80% coverage
- Support for Python 3.10+
- Support for multiple MCP clients (Claude Desktop, Cursor, etc.)
- Error handling with helpful error messages
- Data filtering for list operations (returns only essential fields)

### Technical Details

- Refactored code structure with separation of concerns:
  - `client/` - Pure HTTP client
  - `services/` - Business logic layer
  - `tools/` - MCP tool handlers
- Async/await support for all API operations
- Configurable timeouts (30s for metadata, 60s for queries)
- Support for pagination with `count` and `offset` parameters

[0.1.0]: https://github.com/yourusername/sisense-mcp/releases/tag/v0.1.0
