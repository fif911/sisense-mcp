"""Tests for DashboardService."""

import pytest


@pytest.mark.asyncio
async def test_list_dashboards_list_response(dashboard_service, mock_client):
    """Test list_dashboards with list response."""
    mock_data = [
        {
            "_id": "68c20e36b10aaf740421cf12",
            "title": "Telecom Services (1)",
            "desc": "Telecom services dashboard",
            "source": "67d081cdea0fb30032897721",
            "type": "dashboard",
            "created": "2025-09-10T23:48:06.009Z",
            "lastUpdated": "2025-09-10T23:48:06.009Z",
            "owner": "67c6232ca2e4be002f89c338",
            "userId": "67c6232ca2e4be002f89c338",
            "isPublic": None,
            "lastOpened": "2025-09-11T16:38:36.859Z",
            "parentFolder": None,
            "shares": [{"shareId": "67c6232ca2e4be002f89c338", "type": "user"}],
            "style": {"paletteId": "62ec379f0c396600377f962f"},
            "layout": {},
            "datasource": {"title": "SOC Data Model", "id": "live:SOC Data Model"},
            "filters": [],
            "settings": {"autoUpdateOnFiltersChange": True},
            "tenantId": "629f977c2dd9db001af2bbec",
        }
    ]
    mock_client.get.return_value = mock_data

    result = await dashboard_service.list_dashboards()

    assert len(result) == 1
    assert result[0]["_id"] == "68c20e36b10aaf740421cf12"
    assert result[0]["title"] == "Telecom Services (1)"
    assert result[0]["desc"] == "Telecom services dashboard"
    assert result[0]["source"] == "67d081cdea0fb30032897721"
    # Should be filtered out
    assert "shares" not in result[0]
    assert "style" not in result[0]
    assert "layout" not in result[0]
    assert "datasource" not in result[0]
    assert "filters" not in result[0]
    assert "settings" not in result[0]


@pytest.mark.asyncio
async def test_list_dashboards_dict_response(dashboard_service, mock_client):
    """Test list_dashboards with dict response containing dashboards key."""
    mock_data = {
        "dashboards": [
            {
                "_id": "68c20e36b10aaf740421cf12",
                "title": "Telecom Services (1)",
                "desc": "",
                "source": "67d081cdea0fb30032897721",
                "type": "dashboard",
                "created": "2025-09-10T23:48:06.009Z",
                "lastUpdated": "2025-09-10T23:48:06.009Z",
                "owner": "67c6232ca2e4be002f89c338",
                "isPublic": None,
                "lastOpened": "2025-09-11T16:38:36.859Z",
                "parentFolder": None,
                "shares": [],
                "style": {},
                "datasource": {},
            }
        ]
    }
    mock_client.get.return_value = mock_data

    result = await dashboard_service.list_dashboards()

    assert len(result) == 1
    assert result[0]["_id"] == "68c20e36b10aaf740421cf12"
    assert result[0]["title"] == "Telecom Services (1)"


@pytest.mark.asyncio
async def test_get_dashboard_by_id(dashboard_service, mock_client):
    """Test get_dashboard by ID."""
    mock_dashboard = {
        "_id": "68c20e36b10aaf740421cf12",
        "title": "Telecom Services (1)",
        "desc": "",
        "source": "67d081cdea0fb30032897721",
        "type": "dashboard",
        "shares": [{"shareId": "67c6232ca2e4be002f89c338", "type": "user"}],
        "style": {"paletteId": "62ec379f0c396600377f962f"},
        "owner": "67c6232ca2e4be002f89c338",
        "userId": "67c6232ca2e4be002f89c338",
        "created": "2025-09-10T23:48:06.009Z",
        "lastUpdated": "2025-09-10T23:48:06.009Z",
        "layout": {"instanceid": "test", "type": "grid", "columns": 12},
        "instanceType": "owner",
        "previewLayout": [],
        "oid": "68c20e36b10aaf740421cf05",
        "allowChangeSubscription": False,
        "dataExploration": False,
        "datasource": {
            "title": "SOC Data Model",
            "id": "live:SOC Data Model",
            "fullname": "live:SOC Data Model",
            "live": True,
        },
        "defaultFilters": [],
        "editing": False,
        "filterRelations": [],
        "filterToDatasourceMapping": {},
        "filters": [],
        "isPublic": None,
        "lastOpened": "2025-09-11T16:38:36.859Z",
        "parentFolder": None,
        "settings": {"autoUpdateOnFiltersChange": True},
        "tenantId": "629f977c2dd9db001af2bbec",
    }
    mock_client.get.return_value = mock_dashboard

    result = await dashboard_service.get_dashboard(dashboard_id="68c20e36b10aaf740421cf12")

    assert result == mock_dashboard
    assert result["_id"] == "68c20e36b10aaf740421cf12"
    assert result["title"] == "Telecom Services (1)"
    assert "datasource" in result
    assert "layout" in result
    assert "filters" in result
    mock_client.get.assert_called_once_with("/api/v1/dashboards/68c20e36b10aaf740421cf12")


