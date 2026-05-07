from unittest.mock import Mock, patch

from src.ingestion.api_client import fetch_json, resolve_latest_session


@patch("src.ingestion.api_client.requests.get")
def test_fetch_json_returns_response_data(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [{"session_key": 123}]
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = fetch_json("sessions", {"session_key": "latest"})

    assert result == [{"session_key": 123}]
    mock_get.assert_called_once()


@patch("src.ingestion.api_client.fetch_json")
def test_resolve_latest_session_returns_valid_session(mock_fetch_json):
    mock_fetch_json.return_value = [
        {
            "session_key": 123,
            "meeting_key": 456,
            "session_name": "Race",
            "session_type": "Race",
            "date_start": "2024-01-01T00:00:00+00:00",
            "date_end": "2024-01-01T02:00:00+00:00",
            "year": 2024,
        }
    ]

    session = resolve_latest_session()

    assert session["session_key"] == 123
    assert session["session_name"] == "Race"

