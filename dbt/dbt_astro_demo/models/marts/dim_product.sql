{{
    config(
        materialized='table',
        tags=['analytics_schema'],
        unique_key='product_id'
    )
}}


select distinct
    trim(item.value:"product_id"::varchar(10)) as product_id,
    trim(item.value:"product_name"::varchar(30)) as product_name
from {{ ref('stg_customer_orders') }},
lateral flatten(input => order_items) as item
where product_id is not null
