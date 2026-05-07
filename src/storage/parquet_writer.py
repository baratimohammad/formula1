from pathlib import Path

import pandas as pd


def write_records_to_parquet(
    records: list[dict],
    output_path: str,
    overwrite: bool = False,
) -> None:
    """
    Write a list of dictionaries to a parquet file.

    By default, existing parquet snapshots are left untouched so rerunning
    the same pipeline does not rewrite raw outputs.
    """
    if not records:
        raise ValueError("No records to write")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and not overwrite:
        return

    df = pd.DataFrame(records)
    df.to_parquet(path, index=False)
