-- dim_account: Account dimension table
-- Supports all product types: CASA, Credit Card, Loan, CD, Insurance, Securities

CREATE TABLE IF NOT EXISTS retail_banking_demo_duongvt.dim_account (
    -- Primary Key
    account_id STRING NOT NULL,

    -- Foreign Key
    customer_id STRING NOT NULL,

    -- Account Classification
    account_type STRING NOT NULL,  -- CASA, Credit Card, Loan, CD, Insurance, Securities
    product_name STRING NOT NULL,  -- e.g., "Premium Savings", "Gold Card", "Home Mortgage"

    -- Status
    status STRING NOT NULL,  -- Active, Dormant, Closed

    -- Dates
    open_date DATE NOT NULL,
    maturity_date DATE,  -- For CDs, Loans, Insurance policies

    -- Display
    account_number STRING,  -- Masked for display (e.g., ****1234)

    -- CASA-specific fields
    -- (uses current_balance)

    -- Credit Card-specific fields
    credit_limit NUMERIC,
    available_balance NUMERIC,

    -- Loan-specific fields
    principal_amount NUMERIC,
    interest_rate NUMERIC,
    loan_term_months INT64,
    payoff_amount NUMERIC,
    outstanding_balance NUMERIC,

    -- CD-specific fields
    cd_term_months INT64,
    annual_yield NUMERIC,
    average_balance NUMERIC,
    tin_type STRING,  -- SSN, EIN
    tin_number STRING,  -- Masked

    -- Insurance-specific fields
    coverage_amount NUMERIC,
    premium_amount NUMERIC,
    beneficiary_count INT64,
    policy_status STRING,  -- Quote, New Business, Active, Lapsed
    policy_sub_status STRING,  -- Premium Paying, Not Submitted, etc.

    -- Securities-specific fields
    security_type STRING,  -- Equity, Mutual Fund, SIP, Bond
    units_held NUMERIC,
    purchase_price NUMERIC,
    current_value NUMERIC,

    -- Common fields
    current_balance NUMERIC,
    currency STRING DEFAULT 'USD',

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Index for common lookups
-- CREATE INDEX idx_account_customer ON dim_account(customer_id);
-- CREATE INDEX idx_account_type ON dim_account(account_type);
