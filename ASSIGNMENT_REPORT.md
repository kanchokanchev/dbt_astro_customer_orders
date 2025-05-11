# Customer Orders Data Pipeline

## 1. Project Overview

This project implements a full-stack data pipeline for ingesting, transforming, and analyzing customer order data from a CSV file into Snowflake. It follows a modular architecture using dbt, Astro Airflow, Docker, and Python, with a dimensional modeling approach (Kimball-style) for analytics-ready data.

---

## 2. Snowflake Setup

### 2.1 Snowflake Account Details
- Account URL: https://pnqusxe-dr43857.snowflakecomputing.com
- Account Type: Trial (Demo)

### 2.2 Snowflake Account Credentials
- Account Name: HW
- Account Password: ****
- Account Role: SQL_DEV
- Account Warehouse Assigned: COMPUTE_WH (X-Small)

### 2.3 Snowflake Database Details:
- Database: TEST_DBT_DB
- DB Schemas:
    - RAW
    - STAGING
    - ANALYTICS
    - PRESENTATION

---

## 3. Pipeline Flow

### 3.1 Data Ingestion

- **Source**: CSV from a public HTTP URL
- **Scripts**: Located in `dbt/pipeline`
- **Load method**:
  - `pandas`
  - `snowflake-connector-python` for loading
- **Load pattern**: `TRUNCATE + INSERT` (full refresh)
- **Target**: `RAW.SRC_CUSTOMER_ORDERS`

### 3.2 Data Modeling (Kimball-style)

- **Tool**: dbt
- **Model types**:
  - `DIM_CUSTOMER`
  - `DIM_PRODUCT`
  - `FCT_ORDER`
  - `FCT_ORDER_ITEM`
- **Layered approach**:
  - `staging/`: flat source preparation
  - `marts/`: core facts/dims
  - `presentation/`: aggregated reporting view

### 3.3 Aggregated View

- **Model**: `presentation/pl_sales_by_week.sql`
- **Metrics**:
  - `total_quantity`, `total_revenue`, `order_count`
- **Flags**:
  - `is_top_seller`: True for top product per week

---

## 4. Orchestration

- **Tool**: Astro Airflow
- **DAG**: `airflow/dags/customer_orders_dag.py`
- **Tasks**:
  - Load CSV to Snowflake
  - Run dbt commands (`deps`, `run`, `test`)
- **Execution**: Daily schedule, no catchup
- **Airflow Variables**:
  - `CSV_DATA_URL`, `Snowflake credentials`

---

## 5. Folder Structure

```text
dbt_astro_customer_orders/
├── airflow/
│   ├── dags/                      ← Airflow DAGs
│   ├── include/                   ← Pipeline logic (imported in DAG)
│   ├── Dockerfile, requirements/  ← Astro Airflow setup
├── dbt/
│   ├── dbt_astro_demo/            ← dbt project with models
│   │   ├── staging/
│   │   ├── marts/
│   │   ├── presentation/
│   │   └── sources.yml
│   ├── pipeline/                  ← Python ingestion logic
│   └── profiles.yml               ← dbt Snowflake profile
├── deployment/
│   ├── docker-compose.yml
│   ├── Makefile, Dockerfile       ← CI/CD & deployment tools
|   |── README.md                  ← dbt and Astro Airflow deployment guidelines
└── ASSIGNMENT_REPORT.md           ← This report
