-- Test 1: row count should be non-zero
-- PASS = returns 0 rows
-- FAIL = returns 1 row

SELECT
    'laps_row_count_non_zero' AS test_name,
    COUNT(*) AS row_count
FROM read_parquet('data/raw/laps/session_key=*/laps.parquet')
HAVING COUNT(*) = 0;


-- Test 2: primary key columns should not be null
-- Practical primary key: session_key + driver_number + lap_number
-- PASS = returns 0 rows
-- FAIL = returns rows with null PK values

SELECT
    'laps_primary_key_not_null' AS test_name,
    *
FROM read_parquet('data/raw/laps/session_key=*/laps.parquet')
WHERE session_key IS NULL
   OR driver_number IS NULL
   OR lap_number IS NULL;


-- Test 3: primary key should be unique
-- Practical primary key: session_key + driver_number + lap_number
-- PASS = returns 0 rows
-- FAIL = returns duplicate lap records

SELECT
    'laps_primary_key_unique' AS test_name,
    session_key,
    driver_number,
    lap_number,
    COUNT(*) AS duplicate_count
FROM read_parquet('data/raw/laps/session_key=*/laps.parquet')
GROUP BY
    session_key,
    driver_number,
    lap_number
HAVING COUNT(*) > 1;


-- Test 4: basic data type correctness
-- PASS = returns 0 rows
-- FAIL = returns rows with unexpected data types

SELECT
    'laps_data_type_correctness' AS test_name,
    *
FROM read_parquet('data/raw/laps/session_key=*/laps.parquet')
WHERE typeof(session_key) NOT IN ('INTEGER', 'BIGINT')
   OR typeof(driver_number) NOT IN ('INTEGER', 'BIGINT')
   OR typeof(lap_number) NOT IN ('INTEGER', 'BIGINT')
   OR typeof(lap_duration) NOT IN ('DOUBLE', 'FLOAT', 'REAL', 'DECIMAL');