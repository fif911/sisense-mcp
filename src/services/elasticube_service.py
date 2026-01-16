"""Service for ElastiCube operations."""

from typing import Any

from .sisense_service import SisenseService


class ElastiCubeService(SisenseService):
    """Service for ElastiCube/datamodel operations."""

    def _filter_elasticube_fields(self, elasticube: dict[str, Any]) -> dict[str, Any]:
        """Filter elasticube to only return required fields.

        Args:
            elasticube: Full elasticube object from API

        Returns:
            Filtered elasticube with only essential fields
        """
        return {
            "_id": elasticube.get("_id"),
            "title": elasticube.get("title"),
            "type": elasticube.get("type"),
            "server": elasticube.get("server"),
            "lastUpdated": elasticube.get("lastUpdated"),
        }

    async def list_elasticubes(self) -> list[dict[str, Any]]:
        """List all ElastiCubes/datamodels - filtered to required fields.

        Returns:
            List of filtered elasticube objects with only essential fields

        Raises:
            httpx.HTTPStatusError: If the API request fails
        """
        data = await self.client.get("/api/v1/elasticubes/getElasticubes")

        # Handle different response structures
        if isinstance(data, list):
            return [self._filter_elasticube_fields(item) for item in data]
        elif isinstance(data, dict):
            if "elasticubes" in data and isinstance(data["elasticubes"], list):
                return [self._filter_elasticube_fields(item) for item in data["elasticubes"]]
            # Return as-is if structure is unexpected
            return data
        return data

    async def get_schema(self, elasticube_name: str) -> dict[str, Any]:
        """Get schema (tables/columns) for an ElastiCube.

        Args:
            elasticube_name: Name of the ElastiCube (e.g., '[REPORT] M2M Summary')

        Returns:
            Full schema JSON including datasets, tables, columns, relations, and relationTables

        Raises:
            httpx.HTTPStatusError: If the API request fails
        """
        return await self.client.get("/api/v2/datamodels/schema", params={"title": elasticube_name})

    async def query_sql(
        self, datasource: str, sql_query: str, count: int = 5000, offset: int = 0
    ) -> dict[str, Any]:
        """Execute SQL query on ElastiCube.

        Args:
            datasource: Name of the ElastiCube datasource (e.g., '[REPORT] M2M Summary')
            sql_query: SQL query string (must start with SELECT)
            count: Maximum number of rows to return (default: 5000)
            offset: Offset for pagination (default: 0)

        Returns:
            Query result with rows and metadata

        Raises:
            httpx.HTTPStatusError: If the API request fails or query has errors
        """
        encoded_datasource = self.client.encode_datasource_name(datasource)

        data = await self.client.get(
            f"/api/datasources/{encoded_datasource}/sql",
            params={
                "queryBuildingCube": "false",
                "count": str(count),
                "offset": str(offset),
                "includeMetadata": "true",
                "isMaskedResponse": "false",
                "shouldAddText": "false",
                "query": sql_query,
            },
            timeout=60.0,
        )

        # Check for API error in response body
        if data.get("error"):
            error_details = data.get("details", str(data))
            raise ValueError(f"API returned error: {error_details[:500]}")

        return data
