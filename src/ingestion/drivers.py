from src.ingestion.api_client import fetch_json


def ingest_drivers_for_session(session_key: int) -> list[dict]:
    """
    Ingest all drivers for a given OpenF1 session.

    The returned records are kept source-derived and sorted so rerunning
    ingestion for the same session produces the same logical output.
    """
    drivers = fetch_json("drivers", {"session_key": session_key})
    return sorted(drivers, key=_driver_sort_key)


def _driver_sort_key(driver: dict) -> tuple[bool, int]:
    driver_number = driver.get("driver_number")
    return (driver_number is None, -1 if driver_number is None else driver_number)
