# Power BI dashboard build guide

## Data sources
Import:
- `reports/transactions_clean.csv`
- `reports/data_quality_summary.csv`
- `reports/daily_operations_report.csv`

Set `transaction_date` to Date/Time and `amount` to Decimal Number. Create a Date table if extending the model.

## Page 1 — Operations Overview
Cards: Total Transactions, Total Transaction Value, Success Rate %, Failed Transactions.
Line chart: transaction count by transaction date.
Clustered column chart: transaction count by channel.
Slicers: date, channel, status.

## Page 2 — Channel Performance
Bar chart: transaction value by channel.
Matrix: channel by status with transaction count.
Column chart: success rate by channel (create a channel-level measure using CALCULATE).

## Page 3 — Data Quality
Cards: Raw Records, Clean Records, Records Removed, Data Retention %.
Bar chart: issue type and count from `data_quality_issues.csv`.
Table: transaction ID, issue type, issue description.
Add a note that the counts are validation exceptions in a synthetic learning dataset.

## Model relationships
If importing all master files, relate:
- customers[customer_id] 1:* transactions[customer_id]
- accounts[account_id] 1:* transactions[account_id]
Use single-direction filtering from dimensions to fact table.
