# Data dictionary

All records are synthetic and intended for learning.

## customers.csv

| Column | Meaning |
|---|---|
| customer_id | Synthetic unique customer key |
| customer_name | Synthetic customer label |
| city | Sample city |
| segment | Retail, Premium or Business |

## accounts.csv

| Column | Meaning |
|---|---|
| account_id | Synthetic unique account key |
| customer_id | Customer reference |
| account_type | Savings, Current or Salary |
| account_status | Active, Dormant or Closed |

## transactions_raw.csv

| Column | Meaning |
|---|---|
| transaction_id | Synthetic transaction key; duplicate values are intentionally included |
| account_id | Account reference |
| customer_id | Customer reference; missing values are intentionally included |
| transaction_date | Transaction timestamp |
| channel | Banking channel; invalid values are intentionally included |
| transaction_type | CREDIT or DEBIT |
| amount | Transaction amount in INR; non-positive values are intentionally included |
| currency | Currency code |
| status | SUCCESS, FAILED or PENDING |

## Generated reports

- `transactions_clean.csv`: rows that pass the pipeline's validation rules.
- `data_quality_issues.csv`: one row per detected issue, with transaction ID, issue type and description.
- `data_quality_summary.csv`: high-level counts.
- `daily_operations_report.csv`: daily transaction count, value, successful count, failed count and success rate.
