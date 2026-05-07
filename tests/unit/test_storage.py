import pandas as pd

from src.storage.parquet_writer import write_records_to_parquet


def test_write_records_to_parquet_creates_file(tmp_path):
    records = [
        {
            "session_key": 999,
            "driver_number": 1,
            "full_name": "Max Verstappen",
        }
    ]

    output_path = tmp_path / "drivers.parquet"

    write_records_to_parquet(
        records=records,
        output_path=str(output_path),
        overwrite=True,
    )

    assert output_path.exists()

    df = pd.read_parquet(output_path)

    assert len(df) == 1
    assert df.loc[0, "session_key"] == 999
    assert df.loc[0, "driver_number"] == 1