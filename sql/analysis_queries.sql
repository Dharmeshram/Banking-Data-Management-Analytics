-- 1. Daily transaction volume and value
SELECT DATE(transaction_date) AS txn_day,
       COUNT(*) AS transaction_count,
       ROUND(SUM(amount),2) AS total_amount
FROM transactions
GROUP BY DATE(transaction_date)
ORDER BY txn_day;

-- 2. Channel-wise performance
SELECT channel, COUNT(*) AS txn_count,
       SUM(CASE WHEN status='SUCCESS' THEN 1 ELSE 0 END) AS successful_txns,
       ROUND(100.0 * SUM(CASE WHEN status='SUCCESS' THEN 1 ELSE 0 END)/COUNT(*),2) AS success_rate_pct
FROM transactions
GROUP BY channel
ORDER BY txn_count DESC;

-- 3. Customer segment analysis
SELECT c.segment, COUNT(t.transaction_id) AS txn_count,
       ROUND(SUM(t.amount),2) AS transaction_value
FROM customers c
JOIN transactions t ON c.customer_id=t.customer_id
GROUP BY c.segment;

-- 4. Failed transactions for operational follow-up
SELECT transaction_id, account_id, transaction_date, channel, amount
FROM transactions
WHERE status='FAILED'
ORDER BY transaction_date DESC;

-- 5. Potential high-value transactions (analytical flag, not fraud determination)
SELECT transaction_id, customer_id, channel, amount, transaction_date
FROM transactions
WHERE amount >= 50000
ORDER BY amount DESC;

-- 6. Account reference integrity check
SELECT t.transaction_id, t.account_id
FROM transactions t
LEFT JOIN accounts a ON t.account_id=a.account_id
WHERE a.account_id IS NULL;

-- 7. Duplicate transaction IDs in a raw staging table
SELECT transaction_id, COUNT(*) AS duplicate_count
FROM transactions_staging
GROUP BY transaction_id
HAVING COUNT(*) > 1;

-- 8. Monthly / channel summary using conditional aggregation
SELECT DATE_FORMAT(transaction_date,'%Y-%m') AS txn_month,
       SUM(CASE WHEN channel='UPI' THEN 1 ELSE 0 END) AS upi_count,
       SUM(CASE WHEN channel='ATM' THEN 1 ELSE 0 END) AS atm_count,
       SUM(CASE WHEN channel='Net Banking' THEN 1 ELSE 0 END) AS netbanking_count
FROM transactions
GROUP BY DATE_FORMAT(transaction_date,'%Y-%m');
