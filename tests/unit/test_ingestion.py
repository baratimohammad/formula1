from unittest.mock import patch

from src.ingestion.drivers import ingest_drivers_for_session
from src.ingestion.laps import ingest_laps_for_session


@patch("src.ingestion.drivers.fetch_json")
def test_ingest_drivers_adds_metadata(mock_fetch_json):
    mock_fetch_json.return_value = [
        {
            "driver_number": 1,
            "full_name": "Max Verstappen",
            "team_name": "Red Bull Racing",
        }
    ]

    result = ingest_drivers_for_session(session_key=999)

    assert len(result) == 1
    assert result[0]["session_key"] == 999
    assert result[0]["driver_number"] == 1
    assert "ingested_at_utc" in result[0]


@patch("src.ingestion.laps.fetch_json")
def test_ingest_laps_adds_metadata(mock_fetch_json):
    mock_fetch_json.return_value = [
        {
            "driver_number": 1,
            "lap_number": 10,
            "lap_duration": 92.5,
        }
    ]

    result = ingest_laps_for_session(session_key=999)

    assert len(result) == 1
    assert result[0]["session_key"] == 999
    assert result[0]["driver_number"] == 1
    assert result[0]["lap_number"] == 10
    assert "ingested_at_utc" in result[0]