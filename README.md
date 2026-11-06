# Banking Data Management & Data Quality Analytics

A hands-on portfolio project demonstrating a junior Data / Information Management Analyst workflow using **Python, SQL, Excel, SQLite and Power BI**.

> **Data notice:** This is an educational simulation. All customer, account and transaction records are synthetic. This project is not affiliated with, endorsed by, or used by Citi or any other bank.

## Business problem

Banking operations data can arrive with duplicate transaction IDs, missing customer references, invalid amounts, inconsistent channel values and malformed dates. These issues can reduce the reliability of operational reporting.

This project demonstrates a repeatable workflow to:
1. Ingest synthetic customer, account and transaction files.
2. Standardize fields and validate incoming records.
3. Log data-quality exceptions for review.
4. Load accepted records into a relational database.
5. Produce daily operational and data-quality reports.
6. Explore transaction trends and quality metrics in Excel and Power BI.

## Technology

| Tool | How it is used |
|---|---|
| Python | ETL orchestration and repeatable processing |
| Pandas / NumPy | Data cleaning, validation and aggregation |
| SQL | Relational schema and analytical queries |
| SQLite | Local database created by the ETL script |
| Excel | Operational reporting and reconciliation workbook |
| Power BI | Dashboard design guide and DAX measures |

## Repository structure

```text
Banking-Data-Management-Analytics/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── etl.py
├── data/
│   ├── customers.csv
│   ├── accounts.csv
│   └── transactions_raw.csv
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── reports/
│   ├── transactions_clean.csv
│   ├── data_quality_issues.csv
│   ├── data_quality_summary.csv
│   ├── daily_operations_report.csv
│   └── banking_operations_workbook.xlsx
├── powerbi/
│   ├── DAX_measures.txt
│   └── dashboard_build_guide.md
└── docs/
    ├── data_dictionary.md
    └── project_walkthrough.md
```

## Quick start

### 1. Requirements
- Python 3.10 or newer
- pip
- Optional: Excel or LibreOffice
- Optional: Power BI Desktop (Windows)

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the ETL pipeline

Run this command from the repository root:

```bash
python etl.py
```

The script reads the CSV files in `data/`, creates the `reports/` outputs, and creates `banking_analytics.db` in the repository root.

### 4. Inspect the database

Open `banking_analytics.db` using DB Browser for SQLite, or connect to it from a compatible SQL client.

The ETL creates these tables:
- `customers`
- `accounts`
- `transactions`
- `data_quality_log`

### 5. Explore reports
- `reports/transactions_clean.csv` — accepted transaction records.
- `reports/data_quality_issues.csv` — row-level validation exceptions.
- `reports/data_quality_summary.csv` — key input and output counts.
- `reports/daily_operations_report.csv` — daily transaction volume, value and status counts.
- `reports/banking_operations_workbook.xlsx` — workbook containing raw data, cleaned data and report sheets.

## Data-quality rules

The sample pipeline checks:
- Transaction ID is present and unique.
- Account ID and customer ID are present.
- Transaction date can be parsed.
- Amount is numeric and greater than zero.
- Channel is in the approved list.
- Status is one of `SUCCESS`, `FAILED`, or `PENDING`.
- Transaction account and customer references exist in the supplied master data.

Invalid rows are excluded from the clean output and their exceptions are written to the issue log. In a real banking environment, rejected data should be quarantined and corrected through controlled workflows; it should not be silently discarded.

## SQL skills demonstrated

See `sql/analysis_queries.sql` for examples of:
- Duplicate identification (`GROUP BY`, `HAVING`)
- Missing transaction/customer checks (`LEFT JOIN`)
- Daily and channel-level aggregations
- Conditional aggregation using `CASE WHEN`
- High-value transaction reporting
- Data reconciliation checks

The SQL scripts target MySQL 8 syntax. The Python ETL uses SQLite so the demo can run locally without a database server.

## Power BI dashboard

Power BI Desktop is optional. Follow `powerbi/dashboard_build_guide.md` to build three report pages:

1. **Operations Overview** — transaction count, transaction value, success rate, failed transactions and daily trends.
2. **Channel Performance** — volume and value by channel, channel/status matrix and success rate.
3. **Data Quality** — raw records, clean records, excluded records and issue categories.

Load the generated CSV reports from `reports/`. DAX examples are in `powerbi/DAX_measures.txt`.

**Note:** This repository contains the dashboard specification and DAX measures, not a finished `.pbix` file. Add your own `.pbix` and genuine dashboard screenshots after building the report in Power BI Desktop.

## Excel analysis

The workbook includes:
- Raw Transactions
- Clean Transactions
- Quality Summary
- Quality Issues
- Daily Report

Suggested next steps in Excel:
- Create PivotTables for channel/status and customer-segment summaries.
- Add conditional formatting to failed transactions and data-quality exceptions.
- Reconcile raw, accepted and excluded record counts.

## Example run result

The included synthetic sample currently contains 2,520 raw rows. Running the supplied pipeline produces 2,447 accepted rows and logs the excluded records. The exact counts should be verified by running `python etl.py`.

## Limitations and production considerations

This is a learning project, not a production banking system. It does not process real personal data, connect to banking systems, make credit decisions, or determine fraud. A production implementation would additionally require access controls, encryption, secrets management, audit trails, retention rules, monitoring, formal data ownership and approved exception-handling procedures.

## Skills demonstrated

**SQL | Python | Pandas | ETL | Data Cleaning | Data Validation | Data Quality | Data Reconciliation | Relational Database Design | Excel Reporting | Power BI | DAX**

## Author

Add your name, LinkedIn profile and contact details here before publishing.
