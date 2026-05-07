# OpenF1 Ingestion Pipeline

This project ingests the latest OpenF1 session, drivers, and laps data and stores raw parquet snapshots under `data/raw/`.

## How To Run Locally

Prerequisites:
- Python 3.10
- Internet access to `https://api.openf1.org`

Setup:

```bash
python3.10 -m venv venv
venv/bin/pip install -r requirements.txt
```

Run the pipeline job locally:

```bash
venv/bin/dagster job execute -f orchestration/definitions.py -j openf1_ingestion_job
```

Run the Dagster UI locally:

```bash
venv/bin/dagster dev -f orchestration/definitions.py
```

Run validation checks:

```bash
venv/bin/ruff check src tests orchestration
venv/bin/pytest tests/unit
venv/bin/python tests/create_test_data.py
venv/bin/python tests/run_sql_tests.py
```

## Troubleshooting

- `ModuleNotFoundError`: run commands from the repository root and use the project virtualenv.
- `requests` or connection failures: confirm outbound network access to the OpenF1 API.
- `No records to write`: the upstream API returned no rows for the resolved session; inspect the API response and session metadata.
- CI smoke test failures: check the `Pipeline smoke test` job in `CI`, which validates that the Dagster job can execute successfully.
- Deploy workflow failures: check the `Deploy / Publish Pipeline Snapshot` workflow, which runs the pipeline and uploads raw output plus Dagster run metadata as artifacts.
- Dagster reruns replace data: the `drivers` and `laps` assets call `write_records_to_parquet(..., overwrite=True)`, so reruns refresh those parquet snapshots.

## Monitor Pipeline Health

- GitHub Actions:
  - `CI` validates linting, unit tests, test data creation, and SQL checks.
  - `Pipeline smoke test` in `CI` is the lightweight execution check.
  - `Deploy / Publish Pipeline Snapshot` runs the pipeline on `main` and uploads the generated raw data and Dagster metadata as workflow artifacts.
- Dagster:
  - Monitor asset materializations for `latest_session`, `drivers`, and `laps`.
  - Inspect asset logs for row counts, output paths, and retry activity.
- Data outputs:
  - Confirm expected files exist under `data/raw/sessions/`, `data/raw/drivers/`, and `data/raw/laps/`.

## Handle Failed Runs

- Check the failing step first:
  - local CLI output for `dagster job execute`
  - GitHub Actions logs for CI or smoke-test failures
  - Dagster run logs and asset metadata for orchestrated runs
  - uploaded artifacts from the deploy workflow when you need the produced data snapshot or Dagster metadata
- Fix the underlying issue, then rerun:
  - local reruns should use `venv/bin/dagster job execute -f orchestration/definitions.py -j openf1_ingestion_job`
  - Dagster asset reruns may overwrite `drivers` and `laps`, so treat them as refreshes rather than strict no-op retries
- If a run failed partway through:
  - rerunning the Dagster job will rematerialize the affected assets and rewrite `drivers` and `laps`

## Generative AI Disclosure

Generative AI was used to assist with parts of this repository’s development and documentation. AI-generated suggestions were reviewed and edited by a human before being kept in the codebase.
