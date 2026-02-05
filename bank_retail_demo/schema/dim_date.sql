-- dim_date: Standard date dimension table
-- Pre-populated for 2023-2026 date range

CREATE TABLE IF NOT EXISTS retail_banking_demo_duongvt.dim_date (
    -- Primary Key (YYYYMMDD format)
    date_key INT64 NOT NULL,

    -- Full Date
    full_date DATE NOT NULL,

    -- Day Attributes
    day_of_week INT64 NOT NULL,  -- 1=Sunday, 7=Saturday (ISO would be 1=Monday)
    day_name STRING NOT NULL,  -- Sunday, Monday, ..., Saturday
    day_of_month INT64 NOT NULL,  -- 1-31
    day_of_year INT64 NOT NULL,  -- 1-366

    -- Week Attributes
    week_of_year INT64 NOT NULL,  -- 1-53

    -- Month Attributes
    month INT64 NOT NULL,  -- 1-12
    month_name STRING NOT NULL,  -- January, February, ..., December
    month_short STRING NOT NULL,  -- Jan, Feb, ..., Dec

    -- Quarter Attributes
    quarter INT64 NOT NULL,  -- 1-4
    quarter_name STRING NOT NULL,  -- Q1, Q2, Q3, Q4

    -- Year Attributes
    year INT64 NOT NULL,
    year_month STRING NOT NULL,  -- 2024-01 format for sorting

    -- Fiscal (assuming calendar year = fiscal year)
    fiscal_year INT64 NOT NULL,
    fiscal_quarter INT64 NOT NULL,

    -- Flags
    is_weekend BOOL NOT NULL,
    is_month_start BOOL NOT NULL,
    is_month_end BOOL NOT NULL,
    is_quarter_start BOOL NOT NULL,
    is_quarter_end BOOL NOT NULL,
    is_year_start BOOL NOT NULL,
    is_year_end BOOL NOT NULL,

    -- Banking-specific flags
    is_salary_day BOOL NOT NULL,  -- 1st or 15th of month (common salary dates)
    is_business_day BOOL NOT NULL  -- Not weekend (simplified - doesn't account for holidays)
);

-- Useful for:
-- - Time-based aggregations (daily, weekly, monthly, quarterly, yearly)
-- - Salary detection (is_salary_day)
-- - Business day calculations
-- - Month-over-month comparisons
-- - Trend analysis

-- Population strategy:
-- Generate rows for date range 2023-01-01 to 2026-12-31
-- Use Python or SQL to populate all attributes
