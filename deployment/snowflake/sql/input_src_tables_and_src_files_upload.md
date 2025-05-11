# ❄️ Snowflake SQL: Input Source Data Tables Creation and Manual Files Upload

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

## 3. Create Source Data Tables
### 3.1 [src_customer_orders]
```sql
CREATE OR REPLACE TABLE src_customer_orders (
    customer_id INT NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(100),
    customer_email VARCHAR(100),
    order_id INT NOT NULL,
    order_date DATE NOT NULL,
    order_total NUMBER(5,2) NOT NULL,
    order_items VARIANT NOT NULL
);
DESCRIBE TABLE src_customer_orders;
```

## 4.  Dry Run: Manual Files Upload (Internal Stage)
```sql
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

## 5. Real Run: Manual Files Upload (Internal Stage)
### 5.1 [src_customer_orders]
```sql
TRUNCATE TABLE src_customer_orders;

INSERT INTO src_customer_orders
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

SELECT COUNT(*) FROM src_customer_orders;
SELECT * FROM src_customer_orders;
```

---

## ❄️ Full Snowflake SQL Script
Below is the complete Snowflake SQL script for reference:

```sql
-- 1. Specify Snowflake Role and Warehouse
USE ROLE SQL_DEV;
USE WAREHOUSE COMPUTE_WH;

-- 2. Specify Snowflake Database and Schema
USE DATABASE TEST_DBT_DB;
USE SCHEMA RAW;

-- 3. Create Source Data Tables
-- 3.1 [src_customer_orders]
CREATE OR REPLACE TABLE src_customer_orders (
    customer_id INT NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(100),
    customer_email VARCHAR(100),
    order_id INT NOT NULL,
    order_date DATE NOT NULL,
    order_total NUMBER(5,2) NOT NULL,
    order_items VARIANT NOT NULL
);
DESCRIBE TABLE src_customer_orders;

-- 4. Manual Files Upload (Internal Stage)
-- 4.1 src_customer_orders (Dry Run)
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

-- 5. Real Run: Load Files into Database Tables
-- 5.1 [src_customer_orders]
TRUNCATE TABLE src_customer_orders;

INSERT INTO src_customer_orders
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

SELECT COUNT(*) FROM src_customer_orders;
SELECT * FROM src_customer_orders;
```

---
 