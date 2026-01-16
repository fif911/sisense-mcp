"""Tests for ElastiCubeService."""

import pytest


@pytest.mark.asyncio
async def test_list_elasticubes_list_response(elasticube_service, mock_client):
    """Test list_elasticubes with list response."""
    mock_data = [
        {
            "_id": "66986f16c38c0befbce4c80f",
            "buildDestination": {"destination": "elasticube"},
            "creator": "64f0f302f45dd9002da343ae",
            "datasets": ["a792cf22-4631-4d1d-a20f-d1b7eb91042e"],
            "experiments": {},
            "fiscal": "system",
            "hasDatasetsWithoutConnectionParameters": False,
            "lastUpdated": "2024-08-02T16:50:14.417Z",
            "modelStatistics": {
                "enableModelStatistics": True,
                "allTablesPerCollection": True,
                "maxTablesPerCollection": 0,
                "recollectStatsInterval": 12,
            },
            "modeling-transformations": [],
            "oid": "5c886c69-3301-4ecd-9b3d-7e6f40144a8d",
            "relationType": "direct",
            "server": "LocalHost",
            "shares": [{"partyId": "629f977c2dd9db001af2bbdd", "type": "group", "permission": "a"}],
            "tenantId": "629f977c2dd9db001af2bbec",
            "title": "[REPORT] M2M Summary",
            "type": "extract",
            "importTime": None,
            "lastBuildAttempt": None,
            "lastBuildTime": "2024-08-20T20:14:22.783Z",
            "lastSuccessfulBuildStartTime": "2024-08-20T20:13:13.541Z",
            "lastSuccessfulBuildTime": "2024-08-20T20:14:22.783Z",
            "lastSuccessfulManualBuildStartTime": "2024-08-20T20:13:13.541Z",
            "schemaId": None,
            "shouldUpdateScheduleOnManualBuild": None,
        },
        {
            "_id": "507f1f77bcf86cd799439012",
            "title": "[REPORT] Test Cube",
            "type": "live",
            "server": "Remote",
            "lastUpdated": "2024-01-02T10:30:00.000Z",
            "buildDestination": {"destination": "elasticube"},
            "creator": "64f0f302f45dd9002da343ae",
            "datasets": [],
            "shares": [],
            "tenantId": "629f977c2dd9db001af2bbec",
        },
    ]
    mock_client.get.return_value = mock_data

    result = await elasticube_service.list_elasticubes()

    assert len(result) == 2
    assert result[0]["_id"] == "66986f16c38c0befbce4c80f"
    assert result[0]["title"] == "[REPORT] M2M Summary"
    assert result[0]["type"] == "extract"
    assert result[0]["server"] == "LocalHost"
    assert result[0]["lastUpdated"] == "2024-08-02T16:50:14.417Z"
    # Should be filtered out
    assert "buildDestination" not in result[0]
    assert "creator" not in result[0]
    assert "datasets" not in result[0]
    assert result[1]["_id"] == "507f1f77bcf86cd799439012"


@pytest.mark.asyncio
async def test_list_elasticubes_dict_response(elasticube_service, mock_client):
    """Test list_elasticubes with dict response containing elasticubes key."""
    mock_data = {
        "elasticubes": [
            {
                "_id": "66986f16c38c0befbce4c80f",
                "title": "[REPORT] M2M Summary",
                "type": "extract",
                "server": "LocalHost",
                "lastUpdated": "2024-08-02T16:50:14.417Z",
                "buildDestination": {"destination": "elasticube"},
                "creator": "64f0f302f45dd9002da343ae",
                "datasets": ["a792cf22-4631-4d1d-a20f-d1b7eb91042e"],
                "shares": [],
                "tenantId": "629f977c2dd9db001af2bbec",
            }
        ]
    }
    mock_client.get.return_value = mock_data

    result = await elasticube_service.list_elasticubes()

    assert len(result) == 1
    assert result[0]["_id"] == "66986f16c38c0befbce4c80f"
    assert result[0]["title"] == "[REPORT] M2M Summary"
    # Should be filtered out
    assert "buildDestination" not in result[0]
    assert "creator" not in result[0]


