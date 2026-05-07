from src.storage.parquet_writer import write_records_to_parquet


def main():
    drivers = [
        {
            "session_key": 999,
            "driver_number": 1,
            "full_name": "Max Verstappen",
            "team_name": "Red Bull Racing",
            "ingested_at_utc": "2026-01-01T00:00:00+00:00",
        }
    ]

    laps = [
        {
            "session_key": 999,
            "driver_number": 1,
            "lap_number": 1,
            "lap_duration": 92.5,
            "ingested_at_utc": "2026-01-01T00:00:00+00:00",
        }
    ]

    write_records_to_parquet(
        records=drivers,
        output_path="data/raw/drivers/session_key=999/drivers.parquet",
        overwrite=True,
    )

    write_records_to_parquet(
        records=laps,
        output_path="data/raw/laps/session_key=999/laps.parquet",
        overwrite=True,
    )


if __name__ == "__main__":
    main()