-- fact_loan_schedule: Loan repayment schedule fact table
-- Tracks scheduled and actual loan payments for repayment progress

CREATE TABLE IF NOT EXISTS retail_banking_demo_duongvt.fact_loan_schedule (
    -- Primary Key
    schedule_id STRING NOT NULL,

    -- Foreign Keys
    account_id STRING NOT NULL,
    customer_id STRING NOT NULL,
    date_key INT64 NOT NULL,

    -- Schedule
    due_date DATE NOT NULL,
    payment_number INT64,  -- 1, 2, 3, ... (nth payment)
    total_payments INT64,  -- Total scheduled payments

    -- Scheduled Amounts
    payment_due NUMERIC NOT NULL,  -- Total scheduled payment
    principal_portion NUMERIC NOT NULL,  -- Principal component
    interest_portion NUMERIC NOT NULL,  -- Interest component

    -- Status
    payment_status STRING NOT NULL,  -- Scheduled, Paid, Overdue, Partial, Prepaid

    -- Actual Payment (when paid)
    actual_payment_date DATE,
    actual_amount_paid NUMERIC,
    extra_principal_paid NUMERIC,  -- Any additional principal beyond scheduled

    -- Delinquency
    days_past_due INT64 DEFAULT 0,
    late_fee_charged NUMERIC DEFAULT 0,

    -- Cumulative Tracking
    cumulative_principal_paid NUMERIC,  -- Running total of principal paid
    remaining_balance NUMERIC,  -- Remaining loan balance after this payment

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Key analytics enabled:
-- 1. Repayment Progress (cumulative_principal_paid / original_principal)
-- 2. Pre-payment Detection (extra_principal_paid > 0)
-- 3. Delinquency Tracking (days_past_due > 0)
-- 4. Loan Health (payment_status distribution)
-- 5. Pre-payment Potential (compare customer savings to remaining_balance)

-- PARTITION BY due_date
-- CLUSTER BY customer_id, account_id
