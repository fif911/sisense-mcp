"""Service for Dashboard operations."""

from typing import Any

from .sisense_service import SisenseService

# API version prefix for v1 endpoints
API_V1_PREFIX = "/api/v1"


class DashboardService(SisenseService):
    """Service for Dashboard operations."""

    def _filter_dashboard_fields(self, dashboard: dict[str, Any]) -> dict[str, Any]:
        """Filter dashboard to only return required fields.

        Args:
            dashboard: Full dashboard object from API

        Returns:
            Filtered dashboard with only essential fields
        """
        return {
            "_id": dashboard.get("_id"),
            "title": dashboard.get("title"),
            "desc": dashboard.get("desc"),
            "source": dashboard.get("source"),
            "type": dashboard.get("type"),
            "created": dashboard.get("created"),
            "lastUpdated": dashboard.get("lastUpdated"),
            "owner": dashboard.get("owner"),
            "isPublic": dashboard.get("isPublic"),
            "lastOpened": dashboard.get("lastOpened"),
            "parentFolder": dashboard.get("parentFolder"),
        }

    async def list_dashboards(self) -> list[dict[str, Any]]:
        """Get list of all dashboards - filtered to required fields.

        Returns:
            List of filtered dashboard objects with only essential fields

        Raises:
            httpx.HTTPStatusError: If the API request fails
        """
        data = await self.client.get("/api/v1/dashboards")

        # Filter each dashboard to only required fields
        if isinstance(data, list):
            return [self._filter_dashboard_fields(item) for item in data]
        elif isinstance(data, dict):
            if "dashboards" in data and isinstance(data["dashboards"], list):
                return [self._filter_dashboard_fields(item) for item in data["dashboards"]]
        return data

    async def get_dashboard(
        self, dashboard_id: str = None, dashboard_name: str = None
    ) -> dict[str, Any]:
        """Get dashboard details by ID or name.

        Args:
            dashboard_id: ID of the dashboard (e.g., '68c20e36b10aaf740421cf12')
            dashboard_name: Name/title of the dashboard (e.g., 'Revenue over time')

        Returns:
            Full dashboard object with all fields from the Sisense API

        Raises:
            ValueError: If neither dashboard_id nor dashboard_name is provided
            ValueError: If dashboard with given name is not found
            httpx.HTTPStatusError: If the API request fails
        """
        if not dashboard_id and not dashboard_name:
            raise ValueError("Either dashboard_id or dashboard_name must be provided")

        if dashboard_id:
            # Get by ID directly
            return await self.client.get(f"/api/v1/dashboards/{dashboard_id}")
        else:
            # Get by name - first list all, then find matching title
            dashboards = await self.client.get("/api/v1/dashboards")

            if isinstance(dashboards, list):
                for dashboard in dashboards:
                    if dashboard.get("title") == dashboard_name:
                        return dashboard
            elif isinstance(dashboards, dict) and "dashboards" in dashboards:
                for dashboard in dashboards["dashboards"]:
                    if dashboard.get("title") == dashboard_name:
                        return dashboard

            raise ValueError(f"Dashboard with name '{dashboard_name}' not found")

    async def export_dashboard_png(
        self,
        dashboard_id: str,
        width: int = 1000,
        layout: str = "asis",
        show_dashboard_title: bool = True,
        show_dashboard_filters: bool = True,
        show_datasource_info: bool = True,
        shared_mode: bool = None,
        tenant_id: str = None,
    ) -> bytes:
        """Export dashboard as PNG image.

        Args:
            dashboard_id: ID of the dashboard to export
            width: Image width in pixels (default: 1000)
            layout: Layout mode - "asis" or other layout options (default: "asis")
            show_dashboard_title: Whether to show dashboard title (default: True)
            show_dashboard_filters: Whether to show dashboard filters (default: True)
            show_datasource_info: Whether to show datasource info (default: True)
            shared_mode: If dashboard is in shared mode (optional)
            tenant_id: Tenant ID for x-tenant-id header (optional)

        Returns:
            PNG image data as bytes

        Raises:
            ValueError: If dashboard_id is not provided
            httpx.HTTPStatusError: If the API request fails
        """
        if not dashboard_id:
            raise ValueError("dashboard_id must be provided")

        # This endpoint uses v1 API (other endpoints use 0.9 API)
        endpoint = f"{API_V1_PREFIX}/export/dashboards/{dashboard_id}/png"

        # Prepare request body
        body = {
            "params": {
                "width": width,
                "layout": layout,
                "showDashboardTitle": show_dashboard_title,
                "showDashboardFilters": show_dashboard_filters,
                "showDatasourceInfo": show_datasource_info,
            }
        }

        # Prepare headers (add x-tenant-id if provided)
        headers = {}
        if tenant_id:
            headers["x-tenant-id"] = tenant_id

        # Prepare query parameters
        params = {}
        if shared_mode is not None:
            params["sharedMode"] = str(shared_mode).lower()

        return await self.client.post_binary(
            endpoint, json_data=body, headers=headers, params=params if params else None
        )
