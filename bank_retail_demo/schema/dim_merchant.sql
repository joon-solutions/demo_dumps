-- dim_merchant: Merchant dimension table
-- Contains merchant details with MCC codes for transaction categorization

CREATE TABLE IF NOT EXISTS retail_banking_demo_duongvt.dim_merchant (
    -- Primary Key
    merchant_id STRING NOT NULL,

    -- Merchant Identity
    merchant_name STRING NOT NULL,

    -- MCC (Merchant Category Code) - ISO 18245
    mcc_code STRING NOT NULL,  -- 4-digit code (e.g., "5411" for Grocery Stores)
    mcc_category STRING NOT NULL,  -- Human-readable category

    -- Merchant Type
    merchant_type STRING,  -- Retail, Online, Subscription, Service

    -- Behavioral Flags
    is_subscription_merchant BOOL DEFAULT FALSE,  -- Netflix, Spotify, Gym, etc.

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- MCC Category Reference:
-- Groceries: 5411 (Grocery Stores), 5422 (Freezer Meat), 5441 (Candy/Confectionery)
-- Dining: 5812 (Eating Places), 5813 (Bars), 5814 (Fast Food)
-- Travel: 3000-3299 (Airlines), 7011 (Hotels), 7512 (Car Rental), 4121 (Taxi/Rideshare)
-- Utilities: 4900 (Utilities), 4814 (Telecom), 4899 (Cable/Satellite)
-- Entertainment: 7832 (Movies), 7941 (Sports), 5735 (Record Stores)
-- Healthcare: 8011-8099 (Medical), 5912 (Drug Stores)
-- Shopping: 5311 (Department Stores), 5651 (Clothing), 5732 (Electronics)
-- Subscriptions: 5968 (Direct Marketing - Subscription), 4899 (Streaming)
-- Gas: 5541 (Service Stations), 5542 (Automated Fuel)
-- Other: Various

-- Common subscription merchants for detection:
-- Netflix, Spotify, Apple Music, Amazon Prime, Gym memberships,
-- Adobe, Microsoft 365, Google services, Newspapers, Streaming
