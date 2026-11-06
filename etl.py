"""Clean raw banking transactions, validate records, and load a local SQLite database."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

raw = pd.read_csv(DATA / "transactions_raw.csv")
customers = pd.read_csv(DATA / "customers.csv")
accounts = pd.read_csv(DATA / "accounts.csv")

raw_count = len(raw)
# Normalize text fields and dates
for col in ["transaction_id", "account_id", "customer_id", "channel", "status", "transaction_type", "currency"]:
    raw[col] = raw[col].astype("string").str.strip()
raw["channel"] = raw["channel"].str.title()
raw["status"] = raw["status"].str.upper()
raw["transaction_type"] = raw["transaction_type"].str.upper()
raw["transaction_date"] = pd.to_datetime(raw["transaction_date"], errors="coerce")
raw["amount"] = pd.to_numeric(raw["amount"], errors="coerce")

# Identify quality issues before excluding invalid records
issues = []
def add_issue(mask, issue_type, description):
    for txn_id in raw.loc[mask, "transaction_id"].fillna("MISSING_ID").astype(str):
        issues.append({"transaction_id": txn_id, "issue_type": issue_type, "issue_description": description})

add_issue(raw["transaction_id"].isna(), "MISSING_TRANSACTION_ID", "Transaction ID is missing")
add_issue(raw.duplicated("transaction_id", keep="first"), "DUPLICATE_TRANSACTION", "Repeated transaction ID")
add_issue(raw["amount"].isna(), "INVALID_AMOUNT", "Amount is missing or non-numeric")
add_issue(raw["amount"].le(0), "NON_POSITIVE_AMOUNT", "Amount must be greater than zero")
add_issue(raw["customer_id"].isna(), "MISSING_CUSTOMER_ID", "Customer reference is missing")
add_issue(~raw["channel"].isin(["Upi","Atm","Debit Card","Net Banking","Neft","Imps"]), "INVALID_CHANNEL", "Channel is outside the approved list")
add_issue(raw["transaction_date"].isna(), "INVALID_DATE", "Transaction date is invalid")

# Remove duplicate IDs; retain first occurrence
clean = raw.drop_duplicates(subset=["transaction_id"], keep="first").copy()
# Keep only records passing required-field and domain validations
valid_channels = ["Upi","Atm","Debit Card","Net Banking","Neft","Imps"]
valid_status = ["SUCCESS","FAILED","PENDING"]
valid_types = ["CREDIT","DEBIT"]
clean = clean[
    clean["transaction_id"].notna()
    & clean["account_id"].notna()
    & clean["customer_id"].notna()
    & clean["transaction_date"].notna()
    & clean["amount"].notna()
    & clean["amount"].gt(0)
    & clean["channel"].isin(valid_channels)
    & clean["status"].isin(valid_status)
    & clean["transaction_type"].isin(valid_types)
]
# Referential integrity check against master data
clean = clean[clean["account_id"].isin(accounts["account_id"]) & clean["customer_id"].isin(customers["customer_id"])]

# Write operational outputs
clean.to_csv(REPORTS / "transactions_clean.csv", index=False)
pd.DataFrame(issues).to_csv(REPORTS / "data_quality_issues.csv", index=False)

quality_summary = pd.DataFrame([
    ["Raw records", raw_count],
    ["Clean records loaded", len(clean)],
    ["Records removed", raw_count-len(clean)],
    ["Duplicate transaction rows", int(raw.duplicated("transaction_id").sum())],
    ["Missing customer IDs", int(raw["customer_id"].isna().sum())],
    ["Non-positive amounts", int(raw["amount"].le(0).sum())],
    ["Invalid channels", int((~raw["channel"].isin(valid_channels)).sum())],
], columns=["metric","value"])
quality_summary.to_csv(REPORTS / "data_quality_summary.csv", index=False)

# SQLite database for a zero-setup runnable demo
db_path = ROOT / "banking_analytics.db"
with sqlite3.connect(db_path) as conn:
    customers.to_sql("customers", conn, if_exists="replace", index=False)
    accounts.to_sql("accounts", conn, if_exists="replace", index=False)
    clean.to_sql("transactions", conn, if_exists="replace", index=False)
    pd.DataFrame(issues).to_sql("data_quality_log", conn, if_exists="replace", index=False)

# Daily operations report
clean["transaction_day"] = clean["transaction_date"].dt.date
daily = clean.groupby("transaction_day").agg(
    transaction_count=("transaction_id","count"),
    total_amount=("amount","sum"),
    successful_count=("status", lambda s: (s=="SUCCESS").sum()),
    failed_count=("status", lambda s: (s=="FAILED").sum())
).reset_index()
daily["success_rate_pct"] = (daily["successful_count"] / daily["transaction_count"] * 100).round(2)
daily.to_csv(REPORTS / "daily_operations_report.csv", index=False)

print(f"ETL complete: {raw_count} raw rows -> {len(clean)} clean rows")
print(f"Database: {db_path}")
print(f"Reports: {REPORTS}")
