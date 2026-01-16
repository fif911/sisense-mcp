"""Tests for ElastiCubeService."""

import pytest


@pytest.mark.asyncio
async def test_list_elasticubes_list_response(elasticube_service, mock_client):
    """Test list_elasticubes with list response."""
    mock_data = [
        {
            "_id": "507f1f77bcf86cd799439011",
            "buildDestination": {"destination": "elasticube"},
            "creator": "507f1f77bcf86cd799439013",
            "datasets": ["550e8400-e29b-41d4-a716-446655440001"],
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
            "oid": "550e8400-e29b-41d4-a716-446655440000",
            "relationType": "direct",
            "server": "LocalHost",
            "shares": [{"partyId": "507f1f77bcf86cd799439014", "type": "group", "permission": "a"}],
            "tenantId": "507f1f77bcf86cd799439012",
            "title": "Sales Data Model",
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
            "creator": "507f1f77bcf86cd799439013",
            "datasets": [],
            "shares": [],
            "tenantId": "507f1f77bcf86cd799439012",
        },
    ]
    mock_client.get.return_value = mock_data

    result = await elasticube_service.list_elasticubes()

    assert len(result) == 2
    assert result[0]["_id"] == "507f1f77bcf86cd799439011"
    assert result[0]["title"] == "Sales Data Model"
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
                "_id": "507f1f77bcf86cd799439011",
                "title": "Sales Data Model",
                "type": "extract",
                "server": "LocalHost",
                "lastUpdated": "2024-08-02T16:50:14.417Z",
                "buildDestination": {"destination": "elasticube"},
                "creator": "507f1f77bcf86cd799439013",
                "datasets": ["550e8400-e29b-41d4-a716-446655440001"],
                "shares": [],
                "tenantId": "507f1f77bcf86cd799439012",
            }
        ]
    }
    mock_client.get.return_value = mock_data

    result = await elasticube_service.list_elasticubes()

    assert len(result) == 1
    assert result[0]["_id"] == "507f1f77bcf86cd799439011"
    assert result[0]["title"] == "Sales Data Model"
    # Should be filtered out
    assert "buildDestination" not in result[0]
    assert "creator" not in result[0]


@pytest.mark.asyncio
async def test_get_schema(elasticube_service, mock_client):
    """Test get_schema."""
    mock_schema = {
        "oid": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Sales Data Model",
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
                "oid": "550e8400-e29b-41d4-a716-446655440001",
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
        "creator": {"_id": "507f1f77bcf86cd799439013"},
        "type": "extract",
        "relationType": "direct",
        "tenant": {"_id": "507f1f77bcf86cd799439012"},
        "aiAccessController": None,
        "relationsTables": [],
    }
    mock_client.get.return_value = mock_schema

    result = await elasticube_service.get_schema("Sales Data Model")

    assert result == mock_schema
    assert "datasets" in result
    assert "relations" in result
    assert "relationsTables" in result
    mock_client.get.assert_called_once_with(
        "/api/v2/datamodels/schema", params={"title": "Sales Data Model"}
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
        datasource="Sales Data Model",
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
        "_id": "507f1f77bcf86cd799439011",
        "title": "Sales Data Model",
        "type": "extract",
        "server": "LocalHost",
        "lastUpdated": "2024-08-02T16:50:14.417Z",
        "buildDestination": {"destination": "elasticube"},
        "creator": "507f1f77bcf86cd799439013",
        "datasets": ["550e8400-e29b-41d4-a716-446655440001"],
        "experiments": {},
        "fiscal": "system",
        "hasDatasetsWithoutConnectionParameters": False,
        "modelStatistics": {
            "enableModelStatistics": True,
            "allTablesPerCollection": True,
        },
        "modeling-transformations": [],
        "oid": "550e8400-e29b-41d4-a716-446655440000",
        "relationType": "direct",
        "shares": [],
        "tenantId": "507f1f77bcf86cd799439012",
        "importTime": None,
        "lastBuildAttempt": None,
        "lastBuildTime": "2024-08-20T20:14:22.783Z",
    }

    filtered = elasticube_service._filter_elasticube_fields(full_elasticube)

    assert filtered["_id"] == "507f1f77bcf86cd799439011"
    assert filtered["title"] == "Sales Data Model"
    assert filtered["type"] == "extract"
    assert filtered["server"] == "LocalHost"
    assert filtered["lastUpdated"] == "2024-08-02T16:50:14.417Z"
    # Should be filtered out
    assert "buildDestination" not in filtered
    assert "creator" not in filtered
    assert "datasets" not in filtered
    assert "shares" not in filtered
    assert "tenantId" not in filtered
