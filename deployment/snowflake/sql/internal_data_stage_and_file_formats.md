# ❄️ Snowflake SQL: Internal Data Stage and File Formats Creation

## 1. Specify Snowflake Role and Warehouse
```sql
USE ROLE SQL_DEV;
USE WAREHOUSE COMPUTE_WH;
```

## 2. Specify Snowflake Database and Schema
```sql
USE DATABASE TEST_DBT_DB;
USE SCHEMA RAW;
```

## 3. Create an Internal Data Stage
```sql
CREATE STAGE IF NOT EXISTS TEST_DATA_STAGE;
DESCRIBE STAGE TEST_DATA_STAGE;

-- List Stage Files
LIST @TEST_DATA_STAGE;
```

## 4. Create Data File Formats
### 4.1 Input Data File Format (for loading the input source data files)
```sql
CREATE OR REPLACE FILE FORMAT TEST_INPUT_DATA_FILE_FORMAT
    TYPE = 'CSV'
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    NULL_IF = ('\\N', 'null', 'NULL', '""', '"N/A"', '', 'N/A', '"n/a"', 'n/a');
DESCRIBE FILE FORMAT TEST_INPUT_DATA_FILE_FORMAT;
```

### 4.2 Dry Run: Manual Files Upload (Internal Stage)
```sql
SELECT 
    $1 AS customer_id,
    $2 AS customer_name,
    $3 AS customer_phone,
    $4 AS customer_email,
    $5 AS order_id,
    $6 AS order_date,
    $7 AS order_total,
    $8 AS order_items
FROM '@TEST_DATA_STAGE/customer_orders.csv'
(FILE_FORMAT => TEST_INPUT_DATA_FILE_FORMAT);
```

---

## ❄️ Full Snowflake SQL Script
Below is the complete Snowflake SQL script for reference:

```sql
-- 1. Specify SF Role and Warehouse
USE ROLE SQL_DEV;
USE WAREHOUSE COMPUTE_WH;

-- 2. Specify SF Database and Schema
USE DATABASE TEST_DBT_DB;
USE SCHEMA RAW;

-- 3. Create an Internal Data Stage
CREATE STAGE IF NOT EXISTS TEST_DATA_STAGE;
DESCRIBE STAGE TEST_DATA_STAGE;

-- List Stage Files
LIST @TEST_DATA_STAGE;

-- 4. Create Data File Formats
-- 4.1 Input Data File Format
CREATE OR REPLACE FILE FORMAT TEST_INPUT_DATA_FILE_FORMAT
    TYPE = 'CSV'
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    NULL_IF = ('\\N', 'null', 'NULL', '""', '"N/A"', '', 'N/A', '"n/a"', 'n/a');
DESCRIBE FILE FORMAT TEST_INPUT_DATA_FILE_FORMAT;

-- 4.2 Dry Run: Manual Files Upload (Internal Stage)
SELECT 
    $1 AS customer_id,
    $2 AS customer_name,
    $3 AS customer_phone,
    $4 AS customer_email,
    $5 AS order_id,
    $6 AS order_date,
    $7 AS order_total,
    TRY_PARSE_JSON($8) AS order_items
FROM '@TEST_DATA_STAGE/customer_orders.csv'
(FILE_FORMAT => TEST_INPUT_DATA_FILE_FORMAT);
```

---
 