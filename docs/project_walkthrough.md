# Project walkthrough

## End-to-end flow

1. **Source ingestion:** read customer, account and raw transaction CSV files.
2. **Standardization:** trim text fields, normalize status/type/channel values and parse timestamps.
3. **Profiling and validation:** check uniqueness, required fields, numeric amount rules, allowed values and master-data references.
4. **Exception logging:** write issue-level details to `data_quality_issues.csv` and `data_quality_log`.
5. **Curated data load:** load accepted transactions and master data into SQLite.
6. **Operational reporting:** aggregate daily volume, amount and status metrics.
7. **Business intelligence:** use generated reports as Power BI sources and Excel workbook sheets.

## Important design choice

The pipeline preserves a separate issue log before filtering records. This supports traceability: an analyst can see why a record was excluded rather than losing the exception without explanation.

## Interview discussion points

- Why should a transaction identifier be unique?
- Why validate account/customer references?
- What is the difference between missing, invalid and duplicate data?
- Why keep raw data separate from curated data?
- How would you handle exceptions in a production workflow?
- How would you reconcile source counts with loaded counts?
- What controls would protect confidential customer information?

## Suggested enhancements

- Add automated unit tests for validation rules.
- Add a date dimension and more Power BI measures.
- Add configurable validation rules.
- Add a quarantine table for rejected rows.
- Add structured logging and pipeline run metadata.
- Add a MySQL loader and scheduled execution.
