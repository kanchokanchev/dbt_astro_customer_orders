{{
    config(
        materialized='table',
        tags=['analytics_schema'],
        unique_key='customer_id'
    )
}}


select distinct
    customer_id,
    customer_name,
    customer_phone,
    customer_email
from {{ ref('stg_customer_orders') }}
