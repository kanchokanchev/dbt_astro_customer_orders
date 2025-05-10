{{
    config(
        materialized='table',
        tags=['staging_schema'],
        unique_key='customer_id'
    )
}}


with source_data as (
    select *
    from {{ source ('RAW','SRC_CUSTOMER_ORDERS') }}
)

select
    customer_id,
    trim(customer_name) as customer_name,
    regexp_replace(customer_phone, '[^0-9+]', '') as customer_phone,
    lower(trim(customer_email)) as customer_email,
    order_id,
    try_to_date(order_date) as order_date,
    coalesce(order_total, 0) as order_total,
    try_parse_json(order_items) as order_items,
    current_timestamp() as dbt_loaded_at
from source_data
