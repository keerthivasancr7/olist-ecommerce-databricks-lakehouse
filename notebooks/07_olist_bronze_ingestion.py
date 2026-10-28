# Databricks notebook source

# Step 13: Ingest Olist source tables into Bronze Delta tables

source_tables = {
    "olist_orders_raw": "bronze_olist_orders",
    "olist_customers_raw": "bronze_olist_customers",
    "olist_order_items_raw": "bronze_olist_order_items"
}

catalog_schema = "workspace.default"

for source_name, target_name in source_tables.items():

    source = f"{catalog_schema}.{source_name}"
    target = f"{catalog_schema}.{target_name}"

    df = spark.table(source)

    # Preserve source columns and add ingestion metadata
    from pyspark.sql import functions as F

    bronze_df = df.withColumn(
        "ingested_at",
        F.current_timestamp()
    )

    # Initial full ingestion into a managed Delta table
    (
        bronze_df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(target)
    )

    print(f"{target}: {spark.table(target).count()} rows")

print("Bronze ingestion completed successfully!")
