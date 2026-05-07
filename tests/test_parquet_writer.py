import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.storage.parquet_writer import write_records_to_parquet


class ParquetWriterTests(unittest.TestCase):
    def test_existing_snapshot_is_not_overwritten_by_default(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "drivers.parquet"

            write_records_to_parquet(
                records=[{"session_key": 9158, "driver_number": 1}],
                output_path=str(output_path),
            )
            write_records_to_parquet(
                records=[{"session_key": 9158, "driver_number": 16}],
                output_path=str(output_path),
            )

            written = pd.read_parquet(output_path).to_dict(orient="records")
            self.assertEqual(written, [{"session_key": 9158, "driver_number": 1}])

    def test_existing_snapshot_can_be_overwritten_explicitly(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "drivers.parquet"

            write_records_to_parquet(
                records=[{"session_key": 9158, "driver_number": 1}],
                output_path=str(output_path),
            )
            write_records_to_parquet(
                records=[{"session_key": 9158, "driver_number": 16}],
                output_path=str(output_path),
                overwrite=True,
            )

            written = pd.read_parquet(output_path).to_dict(orient="records")
            self.assertEqual(written, [{"session_key": 9158, "driver_number": 16}])


if __name__ == "__main__":
    unittest.main()
