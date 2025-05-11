{{
    config(
        materialized='table',
        tags=['analytics_schema'],
        unique_key='product_id'
    )
}}


select distinct
    order_id,
    customer_id,
    order_date,
    order_total
from {{ ref('stg_customer_orders') }}
