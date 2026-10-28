# Databricks notebook source

BASE = "workspace.default"

spark.sql(f"""
CREATE OR REPLACE TABLE {BASE}.gold_monthly_sales
USING DELTA
AS
SELECT
    DATE_TRUNC('MONTH', order_purchase_timestamp)
        AS sales_month,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items,
    ROUND(SUM(price), 2) AS merchandise_value,
    ROUND(SUM(freight_value), 2) AS freight_value
FROM {BASE}.gold_fact_order_items
WHERE order_status = 'delivered'
GROUP BY DATE_TRUNC('MONTH', order_purchase_timestamp)
""")

display(spark.table(f"{BASE}.gold_monthly_sales")
    .orderBy("sales_month"))


# COMMAND ----------


BASE = "workspace.default"

spark.sql(f"""
CREATE OR REPLACE TABLE {BASE}.gold_monthly_sales
USING DELTA
AS
SELECT
    DATE_TRUNC('MONTH', order_purchase_timestamp)
        AS sales_month,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items,
    ROUND(SUM(price), 2) AS merchandise_value,
    ROUND(SUM(freight_value), 2) AS freight_value
FROM {BASE}.gold_fact_order_items
WHERE order_status = 'delivered'
GROUP BY DATE_TRUNC('MONTH', order_purchase_timestamp)
""")

display(spark.table(f"{BASE}.gold_monthly_sales")
    .orderBy("sales_month"))


# COMMAND ----------


spark.sql(f"""
CREATE OR REPLACE TABLE {BASE}.gold_state_sales
USING DELTA
AS
SELECT
    c.customer_state,
    COUNT(DISTINCT f.order_id) AS total_orders,
    COUNT(DISTINCT c.customer_unique_id)
        AS unique_customers,
    ROUND(SUM(f.price), 2) AS merchandise_value,
    ROUND(SUM(f.freight_value), 2) AS freight_value
FROM {BASE}.gold_fact_order_items f
JOIN {BASE}.gold_dim_customers c
    ON f.customer_id = c.customer_id
WHERE f.order_status = 'delivered'
GROUP BY c.customer_state
""")

display(spark.table(f"{BASE}.gold_state_sales")
    .orderBy("merchandise_value", ascending=False))


# COMMAND ----------


spark.sql(f"""
CREATE OR REPLACE TABLE {BASE}.gold_order_status
USING DELTA
AS
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM {BASE}.silver_olist_orders
GROUP BY order_status
""")

display(spark.table(f"{BASE}.gold_order_status")
    .orderBy("total_orders", ascending=False))
