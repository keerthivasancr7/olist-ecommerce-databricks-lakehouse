# Databricks notebook source

from pyspark.sql import functions as F

BASE = "workspace.default"

# Read Bronze tables
orders = spark.table(f"{BASE}.bronze_olist_orders")
customers = spark.table(f"{BASE}.bronze_olist_customers")
items = spark.table(f"{BASE}.bronze_olist_order_items")

# SILVER ORDERS
# Preserve all valid order statuses and delivery timestamps
silver_orders = (
    orders
    .filter(F.col("order_id").isNotNull())
    .filter(F.col("customer_id").isNotNull())
    .filter(F.col("order_purchase_timestamp").isNotNull())
    .dropDuplicates(["order_id"])
)

# SILVER CUSTOMERS
silver_customers = (
    customers
    .filter(F.col("customer_id").isNotNull())
    .filter(F.col("customer_unique_id").isNotNull())
    .dropDuplicates(["customer_id"])
    .withColumn(
        "customer_city",
        F.trim(F.col("customer_city"))
    )
)

# SILVER ORDER ITEMS
silver_items = (
    items
    .filter(F.col("order_id").isNotNull())
    .filter(F.col("order_item_id").isNotNull())
    .filter(F.col("product_id").isNotNull())
    .filter(F.col("price").isNotNull())
    .filter(F.col("price") >= 0)
    .filter(F.col("freight_value").isNotNull())
    .filter(F.col("freight_value") >= 0)
    .dropDuplicates(["order_id", "order_item_id"])
)

# Write Silver Delta tables
tables = {
    "silver_olist_orders": silver_orders,
    "silver_olist_customers": silver_customers,
    "silver_olist_order_items": silver_items
}

for name, df in tables.items():
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(f"{BASE}.{name}")
    )

    print(f"{name}: {spark.table(f'{BASE}.{name}').count()} rows")

print("Silver transformation completed successfully!")
