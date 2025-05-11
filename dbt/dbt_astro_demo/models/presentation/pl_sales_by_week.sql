{{ config(
  materialized='view',
  tags=['presentation_schema']
) }}

with weekly_sales as (
  select
    date_trunc('week', o.order_date) as week_start,
    dateadd(day, 6, date_trunc('week', o.order_date)) as week_end,
    oi.product_id,
    p.product_name,
    coalesce(sum(oi.quantity), 0) as total_quantity,
    coalesce(sum(oi.line_total), 0.00) as total_revenue,
    coalesce(count(distinct o.order_id), 0) as order_count
  from {{ ref('fct_order') }} o
  join {{ ref('fct_order_item') }} oi on o.order_id = oi.order_id
  left join {{ ref('dim_product') }} p on oi.product_id = p.product_id
  group by 1, 2, 3, 4
),

ranked_products as (
  select
    *,
    rank() over (partition by week_start order by total_quantity desc) as quantity_rank
  from weekly_sales
)

select
  {{ dbt_utils.generate_surrogate_key(['week_start', 'product_id']) }} as pl_key,
  week_start,
  week_end,
  product_id,
  product_name,
  total_quantity,
  total_revenue,
  order_count,
  (quantity_rank = 1) as is_top_seller,
  current_timestamp() as generated_at
from ranked_products
order by week_start desc, quantity_rank asc