@pytest.mark.asyncio
async def test_get_schema(elasticube_service, mock_client):
    """Test get_schema."""
    mock_schema = {
        "oid": "5c886c69-3301-4ecd-9b3d-7e6f40144a8d",
        "title": "[REPORT] M2M Summary",
        "server": "LocalHost",
        "serverId": "local",
        "shares": [],
        "revision": None,
        "lastBuildTime": "2024-08-20T20:14:22.783Z",
        "lastSuccessfulBuildTime": "2024-08-20T20:14:22.783Z",
        "lastBuildTimeFromNextECM": None,
        "lastPublishTime": None,
        "lastUpdated": "2024-08-02T16:50:14.417Z",
        "datasets": [
            {
                "oid": "a792cf22-4631-4d1d-a20f-d1b7eb91042e",
                "type": "elasticube",
                "connection": {},
                "lastUpdated": "2024-08-02T16:50:14.417Z",
                "database": "test_db",
                "schemaName": "test_schema",
                "name": "Dataset1",
                "fullname": "Dataset1",
                "modelingTransformations": [],
                "schema": {},
                "schedule": {},
                "shares": [],
                "liveQuerySettings": None,
            }
        ],
        "modelingTransformations": [],
        "relations": [],
        "schedule": None,
        "creator": {"_id": "64f0f302f45dd9002da343ae"},
        "type": "extract",
        "relationType": "direct",
        "tenant": {"_id": "629f977c2dd9db001af2bbec"},
        "aiAccessController": None,
        "relationsTables": [],
    }
    mock_client.get.return_value = mock_schema

    result = await elasticube_service.get_schema("[REPORT] M2M Summary")

    assert result == mock_schema
    assert "datasets" in result
    assert "relations" in result
    assert "relationsTables" in result
    mock_client.get.assert_called_once_with(
        "/api/v2/datamodels/schema", params={"title": "[REPORT] M2M Summary"}
    )


@pytest.mark.asyncio
async def test_query_sql_success(elasticube_service, mock_client):
    """Test successful SQL query."""
    mock_result = {
        "rows": [
            {"BRAND_ID": 1, "BRAND_NAME": "Brand A"},
            {"BRAND_ID": 2, "BRAND_NAME": "Brand B"},
        ],
        "metadata": {
            "columns": [
                {"name": "BRAND_ID", "type": "numeric"},
                {"name": "BRAND_NAME", "type": "text"},
            ],
            "rowCount": 2,
        },
    }
    mock_client.get.return_value = mock_result
    mock_client.encode_datasource_name = lambda x: x.replace(" ", "%20")

    result = await elasticube_service.query_sql(
        datasource="[REPORT] M2M Summary",
        sql_query="SELECT * FROM brands LIMIT 10",
        count=10,
        offset=0,
    )

    assert result == mock_result
    assert "rows" in result
    assert "metadata" in result
    assert len(result["rows"]) == 2
    mock_client.get.assert_called_once()
    call_args = mock_client.get.call_args
    assert "/api/datasources" in call_args[0][0]
    assert call_args[1]["timeout"] == 60.0


@pytest.mark.asyncio
async def test_query_sql_with_error(elasticube_service, mock_client):
    """Test SQL query with API error in response."""
    mock_result = {"error": True, "details": "SQL syntax error"}
    mock_client.get.return_value = mock_result

    with pytest.raises(ValueError, match="API returned error"):
        await elasticube_service.query_sql(datasource="[REPORT] Test", sql_query="INVALID SQL")


def test_filter_elasticube_fields(elasticube_service):
    """Test elasticube field filtering."""
    full_elasticube = {
        "_id": "66986f16c38c0befbce4c80f",
        "title": "[REPORT] M2M Summary",
        "type": "extract",
        "server": "LocalHost",
        "lastUpdated": "2024-08-02T16:50:14.417Z",
        "buildDestination": {"destination": "elasticube"},
        "creator": "64f0f302f45dd9002da343ae",
        "datasets": ["a792cf22-4631-4d1d-a20f-d1b7eb91042e"],
        "experiments": {},
        "fiscal": "system",
        "hasDatasetsWithoutConnectionParameters": False,
        "modelStatistics": {
            "enableModelStatistics": True,
            "allTablesPerCollection": True,
        },
        "modeling-transformations": [],
        "oid": "5c886c69-3301-4ecd-9b3d-7e6f40144a8d",
        "relationType": "direct",
        "shares": [],
        "tenantId": "629f977c2dd9db001af2bbec",
        "importTime": None,
        "lastBuildAttempt": None,
        "lastBuildTime": "2024-08-20T20:14:22.783Z",
    }

    filtered = elasticube_service._filter_elasticube_fields(full_elasticube)

    assert filtered["_id"] == "66986f16c38c0befbce4c80f"
    assert filtered["title"] == "[REPORT] M2M Summary"
    assert filtered["type"] == "extract"
    assert filtered["server"] == "LocalHost"
    assert filtered["lastUpdated"] == "2024-08-02T16:50:14.417Z"
    # Should be filtered out
    assert "buildDestination" not in filtered
    assert "creator" not in filtered
    assert "datasets" not in filtered
    assert "shares" not in filtered
    assert "tenantId" not in filtered
