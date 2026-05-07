from datetime import datetime, timezone

from src.ingestion.api_client import fetch_json


def ingest_laps_for_session(session_key: int) -> list[dict]:
    laps = fetch_json("laps", {"session_key": session_key})

    ingested_at = datetime.now(timezone.utc).isoformat()

    for lap in laps:
        lap["session_key"] = session_key
        lap["ingested_at_utc"] = ingested_at

    return laps


def _lap_sort_key(lap: dict) -> tuple[bool, int, bool, int, bool, str]:
    driver_number = lap.get("driver_number")
    lap_number = lap.get("lap_number")
    date_start = lap.get("date_start")
    return (
        driver_number is None,
        -1 if driver_number is None else driver_number,
        lap_number is None,
        -1 if lap_number is None else lap_number,
        date_start is None,
        "" if date_start is None else date_start,
    )
