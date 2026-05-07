from pathlib import Path

import duckdb

from src.config_loader import get_storage_raw_root


def run_sql_file(sql_file: Path) -> None:
    sql = sql_file.read_text().replace(
        "{{ raw_root }}",
        get_storage_raw_root().as_posix(),
    )

    statements = [
        statement.strip()
        for statement in sql.split(";")
        if statement.strip()
    ]

    con = duckdb.connect()

    for statement in statements:
        result = con.execute(statement).fetchdf()

        if not result.empty:
            raise AssertionError(
                f"\nSQL test failed in {sql_file.name}:\n"
                f"{result.to_string(index=False)}"
            )

    print(f"PASSED: {sql_file}")


def main():
    sql_dir = Path("tests/sql")

    for sql_file in sorted(sql_dir.glob("test_*.sql")):
        run_sql_file(sql_file)


if __name__ == "__main__":
    main()
