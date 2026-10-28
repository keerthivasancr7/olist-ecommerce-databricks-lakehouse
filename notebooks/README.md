# Original Databricks notebooks

All seven notebooks were manually exported from the existing Databricks workspace and supplied on 28 October 2026. The source files are preserved unchanged, including notebook headers and cell delimiters.

| Sequence | Source | Purpose |
| --- | --- | --- |
| 07 | [07_olist_bronze_ingestion.py](07_olist_bronze_ingestion.py) | Full bronze ingestion from existing raw tables |
| 08 | [08_olist_silver_transformation.py](08_olist_silver_transformation.py) | Silver filtering and deduplication |
| 09 | [09_olist_relationship_validation.py](09_olist_relationship_validation.py) | Relationship and order-key assertions |
| 10 | [10_olist_gold_dimensional_model.py](10_olist_gold_dimensional_model.py) | Customer dimension and order-item fact |
| 11 | [11_olist_gold_business_analytics.py](11_olist_gold_business_analytics.py) | Monthly/state sales and order statuses |
| 12 | [12_olist_gold_reconciliation.py](12_olist_gold_reconciliation.py) | Merchandise totals and status counts |
| 13 | [13_olist_incremental_loading.py](13_olist_incremental_loading.py) | Separate subset MERGE demonstration |

Run 07–12 in order after preparing the required raw tables. Notebook 13 depends on silver orders from 08 and may run separately after that step. All cells within each notebook must execute in order.

Python syntax was checked locally; Databricks execution was not repeated. See [setup and limitations](../docs/reproduction.md) and the [root README](../README.md).
