"""Service for Dashboard operations."""

from typing import Any

from .sisense_service import SisenseService


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
