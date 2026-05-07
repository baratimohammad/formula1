-- Test 1: row count should be non-zero
-- PASS = returns 0 rows
-- FAIL = returns 1 row

SELECT
    'drivers_row_count_non_zero' AS test_name,
    COUNT(*) AS row_count
FROM read_parquet('{{ raw_root }}/drivers/session_key=*/drivers.parquet', union_by_name = true)
HAVING COUNT(*) = 0;


-- Test 2: primary key columns should not be null
-- Primary key: session_key + driver_number
-- PASS = returns 0 rows
-- FAIL = returns rows with null PK values

SELECT
    'drivers_primary_key_not_null' AS test_name,
    *
FROM read_parquet('{{ raw_root }}/drivers/session_key=*/drivers.parquet', union_by_name = true)
WHERE session_key IS NULL
   OR driver_number IS NULL;


-- Test 3: primary key should be unique
-- Primary key: session_key + driver_number
-- PASS = returns 0 rows
-- FAIL = returns duplicate keys

SELECT
    'drivers_primary_key_unique' AS test_name,
    session_key,
    driver_number,
    COUNT(*) AS duplicate_count
FROM read_parquet('{{ raw_root }}/drivers/session_key=*/drivers.parquet', union_by_name = true)
GROUP BY
    session_key,
    driver_number
HAVING COUNT(*) > 1;


-- Test 4: basic data type correctness
-- In DuckDB, typeof() returns types such as INTEGER, BIGINT, VARCHAR, DOUBLE
-- PASS = returns 0 rows
-- FAIL = returns rows with unexpected data types

SELECT
    'drivers_data_type_correctness' AS test_name,
    *
FROM read_parquet('{{ raw_root }}/drivers/session_key=*/drivers.parquet', union_by_name = true)
WHERE typeof(session_key) NOT IN ('INTEGER', 'BIGINT')
   OR typeof(driver_number) NOT IN ('INTEGER', 'BIGINT')
   OR typeof(full_name) <> 'VARCHAR'
   OR typeof(team_name) <> 'VARCHAR';
