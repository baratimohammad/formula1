import unittest
from unittest.mock import patch

from src.ingestion.drivers import ingest_drivers_for_session
from src.ingestion.laps import ingest_laps_for_session


class IngestionIdempotencyTests(unittest.TestCase):
    @patch("src.ingestion.drivers.fetch_json")
    def test_drivers_ingestion_is_deterministic(self, mock_fetch_json):
        mock_fetch_json.return_value = [
            {"session_key": 9158, "driver_number": 16, "full_name": "Charles LECLERC"},
            {"session_key": 9158, "driver_number": 1, "full_name": "Max VERSTAPPEN"},
        ]

        first_run = ingest_drivers_for_session(9158)
        second_run = ingest_drivers_for_session(9158)

        expected = [
            {"session_key": 9158, "driver_number": 1, "full_name": "Max VERSTAPPEN"},
            {"session_key": 9158, "driver_number": 16, "full_name": "Charles LECLERC"},
        ]

        self.assertEqual(first_run, expected)
        self.assertEqual(second_run, expected)
        self.assertNotIn("ingested_at_utc", first_run[0])

    @patch("src.ingestion.laps.fetch_json")
    def test_laps_ingestion_is_deterministic(self, mock_fetch_json):
        mock_fetch_json.return_value = [
            {
                "session_key": 9158,
                "driver_number": 16,
                "lap_number": 2,
                "date_start": "2026-05-03T17:06:00+00:00",
            },
            {
                "session_key": 9158,
                "driver_number": 1,
                "lap_number": 1,
                "date_start": "2026-05-03T17:04:00+00:00",
            },
            {
                "session_key": 9158,
                "driver_number": 16,
                "lap_number": 1,
                "date_start": "2026-05-03T17:04:00+00:00",
            },
        ]

        first_run = ingest_laps_for_session(9158)
        second_run = ingest_laps_for_session(9158)

        expected = [
            {
                "session_key": 9158,
                "driver_number": 1,
                "lap_number": 1,
                "date_start": "2026-05-03T17:04:00+00:00",
            },
            {
                "session_key": 9158,
                "driver_number": 16,
                "lap_number": 1,
                "date_start": "2026-05-03T17:04:00+00:00",
            },
            {
                "session_key": 9158,
                "driver_number": 16,
                "lap_number": 2,
                "date_start": "2026-05-03T17:06:00+00:00",
            },
        ]

        self.assertEqual(first_run, expected)
        self.assertEqual(second_run, expected)
        self.assertNotIn("ingested_at_utc", first_run[0])


if __name__ == "__main__":
    unittest.main()
