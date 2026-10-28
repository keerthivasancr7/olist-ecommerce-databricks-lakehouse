# Reproduction guide

This guide is derived from the seven original source exports. A fresh Databricks run has not been performed.

## Environment

Use Databricks with Spark, Delta SQL including MERGE, and the notebook `display` function. No pip-installed dependencies are declared. Exact runtime versions are unknown. The notebooks require table read and create/replace permissions.

Every notebook uses `workspace.default`. Import the `.py` source files as notebooks and either use that catalog/schema or change each `BASE`/`catalog_schema` assignment consistently. This repository does not provision catalogs or compute.

## Prepare inputs

Create these tables before notebook 07. The columns below are those referenced downstream, not complete validated schemas:

| Raw table in workspace.default | Required referenced columns |
| --- | --- |
| olist_orders_raw | order_id, customer_id, order_purchase_timestamp, order_status |
| olist_customers_raw | customer_id, customer_unique_id, customer_city, customer_state, customer_zip_code_prefix |
| olist_order_items_raw | order_id, order_item_id, product_id, seller_id, price, freight_value |

Use compatible key types, numeric price/freight columns, and a purchase timestamp compatible with DATE_TRUNC. Source files assume these tables already exist; they do not download CSVs or perform raw type casting. Dataset source/version, ingestion steps, full schemas, and licensing must be supplied separately.

## Execute the batch pipeline

1. **07:** Read raw orders/customers/items; preserve source columns, add current `ingested_at`, write `bronze_olist_orders`, `bronze_olist_customers`, `bronze_olist_order_items` as Delta with overwrite.
2. **08:** Filter orders with nonnull order/customer/purchase timestamp; deduplicate order ID. Filter customers with nonnull customer ID/unique ID, deduplicate customer ID, trim city. Filter items with nonnull order/item/product IDs and nonnegative, nonnull price/freight, deduplicate `(order_id, order_item_id)`. Overwrite corresponding `silver_olist_*` tables.
3. **09:** Assert zero orders missing customers, items missing orders, and duplicate order IDs. Distinct order IDs appearing in items are printed, not asserted.
4. **10:** Create/replace `gold_dim_customers` and `gold_fact_order_items`. Assert unique composite fact keys, no missing dimension references, and exactly **112650** fact rows. This last check is specific to the author's dataset snapshot.
5. **11:** Create/replace `gold_monthly_sales`, `gold_state_sales`, and `gold_order_status`. Sales aggregate delivered orders only, using purchase month and customer state. The first monthly-sales cell is repeated in the original export.
6. **12:** Assert monthly and state merchandise totals each differ from delivered-fact price totals by **less than 0.10**. Assert summed status counts equal the silver order count. Inspect printed results; assertion failures stop execution.

All tables above live in the configured catalog/schema. Full-pipeline reruns overwrite or replace results. Relationship validation should pass before gold modeling, although it does not itself create a table consumed by 10.

## Run the separate incremental demonstration

After 08, run all cells of **13** in order in the same notebook session:

1. Recreate `demo_incremental_orders` from the first 100 silver orders sorted by order ID.
2. Select sorted source rows 96–105 as a ten-row batch and register the temporary view `incremental_batch`.
3. MERGE on order ID, updating matches and inserting new keys. Repeat the same batch and assert both counts remain 105. The source repeats this demonstration in another cell.
4. Assert 105 target rows, no duplicate order IDs, every incoming key present, and all incoming values present in the target using `exceptAll`.

This assumes at least 105 unique silver orders. The intended overlap is five existing plus five new orders. Full notebook reruns reset the target; there is no persistent watermark or CDC source. Its session variables and temporary view must exist before the MERGE/check cells.

## Verification boundary

Python AST parsing succeeded for all seven exports; it does not validate embedded SQL, table schemas, runtime permissions, or assertions against real data. A prior visible job run succeeded on 28 October 2026, but the job configuration and per-task results were not exported. Notebook 13 was not among its six displayed tasks.

Before calling this portable or reproducible, record dataset provenance and schemas, runtime details, job dependencies, and results from a clean-workspace run. Do not reinterpret source assertions as observed results.
