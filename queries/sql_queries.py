# They will be joined on the date column

waw_daily_orders = f"""
    SELECT
    p_creation_date as date
    ,COUNT(order_id) AS waw_orders
FROM delta.central_order_descriptors_odp.order_descriptors_v2 o
WHERE 1=1
    AND o.order_final_status = 'DeliveredStatus'
    AND o.order_parent_id IS NULL
    AND o.order_country_code = 'PL'
    AND o.order_city_code = 'WAW'
    AND o.p_creation_date >= DATE '2024-01-01'
GROUP BY 1
ORDER BY 1
"""
gdn_daily_orders = f"""
    SELECT
    p_creation_date as date
    ,COUNT(order_id) AS gdn_orders
FROM delta.central_order_descriptors_odp.order_descriptors_v2 o
WHERE 1=1
    AND o.order_final_status = 'DeliveredStatus'
    AND o.order_parent_id IS NULL
    AND o.order_country_code = 'PL'
    AND o.order_city_code = 'GDN'
    AND o.p_creation_date >= DATE '2024-01-01'
GROUP BY 1
ORDER BY 1
"""
