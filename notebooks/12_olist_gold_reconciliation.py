# Databricks notebook source

from pyspark.sql import functions as F

BASE = "workspace.default"

fact = spark.table(f"{BASE}.gold_fact_order_items")
monthly = spark.table(f"{BASE}.gold_monthly_sales")
state = spark.table(f"{BASE}.gold_state_sales")
statuses = spark.table(f"{BASE}.gold_order_status")
orders = spark.table(f"{BASE}.silver_olist_orders")

# Only delivered orders are included in sales models
delivered = fact.filter(F.col("order_status") == "delivered")

expected_value = delivered.agg(
    F.sum("price").alias("total")
).first()["total"]

monthly_value = monthly.agg(
    F.sum("merchandise_value").alias("total")
).first()["total"]

state_value = state.agg(
    F.sum("merchandise_value").alias("total")
).first()["total"]

# Validate totals within rounding tolerance
assert abs(float(expected_value) - float(monthly_value)) < 0.10
assert abs(float(expected_value) - float(state_value)) < 0.10

print("PASS: Monthly merchandise totals reconcile")
print("PASS: State merchandise totals reconcile")

# Validate order statuses
status_count = statuses.agg(
    F.sum("total_orders")
).first()[0]

assert status_count == orders.count()

print("PASS: Order status totals reconcile")
print("All Gold reconciliation tests passed!")
