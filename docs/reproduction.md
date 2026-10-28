# Reproduction checklist

Notebook source is pending export. This checklist is not a tested execution guide.

## Confirm from notebooks 07–13

- Exact filenames, languages, purposes, and dependencies
- Dataset source, version, license, required files, and upload location
- Catalog, schema, table, volume, and storage paths
- Runtime/serverless environment, libraries, and permissions
- Parameters and workspace-specific configuration
- Ingestion behavior, rerun behavior, and write modes
- Transformation rules and relationship validation assertions
- Fact/dimension definitions, grain, metrics, and reconciliation assertions
- Expected outputs and evidence used to validate them

## Validate after upload

1. Inspect all seven original notebook exports.
2. Document dataset preparation and workspace setup.
3. Map the six observed job tasks to their source notebooks and confirm dependency order.
4. Recreate that confirmed task graph in a suitable Databricks workspace.
5. Run the project and inspect outputs and validation assertions.
6. Check rerun behavior and document limitations.
7. Replace pending documentation with tested instructions and evidence.

The observed job status was Succeeded on 28 October 2026, with duration 2m 36s on serverless compute. No source-level checks or per-task validation results were inspected. Do not treat this status as proof of data correctness, benchmark performance, or reproducibility.
