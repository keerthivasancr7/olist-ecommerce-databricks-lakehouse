# Olist E-commerce Databricks Lakehouse

An Olist e-commerce data project in Databricks, organized around bronze ingestion, silver transformation, relationship validation, gold dimensional modeling, business analytics, and reconciliation.

**Status:** The seven existing notebooks numbered **07–13** are awaiting export and upload. This repository is not yet a reproducible implementation.

## Verified workspace observations

On 28 October 2026, the connected Databricks Free Edition job page showed job `Olist_Ecommerce_Data_Lakehouse`, serverless compute, and a manual run at 16:26 Europe/Berlin with status **Succeeded** and duration **2m 36s**.

The page listed six tasks:

- `bronze_ingestion`
- `silver_transformation`
- `relationship_validation`
- `gold_dimensional_model`
- `gold_business_analytics`
- `gold_reconciliation`

Notebook source, task dependency order, schemas, quality rules, row counts, and analytical results have not yet been inspected. The mapping between six tasks and seven notebooks remains unverified. A successful job status alone does not establish data correctness or performance.

## Repository structure

- [notebooks/](notebooks/README.md): source inventory and export handoff
- [docs/reproduction.md](docs/reproduction.md): requirements for a reproducible run
- [LICENSE](LICENSE): MIT license for repository code
- `.gitignore`: existing Python exclusions

## Run instructions

Pending source export and review. Dataset location, catalog/schema names, environment requirements, and task dependencies must be confirmed from the actual notebooks before a reliable run guide can be provided. No notebook code or results have been generated to fill missing source.

## Dataset and license

Dataset provenance, version, licensing, and attribution must be verified from the actual project before redistributing data. The repository MIT license does not grant rights to third-party datasets.