@pytest.mark.asyncio
async def test_get_dashboard_by_name(dashboard_service, mock_client):
    """Test get_dashboard by name."""
    mock_dashboards = [
        {
            "_id": "68c20e36b10aaf740421cf12",
            "title": "Telecom Services (1)",
            "desc": "",
            "source": "67d081cdea0fb30032897721",
            "type": "dashboard",
        },
        {
            "_id": "507f1f77bcf86cd799439012",
            "title": "Target Dashboard",
            "desc": "Target description",
            "source": "67d081cdea0fb30032897721",
            "type": "dashboard",
        },
        {
            "_id": "507f1f77bcf86cd799439013",
            "title": "Another Dashboard",
            "desc": "",
            "source": "67d081cdea0fb30032897721",
            "type": "dashboard",
        },
    ]
    mock_client.get.return_value = mock_dashboards

    result = await dashboard_service.get_dashboard(dashboard_name="Target Dashboard")

    assert result["_id"] == "507f1f77bcf86cd799439012"
    assert result["title"] == "Target Dashboard"


@pytest.mark.asyncio
async def test_get_dashboard_by_name_not_found(dashboard_service, mock_client):
    """Test get_dashboard by name when not found."""
    mock_dashboards = [
        {
            "_id": "68c20e36b10aaf740421cf12",
            "title": "Telecom Services (1)",
            "desc": "",
            "source": "67d081cdea0fb30032897721",
            "type": "dashboard",
        }
    ]
    mock_client.get.return_value = mock_dashboards

    with pytest.raises(ValueError, match="Dashboard with name 'NonExistent' not found"):
        await dashboard_service.get_dashboard(dashboard_name="NonExistent")


@pytest.mark.asyncio
async def test_get_dashboard_no_id_or_name(dashboard_service):
    """Test get_dashboard without ID or name."""
    with pytest.raises(ValueError, match="Either dashboard_id or dashboard_name must be provided"):
        await dashboard_service.get_dashboard()


def test_filter_dashboard_fields(dashboard_service):
    """Test dashboard field filtering."""
    full_dashboard = {
        "_id": "68c20e36b10aaf740421cf12",
        "title": "Telecom Services (1)",
        "desc": "",
        "source": "67d081cdea0fb30032897721",
        "type": "dashboard",
        "created": "2025-09-10T23:48:06.009Z",
        "lastUpdated": "2025-09-10T23:48:06.009Z",
        "owner": "67c6232ca2e4be002f89c338",
        "isPublic": None,
        "lastOpened": "2025-09-11T16:38:36.859Z",
        "parentFolder": None,
        "shares": [{"shareId": "67c6232ca2e4be002f89c338", "type": "user"}],
        "style": {"paletteId": "62ec379f0c396600377f962f"},
        "layout": {"instanceid": "test", "type": "grid"},
        "datasource": {"title": "SOC Data Model", "id": "live:SOC Data Model"},
        "filters": [],
        "settings": {"autoUpdateOnFiltersChange": True},
        "tenantId": "629f977c2dd9db001af2bbec",
    }

    filtered = dashboard_service._filter_dashboard_fields(full_dashboard)

    assert filtered["_id"] == "68c20e36b10aaf740421cf12"
    assert filtered["title"] == "Telecom Services (1)"
    assert filtered["desc"] == ""
    assert filtered["source"] == "67d081cdea0fb30032897721"
    # Should be filtered out
    assert "shares" not in filtered
    assert "style" not in filtered
    assert "layout" not in filtered
    assert "datasource" not in filtered
    assert "filters" not in filtered
    assert "settings" not in filtered
    assert "tenantId" not in filtered
