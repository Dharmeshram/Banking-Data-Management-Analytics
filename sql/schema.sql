-- Banking Data Management project schema (MySQL 8+)
CREATE DATABASE IF NOT EXISTS banking_analytics;
USE banking_analytics;

CREATE TABLE IF NOT EXISTS customers (
  customer_id VARCHAR(10) PRIMARY KEY,
  customer_name VARCHAR(100) NOT NULL,
  city VARCHAR(50),
  segment VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS accounts (
  account_id VARCHAR(10) PRIMARY KEY,
  customer_id VARCHAR(10) NOT NULL,
  account_type VARCHAR(30),
  account_status VARCHAR(20),
  CONSTRAINT fk_accounts_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS transactions (
  transaction_id VARCHAR(12) PRIMARY KEY,
  account_id VARCHAR(10) NOT NULL,
  customer_id VARCHAR(10),
  transaction_date DATETIME,
  channel VARCHAR(30),
  transaction_type VARCHAR(10),
  amount DECIMAL(14,2),
  currency CHAR(3),
  status VARCHAR(20),
  CONSTRAINT fk_transactions_account FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE IF NOT EXISTS data_quality_log (
  issue_id INT AUTO_INCREMENT PRIMARY KEY,
  transaction_id VARCHAR(12),
  issue_type VARCHAR(80),
  issue_description VARCHAR(255),
  detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional raw landing table for duplicate profiling before curated loading.
CREATE TABLE IF NOT EXISTS transactions_staging (
  transaction_id VARCHAR(12),
  account_id VARCHAR(10),
  customer_id VARCHAR(10),
  transaction_date DATETIME,
  channel VARCHAR(30),
  transaction_type VARCHAR(10),
  amount DECIMAL(14,2),
  currency CHAR(3),
  status VARCHAR(20)
);
