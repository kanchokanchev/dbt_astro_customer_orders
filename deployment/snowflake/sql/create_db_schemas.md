# ❄️ Snowflake SQL: Input Source Data Tables Creation and Manual Files Upload

## 1. Specify Snowflake Role and Warehouse
```sql
USE ROLE SQL_DEV;
USE WAREHOUSE COMPUTE_XS;
```

## 2. Create Snowflake Database and Schemas
```sql
CREATE DATABASE IF NOT EXISTS TEST_DBT_DB;

CREATE SCHEMA IF NOT EXISTS RAW;
CREATE SCHEMA IF NOT EXISTS STAGING;
CREATE SCHEMA IF NOT EXISTS ANALYTICS;
CREATE SCHEMA IF NOT EXISTS PRESENTATION;
```

---

## ❄️ Full Snowflake SQL Script
Below is the complete Snowflake SQL script for reference:

```sql
-- 1. Specify Snowflake Role and Warehouse
USE ROLE SQL_DEV;
USE WAREHOUSE COMPUTE_XS;

-- 2. Create Snowflake Database and Schemas
CREATE DATABASE IF NOT EXISTS TEST_DBT_DB;

CREATE SCHEMA IF NOT EXISTS RAW;
CREATE SCHEMA IF NOT EXISTS STAGING;
CREATE SCHEMA IF NOT EXISTS ANALYTICS;
```

---
