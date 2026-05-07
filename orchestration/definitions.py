from datetime import datetime, timezone

from dagster import (
    AssetExecutionContext,
    AssetSelection,
    Backoff,
    Definitions,
    Jitter,
    MetadataValue,
    Output,
    RetryPolicy,
    ScheduleDefinition,
    asset,
    define_asset_job,
)

from src.ingestion.api_client import resolve_latest_session
from src.ingestion.drivers import ingest_drivers_for_session
from src.ingestion.laps import ingest_laps_for_session
from src.storage.parquet_writer import write_records_to_parquet


api_retry_policy = RetryPolicy(
    max_retries=3,
    delay=5,
    backoff=Backoff.EXPONENTIAL,
    jitter=Jitter.PLUS_MINUS,
)


@asset(
    retry_policy=api_retry_policy,
    description="Resolve the latest OpenF1 session and return its concrete session_key.",
)
def latest_session(context: AssetExecutionContext) -> Output[dict]:
    session = resolve_latest_session()

    session_key = session["session_key"]
    ingested_at_utc = datetime.now(timezone.utc).isoformat()

    context.log.info(f"Resolved latest session_key={session_key}")

    return Output(
        value=session,
        metadata={
            "session_key": session_key,
            "meeting_key": session.get("meeting_key"),
            "session_name": session.get("session_name"),
            "session_type": session.get("session_type"),
            "year": session.get("year"),
            "materialized_at_utc": MetadataValue.text(ingested_at_utc),
        },
    )


@asset(
    retry_policy=api_retry_policy,
    description="Ingest OpenF1 drivers for the latest resolved session.",
)
def drivers(
    context: AssetExecutionContext,
    latest_session: dict,
) -> Output[dict]:
    session_key = latest_session["session_key"]

    records = ingest_drivers_for_session(session_key)

    output_path = f"data/raw/drivers/session_key={session_key}/drivers.parquet"

    write_records_to_parquet(
        records=records,
        output_path=output_path,
        overwrite=True,
    )

    materialized_at_utc = datetime.now(timezone.utc).isoformat()

    context.log.info(
        f"Wrote {len(records)} driver records for session_key={session_key} to {output_path}"
    )

    return Output(
        value={
            "session_key": session_key,
            "row_count": len(records),
            "output_path": output_path,
        },
        metadata={
            "session_key": session_key,
            "row_count": len(records),
            "output_path": MetadataValue.path(output_path),
            "materialized_at_utc": MetadataValue.text(materialized_at_utc),
        },
    )


@asset(
    retry_policy=api_retry_policy,
    description="Ingest OpenF1 laps for the latest resolved session. Depends on drivers to force sequential execution.",
)
def laps(
    context: AssetExecutionContext,
    latest_session: dict,
    drivers: dict,
) -> Output[dict]:
    session_key = latest_session["session_key"]

    records = ingest_laps_for_session(session_key)

    output_path = f"data/raw/laps/session_key={session_key}/laps.parquet"

    write_records_to_parquet(
        records=records,
        output_path=output_path,
        overwrite=True,
    )

    materialized_at_utc = datetime.now(timezone.utc).isoformat()

    context.log.info(
        f"Wrote {len(records)} lap records for session_key={session_key} to {output_path}"
    )

    return Output(
        value={
            "session_key": session_key,
            "row_count": len(records),
            "output_path": output_path,
            "upstream_drivers_row_count": drivers["row_count"],
        },
        metadata={
            "session_key": session_key,
            "row_count": len(records),
            "output_path": MetadataValue.path(output_path),
            "materialized_at_utc": MetadataValue.text(materialized_at_utc),
        },
    )


openf1_ingestion_job = define_asset_job(
    name="openf1_ingestion_job",
    selection=AssetSelection.keys("drivers", "laps").upstream(),
)


daily_openf1_schedule = ScheduleDefinition(
    name="daily_openf1_schedule",
    job=openf1_ingestion_job,
    cron_schedule="0 0 * * *",
    execution_timezone="UTC",
)


defs = Definitions(
    assets=[
        latest_session,
        drivers,
        laps,
    ],
    jobs=[
        openf1_ingestion_job,
    ],
    schedules=[
        daily_openf1_schedule,
    ],
)