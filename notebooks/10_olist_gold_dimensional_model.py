# Databricks notebook source

BASE = "workspace.default"

spark.sql(f"""
CREATE OR REPLACE TABLE {BASE}.gold_dim_customers
USING DELTA
AS
SELECT
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state,
    customer_zip_code_prefix
FROM {BASE}.silver_olist_customers
""")

print("Customer dimension created!")

print(
    "Customer dimension rows:",
    spark.table(f"{BASE}.gold_dim_customers").count()
)


# COMMAND ----------


BASE = "workspace.default"

spark.sql(f"""
CREATE OR REPLACE TABLE {BASE}.gold_fact_order_items
USING DELTA
AS
SELECT
    i.order_id,
    i.order_item_id,
    o.customer_id,
    i.product_id,
    i.seller_id,
    o.order_status,
    o.order_purchase_timestamp,
    i.price,
    i.freight_value,
    ROUND(i.price + i.freight_value, 2)
        AS item_total
FROM {BASE}.silver_olist_order_items i
INNER JOIN {BASE}.silver_olist_orders o
    ON i.order_id = o.order_id
""")

print("Order-item fact table created!")

fact = spark.table(
    f"{BASE}.gold_fact_order_items"
)

print("Fact rows:", fact.count())

display(fact.limit(10))


# COMMAND ----------


from pyspark.sql import functions as F

BASE = "workspace.default"

dim = spark.table(f"{BASE}.gold_dim_customers")
fact = spark.table(f"{BASE}.gold_fact_order_items")

print("Customer dimension:", dim.count())
print("Order-item fact:", fact.count())

# Check duplicate fact keys
duplicates = (
    fact.groupBy("order_id", "order_item_id")
    .count()
    .filter(F.col("count") > 1)
    .count()
)

# Check missing customer references
missing_customers = fact.join(
    dim.select("customer_id"),
    on="customer_id",
    how="left_anti"
).count()

print("Duplicate fact keys:", duplicates)
print("Missing customer references:", missing_customers)

assert duplicates == 0
assert missing_customers == 0
assert fact.count() == 112650

print("Gold dimensional model validation passed!")
