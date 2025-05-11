{{
    config(
        materialized='table',
        tags=['analytics_schema'],
        unique_key='order_item_key'
    )
}}


with order_items_extracted as (
    select
        order_id::int as order_id,
        trim(item.value:"product_id")::varchar(10) as product_id,
        try_to_date(order_date)::date as order_date,
        coalesce(item.value:"quantity"::int, 0) as quantity,
        coalesce(item.value:"price"::decimal(8, 2), 0.00) as unit_price
    from {{ ref('stg_customer_orders') }},
    lateral flatten(input => order_items) as item
    where product_id is not null
),

final as (
    select
        {{ dbt_utils.generate_surrogate_key(['order_id', 'product_id']) }} as order_item_key,
        order_id,
        product_id,
        order_date,
        quantity,
        unit_price,
        quantity * unit_price as line_total
    from order_items_extracted
)

select * from final
