-- dim_product: Product catalog dimension
-- Reference table for all banking products offered

CREATE TABLE IF NOT EXISTS retail_banking_demo_duongvt.dim_product (
    -- Primary Key
    product_id STRING NOT NULL,

    -- Product Identity
    product_name STRING NOT NULL,
    product_type STRING NOT NULL,  -- Savings, Checking, Credit Card, Personal Loan, Mortgage, CD, Life Insurance, Property Insurance, Equity, Mutual Fund, SIP
    product_category STRING NOT NULL,  -- CASA, Cards, Loans, CDs, Insurance, Securities

    -- Product Details
    description STRING,

    -- Pricing/Terms (where applicable)
    min_balance NUMERIC,
    annual_fee NUMERIC,
    interest_rate_min NUMERIC,
    interest_rate_max NUMERIC,

    -- Status
    is_active BOOL DEFAULT TRUE,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Sample product types by category:
-- CASA: Savings Account, Premium Savings, Checking Account, Money Market
-- Cards: Basic Credit Card, Gold Credit Card, Platinum Credit Card, Business Card
-- Loans: Personal Loan, Home Mortgage, Auto Loan, Education Loan
-- CDs: Standard CD, High-Yield CD, Jumbo CD
-- Insurance: Term Life, Whole Life, Property Insurance, Umbrella Policy
-- Securities: Equity Fund, Bond Fund, Mutual Fund, SIP
