# Databricks notebook source

BASE = "workspace.default"

spark.sql(f"""
CREATE OR REPLACE TABLE {BASE}.demo_incremental_orders
USING DELTA
AS
SELECT *
FROM {BASE}.silver_olist_orders
ORDER BY order_id
LIMIT 100
""")

print(
    "Initial records:",
    spark.table(f"{BASE}.demo_incremental_orders").count()
)


# COMMAND ----------


from pyspark.sql import functions as F
from pyspark.sql.window import Window

BASE = "workspace.default"

source = spark.table(f"{BASE}.silver_olist_orders")

window = Window.orderBy("order_id")

batch = (
    source
    .withColumn("row_num", F.row_number().over(window))
    .filter(F.col("row_num").between(96, 105))
    .drop("row_num")
)

batch.createOrReplaceTempView("incremental_batch")

print("Incoming batch records:", batch.count())


# COMMAND ----------


BASE = "workspace.default"

merge_sql = f"""
MERGE INTO {BASE}.demo_incremental_orders AS target
USING incremental_batch AS source
ON target.order_id = source.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
"""

# First incremental load
spark.sql(merge_sql)

first_count = spark.table(
    f"{BASE}.demo_incremental_orders"
).count()

print("Records after first MERGE:", first_count)

# Repeat the same batch
spark.sql(merge_sql)

second_count = spark.table(
    f"{BASE}.demo_incremental_orders"
).count()

print("Records after second MERGE:", second_count)

assert first_count == 105
assert second_count == 105

print("PASS: Incremental loading is idempotent!")


# COMMAND ----------


merge_sql = f"""
MERGE INTO {BASE}.demo_incremental_orders AS target
USING incremental_batch AS source
ON target.order_id = source.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
"""

spark.sql(merge_sql)

count_after_merge = spark.table(
    f"{BASE}.demo_incremental_orders"
).count()

print("Records after first MERGE:", count_after_merge)

# Run the same batch again to verify idempotency
spark.sql(merge_sql)

count_after_rerun = spark.table(
    f"{BASE}.demo_incremental_orders"
).count()

print("Records after second MERGE:", count_after_rerun)

assert count_after_merge == 105
assert count_after_rerun == 105

print("PASS: Incremental loading is idempotent!")


# COMMAND ----------


from pyspark.sql import functions as F

BASE = "workspace.default"

target = spark.table(
    f"{BASE}.demo_incremental_orders"
)

# Test 1: Exactly 105 rows
assert target.count() == 105
print("PASS: Correct total record count")

# Test 2: No duplicate order IDs
duplicate_count = (
    target.groupBy("order_id")
    .count()
    .filter(F.col("count") > 1)
    .count()
)

assert duplicate_count == 0
print("PASS: No duplicate order IDs")

# Test 3: Every incoming order exists in target
missing_orders = batch.select("order_id").join(
    target.select("order_id"),
    on="order_id",
    how="left_anti"
).count()

assert missing_orders == 0
print("PASS: All incoming orders exist in target")

# Test 4: Incoming values match target
columns = batch.columns

mismatches = (
    batch.select(*columns)
    .exceptAll(target.select(*columns))
    .count()
)

assert mismatches == 0
print("PASS: Incoming records match target")

print("All incremental loading tests passed!")
