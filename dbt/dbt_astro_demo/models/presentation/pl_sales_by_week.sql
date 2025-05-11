{{ config(
  materialized='view',
  tags=['presentation_schema']
) }}


with weekly_sales as (
  select
    date_trunc('week', o.order_date) as week_start,
    oi.product_id,
    p.product_name,
    sum(oi.quantity) as total_quantity,
    sum(oi.line_total) as total_revenue,
    count(distinct o.order_id) as order_count
  from {{ ref('fct_order') }} o
  join {{ ref('fct_order_item') }} oi on o.order_id = oi.order_id
  LEFT JOIN {{ ref('dim_product') }} p
    ON oi.product_id = p.product_id
  group by 1, 2, 3
),

ranked_products as (
  select
    *,
    rank() over (partition by week_start order by total_quantity desc) as quantity_rank
  from weekly_sales
)

select
  week_start,
  product_id,
  product_name,
  total_quantity,
  total_revenue,
  order_count,
  (quantity_rank = 1) as is_top_seller,
  current_timestamp() as generated_at
from ranked_products
order by week_start desc, quantity_rank asc
