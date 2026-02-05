-- fact_interaction: Customer interaction/touchpoint fact table
-- Tracks all customer engagements across channels

CREATE TABLE IF NOT EXISTS retail_banking_demo_duongvt.fact_interaction (
    -- Primary Key
    interaction_id STRING NOT NULL,

    -- Foreign Keys
    customer_id STRING NOT NULL,
    date_key INT64 NOT NULL,

    -- Interaction Timestamp
    interaction_date TIMESTAMP NOT NULL,

    -- Channel
    channel STRING NOT NULL,  -- App, Call Center, Branch, Chatbot, Email, SMS

    -- Reason/Type
    reason STRING NOT NULL,  -- Login, Account Inquiry, Fee Dispute, Card Issue, Loan Application, General Info, Complaint, Support

    -- Sentiment (from NPS surveys, call analysis, or chat sentiment)
    sentiment_score NUMERIC,  -- 0.0 to 1.0 (0 = negative, 1 = positive)

    -- Resolution
    resolution_status STRING,  -- Resolved, Pending, Escalated, In Progress

    -- Duration (for calls/chats)
    duration_seconds INT64,

    -- Agent (for assisted interactions)
    agent_id STRING,

    -- Additional Context
    notes STRING,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Key analytics enabled:
-- 1. Channel Mix (channel distribution by segment)
-- 2. Engagement Score calculation (interaction frequency, recency)
-- 3. Churn Risk signals (declining sentiment, increased complaints)
-- 4. Support ticket analysis (reason distribution)
-- 5. Channel preference by persona

-- PARTITION BY DATE(interaction_date)
-- CLUSTER BY customer_id, channel
