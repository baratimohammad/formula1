from src.ingestion.api_client import fetch_json


def ingest_laps_for_session(session_key: int) -> list[dict]:
    """
    Ingest all laps for a given OpenF1 session.

    The returned records are kept source-derived and sorted so rerunning
    ingestion for the same session produces the same logical output.
    """
    laps = fetch_json("laps", {"session_key": session_key})
    return sorted(laps, key=_lap_sort_key)


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
