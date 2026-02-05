-- fact_transaction: Transaction fact table
-- Core transaction data with behavioral flags for analytics

CREATE TABLE IF NOT EXISTS retail_banking_demo_duongvt.fact_transaction (
    -- Primary Key
    transaction_id STRING NOT NULL,

    -- Foreign Keys
    customer_id STRING NOT NULL,
    account_id STRING NOT NULL,
    merchant_id STRING,  -- Nullable for transfers without merchant
    date_key INT64 NOT NULL,

    -- Transaction Timestamp
    transaction_date TIMESTAMP NOT NULL,

    -- Transaction Details
    amount NUMERIC NOT NULL,
    transaction_type STRING NOT NULL,  -- credit, debit, transfer
    payment_method STRING,  -- Credit Card, Debit Card, Bank Transfer, Direct Debit, Cash

    -- Categorization (denormalized for query performance)
    mcc_category STRING,  -- Groceries, Dining, Travel, Utilities, Entertainment, Healthcare, Shopping, Subscriptions, Gas, Other

    -- Behavioral Flags (key for Customer 360 insights)
    is_recurring BOOL DEFAULT FALSE,  -- For subscription detection
    recurring_frequency STRING,  -- monthly, weekly, annual (if is_recurring = true)

    -- Counterparty Analysis (for wallet leakage)
    counterparty_type STRING,  -- internal (within bank), external (other bank/fintech), self (own accounts)
    counterparty_name STRING,  -- Name of receiving party for transfers

    -- Additional Context
    description STRING,  -- Transaction description/memo
    channel STRING,  -- App, Branch, ATM, Online, POS

    -- Reference
    reference_number STRING,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Key analytics enabled:
-- 1. Spend by Category (mcc_category grouping)
-- 2. Top Merchants (merchant_id aggregation)
-- 3. Subscription Detection (is_recurring = true)
-- 4. Cash Flow Velocity (transaction_type credit vs debit)
-- 5. Wallet Leakage (counterparty_type = external)
-- 6. Channel Preferences (channel distribution)

-- Partitioning recommendation:
-- PARTITION BY DATE(transaction_date)
-- CLUSTER BY customer_id, account_id
