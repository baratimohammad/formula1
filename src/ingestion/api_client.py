import requests

BASE_URL = "https://api.openf1.org/v1"


def fetch_json(endpoint: str, params: dict | None = None) -> list[dict]:
    """
    Fetch JSON data from an OpenF1 API endpoint.

    Example:
        fetch_json("drivers", {"session_key": 9158})
    """
    response = requests.get(
        f"{BASE_URL}/{endpoint}",
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def resolve_latest_session() -> dict:
    """
    Resolve the latest OpenF1 session.

    This should be called once at the start of the pipeline.
    Downstream ingestion should use the concrete session_key returned here.
    """
    sessions = fetch_json("sessions", {"session_key": "latest"})

    if not sessions:
        raise ValueError("No latest session returned by OpenF1")

    session = sessions[0]

    required_fields = [
        "session_key",
        "meeting_key",
        "session_name",
        "session_type",
        "date_start",
        "date_end",
        "year",
    ]

    missing = [field for field in required_fields if field not in session]

    if missing:
        raise ValueError(f"Session response missing fields: {missing}")

    return session