from datetime import datetime, timezone

from src.ingestion.api_client import fetch_json


def ingest_drivers_for_session(session_key: int) -> list[dict]:
    drivers = fetch_json("drivers", {"session_key": session_key})

    ingested_at = datetime.now(timezone.utc).isoformat()

    for driver in drivers:
        driver["session_key"] = session_key
        driver["ingested_at_utc"] = ingested_at

    return drivers


def _driver_sort_key(driver: dict) -> tuple[bool, int]:
    driver_number = driver.get("driver_number")
    return (driver_number is None, -1 if driver_number is None else driver_number)
