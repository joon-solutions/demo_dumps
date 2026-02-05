-- dim_customer: Customer dimension table
-- Contains demographics, segmentation, persona, and behavioral attributes

CREATE TABLE IF NOT EXISTS dim_customer (
    -- Primary Key
    customer_id STRING NOT NULL,

    -- Personal Information
    first_name STRING NOT NULL,
    last_name STRING NOT NULL,
    date_of_birth DATE,
    age INT64,
    gender STRING,  -- Male, Female, Other, Prefer not to say

    -- Contact Information
    email STRING,
    phone STRING,

    -- Address
    address_city STRING,
    address_state STRING,
    address_country STRING,

    -- Demographics
    marital_status STRING,  -- Single, Married, Divorced, Widowed
    has_children BOOL,
    num_dependents INT64,

    -- Employment
    occupation STRING,
    employment_type STRING,  -- Salaried, Self-Employed, Retired, Student, Unemployed
    income_bracket STRING,  -- <25K, 25-50K, 50-100K, 100-250K, 250K+

    -- Housing
    home_ownership STRING,  -- Own, Rent, Other

    -- Banking Segment
    segment STRING NOT NULL,  -- Mass Market, Affluent, High Net Worth

    -- Compliance
    kyc_status STRING,  -- Verified, Pending, Expired

    -- Relationship
    join_date DATE NOT NULL,

    -- Behavioral
    preferred_channel STRING,  -- App, Branch, Call Center, Chatbot
    engagement_score INT64,  -- 0-100, calculated from activity

    -- Persona (derived from spending patterns)
    persona_tag STRING,  -- Frequent Traveler, Young Parent, Digital Native, College Student, Boomer

    -- Risk
    risk_tolerance STRING,  -- Low, Medium, High

    -- Churn
    churn_status BOOL DEFAULT FALSE,
    churn_date DATE,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Clustering for common query patterns
-- CLUSTER BY segment, persona_tag;
