-- fact_account_snapshot: Account balance snapshot fact table
-- Monthly snapshots for balance trends and credit utilization

CREATE TABLE IF NOT EXISTS retail_banking_demo_duongvt.fact_account_snapshot (
    -- Primary Key
    snapshot_id STRING NOT NULL,

    -- Foreign Keys
    account_id STRING NOT NULL,
    customer_id STRING NOT NULL,
    date_key INT64 NOT NULL,

    -- Snapshot Date
    snapshot_date DATE NOT NULL,

    -- Balance Information
    balance NUMERIC NOT NULL,
    month_avg_balance NUMERIC,  -- Average daily balance for the month
    month_end_balance NUMERIC,  -- Balance at month end

    -- Credit Card Specific
    available_credit NUMERIC,  -- For cards: credit_limit - balance
    credit_utilization_pct NUMERIC,  -- For cards: (balance / credit_limit) * 100

    -- Loan Specific
    principal_paid NUMERIC,  -- Cumulative principal paid
    principal_remaining NUMERIC,  -- Outstanding principal
    interest_accrued NUMERIC,  -- Interest for the period

    -- Cash Flow (derived from transactions for the period)
    total_credits_mtd NUMERIC,  -- Month-to-date inflows (credits)
    total_debits_mtd NUMERIC,  -- Month-to-date outflows (debits)
    net_cash_flow_mtd NUMERIC,  -- credits - debits

    -- Product Count (at customer level)
    customer_product_count INT64,  -- Total products held by customer at this point

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Key analytics enabled:
-- 1. Balance Trend Chart (month_avg_balance vs month_end_balance over time)
-- 2. Credit Utilization (credit_utilization_pct for Cards tab)
-- 3. Cash Flow Velocity (total_credits_mtd vs total_debits_mtd)
-- 4. Loan Repayment Progress (principal_paid / original_principal)
-- 5. Share of Wallet (customer_product_count aggregation)
-- 6. Portfolio Health (sum of balances by asset/liability type)

-- Granularity: Monthly snapshots per account
-- PARTITION BY snapshot_date
-- CLUSTER BY customer_id, account_id
