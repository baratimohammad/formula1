from datetime import datetime, timezone

from src.ingestion.api_client import resolve_latest_session
from src.ingestion.drivers import ingest_drivers_for_session
from src.ingestion.laps import ingest_laps_for_session
from src.storage.parquet_writer import write_records_to_parquet


def _attach_ingested_at_utc(records: list[dict], ingested_at_utc: str) -> list[dict]:
    return [{**record, "ingested_at_utc": ingested_at_utc} for record in records]


def main():
    session = resolve_latest_session()
    session_key = session["session_key"]
    ingested_at_utc = datetime.now(timezone.utc).isoformat()

    drivers = _attach_ingested_at_utc(
        ingest_drivers_for_session(session_key),
        ingested_at_utc,
    )
    laps = _attach_ingested_at_utc(
        ingest_laps_for_session(session_key),
        ingested_at_utc,
    )

    write_records_to_parquet(
        records=[session],
        output_path=f"data/raw/sessions/session_key={session_key}/session.parquet",
    )

    write_records_to_parquet(
        records=drivers,
        output_path=f"data/raw/drivers/session_key={session_key}/drivers.parquet",
    )

    write_records_to_parquet(
        records=laps,
        output_path=f"data/raw/laps/session_key={session_key}/laps.parquet",
    )

    print(f"Ingested session: {session_key}")
    print(f"Drivers: {len(drivers)}")
    print(f"Laps: {len(laps)}")


if __name__ == "__main__":
    main()
