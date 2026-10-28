# Databricks notebook source

from pyspark.sql import functions as F

BASE = "workspace.default"

orders = spark.table(f"{BASE}.silver_olist_orders")
customers = spark.table(f"{BASE}.silver_olist_customers")
items = spark.table(f"{BASE}.silver_olist_order_items")

# Test 1: Orders referencing missing customers
missing_customers = orders.join(
    customers.select("customer_id"),
    on="customer_id",
    how="left_anti"
).count()

print("Orders without matching customers:", missing_customers)

# Test 2: Items referencing missing orders
orphan_items = items.join(
    orders.select("order_id"),
    on="order_id",
    how="left_anti"
).count()

print("Order items without matching orders:", orphan_items)

# Test 3: Orders containing items
orders_with_items = items.select(
    "order_id"
).distinct().count()

print("Orders with items:", orders_with_items)

# Test 4: Verify order ID uniqueness
duplicate_orders = (
    orders.groupBy("order_id")
    .count()
    .filter(F.col("count") > 1)
    .count()
)

print("Duplicate order IDs:", duplicate_orders)

assert missing_customers == 0, "Missing customers found"
assert orphan_items == 0, "Orphan order items found"
assert duplicate_orders == 0, "Duplicate orders found"

print("All relationship validation tests passed!")
